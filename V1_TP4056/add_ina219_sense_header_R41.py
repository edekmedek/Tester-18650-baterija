from pathlib import Path
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_battery_charger_routed_R39.kicad_pcb'
dst=d/'Tester18650_V1_ina_sense_header_R41.kicad_pcb'
if not src.exists():raise SystemExit('R39 board not found')
if dst.exists():raise SystemExit('R41 exists; refusing overwrite')
b=p.LoadBoard(str(src))
footprints={f.GetReference():f for f in b.GetFootprints()}
assert 'J5' not in footprints
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
root=Path(r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_PinHeader_2.54mm.pretty')
kind='PinHeader_1x02_P2.54mm_Vertical'
if not (root/(kind+'.kicad_mod')).exists():raise SystemExit('Footprint missing: '+str(root))
j=p.FootprintLoad(str(root),kind)
if j is None:raise SystemExit('Cannot load J5 footprint')
j.SetReference('J5')
j.SetValue('INA219_SENSE_CABLE')
j.SetPosition(xy(72,85))
pads={x.GetNumber():x for x in j.Pads()}
assert set(pads)=={'1','2'},set(pads)
def newnet(name):
 if any(n.GetNetname()==name for n in b.GetNetInfo().NetsByNetcode().values()):
  raise SystemExit('Existing net '+name)
 net=p.NETINFO_ITEM(b,name);b.Add(net);return net
pads['1'].SetNet(newnet('INA_VIN_PLUS'))
pads['2'].SetNet(newnet('INA_VIN_MINUS'))
b.Add(j)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J5.1 INA_VIN_PLUS and J5.2 INA_VIN_MINUS; NOT ROUTED to cell or load')
print('J4 is power and I2C ONLY; J5 is sensor analog input CABLE interface, not module physical footprint.')
print('IMPORTANT: module INA219 VIN+ and VIN- are shunt inputs. Actual breakout may already have onboard shunt.')
print('Run DRC. No battery, no fabrication approval.')
