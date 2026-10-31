from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_pwm_interface_R13.kicad_pcb"
dst=d/"Tester18650_V1_power_interface_R14.kicad_pcb"
if not src.exists():raise SystemExit("Missing R13")
if dst.exists():raise SystemExit("R14 already exists")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):
 a=[x for x in f[ref].Pads() if x.GetNumber()==str(num)]
 assert len(a)==1
 return a[0]
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
u=pad("U1",8)
j=pad("J3",2)
assert u.GetNetname()=="VCC_3V3"
assert not j.GetNetname(),"J3.2 already assigned"
j.SetNet(u.GetNet())
def route(a,z,net,layer):
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(x,y,net):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
# J3.2 power via back layer. Route from x32 y84.54 up to x35 y39,
# then across to x64 y39, via near U1 pin8. Gate B.Cu is at x47 y43..55.
# Crossing gate at y39 is above gate via, so avoids B.Cu short.
net=u.GetNet()
route(j.GetPosition(),xy(35,84.54),net,p.F_Cu)
via(35,84.54,net)
for a,z in zip([xy(35,84.54),xy(35,39),xy(64,39)],[xy(35,39),xy(64,39),xy(64,40.5)]):
 route(a,z,net,p.B_Cu)
via(64,40.5,net)
route(xy(64,40.5),u.GetPosition(),net,p.F_Cu)
p.SaveBoard(str(dst),b)
assert len(p.LoadBoard(str(dst)).GetFootprints())==len(f)
print("OK:",dst)
print("J3 pin2 VCC_3V3 connected to U1 pin8. 3.3V supply NOT verified. DRC required.")
