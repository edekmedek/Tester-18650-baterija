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
for ref in ('R4','BTH1'):
    assert not fields(fps[ref],'pad'),f'Invented physical pads in unresolved {ref}'
p2=json.loads((root/'pcb_sources/p2/geometry.json').read_text())
import hashlib
for filename,digest in p2['sources_sha256'].items():
    assert hashlib.sha256((root/'pcb_sources/p2'/filename).read_bytes()).hexdigest()==digest,filename
for ref,key in [('Q1','Q1')]:
    expected=p2['reference_detail'][key]['pads_grid']
    pads={p[1]:p for p in fields(fps[ref],'pad')}
    assert set(pads)==set(expected)
    for number,(x,y) in expected.items():
        target=((x-1.5)*2.54,(y-5)*2.54) if ref=='K1' else (x*2.54,y*2.54)
        assert xy(pads[number],'at')==tuple(round(v,6) for v in target)
        assert not fields(pads[number],'net'),f'Unproved terminal map in {ref}'
for ref in ('R1','R2','R3'):
    pads=fields(fps[ref],'pad')
    assert len(pads)==2
    assert {xy(p,'at') for p in pads}=={(0,-3.81),(0,3.81)}
assert not fields(fps['Q1'],'model') and not fields(fps['R3'],'model') and not fields(fps['R4'],'model'), 'No guessed bodies'
assert any('SUBSTITUTE.step' in m[1] for m in fields(fps['R1'],'model'))
p3=json.loads((root/'pcb_sources/p3/geometry.json').read_text())
for filename,digest in p3['sha256'].items():
    assert hashlib.sha256((root/'pcb_sources/p3'/filename).read_bytes()).hexdigest()==digest
assert hashlib.sha256((root/p3['cad_reference']['footprint']).read_bytes()).hexdigest()==p3['cad_reference']['sha256']
k1pads=fields(fps['K1'],'pad')
assert Counter(p[1] for p in k1pads)=={'A1':1,'A2':1,'11':2,'12':2,'14':2}
actual=[]
for p in k1pads:
    x,y=xy(p,'at');actual.append((p[1],x,y))
    assert one(p,'net')[1]==p3['pad_nets'][p[1]]
expected=[(p['pin'],round(-(p['y']+3.75),6),round(p['x']-12.15,6)) for p in p3['native_top_view_mm']]
assert sorted(actual)==sorted(expected)
assert next(x for pn,x,y in actual if pn=='A1')<next(x for pn,x,y in actual if pn=='A2'), 'Bottom-view A1/A2 must not be copied without mirroring'
model=json.loads((root/'reports/pcb/p3-relay-model.json').read_text())
assert model['pin_count']==8
assert sorted((x,y) for pn,x,y in actual)==sorted(tuple(p) for p in model['top_view_local_pin_centers_mm'])
assert any('8PIN_KICAD_REFERENCE.step' in m[1] for m in fields(fps['K1'],'model'))
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
assert len(segments)==33
assert {one(t,'net')[1] for t in segments}==set(allowed)|{'/LOAD_IN','/VIN_PLUS','/BAT_PLUS','unconnected-(K1-Pad12)'}
# Every original trace remains at the original coordinates (incremental edit).
for net,x1,y1,x2,y2 in manifest['p2_tracks_preserved']:
    assert any(one(t,'net')[1]==net and xy(t,'start')==(round(x1/1e6,6),round(y1/1e6,6)) and xy(t,'end')==(round(x2/1e6,6),round(y2/1e6,6)) for t in segments)


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
# Parallel load ends and duplicate INA pads are confirmed independently of crop colours.
def connected(net,start,end):
    graph={}
    for seg in segments:
        if one(seg,'net')[1]!=net:continue
        a,b=xy(seg,'start'),xy(seg,'end')
        graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
    pending=[start];seen=set()
    while pending:
        point=pending.pop()
        if point in seen:continue
        seen.add(point);pending.extend(graph.get(point,set())-seen)
    return end in seen
for pn,net in [('1','/LOAD_IN'),('2','/VIN_PLUS')]:
    assert connected(net,pad_position('R1',pn),pad_position('R2',pn))
for pn,net in [('5','/VIN_PLUS'),('6','/BAT_MINUS')]:
    loc=xy(fps['J2'],'at')
    pads=[tuple(round(a+b,6) for a,b in zip(loc,xy(p,'at'))) for p in fields(fps['J2'],'pad') if p[1]==pn]
    assert connected(net,*pads)
assert not connected('/VIN_PLUS',pad_position('R1','2'),pad_position('J2','5')), 'Do not adopt assumed VIN polarity'
for pn,net in [('11','/BAT_PLUS'),('12','unconnected-(K1-Pad12)'),('14','/LOAD_IN')]:
    loc=xy(fps['K1'],'at')
    ps=[tuple(round(a+b,6) for a,b in zip(loc,xy(p,'at'))) for p in k1pads if p[1]==pn]
    assert connected(net,*ps)
assert connected('/BAT_PLUS',pad_position('BT1','1'),pad_position('K1','11'))
assert connected('/LOAD_IN',pad_position('K1','14'),pad_position('R1','1'))
assert one(next(p for p in k1pads if p[1]=='11'),'net')[1]!=one(next(p for p in k1pads if p[1]=='14'),'net')[1]
assert not any(one(seg,'net')[1] in ('/+5V_RELEJ','/K1_C') for seg in segments), 'Unproved supply/C3209 destinations remain unrouted'
# Qualitative photo registration; metric reconstruction is NOT claimed.
p=manifest['placements']
assert p['J1'][1]<p['K1'][1]<p['BTH1'][1]
assert p['J1'][2]<p['Q1'][2]<p['R1'][2]<p['R2'][2]
assert p['J2'][1]==p['J1'][1] and p['J2'][2]>p['J1'][2]
a,b=manifest['thermal_body_xy_mm']['R1'],manifest['thermal_body_xy_mm']['R2']
assert b[1]-a[3]>=17.5
assert 89.675-a[2]>=20 and a[0]-43>=19
r=json.loads((root/'reports/pcb/drc.json').read_text())
assert r['kicad_version'].startswith('10.')
assert not r['violations']
assert len(r['unconnected_items'])==2
assert Counter(v['type'] for v in r['schematic_parity'])=={'net_conflict':5}
assert not any(v.get('excluded',False) for group in ('violations','unconnected_items','schematic_parity') for v in r[group])
print('PASS: incremental native KiCad 10 PCB edit; all 23 P2 tracks preserved.')
print('PASS: eight K1 physical pads / five functions, correct top-view rotation, A1 left/A2 right, all duplicate contacts assigned to the same schematic net.')
print('PASS: all eight model pin centres align with holes; available KiCad source coordinates/hashes checked. Direct TE dimensional tolerances remain unverified (PDF proxy403).')
print('PASS: BAT+ to COM11 and NO14 to parallel R1/R2 routed; 33 segments / 7 copper nets; no COM-NO bypass, speculative C3209/supply or external INA route.')
print('PASS: Q1 crop holes remain unmapped; R4/holder have no invented pads; photo order and thermal reference gaps retained.')
print('DRC NON-CLEAN: 0 geometric violations, 2 unconnected errors, 5 schematic-parity warnings; native status 5.')
print('BLOCKED FOR MANUFACTURING: direct TE dimensional/tolerance check, C3209 pinout, R4 geometry, clones/holder, resistor fit/lead forming, supplies and divider topology.')
