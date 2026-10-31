from pathlib import Path
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_battery_charger_nets_R38.kicad_pcb'
dst=d/'Tester18650_V1_battery_charger_routed_R39.kicad_pcb'
if not src.exists():raise SystemExit('R38 board missing')
if dst.exists():raise SystemExit('R39 already exists; refusing overwrite')
b=p.LoadBoard(str(src))
f={foot.GetReference():foot for foot in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def check(name,a,z):
 assert pad(*a).GetNetname()==name,(a,pad(*a).GetNetname())
 assert pad(*z).GetNetname()==name,(z,pad(*z).GetNetname())
 return pad(*a).GetNet()
def track(points,n):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b)
  t.SetStart(xy(*a));t.SetEnd(xy(*z))
  t.SetWidth(p.FromMM(0.5))
  t.SetLayer(p.F_Cu);t.SetNet(n);b.Add(t)
pos=check('CELL_PLUS',('J2','1'),('J1','1'))
neg=check('CELL_MINUS',('J2','2'),('J1','2'))
# Dedicated opposite-side corridors separate cell rails from other connector pins.
track([(32,35),(28,35),(28,63),(32,63)],pos)
track([(32,37.54),(38,37.54),(38,65.54),(32,65.54)],neg)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J2 B+ to J1 cell+ and J2 B- to J1 cell- routed on F.Cu, 0.5 mm.')
print('Run DRC; battery charger/load electrical safety NOT VERIFIED.')
print('J2 is a logical cable mapping, never assume physical TP4056 footprint/pad order.')
