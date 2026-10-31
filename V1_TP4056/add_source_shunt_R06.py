from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_irf3205_R05.kicad_pcb"
dst=d/"Tester18650_V1_shunt_R06.kicad_pcb"
if not src.exists():raise SystemExit("R05 board missing")
if dst.exists():raise SystemExit("Refusing overwrite R06")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
assert f["Q1"].GetValue()=="IRF3205"
def pad(ref,num):
    matches=[x for x in f[ref].Pads() if x.GetNumber()==num]
    assert len(matches)==1,(ref,num)
    return matches[0]
source=pad("Q1","3")
shunt_hi=pad("RSH1","1")
shunt_lo=pad("RSH1","2")
sense=pad("U1","2")
ground=pad("U1","4")
assert sense.GetNetname()=="CURRENT_SENSE" and ground.GetNetname()=="GND"
assert all(not x.GetNetname() for x in (source,shunt_hi,shunt_lo))
source.SetNet(sense.GetNet())
shunt_hi.SetNet(sense.GetNet())
shunt_lo.SetNet(ground.GetNet())
# Both Q1 source and shunt are through-hole, use back copper to avoid gate traces.
a=source.GetPosition();z=shunt_hi.GetPosition()
# route source down and left, avoids Q1 pin1/2 on back and gate trace at y55
mid=p.VECTOR2I(a.x,z.y)
for start,end in ((a,mid),(mid,z)):
    t=p.PCB_TRACK(b);t.SetStart(start);t.SetEnd(end)
    t.SetWidth(p.FromMM(0.75));t.SetLayer(p.B_Cu);t.SetNet(sense.GetNet());b.Add(t)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetFootprints())==8
print("OK:",dst)
print("Q1 Source pad3 -> RSH1 pad1, CURRENT_SENSE (B.Cu, 0.75mm)")
print("RSH1 pad2 assigned GND but NOT routed")
print("U1 pin2 assigned CURRENT_SENSE but NOT routed")
print("Run DRC; battery and TP4056 remain disconnected.")
