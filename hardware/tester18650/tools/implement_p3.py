"""Map the eight-terminal RT314006 reference and route confirmed relay contacts."""
import json,re,csv
import xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as k

root=Path(__file__).resolve().parents[1]
assert k.GetBuildVersion().startswith('10.')
path=root/'tester18650.kicad_pcb';board=k.LoadBoard(str(path))
assert board.GetTitleBlock().GetRevision()=='P2','One-time migration of reviewed P2'
lib=root/'footprints/Tester18650.pretty'
source=json.loads((root/'pcb_sources/p3/geometry.json').read_text())
name='RT314006_16A_8PIN_5MM_KICAD_REFERENCE'
Q=lambda s:json.dumps(str(s))
V=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def text(t,x,y,layer='F.Fab',size=.85):
    return f'(fp_text user {Q(t)} (at {x} {y}) (layer "{layer}") (effects (font (size {size} {size}) (thickness .13))))'
def rect(x1,y1,x2,y2,layer):
    return f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width .1) (type default)) (fill none) (layer "{layer}"))'
body=[rect(-6.35,-14.5,6.35,14.5,'F.Fab'),rect(-6.55,-14.7,6.55,14.7,'F.SilkS'),
      rect(-6.85,-15,6.85,15,'F.CrtYd'),text('K1 RT314006',0,-18,'F.SilkS'),
      text('8 PINS MAPPED',0,17.5,'F.SilkS'),
      '(model "${KIPRJMOD}/models/RT314006_16A_8PIN_KICAD_REFERENCE.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))']
coords=[]
for a in source['native_top_view_mm']:
    x=round(-(a['y']+3.75),6);y=round(a['x']-12.15,6);pin=a['pin']
    sx,sy=(2,3) if pin in ('A1','A2') else (3,2)
    shape='rect' if pin=='A1' else 'oval'
    body.append(f'(pad {Q(pin)} thru_hole {shape} (at {x} {y}) (size {sx} {sy}) (drill 1.3) (layers "*.Cu" "*.Mask"))')
    if pin in ('A1','A2'):body.append(text(pin,x,-15.9))
    coords.append((pin,x,y))
for pin,label,y in [('12','12 NC',3.11),('11','11 COM',8.15),('14','14 NO',13.19)]:body.append(text(label,10,y))
description='RT314006: eight physical terminals / five electrical functions. User confirms manufacturer 16A 5mm 1FormC bottom-view assignment. Coordinates from standard KiCad RT1 16A top-view library, clockwise 90 degrees to photo orientation. 7.5mm rows; library longitudinal positions 15.26/20.30/25.34mm. NOT an independently inspected exact TE dimensional drawing; see P3 source ledger.'
(lib/(name+'.kicad_mod')).write_text(f'''(footprint {Q(name)} (version 20260206) (generator "pcbnew") (layer "F.Cu")
 (descr {Q(description)}) (attr through_hole)
 (property "Reference" "REF**" (at 0 -18) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))
 (property "Value" "RT314006" (at 0 19) (layer "F.Fab") (effects (font (size 1 1) (thickness .15))))
 (property "Datasheet" "{source['manufacturer']['url']}" (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness .15))))
 {' '.join(body)})\n''')
fps={f.GetReference():f for f in board.GetFootprints()}
old=fps['K1'];reader=k.PCB_IO_KICAD_SEXPR();fp=reader.FootprintLoad(str(lib),name)
fp.SetFPID(k.LIB_ID('Tester18650',name));fp.SetReference('K1');fp.SetValue(old.GetValue())
fp.SetPosition(old.GetPosition());fp.SetPath(old.GetPath());fp.SetAttributes(old.GetAttributes())
fp.SetField('Datasheet',source['manufacturer']['url']);fp.GetField('Datasheet').SetVisible(False)
fp.Reference().SetVisible(False);fp.Value().SetVisible(False)
netpins={(p.attrib['ref'],p.attrib['pin']):n.attrib['name'] for n in ET.parse(root/'reports/netlist.xml').findall('./nets/net') for p in n.findall('node')}
def net(n):
    item=board.FindNet(n)
    if item is None or item.GetNetCode()<0:item=k.NETINFO_ITEM(board,n);board.Add(item)
    return item
for p in fp.Pads():p.SetNet(net(netpins[('K1',p.GetNumber())]))
board.Remove(old);board.Add(fp);fps['K1']=fp
origin=(90,25)
local=lambda x,y:V(x+origin[0],y+origin[1])
original=[(str(t.GetNetname()),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y) for t in board.GetTracks()]
assert len(original)==23
def pads(ref,pn):return sorted((p for p in fps[ref].Pads() if p.GetNumber()==pn),key=lambda p:p.GetPosition().x)
def track(n,points,width):
    for a,b in zip(points,points[1:]):
        t=k.PCB_TRACK(board);t.SetStart(a);t.SetEnd(b);t.SetWidth(k.FromMM(width));t.SetLayer(k.F_Cu);t.SetNet(net(n));board.Add(t)
for pn in ('11','12','14'):
    ends=[p.GetPosition() for p in pads('K1',pn)]
    track(netpins[('K1',pn)],ends,.8 if pn=='12' else 1.2)
track('/BAT_PLUS',[pads('BT1','1')[0].GetPosition(),local(104,10),local(104,22),local(85,22),local(85,35.15),pads('K1','11')[-1].GetPosition()],1.2)
track('/LOAD_IN',[pads('K1','14')[0].GetPosition(),local(52,40.19),local(52,79.19)],1.2)
# A1/+5V and A2/collector are assigned but deliberately await physical supply
# and C3209 endpoints. NC pairs only join the same unused physical contact.
for d in board.GetDrawings():
    if isinstance(d,k.PCB_TEXT) and d.GetText()=='P2 / 116x132 / NOT FOR FAB':d.SetText('P3 / 116x132 / NOT FOR FAB')
board.GetTitleBlock().SetRevision('P3')
board.GetTitleBlock().SetTitle('Tester 18650 / P3 - eight relay pins mapped - NOT FOR FAB')
board.GetTitleBlock().SetComment(0,'K1: eight physical pins / five functions. KiCad dimensional reference; see PCB.md')
board.GetTitleBlock().SetComment(1,'BAT+ -> COM / NO -> parallel load routed. INA polarity and C3209 unresolved.')
k.SaveBoard(str(path),board)
p=root/'tester18650.kicad_sch';s=p.read_text()
for line in s.splitlines():
    if line.startswith('(symbol (lib_id ') and '(property "Reference" "K1"' in line:
        updated=re.sub(r'\(property "Footprint" "[^"]*"',f'(property "Footprint" "Tester18650:{name}"',line)
        updated=re.sub(r'\(property "Datasheet" "[^"]*"',f'(property "Datasheet" "{source["manufacturer"]["url"]}"',updated)
        s=s.replace(line,updated)
s=s.replace('Radni kontakt zatvara krug pri aktivaciji releja. COM / NO / NC su funkcije, a ne potvrda fizičkih nožica (N1).','COM / NO / NC su funkcije; K1 je mapiran na 8 PCB padova (16A). Fizičko ožičenje nije potvrđeno (N1).')
p.write_text(s)
p=root/'reports/pcb/placement-map.json';data=json.loads(p.read_text())
data['revision']='P3';data['placements']['K1'][0]=name;data['p2_tracks_preserved']=original
data['copper_nets']=sorted({str(t.GetNetname()) for t in board.GetTracks()})
data['note']='K1 eight physical pins mapped; proper top-view rotation, A1 left/A2 right with coil up. KiCad library dimensions need final TE dimensional/tolerance inspection. Other P2 mechanical/electrical uncertainties remain.'
p.write_text(json.dumps(data,indent=2)+'\n')
with (root/'reports/pcb/K1_COORDINATES.csv').open('w') as out:
    w=csv.writer(out,lineterminator="\n");w.writerow(['terminal','top_view_local_x_mm','top_view_local_y_mm','schematic_net'])
    for pn,x,y in coords:w.writerow([pn,x,y,netpins[('K1',pn)]])
print('P3 saved: eight mapped K1 pins, all duplicate contact pairs joined, BAT+ to COM and NO to parallel load routed. No speculative supply/C3209/INA connections.')
