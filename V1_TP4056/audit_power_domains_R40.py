from pathlib import Path
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_battery_charger_routed_R39.kicad_pcb'
report=d/'R40_power_domains_report.txt'
if not src.exists():raise SystemExit('Missing R39 PCB')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
expected={('J1','1'):'CELL_PLUS',('J1','2'):'CELL_MINUS',('J2','1'):'CELL_PLUS',('J2','2'):'CELL_MINUS',('J2','3'):'TP_OUT_PLUS',('J2','4'):'TP_OUT_MINUS',('J3','3'):'GND',('J4','2'):'GND',('Q1','2'):''}
lines=['R40 POWER DOMAIN AUDIT (READ ONLY)','Board: '+str(src),'']
for (ref,num),want in expected.items():
 got=pad(ref,num).GetNetname()
 lines.append(f'{ref}.{num}: {got or "UNASSIGNED"}')
 if got!=want:raise SystemExit(f'UNEXPECTED {ref}.{num}: {got!r}; expected {want!r}')
assert len({'CELL_MINUS','TP_OUT_MINUS','GND'})==3
lines+=['','PASS: Battery negative, charger protected output negative and controller ground are distinct named nets.','PASS: MOSFET drain has no assigned net; no load path approved.','CAUTION: distinct nets in the PCB do not prove physical isolation inside TP4056 module.','BLOCKED: actual module pinout/protection, charger/load switch, low-voltage cutoff, current control and linear SOA.','NOT READY for 18650 connection, charging, discharging or fabrication.']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('Saved:',report)
