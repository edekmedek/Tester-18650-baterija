from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_esp32_ground_R24.kicad_pcb'
dst=d/'Tester18650_V1_esp32_ground_R25.kicad_pcb'
if not src.exists():raise SystemExit('R24 missing')
if dst.exists():raise SystemExit('R25 exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
j=next(x for x in f['J3'].Pads() if x.GetNumber()=='3')
assert j.GetNetname()=='GND'
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def track(a,z):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.35));t.SetLayer(p.B_Cu);t.SetNet(j.GetNet());b.Add(t)
# J3 through-hole pin3 to existing GND B.Cu trace endpoint at (57.525,50).
# Avoid crossing VCC B.Cu vertical x35 y35..84.54 by routing below its endpoint.
track((32,87.08),(36,87.08))
track((36,87.08),(36,74))
track((36,74),(57.525,74))
track((57.525,74),(57.525,50))
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J3.3 GND routed on B.Cu; DRC REQUIRED. No battery.')
