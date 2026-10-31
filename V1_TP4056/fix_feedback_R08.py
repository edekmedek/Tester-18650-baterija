from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_feedback_R07_fixed.kicad_pcb"
dst=d/"Tester18650_V1_feedback_R08.kicad_pcb"
if not src.exists():raise SystemExit("R07 board missing")
if dst.exists():raise SystemExit("R08 already exists")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
g=next(x for x in f["U1"].Pads() if x.GetNumber()=="4")
r=next(x for x in f["RSH1"].Pads() if x.GetNumber()=="2")
assert g.GetNetname()==r.GetNetname()=="GND"
net=g.GetNet()
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
# R07 GND back-layer segment at x=68, y50..75 crosses gate back-layer y55.
# Replace ONLY that vertical segment with two vias and a front-copper detour.
bad=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetNetname()=="GND" and t.GetLayer()==p.B_Cu and {tuple((round(p.ToMM(v.x),3),round(p.ToMM(v.y),3))) for v in (t.GetStart(),t.GetEnd())}=={(68.,50.),(68.,75.)}]
assert len(bad)==1,"Expected exactly one crossing segment"
b.Remove(bad[0])
# On front layer at x=68, y50..75, near RSH1 pad x83 and U1 x60; check DRC.
for x,y in ((68,50),(68,75)):
 v=p.PCB_VIA(b);v.SetPosition(pt(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4))
 v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
t=p.PCB_TRACK(b);t.SetStart(pt(68,50));t.SetEnd(pt(68,75));t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetFootprints())==8
print("OK:",dst)
print("GND crossing segment moved from B.Cu to F.Cu using two vias.")
print("DRC REQUIRED. No battery connection.")
