from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_shunt_R06.kicad_pcb"
dst=d/"Tester18650_V1_feedback_R07.kicad_pcb"
if not src.exists(): raise SystemExit("Missing R06")
if dst.exists(): raise SystemExit("Refusing overwrite")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):
    a=[x for x in f[ref].Pads() if x.GetNumber()==num]
    assert len(a)==1
    return a[0]
def point(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def track(a,z,layer,net,width=0.25):
    if a==z:return
    t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z)
    t.SetLayer(layer);t.SetWidth(p.FromMM(width));t.SetNet(net);b.Add(t)
def via(pos,net):
    v=p.PCB_VIA(b);v.SetPosition(pos);v.SetWidth(p.FromMM(0.8))
    v.SetDrill(p.FromMM(0.4));v.SetViaType(p.VIATYPE_THROUGH)
    v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
# Sense: top-layer from U1 pin2 to free corridor, then back layer to shunt high.
s=pad("U1","2");sh=pad("RSH1","1")
assert s.GetNetname()==sh.GetNetname()=="CURRENT_SENSE"
v1=point(54,44.365)
track(s.GetPosition(),v1,p.F_Cu,s.GetNet());via(v1,s.GetNet())
# Back copper: avoid gate route at y55 by running at y60, cross gate at x~80,
# but crossing on same layer is forbidden: instead route sense on F.Cu after a second via.
v2=point(78,60)
# route on back from x54 y44.365 to x54 y60, then x78 y60
track(v1,point(54,60),p.B_Cu,s.GetNet())
track(point(54,60),v2,p.B_Cu,s.GetNet())
via(v2,s.GetNet())
track(v2,point(83,60),p.F_Cu,s.GetNet())
track(point(83,60),sh.GetPosition(),p.F_Cu,s.GetNet())
# Ground: from U1 pin4 via front route around bottom of board to shunt pad2.
g=pad("U1","4");gl=pad("RSH1","2")
assert g.GetNetname()==gl.GetNetname()=="GND"
track(g.GetPosition(),point(53,46.905),p.F_Cu,g.GetNet())
track(point(53,46.905),point(53,105),p.F_Cu,g.GetNet())
track(point(53,105),point(115,105),p.F_Cu,g.GetNet())
track(point(115,105),point(115,65),p.F_Cu,g.GetNet())
track(point(115,65),gl.GetPosition(),p.F_Cu,g.GetNet())
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetFootprints())==8
print("OK:",dst)
print("CURRENT_SENSE and GND tracks added; R06 unchanged")
print("WARNING: DRC MUST PASS before accepting this revision. No cell connection.")
