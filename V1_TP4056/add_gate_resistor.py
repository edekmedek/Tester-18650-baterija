# KiCad 10: add resistor footprint and one verified trace from MCP6002 OUTA to Rgate.
# Rgate other end remains unconnected until MOSFET part number/pinout verified.
from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_nets_R01.kicad_pcb"
dst=d/"Tester18650_V1_gate_R02.kicad_pcb"
lib=Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty")
if not src.exists(): raise SystemExit("Missing PCB: "+str(src))
if dst.exists(): raise SystemExit("Refusing to overwrite: "+str(dst))
b=p.LoadBoard(str(src))
if b is None: raise SystemExit("PCB load failed")
f={x.GetReference():x for x in b.GetFootprints()}
assert "RG1" not in f and "U1" in f
op=next(x for x in f["U1"].Pads() if x.GetNumber()=="1")
assert op.GetNetname()=="OPAMP_A_OUT"
rg=p.FootprintLoad(str(lib),"R_0805_2012Metric")
if rg is None: raise SystemExit("R_0805 footprint not found")
rg.SetReference("RG1");rg.SetValue("100R")
rg.SetPosition(p.VECTOR2I(p.FromMM(51),p.FromMM(43.09)))
b.Add(rg)
pads={x.GetNumber():x for x in rg.Pads()}
assert set(pads)=={"1","2"}
pads["2"].SetNet(op.GetNet())
# Draw only a net-matched trace between known U1 pin 1 and RG1 pin 2.
a=op.GetPosition();z=pads["2"].GetPosition()
track=p.PCB_TRACK(b)
track.SetStart(a);track.SetEnd(z)
track.SetWidth(p.FromMM(0.25))
track.SetLayer(p.F_Cu);track.SetNet(op.GetNet())
b.Add(track)
p.SaveBoard(str(dst),b)
check=p.LoadBoard(str(dst))
assert check and len(check.GetTracks())==1
print("OK:",dst)
print("RG1 100R footprint added; 1 trace U1.1 -> RG1.2, net OPAMP_A_OUT")
print("RG1.1 remains unconnected pending selected MOSFET pinout")
print("NOT validated by DRC; do not manufacture or connect a battery.")
