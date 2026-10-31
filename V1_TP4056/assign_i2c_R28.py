from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_esp32_ground_R27.kicad_pcb'
dst=d/'Tester18650_V1_i2c_nets_R28.kicad_pcb'
if not src.exists():raise SystemExit('R27 missing')
if dst.exists():raise SystemExit('R28 exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
for ref,num in [('J3',4),('J3',5),('J4',3),('J4',4)]:assert not pad(ref,num).GetNetname()
for name,points in [('I2C_SDA',[('J3',4),('J4',3)]),('I2C_SCL',[('J3',5),('J4',4)])]:
 n=p.NETINFO_ITEM(b,name);b.Add(n)
 for ref,num in points:pad(ref,num).SetNet(n)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('Logical cable-interface nets only: J3.4 to J4.3 SDA; J3.5 to J4.4 SCL.')
print('NOT ROUTED; module physical pin order UNVERIFIED; DRC required.')