from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_outline_R03.kicad_pcb"
dst=d/"Tester18650_V1_irf3205_R04.kicad_pcb"
if not src.exists(): raise SystemExit("Missing R03 board")
if dst.exists(): raise SystemExit("Refusing overwrite")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
assert "Q1" in f and "RG1" in f
assert len(b.GetTracks())==1
q=f["Q1"];rg=f["RG1"]
assert q.GetFPIDAsString().endswith("TO-220-3_Vertical")
q.SetValue("IRF3205")
gate=next(x for x in q.Pads() if x.GetNumber()=="1")
rpad=next(x for x in rg.Pads() if x.GetNumber()=="1")
assert not gate.GetNetname() and not rpad.GetNetname()
net=p.NETINFO_ITEM(b,"MOSFET_GATE")
b.Add(net)
gate.SetNet(net);rpad.SetNet(net)
# Connect only verified TO-220 gate (pad 1) to series resistor free end.
# One short trace per segment, with orthogonal routing and a clearance check deferred to DRC.
a=rpad.GetPosition();z=gate.GetPosition()
corner=p.VECTOR2I(z.x,a.y)
for start,end in ((a,corner),(corner,z)):
    if start==end: continue
    tr=p.PCB_TRACK(b)
    tr.SetStart(start);tr.SetEnd(end)
    tr.SetWidth(p.FromMM(0.25))
    tr.SetLayer(p.F_Cu);tr.SetNet(net)
    b.Add(tr)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetTracks())==3
print("OK:",dst)
print("Q1 IRF3205 gate pad 1 connected to RG1 pad 1, MOSFET_GATE")
print("Tracks:",len(v.GetTracks()))
print("WARNING: Run DRC. Drain, source, cell and charging circuitry remain unconnected.")
