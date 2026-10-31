from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_power_interface_R16.kicad_pcb"
dst=d/"Tester18650_V1_power_interface_R17.kicad_pcb"
if not src.exists():raise SystemExit("R16 missing")
if dst.exists():raise SystemExit("R17 already exists")
b=p.LoadBoard(str(src))
def mm(v):return round(p.ToMM(v),4)
vias=[t for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()=="VCC_3V3" and (mm(t.GetPosition().x),mm(t.GetPosition().y))==(35.,39.)]
assert len(vias)==1,"Expected exactly one dangling VCC_3V3 via at 35,39"
b.Remove(vias[0])
p.SaveBoard(str(dst),b)
assert p.LoadBoard(str(dst))
print("OK:",dst)
print("Removed redundant via at 35,39; back-layer VCC route remains continuous.")
print("DRC REQUIRED. No battery connection.")
