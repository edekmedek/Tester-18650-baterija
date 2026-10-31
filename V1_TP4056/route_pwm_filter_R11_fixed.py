from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_setpoint_R10.kicad_pcb"
dst=d/"Tester18650_V1_setpoint_R11.kicad_pcb"
if not src.exists():raise SystemExit("R10 missing")
if dst.exists():raise SystemExit("R11 already exists")
b=p.LoadBoard(str(src))
f={v.GetReference():v for v in b.GetFootprints()}
def pad(ref,num):
 matches=[x for x in f[ref].Pads() if x.GetNumber()==str(num)]
 assert len(matches)==1,(ref,num,len(matches))
 return matches[0]
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def mm(pos):return round(p.ToMM(pos.x),4),round(p.ToMM(pos.y),4)
refs=[("R1",2),("R2",1),("C1",1),("R3",1)]
pads=[pad(r,n) for r,n in refs]
assert all(a.GetNetname()=="PWM_FILTER" for a in pads)
coords=[mm(a.GetPosition()) for a in pads]
for ref,coord in zip(refs,coords):print(ref,coord)
assert all(abs(y-32)<.1 for x,y in coords),coords
assert coords==sorted(coords),coords
assert all(60<x<95 for x,y in coords)
net=pads[0].GetNet()
def track(a,z):
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
for a,(x,y) in zip(pads,coords):track(a.GetPosition(),xy(x,28))
track(xy(coords[0][0],28),xy(coords[-1][0],28))
p.SaveBoard(str(dst),b)
assert len(p.LoadBoard(str(dst)).GetFootprints())==len(f)
print("OK:",dst)
print("PWM_FILTER routed. Run DRC. Battery not safe to connect.")
