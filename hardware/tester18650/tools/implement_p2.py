"""Edit the EXISTING board using KiCad 10; crop geometry never supplies a netlist."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as k

root=Path(__file__).resolve().parents[1]
assert k.GetBuildVersion().startswith('10.'),k.GetBuildVersion()
lib=root/'footprints/Tester18650.pretty'
board=k.LoadBoard(str(root/'tester18650.kicad_pcb'))
assert board.GetTitleBlock().GetRevision()=='P1','P2 migration runs once on the reviewed P1 board'
original_tracks=[(str(t.GetNetname()),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y) for t in board.GetTracks()]
assert len(original_tracks)==15
V=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
Q=lambda s:json.dumps(str(s))
origin=(90,25)

def rect(x1,y1,x2,y2,layer='F.Fab'):
    return f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width .1) (type default)) (fill none) (layer "{layer}"))'
def text(t,x,y,layer='F.SilkS',size=.85):
    return f'(fp_text user {Q(t)} (at {x} {y}) (layer "{layer}") (effects (font (size {size} {size}) (thickness .13))))'
def pad(n,x,y,drill,diam):
    return f'(pad {Q(n)} thru_hole circle (at {x} {y}) (size {diam} {diam}) (drill {drill}) (layers "*.Cu" "*.Mask"))'
def model(name):
    return f'(model "${{KIPRJMOD}}/models/{name}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'
def make(name,description,body):
    (lib/(name+'.kicad_mod')).write_text(f'''(footprint {Q(name)} (version 20260206) (generator "pcbnew") (layer "F.Cu")
      (descr {Q(description)}) (attr through_hole)
      (property "Reference" "REF**" (at 0 -2) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))
      (property "Value" {Q(name)} (at 0 2) (layer "F.Fab") (effects (font (size 1 1) (thickness .15))))
      {' '.join(body)})\n''')

crop=json.loads((root/'pcb_sources/p2/geometry.json').read_text())['reference_detail']
relay_pads={n:((xy[0]-1.5)*2.54,(xy[1]-5)*2.54) for n,xy in crop['K1']['pads_grid'].items()}
body=[rect(-6.35,-14.5,6.35,14.5),rect(-6.85,-15,6.85,15,'F.CrtYd'),
      text('K1 BODY REF',0,-17),text('8 GRID PADS: MAP TBD',0,17),model('RT314006_DIMENSION_REFERENCE_NO_PINS.step')]
for n,(x,y) in relay_pads.items():
    body.append(pad(n,x,y,1.3,2.4))
    # The original crop labels are recorded, not converted to manufacturer pins.
    body.append(text(n.replace('REF_','')+'?',x+(-3 if x<0 else 3),y,'F.Fab',.7))
make('RT314006_CROP_GRID_UNMAPPED','Confirmed carrier raster from ONLY user crop: 8 reference landing points, NOT 8 asserted relay pins. Manufacturer five-pin mapping UNRESOLVED. All reference pads electrically unassigned. 1.3mm holes are a new PCB choice from KiCad RT1 reference, not a measured perfboard drill.',body)

body=[rect(-1.5,-4,1.5,4,'F.CrtYd'),text('Q1 C3209',0,-5.5),text('PINOUT TBD',0,5.5)]
for n,(x,y) in crop['Q1']['pads_grid'].items():
    body.extend([pad(n,x*2.54,y*2.54,.9,1.8),text(n.split('_')[1]+'?',3.5,y*2.54)])
make('C3209_CROP_GRID_UNMAPPED','Three confirmed carrier holes at 2.54mm. TOP/MID/BOT are physical positions; E/C/B crop annotations do NOT prove actual C3209 pinout. No electrical nets or fabricated transistor body. 0.9mm drill is an unvalidated new design choice.',body)

make('Cement_5WAXIAL_VERTICAL_7.62_SUBSTITUTE','Crop-confirmed 7.62mm two-hole raster, 1.2mm holes/2.4mm pads from KiCad power-resistor library. Proposed Yageo/Reichelt 5W AXIAL 22 substitute, body 25x6.4x6.4mm. NOT identified photographed part. Vertical forming/standoff are unvalidated new design choices.',[
    pad('1',0,-3.81,1.2,2.4),pad('2',0,3.81,1.2,2.4),
    rect(-3.2,-7.01,3.2,-.61),rect(-4,-7.8,4,5.2,'F.CrtYd'),
    text('22R / 5W ALT',0,6.8),model('Cement_5WAXIAL_VERTICAL_SUBSTITUTE.step')])
make('R3_CROP_GRID_7.62_BODY_TBD','R3 two-hole carrier raster confirmed from crop; body/package and circuit topology unknown. 0.8mm holes are a new PCB design choice. No guessed 0.25W body model.',[
    pad('1',0,-3.81,.8,1.8),pad('2',0,3.81,.8,1.8),rect(-1.5,-5.3,1.5,5.3,'F.CrtYd'),
    text('R3 10k',3.8,-2),text('BODY TBD',4.5,1)])
make('R4_LABEL_ONLY_NO_PADS','Only R4 label is visible in crop; full terminal pair clipped. No extrapolated raster, holes, package or circuit topology.',[
    text('R4 20k',0,-1.2),text('PADS / BODY TBD',0,1.2),rect(-4,-4,4,4,'F.Fab')])
make('Keystone1042_LAYOUT_REFERENCE_NO_PADS','Keystone1042 library reference only, NOT identified as photographed holder. NO manufacturing pads/holes. Source underboard posts removed for reference rendering. Exact holder fit remains unverified.',[
    rect(-10.325,-43.205,10.325,43.205),rect(-10.825,-43.705,10.825,43.705,'F.CrtYd'),
    text('KEYSTONE 1042 REF',0,45),text('NO MOUNTING PADS',0,47),model('Keystone1042_REFERENCE_NO_MOUNTING.step')])

changes={'K1':'RT314006_CROP_GRID_UNMAPPED','Q1':'C3209_CROP_GRID_UNMAPPED',
         'R1':'Cement_5WAXIAL_VERTICAL_7.62_SUBSTITUTE','R2':'Cement_5WAXIAL_VERTICAL_7.62_SUBSTITUTE',
         'R3':'R3_CROP_GRID_7.62_BODY_TBD','R4':'R4_LABEL_ONLY_NO_PADS',
         'BTH1':'Keystone1042_LAYOUT_REFERENCE_NO_PADS'}
netpins={(p.attrib['ref'],p.attrib['pin']):n.attrib['name'] for n in ET.parse(root/'reports/netlist.xml').findall('./nets/net') for p in n.findall('node')}
def net(name):
    item=board.FindNet(name)
    if item is None or item.GetNetCode()<0:
        item=k.NETINFO_ITEM(board,name);board.Add(item)
    return item
fps={f.GetReference():f for f in board.GetFootprints()}
reader=k.PCB_IO_KICAD_SEXPR()
# Preload replacements before detaching old footprints. This also keeps the
# native Python API's plugin/cache objects alive throughout the transaction.
replacements={ref:reader.FootprintLoad(str(lib),name) for ref,name in changes.items()}
detached=[]
for ref,name in changes.items():
    old=fps[ref];new=replacements[ref]
    print('Replacing',ref,name,type(new).__name__,flush=True)
    new.SetFPID(k.LIB_ID('Tester18650',name));new.SetReference(ref);new.SetValue(old.GetValue())
    new.SetPosition(old.GetPosition());new.SetPath(old.GetPath());new.SetAttributes(old.GetAttributes())
    new.Reference().SetVisible(False);new.Value().SetVisible(False)
    board.Remove(old);detached.append(old);board.Add(new);fps[ref]=new
    if ref in ('R1','R2','R3'):
        for p in new.Pads():p.SetNet(net(netpins[(ref,p.GetNumber())]))

# Keep all three existing P1 copper routes and add only independently confirmed
# two-resistor parallel links and duplicate same-function INA landing points.
def pos(ref,pn):return next(p.GetPosition() for p in fps[ref].Pads() if p.GetNumber()==pn)
def track(name,points,width=.8,layer=k.F_Cu):
    for a,b in zip(points,points[1:]):
        t=k.PCB_TRACK(board);t.SetStart(a);t.SetEnd(b);t.SetWidth(k.FromMM(width));t.SetLayer(layer);t.SetNet(net(name));board.Add(t)
def local(x,y):return V(x+origin[0],y+origin[1])
track(netpins[('R1','1')],[pos('R1','1'),local(52,79.19),local(52,103.19),pos('R2','1')])
track(netpins[('R1','2')],[pos('R1','2'),local(80,86.81),local(80,110.81),pos('R2','2')])
for pn in ('5','6'):
    pads=[p.GetPosition() for p in fps['J2'].Pads() if p.GetNumber()==pn]
    track(netpins[('J2',pn)],pads,1)

# Replace P1 rectangular thermal allocations with body-reference keepouts.
# A pad-access notch allows the confirmed lead to leave towards the left.
for zone in list(board.Zones()):
    if zone.GetIsRuleArea():
        bb=zone.GetBoundingBox()
        if k.ToMM(bb.GetX())>140:board.Remove(zone)
for cy in (83,107):
    top,bottom=cy-7.01,cy-.61
    points=[(62.8,top),(69.2,top),(69.2,bottom),(62.8,bottom),
            (62.8,cy-2.31),(67.5,cy-2.31),(67.5,cy-5.31),(62.8,cy-5.31)]
    zone=k.ZONE(board);zone.SetIsRuleArea(True);layers=k.LSET();layers.AddLayer(k.F_Cu);layers.AddLayer(k.B_Cu);zone.SetLayerSet(layers)
    zone.SetDoNotAllowZoneFills(True);zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True)
    poly=zone.Outline();poly.NewOutline()
    for x,y in points:
        point=local(x,y);poly.Append(point.x,point.y)
    board.Add(zone)

relabel={'AMBER = AREA ONLY':'K1 / BTH1 = BODY REFERENCES',
         'PACKAGE / PINOUT TBD':'Q1 / R3 / R4: BODY UNKNOWN',
         'P1 / 116x132 DESIGN':'P2 / 116x132 / NOT FOR FAB',
         '10mm':'R1 / R2', 'GAP':'SUBSTITUTE',
         'HOLDER AREA':'HOLDER FIT UNVERIFIED',
         'INA VIN: NO ROUTES':'VIN EXTERNAL: OPEN'}
for drawing in board.GetDrawings():
    if isinstance(drawing,k.PCB_TEXT) and drawing.GetText() in relabel:drawing.SetText(relabel[drawing.GetText()])
for ref,cy in [('R1',83),('R2',107)]:
    label=k.PCB_TEXT(board);label.SetText(ref);label.SetPosition(local(75,cy))
    label.SetTextSize(V(1,1));label.SetTextThickness(k.FromMM(.16));label.SetLayer(k.F_SilkS);board.Add(label)
board.GetTitleBlock().SetTitle('Tester 18650 / P2 - photo + confirmed crop - NOT FOR FAB')
board.GetTitleBlock().SetRevision('P2')
board.GetTitleBlock().SetComment(0,'Crop-grid pads do NOT prove C3209 / relay pinout; see PCB.md')
board.GetTitleBlock().SetComment(1,'Resistors: proposed substitute. Holder: reference only. ERC/DRC NON-CLEAN.')
k.SaveBoard(str(root/'tester18650.kicad_pcb'),board)

schema=root/'tester18650.kicad_sch';raw=schema.read_text()
for line in raw.splitlines():
    if not line.startswith('(symbol (lib_id '):continue
    m=re.search(r'\(property "Reference" "([^"]+)"',line)
    if m and m[1] in changes:
        changed=re.sub(r'\(property "Footprint" "[^"]*"',f'(property "Footprint" "Tester18650:{changes[m[1]]}"',line)
        raw=raw.replace(line,changed)
schema.write_text(raw)
placement=root/'reports/pcb/placement-map.json';data=json.loads(placement.read_text())
for ref,name in changes.items():data['placements'][ref][0]=name
data['revision']='P2';data['copper_nets']=sorted({str(t.GetNetname()) for t in board.GetTracks()})
data['reference_body_mm']={'K1':[12.7,29,15.7],'R1':[6.4,6.4,25],'R2':[6.4,6.4,25],'BTH1':[20.65,86.41,16.3]}
data['thermal_body_xy_mm']={'R1':[62.8,75.99,69.2,82.39],'R2':[62.8,99.99,69.2,106.39]}
data['note']='Confirmed crop raster is separate from manufacturer pin mapping. R1/R2 bodies are proposed vertical substitutes, not photo measurements. Q1/R3/R4 body unknown. Holder reference only.'
data['p1_tracks_preserved']=original_tracks
placement.write_text(json.dumps(data,indent=2)+'\n')
print('Edited existing native KiCad 10 PCB: crop pads K1/Q1/R1/R2/R3, resistor substitutes, relay/holder reference bodies; added 8 confirmed copper segments. Unknown terminal mapping stays open.')
