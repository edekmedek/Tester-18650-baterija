from pathlib import Path
from collections import defaultdict
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_decoupling_R19.kicad_pcb"
out=d/"R20_electrical_audit.txt"
if not src.exists():raise SystemExit("Missing R19 board")
b=p.LoadBoard(str(src))
lines=["R20 READ-ONLY ELECTRICAL AUDIT","Board: "+src.name,"No PCB modifications performed.",""]
nets=defaultdict(list)
for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
 lines.append(f"{f.GetReference()} {f.GetValue()} [{f.GetFPIDAsString()}]")
 for a in sorted(f.Pads(),key=lambda a:(len(a.GetNumber()),a.GetNumber())):
  x=p.ToMM(a.GetPosition().x);y=p.ToMM(a.GetPosition().y)
  n=a.GetNetname() or "UNASSIGNED"
  lines.append(f"  pin {a.GetNumber():>2}  {n:<22} ({x:.3f}, {y:.3f})")
  nets[n].append(f"{f.GetReference()}.{a.GetNumber()}")
lines+=["","NET MEMBERSHIP"]
for n,m in sorted(nets.items()):
 lines.append(f"{n}: {', '.join(m)}")
lines+=["","SAFETY GATE","DRC 0 does NOT imply a complete schematic or safe battery operation.","Do not connect battery, fabricate, or assume module pinout."]
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("AUDIT SAVED:",out)
print("Unassigned pads:",len(nets.get("UNASSIGNED",[])))
print("Unassigned list:",", ".join(nets.get("UNASSIGNED",[])))
