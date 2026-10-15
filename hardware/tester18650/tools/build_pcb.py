#!/usr/bin/env python3
"""Generate the explicit PCB draft from cited geometry; never guess missing pads."""
import json
import re
import uuid
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as k

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'footprints/Tester18650.pretty'
MODEL = ROOT / 'models'
SOURCE = json.loads((ROOT / 'pcb_sources/reference-geometry.json').read_text())
Q = lambda s: json.dumps(str(s))
V = lambda x, y: k.VECTOR2I(k.FromMM(x), k.FromMM(y))
U = lambda: str(uuid.uuid4())
F = lambda v: f'{float(v):.6f}'.rstrip('0').rstrip('.') or '0'


def line(x1,y1,x2,y2,layer='F.Fab',width=.15):
    return f'(fp_line (start {F(x1)} {F(y1)}) (end {F(x2)} {F(y2)}) (stroke (width {width}) (type default)) (layer "{layer}"))'


def rect(x1,y1,x2,y2,layer='F.Fab',width=.15):
    return '\n'.join(line(*a,*b,layer,width) for a,b in [((x1,y1),(x2,y1)),((x2,y1),(x2,y2)),((x2,y2),(x1,y2)),((x1,y2),(x1,y1))])


def ftext(text,x,y,layer='F.SilkS',size=1):
    return f'(fp_text user {Q(text)} (at {F(x)} {F(y)}) (layer "{layer}") (effects (font (size {size} {size}) (thickness .16))))'


def pad(n,x,y,drill,diam):
    return f'(pad {Q(n)} thru_hole circle (at {F(x)} {F(y)}) (size {F(diam)} {F(diam)}) (drill {F(drill)}) (layers "*.Cu" "*.Mask"))'


MARKERS={}
def plane(name,w,h,color):
    """Graphical 0.02 mm marker, explicitly NOT a physical component body."""
    MARKERS[name]={'width':w,'height':h,'color':list(map(float,color.split())),
                   'center_y':-1.725 if name.startswith('NodeMCU') else 0,
                   'graphic_thickness':.02,'physical_package':False}
    return f'(model "${{KIPRJMOD}}/models/{name}.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'


def footprint(name,description,body):
    content = f'''(footprint {Q(name)} (version 20241229) (generator "pcbnew") (layer "F.Cu")
(descr {Q(description)}) (attr through_hole)
(property "Reference" "REF**" (at 0 -2) (layer "F.SilkS") (effects (font (size 1 1) (thickness .16))))
(property "Value" {Q(name)} (at 0 2) (layer "F.Fab") (effects (font (size 1 1) (thickness .15))))
{body}
)\n'''
    (LIB/(name+'.kicad_mod')).write_text(content)


# Photo is a CH340 / Ver 0.1 style board. Use the manufacturer's historical
# CH340 pin/outline reference, rotated with USB upward as in the photograph.
# It is NOT claimed to be an identified exact clone or a verified final socket.
node_map={'D5':'1','D4':'2','D1':'3','A0':'4','5V':'5','GND@0':'6'}
node_positions={};body=[]
for a in SOURCE['nodemcu']['wires']:
    body.append(line(-float(a['x1']),float(a['y1']),-float(a['x2']),float(a['y2'])))
for a in SOURCE['nodemcu']['pads']:
    x,y=-float(a['x']),float(a['y']);n=node_map.get(a['name'],'')
    body.append(pad(n,x,y,float(a['drill']),float(a['diameter'])))
    if n:node_positions[n]=(x,y)
body += [rect(-15.75,-22.1,15.75,25.55,'F.CrtYd',.05),
         ftext('NODEMCU CH340 REF',0,-18.5),

         plane('NodeMCU_CH340_reference_plane',30.48,46.63,'0.13 0.32 0.62')]
footprint('NodeMCU_CH340_Manufacturer_REFERENCE','Official historical CH340 DevKit reference: 30.48 wide, 27.94 row spacing, 2.54 pitch. Exact pictured Ver 0.1 clone and mechanical fit UNVERIFIED.', '\n'.join(body))

# Pictured purple Soldered INA219 breakout: original manufacturer's KiCad source.
# Existing schematic logical indexes are mapped explicitly to physical functions.
ina_map={'SDA':'1','SCL':'2','VCC':'3','GND':'4','IN+':'5','IN-':'6'}
ina_positions={};body=[]
for a in SOURCE['ina219']['pads']:
    n=ina_map[a['net']];x,y=a['x'],a['y']
    body.append(pad(n,x,y,a['drill'],a['diameter']))
    if a['ref']=='K3':
        body.append(ftext(a['net'],x+4,y,'F.Fab',.8))
        ina_positions[n]=(x,y)
    else:ina_positions.setdefault(n,(x,y))
body += [rect(-19,-11,19,11,'F.Fab'),rect(-19,-11,19,11,'F.SilkS'),
         rect(-19.5,-11.5,19.5,11.5,'F.CrtYd',.05),
         ftext('SOLDERED INA219',0,-8),ftext('SOURCE CAD V1.0',0,8,'F.Fab',.9),
         '(model "${KIPRJMOD}/models/Soldered_INA219_photo_variant.step" (offset (xyz -19 -11 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))']
footprint('INA219_Soldered333066_Manufacturer_REF','Soldered original CAD V1.0: 38 x 22 board, 2.54 control header, 5 mm current-terminal pitch. Photo visually matches family; exact revision/fit still requires confirmation.', '\n'.join(body))

# Unknown physical parts get an explicit placement reservation WITHOUT pads,
# drills or a fabricated body. Width/height below are PCB planning allocations.
reservations={'K1':('RT314006',18,34),'Q1':('C3209',12,10),
              'R1':('22R / 5W',20,14),'R2':('22R / 5W',20,14),
              'R3':('10k',8,8),'R4':('20k',8,8),
              'BTH1':('18650 HOLDER',22,98)}
for ref,(value,w,h) in reservations.items():
    name='RESERVE_'+ref+'_PACKAGE_TBD'
    body=[rect(-w/2,-h/2,w/2,h/2,'F.SilkS'),rect(-w/2-.5,-h/2-.5,w/2+.5,h/2+.5,'F.CrtYd',.05),
          ftext(ref,0,-2,'F.SilkS',1.15),ftext(value,0,0,'F.SilkS',.85),ftext('TBD',0,2,'F.SilkS',.8),
          ftext(f'ALLOCATION {w}x{h} - NOT BODY' if w>12 else 'AREA ONLY',0,h/2+1.5,'F.Fab',.9),
          plane(name,w,h,'0.85 0.39 0.08')]
    footprint(name,'PLACEMENT AREA ONLY. Unknown physical dimensions/package/pinout; NO PADS OR DRILLS. NOT manufacturing geometry.', '\n'.join(body))

# Battery wire termination is a NEW carrier-board design choice, not a claimed
# identification of the battery holder or an undocumented connector.
footprint('Battery_Wire_Termination_DESIGN','New PCB solder-wire termination. 6 mm pitch, 1.2 mm finished holes chosen for draft; wire gauge/strain relief unverified.',
    pad('1',0,0,1.2,2.8)+'\n'+pad('2',0,6,1.2,2.8)+'\n'+rect(-2.5,-2.5,2.5,8.5,'F.CrtYd',.05)+'\n'+ftext('+',-3,0)+'\n'+ftext('-',-3,6))

# Persist manufacturer-derived reference footprints and deterministic mapping.
(ROOT/'fp-lib-table').write_text('(fp_lib_table (version 7)\n (lib (name "Tester18650")(type "KiCad")(uri "${KIPRJMOD}/footprints/Tester18650.pretty")(options "")(descr "Reference modules and explicit unsized reservations"))\n)\n')

board=k.BOARD(); board.SetCopperLayerCount(2)
board.GetDesignSettings().SetBoardThickness(k.FromMM(1.6))
symbol_values={c.attrib['ref']:c.findtext('value') for c in ET.parse(ROOT/'reports/netlist.xml').findall('./components/comp')}
netnames=[n.attrib['name'] for n in ET.parse(ROOT/'reports/netlist.xml').findall('./nets/net')]
nets={}
for name in netnames:
    item=k.NETINFO_ITEM(board,name);board.Add(item);nets[name]=item
schema=(ROOT/'tester18650.kicad_sch').read_text()
sheet_uuid=re.search(r'\(uuid ([^)]+)\)',schema)[1]
instances={}
for match in re.finditer(r'\(symbol \(lib_id .*?(?=\n\(|\Z)',schema,re.S):
    raw=match[0]
    m=re.search(r'\(property "Reference" "([^"]+)"',raw)
    if m:instances[m[1]]=re.search(r'\(uuid ([^)]+)\)',raw)[1]
net_of_pin={(p.attrib['ref'],p.attrib['pin']):n.attrib['name'] for n in ET.parse(ROOT/'reports/netlist.xml').findall('./nets/net') for p in n.findall('node')}
placements={'J1':('NodeMCU_CH340_Manufacturer_REFERENCE',24,26),
            'J2':('INA219_Soldered333066_Manufacturer_REF',24,111),
            'K1':('RESERVE_K1_PACKAGE_TBD',61,27),
            'Q1':('RESERVE_Q1_PACKAGE_TBD',61,62),
            'R1':('RESERVE_R1_PACKAGE_TBD',66,83),
            'R2':('RESERVE_R2_PACKAGE_TBD',66,107),
            'R3':('RESERVE_R3_PACKAGE_TBD',47,55),
            'R4':('RESERVE_R4_PACKAGE_TBD',47,67),
            'BT1':('Battery_Wire_Termination_DESIGN',98,10),
            'BTH1':('RESERVE_BTH1_PACKAGE_TBD',100,70)}
placed={}
for ref,(name,x,y) in placements.items():
    fp=k.FootprintLoad(str(LIB),name)
    fp.SetFPID(k.LIB_ID('Tester18650',name));fp.SetReference(ref)
    fp.SetValue(symbol_values.get(ref,'18650 holder allocation only'))
    fp.SetPosition(V(x,y))
    if ref in instances:fp.SetPath(k.KIID_PATH('/'+sheet_uuid+'/'+instances[ref]))
    else:fp.SetAttributes(fp.GetAttributes() | k.FP_BOARD_ONLY)
    fp.Reference().SetVisible(False);fp.Value().SetVisible(False)
    for p in fp.Pads():
        pn=p.GetNumber()
        if pn and (ref,pn) in net_of_pin:p.SetNet(nets[net_of_pin[(ref,pn)]])
    board.Add(fp);placed[ref]=fp


def shape_line(a,b,layer=k.Edge_Cuts,width=.1):
    s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(V(*a));s.SetEnd(V(*b));s.SetLayer(layer);s.SetWidth(k.FromMM(width));board.Add(s)


for a,b in [((0,0),(116,0)),((116,0),(116,132)),((116,132),(0,132)),((0,132),(0,0))]:shape_line(a,b)
# No fabricated enclosure constraints: board size, four M3 clearances and stackup
# are explicit draft design choices.
for i,(x,y) in enumerate([(4,4),(112,4),(112,128),(4,128)],1):
    fp=k.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_3.2mm_M3')
    fp.SetReference('H'+str(i));fp.SetValue('M3 / DESIGN');fp.SetPosition(V(x,y));fp.SetAttributes(fp.GetAttributes() | k.FP_BOARD_ONLY)
    fp.Reference().SetVisible(False);fp.Value().SetVisible(False);board.Add(fp)


def text(t,x,y,size=1,layer=k.F_SilkS,thick=.17):
    o=k.PCB_TEXT(board);o.SetText(t);o.SetPosition(V(x,y));o.SetTextSize(V(size,size));o.SetTextThickness(k.FromMM(thick));o.SetLayer(layer);board.Add(o)


text('TESTER 18650 / PHOTO LAYOUT',57,3,1.2)
text('NOT FOR FABRICATION',61,6,1)
text('USB UP / AS PHOTO',23,1.8,.8)
text('J1 REF / FIT TBD',23,54,1)
text('HEAT',66,73,1)
text('10mm',66,96,.85)
text('GAP',66,98,.85)
text('HOLDER AREA',98,122,.9)
text('BT1 +/-',98,5,.85)
text('J2 / PHOTO FAMILY',24,96,1)
text('INA VIN: NO ROUTES',24,125,.9)
text('AMBER = AREA ONLY',63,120,.9)
text('PACKAGE / PINOUT TBD',63,124,.85)
text('P1 / 116x132 DESIGN',56,130,.85)

# Copper and pour keepouts under reserved hot-component areas. No new unknown nets.
for x1,y1,x2,y2 in [(56,76,76,90),(56,100,76,114),(16.38,45,31.62,51.04)]:
    zone=k.ZONE(board);zone.SetIsRuleArea(True)
    layers=k.LSET();layers.AddLayer(k.F_Cu);layers.AddLayer(k.B_Cu);zone.SetLayerSet(layers)
    zone.SetDoNotAllowCopperPour(True);zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True)
    poly=zone.Outline();poly.NewOutline()
    for x,y in [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]:poly.Append(k.FromMM(x),k.FromMM(y))
    board.Add(zone)


def pos(ref,pn):
    return next(p.GetPosition() for p in placed[ref].Pads() if p.GetNumber()==pn)


def track(net,layer,width,points):
    for a,b in zip(points,points[1:]):
        t=k.PCB_TRACK(board);t.SetStart(a if isinstance(a,k.VECTOR2I) else V(*a));t.SetEnd(b if isinstance(b,k.VECTOR2I) else V(*b))
        t.SetWidth(k.FromMM(width));t.SetLayer(layer);t.SetNet(nets[net]);board.Add(t)


# Only logically confirmed connections. VIN orientation remains an assumption,
# so VIN+/VIN-, INA VCC/GND, driver, load and divider get NO arbitrary traces.
track('/I2C_SDA_GPIO2',k.F_Cu,.35,[pos('J1','2'),(3,33.62),(3,118),(15,118),(15,109.73),pos('J2','1')])
track('/I2C_SCL_GPIO5',k.B_Cu,.35,[pos('J1','3'),(5,41.24),(5,100),(16,100),(16,107.19),pos('J2','2')])
track('/BAT_MINUS',k.F_Cu,.8,[pos('J1','6'),(43,20.92),(43,8),(91,8),(91,16),pos('BT1','2')])

# Move the design into the drawing-sheet working area; local photo placement
# coordinates remain documented in the manifest.
origin=V(90,25)
for item in list(board.GetFootprints())+list(board.GetTracks())+list(board.GetDrawings())+list(board.Zones()):item.Move(origin)
board.GetDesignSettings().SetAuxOrigin(origin)
board.GetTitleBlock().SetTitle('Tester 18650 / P1 - photo layout - NOT FOR FAB')
board.GetTitleBlock().SetRevision('P1');board.GetTitleBlock().SetDate('2026-10-15')
board.GetTitleBlock().SetComment(0,'Reference CAD / unsized areas: see PCB.md')
board.GetTitleBlock().SetComment(1,'Photos guide placement; dimensions and pinouts remain unverified')
# Project uses A4 landscape; PDF scale 1 makes geometry checkable with a ruler.
# Native default drawing sheet; CLI export sets the required plot scale.
k.SaveBoard(str(ROOT/'tester18650.kicad_pcb'),board)
(ROOT/'reports/pcb/placement-map.json').write_text(json.dumps({'board_mm':[116,132,1.6],'drawing_origin_mm':[90,25],'placements':placements,'reference_pads':{'J1':node_positions,'J2':ina_positions},'copper_nets':['/I2C_SDA_GPIO2','/I2C_SCL_GPIO5','/BAT_MINUS'],'thermal_allocation_mm':{'R1':[56,76,76,90],'R2':[56,100,76,114]},'note':'Allocation sizes are design choices, NEVER component body dimensions.'},indent=2)+'\n')
print('PCB created: 9 tester placements + battery-holder allocation + 4 design mounting holes; 3 confirmed nets routed.')
(MODEL/'marker-geometry.json').write_text(json.dumps(MARKERS,indent=2)+'\n')
