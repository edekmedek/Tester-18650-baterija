from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_i2c_routed_R29.kicad_pcb'
dst=d/'Tester18650_V1_ina_power_R30.kicad_pcb'
if not src.exists():raise SystemExit('R29 missing')
if dst.exists():raise SystemExit('R30 exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
v=pad('J3',2).GetNet();g=pad('J3',3).GetNet()
assert v.GetNetname()=='VCC_3V3' and g.GetNetname()=='GND'
assert not pad('J4',1).GetNetname() and not pad('J4',2).GetNetname()
pad('J4',1).SetNet(v);pad('J4',2).SetNet(g)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J4.1 assigned VCC_3V3; J4.2 assigned GND. Not routed; run DRC.')
print('Cable mapping ONLY. Verify INA219 breakout supports 3.3V and pin order before physical connection.')