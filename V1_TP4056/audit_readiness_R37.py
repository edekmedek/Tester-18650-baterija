from pathlib import Path
import csv
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_gate_pulldown_R36.kicad_pcb'
out=d/'R37_pad_net_audit.csv'
report=d/'R37_readiness_report.txt'
if not src.exists():raise SystemExit('R36 board missing')
b=p.LoadBoard(str(src))
rows=[]
for f in sorted(b.GetFootprints(),key=lambda x:x.GetReference()):
 for pad in sorted(f.Pads(),key=lambda x:int(x.GetNumber()) if x.GetNumber().isdigit() else 999):
  pos=pad.GetPosition()
  rows.append([f.GetReference(),f.GetValue(),pad.GetNumber(),pad.GetNetname() or 'UNASSIGNED',round(p.ToMM(pos.x),4),round(p.ToMM(pos.y),4)])
with out.open('w',newline='',encoding='utf-8-sig') as fh:
 w=csv.writer(fh);w.writerow(['Ref','Value','Pad','Net','X_mm','Y_mm']);w.writerows(rows)
unassigned=[r for r in rows if r[3]=='UNASSIGNED']
lines=['R37 READ-ONLY ELECTRICAL AUDIT','Source: '+str(src),'Total pads: '+str(len(rows)),'Unassigned pads: '+str(len(unassigned))]
lines+=['  '+r[0]+'.'+r[2]+' '+r[1] for r in unassigned]
for ref,num,expected in [('R4','1','MOSFET_GATE'),('R4','2','GND'),('J4','1','VCC_3V3'),('J4','2','GND'),('J4','3','I2C_SDA'),('J4','4','I2C_SCL')]:
 match=[r for r in rows if r[0]==ref and r[2]==num]
 if len(match)!=1 or match[0][3]!=expected:raise SystemExit('NET MISMATCH '+ref+'.'+num+' expected '+expected)
lines+=['Verified assigned logical nets for R4 and J4.','DANGER: KiCad DRC checks routed nets, not complete circuit design.','No source KiCad schematic/ERC confirmed; charger, protection, ADC sensing, independent cutoff and MOSFET SOA NOT verified.','No battery or charger connection; no fabrication approval.']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('CSV:',out)
print('Report:',report)
