from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_setpoint_R11.kicad_pcb"
dst=d/"Tester18650_V1_setpoint_R12.kicad_pcb"
if not src.exists():raise SystemExit("Missing R11")
if dst.exists():raise SystemExit("R12 already exists")
b=p.LoadBoard(str(src))
f={a.GetReference():a for a in b.GetFootprints()}
def pad(ref,num):
 return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def route(net,layer,pts):
 for a,z in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(net,x,y):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
def check(ref,num,net):
 a=pad(ref,num)
 assert a.GetNetname()==net,(ref,num,a.GetNetname())
 return a
s1=check("U1",3,"CURRENT_SETPOINT")
s2=check("R3",2,"CURRENT_SETPOINT")
g1=check("R2",2,"GND")
g2=check("C1",2,"GND")
g3=check("U1",4,"GND")
# Setpoint front stub at U1, rear route above other signal nets.
route(s1.GetNet(),p.F_Cu,[s1.GetPosition(),xy(55,45.635)])
via(s1.GetNet(),55,45.635)
route(s1.GetNet(),p.B_Cu,[xy(55,45.635),xy(55,38),xy(90,38),xy(90,32)])
via(s1.GetNet(),90,32)
route(s1.GetNet(),p.F_Cu,[xy(90,32),s2.GetPosition()])
# GND top side: two components to one trunk, then via to existing U1 ground via.
route(g1.GetNet(),p.F_Cu,[g1.GetPosition(),xy(75.9125,42)])
route(g1.GetNet(),p.F_Cu,[g2.GetPosition(),xy(81.95,35),xy(75.9125,35)])
via(g1.GetNet(),75.9125,42)
route(g1.GetNet(),p.B_Cu,[xy(75.9125,42),xy(65,42),xy(65,50),xy(57.525,50)])
p.SaveBoard(str(dst),b)
assert len(p.LoadBoard(str(dst)).GetFootprints())==len(f)
print("OK:",dst)
print("Setpoint and two ground connections routed. DRC REQUIRED.")
print("PWM_RAW and power remain undefined. DO NOT connect battery.")
