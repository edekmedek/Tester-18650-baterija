from pathlib import Path
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_ina_power_R33.kicad_pcb'
dst=d/'Tester18650_V1_gate_pulldown_R35.kicad_pcb'
if not src.exists():raise SystemExit('R33 board missing')
if dst.exists():raise SystemExit('R35 board already exists: refusing overwrite')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
assert 'R4' not in f
def getnet(name):
 for n in b.GetNetInfo().NetsByNetcode().values():
  if n.GetNetname()==name:return n
 raise RuntimeError('Missing net: '+name)
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
root=Path(r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty')
name='R_0805_2012Metric'
if not (root/(name+'.kicad_mod')).exists():raise SystemExit('Footprint not installed')
r=p.FootprintLoad(str(root),name)
if r is None:raise SystemExit('Unable to load footprint')
r.SetReference('R4')
r.SetValue('100k')
r.SetPosition(xy(96,38))
pads={a.GetNumber():a for a in r.Pads()}
assert set(pads)=={'1','2'}
pads['1'].SetNet(getnet('MOSFET_GATE'))
pads['2'].SetNet(getnet('GND'))
b.Add(r)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('R4 100k gate-to-GND pulldown footprint ADDED, NOT ROUTED. Run DRC.')
print('R4 is not independent hardware protection; linear-mode MOSFET safety remains unresolved.')
