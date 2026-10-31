from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_irf3205_R04.kicad_pcb"
dst=d/"Tester18650_V1_irf3205_R05.kicad_pcb"
if not src.exists(): raise SystemExit("Missing R04 PCB")
if dst.exists(): raise SystemExit("Refusing to overwrite R05")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
rg=f["RG1"];q=f["Q1"]
a=next(x for x in rg.Pads() if x.GetNumber()=="1")
z=next(x for x in q.Pads() if x.GetNumber()=="1")
assert a.GetNetname()==z.GetNetname()=="MOSFET_GATE"
net=a.GetNet()
# Remove only the two faulty R04 gate tracks, preserve U1->RG1.
bad=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetNetname()=="MOSFET_GATE"]
assert len(bad)==2, "Unexpected gate track count"
for t in bad: b.Remove(t)
# RG1 is SMD on front. Move to rear copper through via LEFT of resistor,
# then route on B.Cu to the through-hole TO-220 gate pin.
x=p.FromMM(47.0)
vpos=p.VECTOR2I(x,a.GetPosition().y)
via=p.PCB_VIA(b)
via.SetPosition(vpos);via.SetWidth(p.FromMM(0.8));via.SetDrill(p.FromMM(0.4))
via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(net)
b.Add(via)
def trace(start,end,layer):
    if start==end:return
    t=p.PCB_TRACK(b);t.SetStart(start);t.SetEnd(end);t.SetWidth(p.FromMM(0.25))
    t.SetLayer(layer);t.SetNet(net);b.Add(t)
trace(a.GetPosition(),vpos,p.F_Cu)
# Route rear via lower corridor, away from U1 pads and other front tracks.
p1=p.VECTOR2I(x,p.FromMM(55))
p2=p.VECTOR2I(z.GetPosition().x,p.FromMM(55))
trace(vpos,p1,p.B_Cu)
trace(p1,p2,p.B_Cu)
trace(p2,z.GetPosition(),p.B_Cu)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetFootprints())==8
print("OK:",dst)
print("Gate net moved to B.Cu using one via; R04 remains unchanged")
print("Tracks including via:",len(v.GetTracks()))
print("REQUIRED: run KiCad DRC. Do not connect a battery.")
