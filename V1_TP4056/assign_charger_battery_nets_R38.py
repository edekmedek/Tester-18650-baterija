from pathlib import Path
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_gate_pulldown_R36.kicad_pcb'
dst=d/'Tester18650_V1_battery_charger_nets_R38.kicad_pcb'
if not src.exists():raise SystemExit('R36 PCB not found')
if dst.exists():raise SystemExit('R38 already exists; refusing overwrite')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):
 return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
for ref,num in [('J1',1),('J1',2),('J2',1),('J2',2),('J2',3),('J2',4)]:
 assert not pad(ref,num).GetNetname(),f'Already assigned: {ref}.{num}'
def new(name):
 for existing in b.GetNetInfo().NetsByNetcode().values():
  if existing.GetNetname()==name:raise SystemExit('Net already exists: '+name)
 n=p.NETINFO_ITEM(b,name);b.Add(n);return n
for name,points in [
 ('CELL_PLUS',[('J1',1),('J2',1)]),
 ('CELL_MINUS',[('J1',2),('J2',2)]),
 ('TP_OUT_PLUS',[('J2',3)]),
 ('TP_OUT_MINUS',[('J2',4)])
]:
 n=new(name)
 for ref,num in points:pad(ref,num).SetNet(n)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J1.1 CELL_PLUS <-> J2.1 B+ logical net, NOT ROUTED')
print('J1.2 CELL_MINUS <-> J2.2 B- logical net, NOT ROUTED')
print('J2.3 TP_OUT_PLUS; J2.4 TP_OUT_MINUS: deliberately ISOLATED')
print('J2.5/J2.6 remain unassigned; J2 is CABLE INTERFACE, NOT module footprint')
print('NO BATTERY CONNECTION: verify actual TP4056 silkscreen, protection and charger/load interlock first.')
print('Run DRC; two unconnected battery pairs expected.')
