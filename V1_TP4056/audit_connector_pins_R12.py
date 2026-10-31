from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_setpoint_R12.kicad_pcb"
if not src.exists():raise SystemExit("R12 not found")
b=p.LoadBoard(str(src))
print("R12 HARDWARE PIN AUDIT - read only")
for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
 print("\n",f.GetReference(),f.GetValue(),f.GetFPIDAsString())
 for a in sorted(f.Pads(),key=lambda a:int(a.GetNumber()) if a.GetNumber().isdigit() else 999):
  pos=a.GetPosition()
  print(" PAD",a.GetNumber(),"x",round(p.ToMM(pos.x),3),"y",round(p.ToMM(pos.y),3),"NET",a.GetNetname() or "<NONE>")
print("\nNO MODIFICATIONS. Check physical ESP32 module, TP4056 board and INA219 breakout pin labels before assigning connector nets.")
