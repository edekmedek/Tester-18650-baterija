#!/usr/bin/env python3
"""Validate KiCad-exported functional nets and documented open pins."""
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
    '/BAT_PLUS': {('BT1', '1'), ('K1', '11')},
    '/BAT_MINUS': {('BT1', '2'), ('J1', '6'), ('J2', '6'), ('RSH1', '2')},
    '/LOAD_IN': {('K1', '14'), ('R1', '1'), ('R2', '1')},
    '/VIN_PLUS': {('R1', '2'), ('R2', '2'), ('RSH1', '1'), ('J2', '5')},
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

open_pins = {
    ('J1', '5'), ('J2', '3'), ('J2', '4'),
    ('K1', '12'), ('Q1', '1'), ('Q1', '3'),
    ('R3', '1'), ('R3', '2'), ('R4', '1'), ('R4', '2'),
}
for pin in open_pins:
    matches = [pins for pins in nets.values() if pin in pins]
    if matches != [{pin}]:
        sys.exit(f'FAIL open pin unexpectedly connected: {pin}: {matches}')
if len(nets) != len(expected) + len(open_pins):
    sys.exit(f'FAIL unexpected nets: {len(nets)}')

components = {c.attrib['ref']: c for c in netlist.findall('./components/comp')}
for ref, value in {'R1': '22 Ω / 5 W', 'R2': '22 Ω / 5 W', 'R3': '10 kΩ',
                   'R4': '20 kΩ', 'K1': 'Schrack RT314006', 'RSH1': 'vrijednost ?'}.items():
    if components[ref].findtext('value') != value:
        sys.exit(f'FAIL component value: {ref}')
if len(components) != 12:
    sys.exit('FAIL unexpected component count (including documentation terminals)')

report = json.loads((project / 'reports/erc.json').read_text())
violations = [v for s in report['sheets'] for v in s['violations']]
summary = Counter((v['severity'], v['type']) for v in violations)
expected_summary = Counter({('error', 'pin_not_connected'): 10,
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
if found_unconnected != open_pins:
    sys.exit(f'FAIL ERC open pins mismatch: {found_unconnected}')
if not report['kicad_version'].startswith('10.'):
    sys.exit('FAIL KiCad 10 required')

# Model only the requested load path from the exported netlist. A relay contact
# is an edge when energized; it must never be bypassed by copper.
pin_to_net = {pin: name for name, group in nets.items() for pin in group}
def load_path_exists(energized, fitted_loads=('R1', 'R2')):
    graph = {name: set() for name in nets}
    bridges = [(('RSH1', '1'), ('RSH1', '2'))]
    bridges += [((ref, '1'), (ref, '2')) for ref in fitted_loads]
    if energized:
        bridges.append((('K1', '11'), ('K1', '14')))
    for a, b in bridges:
        left, right = pin_to_net[a], pin_to_net[b]
        graph[left].add(right)
        graph[right].add(left)
    visited, pending = set(), [pin_to_net[('BT1', '1')]]
    while pending:
        node = pending.pop()
        if node in visited:
            continue
        visited.add(node)
        pending.extend(graph[node] - visited)
    return pin_to_net[('BT1', '2')] in visited
if load_path_exists(False):
    sys.exit('FAIL: load path bypasses the open relay contact')
if not load_path_exists(True):
    sys.exit('FAIL: energized COM-NO path does not reach BAT- through INA219')
for fitted in [('R1',), ('R2',)]:
    if not load_path_exists(True, fitted):
        sys.exit(f'FAIL: missing parallel branch {fitted}')
if load_path_exists(True, ()):
    sys.exit('FAIL: load resistors are bypassed')
print('PASS: COM-NO switches the load path; each parallel branch reaches the internal shunt and BAT-.')
print('PASS: 10 exact functional nets; 10 open pins and component values verified.')
print('ERC remains NON-CLEAN: 11 errors + 1 warning, including the unused NC contact.')
