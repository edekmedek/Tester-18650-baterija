from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import pcbnew as p

d=Path(__file__).resolve().parent
pcb=d/'Tester18650_V1_ina_sense_labels_R42.kicad_pcb'
sch=d/'Tester18650_V1_asbuilt_R47.kicad_sch'
xml=d/'R49_schematic_netlist.xml'
report=d/'R49_netlist_comparison.txt'
cli=Path(r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe')
for item in (pcb,sch,cli):
 if not item.exists():raise SystemExit('Missing: '+str(item))
result=subprocess.run([str(cli),'sch','export','netlist','--format','kicadxml','--output',str(xml),str(sch)],capture_output=True,text=True)
if result.returncode:
 raise SystemExit('KiCad netlist export failed: '+result.stdout+' '+result.stderr)
board=p.LoadBoard(str(pcb))
pcb_nodes={}
for fp in board.GetFootprints():
 ref=fp.GetReference()
 for pad in fp.Pads():
  pcb_nodes[(ref,pad.GetNumber())]=pad.GetNetname() or ''
root=ET.parse(xml).getroot()
net_nodes={}
for net in root.findall('.//nets/net'):
 name=net.get('name','')
 for node in net.findall('node'):
  k=(node.get('ref',''),node.get('pin',''))
  if k in net_nodes:raise SystemExit('Duplicate schematic pin '+str(k))
  net_nodes[k]=name
missing=sorted(k for k,v in pcb_nodes.items() if v and k not in net_nodes)
extra=sorted(set(net_nodes)-set(pcb_nodes))
mismatches=[]
for key in sorted(set(pcb_nodes)&set(net_nodes)):
 a=pcb_nodes[key]
 z=net_nodes[key]
 if z.startswith('/') and z[1:]==a:z=a
 if a and a!=z:
  mismatches.append((key,a,z))
singletons={}
for key,value in pcb_nodes.items():
 if value:singletons[value]=singletons.get(value,0)+1
lines=['R49 KiCad XML netlist vs actual R42 PCB','PCB pad count: '+str(len(pcb_nodes)),'Netlist XML nodes: '+str(len(net_nodes)),'Missing assigned schematic nodes: '+str(len(missing)),'Extra schematic nodes: '+str(len(extra)),'Mismatched net names: '+str(len(mismatches))]
lines+=['PCB assigned-only pins: '+str(missing),'Schematic-only pins: '+str(extra)]
lines+=['Net mismatches: '+str(mismatches)]
lines+=['Singleton nets (intentionally isolated names): '+str(sorted(x for x,n in singletons.items() if n==1))]
lines+=['NOTE: PCB/netlist agreement is not electrical design validation.','No battery or fabrication approval.']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('Saved:',report)
if missing or extra or mismatches:raise SystemExit('FAIL: PCB and schematic do not match. Check R49 report.')
print('PASS: all assigned pin nets match, after normalizing KiCad local-label / prefixes.')
