from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_ina_sense_header_R41.kicad_pcb'
dst=d/'Tester18650_V1_ina_sense_labels_R42.kicad_pcb'
if not src.exists(): raise SystemExit('R41 PCB missing')
if dst.exists(): raise SystemExit('R42 PCB already exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
assert 'J5' in f
pads={x.GetNumber():x for x in f['J5'].Pads()}
assert pads['1'].GetNetname()=='INA_VIN_PLUS'
assert pads['2'].GetNetname()=='INA_VIN_MINUS'
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def mm(v):return round(p.ToMM(v.x),3),round(p.ToMM(v.y),3)
x1,y1=mm(pads['1'].GetPosition())
x2,y2=mm(pads['2'].GetPosition())
print('J5 actual pad positions:',(x1,y1),(x2,y2))
assert abs(x1-x2)<0.01 and abs(y2-y1-2.54)<0.01,'Unexpected J5 pad geometry'
def silk(text,x,y):
 t=p.PCB_TEXT(b)
 t.SetText(text);t.SetPosition(xy(x,y))
 t.SetLayer(p.F_SilkS)
 t.SetTextSize(xy(1.0,1.0))
 t.SetTextThickness(p.FromMM(0.15))
 b.Add(t)
silk('INA VIN+',x1+10,y1)
silk('INA VIN-',x2+10,y2)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('Two clear INA219 sense silk labels added; run DRC.')
print('The VIN+/VIN- nets remain intentionally not connected to battery/load.')
