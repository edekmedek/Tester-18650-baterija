from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_power_interface_R17.kicad_pcb"
dst=d/"Tester18650_V1_decoupling_R18.kicad_pcb"
if not src.exists():raise SystemExit("R17 missing")
if dst.exists():raise SystemExit("R18 already exists")
b=p.LoadBoard(str(src))
root=Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty")
name="C_0805_2012Metric"
assert (root/(name+".kicad_mod")).exists(),str(root)
c=p.FootprintLoad(str(root),name)
if c is None:raise SystemExit("Cannot load capacitor footprint")
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def net(name):
 for v in b.GetNetInfo().NetsByNetcode().values():
  if v.GetNetname()==name:return v
 raise RuntimeError("Net missing: "+name)
c.SetReference("C2");c.SetValue("100n");c.SetPosition(xy(67,46))
pads={a.GetNumber():a for a in c.Pads()}
assert set(pads)=={"1","2"}
pads["1"].SetNet(net("VCC_3V3"))
pads["2"].SetNet(net("GND"))
b.Add(c)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert len(v.GetFootprints())==len(b.GetFootprints())
print("OK:",dst)
print("C2 100n placed near U1. NOT ROUTED. Run DRC; two unconnected pads expected.")
print("Battery not safe to connect.")
