from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_opamp_unused_R21.kicad_pcb'
dst=d/'Tester18650_V1_esp32_ground_R24.kicad_pcb'
if not src.exists():raise SystemExit('R21 board missing')
if dst.exists():raise SystemExit('R24 already exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
j=next(x for x in f['J3'].Pads() if x.GetNumber()=='3')
u=next(x for x in f['U1'].Pads() if x.GetNumber()=='4')
assert not j.GetNetname() and u.GetNetname()=='GND'
j.SetNet(u.GetNet())
p.SaveBoard(str(dst),b)
assert p.LoadBoard(str(dst))
print('OK:',dst)
print('J3 pin3 assigned GND, not routed; DRC should report one new unconnected item.')
print('Do not connect battery.')
