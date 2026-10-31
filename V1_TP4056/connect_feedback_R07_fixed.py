from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_shunt_R06.kicad_pcb"
dst=d/"Tester18650_V1_feedback_R07_fixed.kicad_pcb"
if not src.exists():raise SystemExit("R06 not found")
if dst.exists():raise SystemExit("R07 exists; refusing overwrite")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,n):return next(x for x in f[ref].Pads() if x.GetNumber()==n)
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def seg(a,z,net,layer=p.F_Cu):
 if a==z:return
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
# Route sense on front from U1 pin 2 left to x=54 then below U1 to shunt.
# U1 pin 4 at x57.525 y46.905; sense uses x54 corridor and y=58.
s=pad("U1","2");h=pad("RSH1","1")
assert s.GetNetname()==h.GetNetname()=="CURRENT_SENSE"
pts=[s.GetPosition(),xy(54,44.365),xy(54,58),xy(79,58),xy(79,65),h.GetPosition()]
for a,z in zip(pts,pts[1:]):seg(a,z,s.GetNet())
# Ground from U1 pin4 to shunt pad2 routed outside right and below components.
# A B.Cu via near U1 pin4 avoids crossing sense front traces.
g=pad("U1","4");r=pad("RSH1","2")
assert g.GetNetname()==r.GetNetname()=="GND"
vpos=xy(57.525,50)
seg(g.GetPosition(),vpos,g.GetNet())
via=p.PCB_VIA(b);via.SetPosition(vpos);via.SetWidth(p.FromMM(.8));via.SetDrill(p.FromMM(.4))
via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(g.GetNet());b.Add(via)
# Back corridor x=68 y=75, then right to shunt pad2 via x=115.
pts=[vpos,xy(68,50),xy(68,75),xy(115,75),xy(115,65),r.GetPosition()]
for a,z in zip(pts,pts[1:]):seg(a,z,g.GetNet(),p.B_Cu)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetFootprints())==8
print("OK:",dst)
print("Added CURRENT_SENSE and GND traces. DRC required; do not connect battery.")
