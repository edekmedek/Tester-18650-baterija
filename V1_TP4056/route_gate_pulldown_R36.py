from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_gate_pulldown_R35.kicad_pcb'
dst=d/'Tester18650_V1_gate_pulldown_R36.kicad_pcb'
if not src.exists():raise SystemExit('R35 board missing')
if dst.exists():raise SystemExit('R36 already exists, refusing overwrite')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def mm(v):return (round(p.ToMM(v.x),4),round(p.ToMM(v.y),4))
gate=pad('R4',1);gnd=pad('R4',2)
assert gate.GetNetname()=='MOSFET_GATE' and gnd.GetNetname()=='GND'
assert mm(gate.GetPosition())==(95.0875,38.0),mm(gate.GetPosition())
assert mm(gnd.GetPosition())==(96.9125,38.0),mm(gnd.GetPosition())
assert pad('Q1',1).GetNetname()=='MOSFET_GATE'
assert pad('RSH1',2).GetNetname()=='GND'
def route(points,net):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(0.25));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
route([(95.0875,38),(95.0875,40),(85,40),(85,45)],gate.GetNet())
route([(96.9125,38),(103,38),(103,65),(110.94,65)],gnd.GetNet())
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('R4 100k gate-GND routed on F.Cu; run DRC before accepting.')
print('No battery connection. Not approved for fabrication.')
