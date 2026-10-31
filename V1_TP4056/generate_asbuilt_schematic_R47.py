from pathlib import Path
import uuid
import pcbnew as p

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_ina_sense_labels_R42.kicad_pcb'
out=d/'Tester18650_V1_asbuilt_R47.kicad_sch'
if not src.exists():raise SystemExit('R42 PCB missing')
if out.exists():raise SystemExit('R47 already exists; refusing overwrite')
b=p.LoadBoard(str(src))
fps=sorted(b.GetFootprints(),key=lambda x:x.GetReference())
root=str(uuid.uuid4())
uid=lambda:str(uuid.uuid4())
def q(s):return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'
def f(n):return ('%.4f'%n).rstrip('0').rstrip('.')
def prop(k,v,x,y):
 return '(property '+q(k)+' '+q(v)+f' (at {f(x)} {f(y)} 0) (effects (font (size 1 1))))'
def pads(fp):return sorted(fp.Pads(),key=lambda a:int(a.GetNumber()))
def resolved_footprint(fp):
 raw=str(fp.GetFPIDAsString())
 if ':' in raw:
  nick,item=raw.split(':',1)
  folder=Path(r'C:\\Program Files\\KiCad\\10.0\\share\\kicad\\footprints')/(nick+'.pretty')
  if (folder/(item+'.kicad_mod')).exists():return raw
 item=raw.split(':')[-1]
 rootfp=Path(r'C:\\Program Files\\KiCad\\10.0\\share\\kicad\\footprints')
 guesses={
  'C':'Capacitor_SMD','R':'Resistor_SMD',
  'J':'Connector_PinHeader_2.54mm','Q':'Package_TO_SOT_THT','U':'Package_SO',
 }
 ref=fp.GetReference()
 first=ref[0]
 options=[folder for folder in rootfp.glob('*.pretty') if (folder/(item+'.kicad_mod')).exists()]
 if len(options)==1:return options[0].stem+':'+item
 if len(options)>1:
  match=[folder for folder in options if folder.stem.startswith(guesses.get(first,'__NONE__'))]
  if len(match)==1:return match[0].stem+':'+item
 print('UNVERIFIED footprint reference',ref,'FPID',raw,'matching libraries:',[x.stem for x in options])
 return raw

def lib(n):
 h=max(5.08,(n-1)*2.54+5.08)
 t=['(symbol '+q('Audit:Pads_'+str(n))+' (pin_numbers (hide yes)) (pin_names (offset 0) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)',
 prop('Reference','J',0,3),prop('Value','Pads_'+str(n),0,-3),
 '(symbol '+q('Pads_'+str(n)+'_0_1')+f' (rectangle (start -5.08 2.54) (end 5.08 {f(-h+2.54)}) (stroke (width 0.254) (type default)) (fill (type background))))',
 '(symbol '+q('Pads_'+str(n)+'_1_1')]
 for i in range(n):
  t.append(f'(pin passive line (at -7.62 {f(-i*2.54)} 0) (length 2.54) (name {q(str(i+1))} (effects (font (size 1 1)))) (number {q(str(i+1))} (effects (font (size 1 1)))) )')
 return ''.join(t)+'))'
for fp in fps:
 nums=[a.GetNumber() for a in pads(fp)]
 if nums!=[str(i) for i in range(1,len(nums)+1)]:raise SystemExit(f'Unsupported pad numbering {fp.GetReference()}: {nums}')
count=sorted(set(len(pads(fp)) for fp in fps))
s=['(kicad_sch','(version 20250114)','(generator "eeschema")','(generator_version "10.0")','(uuid '+q(root)+')','(paper "A3")','(title_block (title "18650 - AS-BUILT PCB NET AUDIT R47") (rev "R47"))','(lib_symbols',*(lib(n) for n in count),')']
for idx,fp in enumerate(fps):
 n=len(pads(fp));x=40.64+(idx//6)*71.12;y=31.75+(idx%6)*46.99;ref=fp.GetReference()
 s.append('(symbol (lib_id '+q('Audit:Pads_'+str(n))+f') (at {f(x)} {f(y)} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid())})'+prop('Reference',ref,x,y-7)+prop('Value',fp.GetValue(),x,y-5)+prop('Footprint',resolved_footprint(fp),x,y-3)+'(instances (project '+q(out.stem)+' (path '+q('/'+root)+' (reference '+q(ref)+') (unit 1))))'+')')
 for i,pad in enumerate(pads(fp)):
  px=x-7.62;py=y+i*2.54;net=pad.GetNetname()
  if net:s.append('(label '+q(net)+f' (at {f(px)} {f(py)} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid {q(uid())}))')
  else:s.append(f'(no_connect (at {f(px)} {f(py)}) (uuid {q(uid())}))')
s+=['(sheet_instances (path "/" (page "1")))',')']
data='\n'.join(s)+'\n'
depth=0;quoted=False;escaped=False
for ch in data:
 if quoted:
  if escaped:escaped=False
  elif ch=='\\':escaped=True
  elif ch=='"':quoted=False
 elif ch=='"':quoted=True
 elif ch=='(':depth+=1
 elif ch==')':depth-=1
 if depth<0:raise SystemExit('Syntax parentheses unbalanced')
assert depth==0 and not quoted
# Resolve embedded custom symbols with a project-local library, preserving original PCB-only net names.
libfile=d/'Audit.kicad_sym'
table=d/'sym-lib-table'
project=d/(out.stem+'.kicad_pro')
libdata='(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+ '\n'.join(lib(n).replace(q('Audit:Pads_'+str(n)),q('Pads_'+str(n)),1) for n in count)+'\n)\n'
if libfile.exists() and libfile.read_text(encoding='utf-8')!=libdata:
 raise SystemExit('Existing Audit.kicad_sym differs; refusing overwrite')
if table.exists() and 'name "Audit"' not in table.read_text(encoding='utf-8'):
 raise SystemExit('Existing sym-lib-table requires manual library merge; refusing overwrite')
libfile.write_text(libdata,encoding='utf-8')
if not project.exists():
 project.write_text('{"meta":{"filename":'+q(project.name)+',"version":1}}\n',encoding='utf-8')
if table.exists():
 print('Symbol library table exists:',table)
else:
 print('Creating symbol library table:',table)
 table.write_text('(sym_lib_table (lib (name "Audit") (type "KiCad") (uri "${KIPRJMOD}/Audit.kicad_sym") (options "") (descr "")))\n',encoding='utf-8')
out.write_text(data,encoding='utf-8')
print('OK:',out,'footprints:',len(fps),'pads:',sum(len(pads(x)) for x in fps))
print('R47: local Audit library, project file and resolved installed footprint IDs generated.')
print('R47 is AS-BUILT ONLY, not an electrical design or fabrication approval.')
print('Run KiCad schematic netlist export and ERC; audit warnings expected.')
