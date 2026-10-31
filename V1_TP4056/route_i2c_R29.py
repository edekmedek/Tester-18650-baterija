from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_i2c_nets_R28.kicad_pcb'
dst=d/'Tester18650_V1_i2c_routed_R29.kicad_pcb'
if not src.exists():raise SystemExit('R28 missing')
if dst.exists():raise SystemExit('R29 exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def track(a,z,net):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
assert pad('J3',4).GetNetname()=='I2C_SDA'
assert pad('J3',5).GetNetname()=='I2C_SCL'
for ref,number,pts in [('J3',4,[(32,89.62),(38,89.62),(38,85.08),(60,85.08)]),('J3',5,[(32,92.16),(42,92.16),(42,87.62),(60,87.62)])]:
 n=pad(ref,number).GetNet()
 for a,z in zip(pts,pts[1:]):track(a,z,n)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('SDA/SCL routed on F.Cu; DRC REQUIRED. Physical breakout pin order not verified.')