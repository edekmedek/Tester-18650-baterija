from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_ina_power_R31.kicad_pcb'
dst=d/'Tester18650_V1_ina_power_R32.kicad_pcb'
if not src.exists():raise SystemExit('R31 missing')
if dst.exists():raise SystemExit('R32 exists')
b=p.LoadBoard(str(src))
def mm(v):return round(p.ToMM(v.x),3),round(p.ToMM(v.y),3)
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
bad=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetLayer()==p.B_Cu and t.GetNetname()=='VCC_3V3' and {mm(t.GetStart()),mm(t.GetEnd())}=={(35.,80.),(60.,80.)}]
assert len(bad)==1,'R31 segment not found'
net=bad[0].GetNet();b.Remove(bad[0])
def via(x,y):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
def track(a,z,layer):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
# Via near VCC trunk x35 y80; front-layer crossing of x36 GND rear is safe.
via(35,80)
track((35,80),(60,80),p.F_Cu)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J4.1 3V3 horizontal moved to F.Cu; run DRC. No battery.')