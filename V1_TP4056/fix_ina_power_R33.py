from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_ina_power_R32.kicad_pcb'
dst=d/'Tester18650_V1_ina_power_R33.kicad_pcb'
if not src.exists():raise SystemExit('R32 missing')
if dst.exists():raise SystemExit('R33 already exists')
b=p.LoadBoard(str(src))
def mm(v):return round(p.ToMM(v.x),3),round(p.ToMM(v.y),3)
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
matches=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetLayer()==p.F_Cu and t.GetNetname()=='VCC_3V3' and {mm(t.GetStart()),mm(t.GetEnd())}=={(35.,80.),(60.,80.)}]
assert len(matches)==1,'R32 front segment not found'
net=matches[0].GetNet();b.Remove(matches[0])
def trace(a,z,layer):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(x,y):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
trace((35,80),(38,80),p.F_Cu)
via(38,80)
trace((38,80),(43,80),p.B_Cu)
via(43,80)
trace((43,80),(60,80),p.F_Cu)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('VCC crosses PWM on B.Cu between x38 and x43. Run DRC. No battery.')