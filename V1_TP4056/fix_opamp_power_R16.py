from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_power_interface_R15.kicad_pcb"
dst=d/"Tester18650_V1_power_interface_R16.kicad_pcb"
if not src.exists():raise SystemExit("R15 missing")
if dst.exists():raise SystemExit("R16 already exists")
b=p.LoadBoard(str(src))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def pt(v):return round(p.ToMM(v.x),4),round(p.ToMM(v.y),4)
def ends(t):return {pt(t.GetStart()),pt(t.GetEnd())}
bad=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetNetname()=="VCC_3V3" and t.GetLayer()==p.F_Cu and ends(t)=={(35.,39.),(64.,39.)}]
assert len(bad)==1,"Expected one R15 crossing segment"
net=bad[0].GetNet();b.Remove(bad[0])
def track(a,z,layer):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(x,y):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
# B.Cu at y35 passes ABOVE CURRENT_SETPOINT B.Cu vertical x55 y38..45.
# F.Cu x64 y35..39 avoids PWM_RAW F.Cu vertical x40 y27..82.
# Existing VCC_3V3 vias at (35,39) and (64,39) remain on same net.
track((35,39),(35,35),p.B_Cu)
track((35,35),(64,35),p.B_Cu)
via(64,35)
track((64,35),(64,39),p.F_Cu)
p.SaveBoard(str(dst),b)
assert p.LoadBoard(str(dst))
print("OK:",dst)
print("VCC_3V3 detoured via B.Cu y35, F.Cu x64. Run DRC; no battery.")
