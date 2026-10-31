from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import pcbnew as p

d=Path(__file__).resolve().parent
pcb=d/'Tester18650_V1_ina_sense_labels_R42.kicad_pcb'
sch=d/'Tester18650_V1_power_sources_R60.kicad_sch'
xml=d/'R61_schematic_netlist.xml'
report=d/'R61_netlist_comparison.txt'
cli=Path(r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe')
for item in (pcb,sch,cli):
 if not item.exists():raise SystemExit('Missing: '+str(item))
result=subprocess.run([str(cli),'sch','export','netlist','--format','kicadxml','--output',str(xml),str(sch)],capture_output=True,text=True)
if result.returncode:
 raise SystemExit('KiCad netlist export failed: '+result.stdout+' '+result.stderr)
board=p.LoadBoard(str(pcb))
pcb_nodes={}
for fp in board.GetFootprints():
 for pad in fp.Pads():
  pcb_nodes[(fp.GetReference(),pad.GetNumber())]=pad.GetNetname() or ''
root=ET.parse(xml).getroot()
net_nodes={}
power_nodes=[]
for net in root.findall('.//nets/net'):
 name=net.get('name','')
 for node in net.findall('node'):
  k=(node.get('ref',''),node.get('pin',''))
  if k in net_nodes or k in power_nodes:raise SystemExit('Duplicate schematic pin '+str(k))
  if k[0] in ('PF1','PF2'):
   power_nodes.append(k)
  else:
   net_nodes[k]=name
missing=sorted(set(pcb_nodes)-set(net_nodes))
extra=sorted(set(net_nodes)-set(pcb_nodes))
mismatches=[]
for key in sorted(set(pcb_nodes)&set(net_nodes)):
 expected=pcb_nodes[key]
 actual=net_nodes[key]
 if actual.startswith('/') and actual[1:]==expected:actual=expected
 if expected and expected!=actual:mismatches.append((key,expected,actual))
 if not expected and actual and not actual.startswith('unconnected-'):
  mismatches.append((key,'UNASSIGNED',actual))
lines=['R61 KiCad R60 schematic vs R42 PCB',
 'PCB pads: '+str(len(pcb_nodes)),
 'Schematic component pins: '+str(len(net_nodes)),
 'Power source markers excluded from physical PCB comparison: '+str(sorted(power_nodes)),
 'Missing pins: '+str(missing),
 'Extra pins: '+str(extra),
 'Mismatched nets: '+str(mismatches),
 'NOTE: logical net equality is not electrical safety approval.',
 'NO battery, charger or fabrication approval.']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('Saved:',report)
if missing or extra or mismatches:raise SystemExit('FAIL: inspect R61 report')
print('PASS: R60 schematic pin connections match R42 PCB, excluding nonphysical PWR_FLAG symbols.')
