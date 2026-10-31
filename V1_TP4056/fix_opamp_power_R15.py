from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_power_interface_R14.kicad_pcb"
dst=d/"Tester18650_V1_power_interface_R15.kicad_pcb"
if not src.exists():raise SystemExit("R14 missing")
if dst.exists():raise SystemExit("R15 already exists")
b=p.LoadBoard(str(src))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def pt(v):return (round(p.ToMM(v.x),4),round(p.ToMM(v.y),4))
def ends(t):return {pt(t.GetStart()),pt(t.GetEnd())}
# R14 rear horizontal x35..64 at y39 intersects setpoint vertical x55 y38..45.635.
# Move only this horizontal to F.Cu between vias at x35 and x64.
bad=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetLayer()==p.B_Cu and t.GetNetname()=="VCC_3V3" and ends(t)=={(35.,39.),(64.,39.)}]
assert len(bad)==1,[(t.GetNetname(),ends(t)) for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetNetname()=="VCC_3V3"]
net=bad[0].GetNet()
b.Remove(bad[0])
def via(x,y):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
def route(a,z):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
via(35,39);via(64,39)
route((35,39),(64,39))
p.SaveBoard(str(dst),b)
assert p.LoadBoard(str(dst))
print("OK:",dst)
print("VCC_3V3 horizontal y39 moved to F.Cu using two vias. DRC REQUIRED.")
