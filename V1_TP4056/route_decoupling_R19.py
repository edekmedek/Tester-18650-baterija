from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_decoupling_R18.kicad_pcb"
dst=d/"Tester18650_V1_decoupling_R19.kicad_pcb"
if not src.exists():raise SystemExit("R18 missing")
if dst.exists():raise SystemExit("R19 already exists")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
assert "C2" in f
pads={x.GetNumber():x for x in f["C2"].Pads()}
assert pads["1"].GetNetname()=="VCC_3V3" and pads["2"].GetNetname()=="GND"
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def route(a,z,net,layer=p.F_Cu):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(x,y,net):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
# VCC from existing route end x64 y40.5 to C2 pad1 x66.05 y46
v=pads["1"].GetNet()
route((64,40.5),(64,46),v)
route((64,46),(66.05,46),v)
# Ground: short F.Cu via from C2 pad2 then B.Cu to existing ground track near U1.
g=pads["2"].GetNet()
route((67.95,46),(70,46),g)
via(70,46,g)
route((70,46),(70,50),g,p.B_Cu)
route((70,50),(57.525,50),g,p.B_Cu)
p.SaveBoard(str(dst),b)
assert p.LoadBoard(str(dst))
print("OK:",dst)
print("C2 VCC and GND tracks added. KiCad DRC REQUIRED. DO NOT connect battery.")
