from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_setpoint_R10.kicad_pcb"
dst=d/"Tester18650_V1_setpoint_R11.kicad_pcb"
if not src.exists():raise SystemExit("R10 missing")
if dst.exists():raise SystemExit("R11 exists; refusing overwrite")
b=p.LoadBoard(str(src))
f={v.GetReference():v for v in b.GetFootprints()}
def pad(ref,num):
 return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def mm(pos):return round(p.ToMM(pos.x),4),round(p.ToMM(pos.y),4)
refs=[("R1",2),("R2",1),("C1",1),("R3",1)]
pads=[pad(r,n) for r,n in refs]
assert all(x.GetNetname()=="PWM_FILTER" for x in pads)
# All pads are horizontal 0805 at y32, common bus above the parts.
# Assert actual coordinates rather than assuming footprint orientation.
for a,(x,y) in zip(pads,[(69.9125,32),(74.0875,32),(80.0875,32),(86.0875,32)]):
 assert abs(mm(a.GetPosition())[0]-x)<.02 and abs(mm(a.GetPosition())[1]-y)<.02,(a.GetParent().GetReference(),mm(a.GetPosition()))
net=pads[0].GetNet()
def track(a,z):
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
for a in pads:track(a.GetPosition(),xy(mm(a.GetPosition())[0],28))
track(xy(69.9125,28),xy(86.0875,28))
p.SaveBoard(str(dst),b)
assert len(p.LoadBoard(str(dst)).GetFootprints())==len(f)
print("OK:",dst)
print("PWM_FILTER bus routed on F.Cu. DRC required. Other setpoint nets remain unconnected.")
