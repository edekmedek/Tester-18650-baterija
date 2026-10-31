from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_esp32_ground_R26.kicad_pcb'
dst=d/'Tester18650_V1_esp32_ground_R27.kicad_pcb'
if not src.exists():raise SystemExit('R26 missing')
if dst.exists():raise SystemExit('R27 already exists')
b=p.LoadBoard(str(src))
def pos(v):return round(p.ToMM(v.x),3),round(p.ToMM(v.y),3)
a=[t for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND' and pos(t.GetPosition())==(57.525,50.0)]
assert len(a)==2,f'Expected exactly two duplicate GND vias; found {len(a)}'
b.Remove(a[-1])
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('Removed one duplicate GND via at (57.525,50). Run DRC.')