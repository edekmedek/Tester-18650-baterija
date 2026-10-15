#!/usr/bin/env python3
"""Validate actual KiCad-exported nets and explicitly unresolved interfaces."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

project = Path(__file__).resolve().parents[1]
netlist = ET.parse(project / 'reports/netlist.xml').getroot()
nets = {
    n.attrib['name']: {(p.attrib['ref'], p.attrib['pin']) for p in n.findall('node')}
    for n in netlist.findall('./nets/net')
}
expected = {
    '/BAT_PLUS': {('BT1', '1'), ('TP1', '1')},
    '/BAT_MINUS': {('BT1', '2'), ('J1', '6'), ('TP4', '1')},
    '/LOAD_IN': {('R1', '1'), ('R2', '1'), ('TP2', '1')},
    '/LOAD_OUT': {('R1', '2'), ('R2', '2'), ('TP3', '1')},
    '/K1_C': {('K1', 'A2'), ('Q1', '2')},
    '/+5V_RELEJ': {('K1', 'A1')},
    '/I2C_SDA_GPIO2': {('J1', '2'), ('J2', '1')},
    '/I2C_SCL_GPIO5': {('J1', '3'), ('J2', '2')},
    '/RELAY_GPIO14': {('J1', '1'), ('TP5', '1')},
    '/ADC_A0': {('J1', '4'), ('TP6', '1')},
}
for name, pins in expected.items():
    if nets.get(name) != pins:
        sys.exit(f'FAIL {name}: expected {pins}, found {nets.get(name)}')

unresolved = {
    ('J1', '5'), ('J2', '3'), ('J2', '4'), ('J2', '5'), ('J2', '6'),
    ('K1', '11'), ('K1', '12'), ('K1', '14'), ('Q1', '1'), ('Q1', '3'),
    ('R3', '1'), ('R3', '2'), ('R4', '1'), ('R4', '2'),
}
for pin in unresolved:
    matches = [pins for pins in nets.values() if pin in pins]
    if matches != [{pin}]:
        sys.exit(f'FAIL unresolved pin unexpectedly connected: {pin}: {matches}')
if len(nets) != len(expected) + len(unresolved):
    sys.exit(f'FAIL unexpected nets: {len(nets)}')

components = {c.attrib['ref']: c for c in netlist.findall('./components/comp')}
for ref, value in {'R1': '22 Ω / 5 W', 'R2': '22 Ω / 5 W', 'R3': '10 kΩ',
                   'R4': '20 kΩ', 'K1': 'Schrack RT314006'}.items():
    if components[ref].findtext('value') != value:
        sys.exit(f'FAIL component value: {ref}')
if len(components) != 15:
    sys.exit('FAIL unexpected component count (including documentation terminals)')

report = json.loads((project / 'reports/erc.json').read_text())
violations = [v for s in report['sheets'] for v in s['violations']]
summary = Counter((v['severity'], v['type']) for v in violations)
expected_summary = Counter({('error', 'pin_not_connected'): 14,
                            ('error', 'pin_not_driven'): 1,
                            ('warning', 'isolated_pin_label'): 1})
if summary != expected_summary or any(v.get('excluded', False) for v in violations):
    sys.exit(f'FAIL changed ERC findings: {summary}')
found_unconnected = set()
for v in violations:
    if v['type'] == 'pin_not_connected':
        for item in v['items']:
            match = re.search(r'Symbol (\S+) Pin (\S+)', item['description'])
            if not match:
                sys.exit('FAIL cannot identify ERC pin')
            found_unconnected.add(match.groups())
    elif v['type'] == 'pin_not_driven':
        if not any('Symbol Q1 Pin 1 ' in i['description'] for i in v['items']):
            sys.exit('FAIL unexpected undriven pin')
    elif not any("Label '+5V_RELEJ'" in i['description'] for i in v['items']):
        sys.exit('FAIL unexpected isolated label')
if found_unconnected != unresolved:
    sys.exit(f'FAIL ERC unresolved pins mismatch: {found_unconnected}')
if not report['kicad_version'].startswith('10.'):
    sys.exit('FAIL KiCad 10 required')
print('PASS: 10 exact functional nets, 14 unresolved pins isolated, component values verified.')
print('ERC remains NON-CLEAN: 15 errors + 1 warning; all match documented unknowns.')
