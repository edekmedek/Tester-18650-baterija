#!/usr/bin/env python3
"""Validate the native KiCad 10 board, source-derived pads and photo layout constraints."""
import json
import re
from pathlib import Path
from collections import Counter

root=Path(__file__).resolve().parents[1]

def parse(s):
    stack=[];result=None
    for token in re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s):
        if token=='(':
            obj=[]
            if stack:stack[-1].append(obj)
            else:result=obj
            stack.append(obj)
        elif token==')':stack.pop()
        else:stack[-1].append(json.loads(token) if token.startswith('"') else token)
    assert not stack
    return result

def fields(obj,key):return [x for x in obj if isinstance(x,list) and x and x[0]==key]
def one(obj,key):return fields(obj,key)[0]
def xy(obj,key):return tuple(round(float(v),6) for v in one(obj,key)[1:3])
board=parse((root/'tester18650.kicad_pcb').read_text())
assert int(one(board,'version')[1])>=20260206, 'Final board must be saved in KiCad 10 format'
manifest=json.loads((root/'reports/pcb/placement-map.json').read_text())
source=json.loads((root/'pcb_sources/reference-geometry.json').read_text())
origin=tuple(manifest['drawing_origin_mm'])
fps={next(p[2] for p in fields(f,'property') if p[1]=='Reference'):f for f in fields(board,'footprint')}
assert set(fps)=={'J1','J2','K1','Q1','R1','R2','R3','R4','BT1','BTH1','H1','H2','H3','H4'}
for ref,(_name,x,y) in manifest['placements'].items():
    assert xy(fps[ref],'at')==(x+origin[0],y+origin[1]),ref
for ref in ('K1','Q1','R1','R2','R3','R4','BTH1'):
    assert not fields(fps[ref],'pad'),f'Invented physical pads in unresolved {ref}'
assert len(fields(fps['J1'],'pad'))==30
assert len(fields(fps['J2'],'pad'))==8
# Check ALL reference pad coordinates and drill sizes against the manufacturer CAD extract.
expected_node=[(-float(p['x']),float(p['y']),float(p['drill'])) for p in source['nodemcu']['pads']]
expected_ina=[(p['x'],p['y'],p['drill']) for p in source['ina219']['pads']]
for ref,expected in [('J1',expected_node),('J2',expected_ina)]:
    actual=[(*xy(p,'at'),float(one(p,'drill')[1])) for p in fields(fps[ref],'pad')]
    assert sorted(tuple(round(x,5) for x in a) for a in actual)==sorted(tuple(round(x,5) for x in a) for a in expected),ref

allowed={'/I2C_SDA_GPIO2':(('J1','2'),('J2','1')),
         '/I2C_SCL_GPIO5':(('J1','3'),('J2','2')),
         '/BAT_MINUS':(('J1','6'),('BT1','2'))}
segments=fields(board,'segment')
assert len(segments)==15
assert {one(t,'net')[1] for t in segments}==set(allowed)

def pad_position(ref,number):
    p=next(p for p in fields(fps[ref],'pad') if p[1]==number)
    pos=xy(fps[ref],'at');local=xy(p,'at')
    return tuple(round(a+b,6) for a,b in zip(pos,local))
for net,(start,end) in allowed.items():
    graph={}
    for seg in segments:
        if one(seg,'net')[1]!=net:continue
        a,b=xy(seg,'start'),xy(seg,'end')
        graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
    seen=set();pending=[pad_position(*start)]
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);pending.extend(graph.get(p,set())-seen)
    assert pad_position(*end) in seen,net
    if net=='/BAT_MINUS':
        assert all(pad_position('J2',n) not in seen for n in ('5','6')), 'Do not route assumed VIN polarity'
assert not fields(board,'via'), 'No unexplained vias'
assert all(fields(z,'keepout') for z in fields(board,'zone')), 'No hidden copper pours'
# Qualitative photo registration; metric reconstruction is NOT claimed.
p=manifest['placements']
assert p['J1'][1]<p['K1'][1]<p['BTH1'][1]
assert p['J1'][2]<p['Q1'][2]<p['R1'][2]<p['R2'][2]
assert p['J2'][1]==p['J1'][1] and p['J2'][2]>p['J1'][2]
a,b=manifest['thermal_allocation_mm']['R1'],manifest['thermal_allocation_mm']['R2']
assert b[1]-a[3]>=10
assert 89-a[2]>=13 and a[0]-43>=13
r=json.loads((root/'reports/pcb/drc.json').read_text())
assert r['kicad_version'].startswith('10.')
assert not r['violations']
assert len(r['unconnected_items'])==3
assert Counter(v['type'] for v in r['schematic_parity'])=={'net_conflict':16}
assert not any(v.get('excluded',False) for group in ('violations','unconnected_items','schematic_parity') for v in r[group])
print('PASS: native KiCad 10 board; all nine tester placements plus holder and mounting holes.')
print('PASS: manufacturer-reference pad coordinates/drills reproduced; unresolved packages contain NO invented pads.')
print('PASS: exactly 3 confirmed copper nets / 15 segments; no VIN, driver or divider routing.')
print('PASS: photo-directed order; 10 mm between heat allocations; 13 mm lateral separation from INA/holder allocations.')
print('DRC NON-CLEAN: 0 geometric violations, 3 unconnected errors, 16 schema-parity warnings; native status 5.')
print('BLOCKED FOR MANUFACTURING: missing physical packages/pads, exact clone fit and unresolved electrical connections.')
