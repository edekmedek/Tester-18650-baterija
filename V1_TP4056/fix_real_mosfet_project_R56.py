from pathlib import Path
import re

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_asbuilt_R47.kicad_sch'
out=d/'Tester18650_V1_real_mosfet_R56.kicad_sch'
libpath=Path(r'C:\Program Files\KiCad\10.0\share\kicad\symbols\Transistor_FET.kicad_sym')
if not src.exists() or not libpath.exists():
 raise SystemExit('R47 schematic or transistor library missing')
if out.exists():raise SystemExit('R56 already exists')
def block(s,start):
 level=0;quoted=False;escape=False
 for i in range(start,len(s)):
  ch=s[i]
  if quoted:
   if escape:escape=False
   elif ch=='\\':escape=True
   elif ch=='"':quoted=False
  elif ch=='"':quoted=True
  elif ch=='(':level+=1
  elif ch==')':
   level-=1
   if level==0:return s[start:i+1]
 raise ValueError('Unbalanced s-expression')
def search_block(s,pattern):
 hits=list(re.finditer(pattern,s))
 if len(hits)!=1:raise RuntimeError('Expected one match for '+pattern+': '+str(len(hits)))
 return block(s,hits[0].start())
def q(s):
 return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'
def fmt(x):
 return ('%.4f'%x).rstrip('0').rstrip('.')
data=src.read_text(encoding='utf-8')
library=libpath.read_text(encoding='utf-8')
parent=search_block(library,r'\(symbol\s+"BUZ11"')
derived=search_block(library,r'\(symbol\s+"IRF3205"')
assert '(extends "BUZ11")' in derived
pins={}
for m in re.finditer(r'\(pin\s+(?:input|output|passive|power_in|power_out)',parent):
 item=block(parent,m.start())
 number=re.search(r'\(number\s+"([^"]+)"',item)
 at=re.search(r'\(at\s+(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)\)',item)
 if number and at:
  number=number.group(1)
  assert number not in pins
  pins[number]=(float(at.group(1)),float(at.group(2)))
assert set(pins)=={'1','2','3'},pins
embedded=parent.replace('(symbol "BUZ11"','(symbol "Transistor_FET:IRF3205"',1).replace('BUZ11_','IRF3205_')
# Replace library definition only (NOT the Q1 instance).
generic=search_block(data,r'\(symbol\s+"Audit:Pads_3"')
# Keep generic library as Q1 no longer uses it; add real symbol before closing lib_symbols.
libblock=search_block(data,r'\(lib_symbols\b')
data=data.replace(libblock,libblock[:-1]+'\n'+embedded+'\n)',1)
# Remove old Q1 instance, and its three generated endpoint labels/NC markers.
old=search_block(data,r'\(symbol\s+\(lib_id\s+"Audit:Pads_3"\)')
assert '(reference "Q1")' in old
data=data.replace(old,'',1)
# R47 audit layout contains Q1 at x=111.76 y=78.74, pins at x=104.14.
base_x=111.76;base_y=78.74
for pin,(name,delta) in {'1':('MOSFET_GATE',0.0),'2':(None,2.54),'3':('CURRENT_SENSE',5.08)}.items():
 oldx=fmt(base_x-7.62);oldy=fmt(base_y+delta)
 if name:
  pattern=r'\(label\s+"'+re.escape(name)+r'"\s+\(at\s+'+re.escape(oldx)+r'\s+'+re.escape(oldy)+r'\s+0\)'
 else:
  pattern=r'\(no_connect\s+\(at\s+'+re.escape(oldx)+r'\s+'+re.escape(oldy)+r'\)'
 old_item=search_block(data,pattern)
 data=data.replace(old_item,'',1)
# Put real Q1 far from other audit components on the same A3 page.
x=243.84;y=77.47
root_id=re.search(r'\(uuid\s+"([^"]+)"',data).group(1)
import uuid
def new_uuid():return str(uuid.uuid4())
def prop(k,v,px,py):
 return '(property '+q(k)+' '+q(v)+' (at '+fmt(px)+' '+fmt(py)+' 0) (effects (font (size 1 1))))'
new_symbol='(symbol (lib_id "Transistor_FET:IRF3205") (at '+fmt(x)+' '+fmt(y)+' 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid '+q(new_uuid())+')'
new_symbol+=prop('Reference','Q1',x,y-10)+prop('Value','IRF3205',x,y-8)
# Preserve exact footprint assignment from R47 via PCB audit instance.
match=re.search(r'\(property "Footprint" "([^"]+)"',old)
if not match:raise RuntimeError('Q1 footprint not found')
new_symbol+=prop('Footprint',match.group(1),x,y-6)
new_symbol+='(instances (project "Tester18650_V1_real_mosfet_R56" (path "/'+root_id+'" (reference "Q1") (unit 1)))) )'
for num,name in [('1','MOSFET_GATE'),('2',None),('3','CURRENT_SENSE')]:
 dx,dy=pins[num]
 px=fmt(x+dx);py=fmt(y-dy)
 if name:
  new_symbol+='(label '+q(name)+' (at '+px+' '+py+' 0) (effects (font (size 1 1)) (justify left bottom)) (uuid '+q(new_uuid())+'))'
 else:
  new_symbol+='(no_connect (at '+px+' '+py+') (uuid '+q(new_uuid())+'))'
data=data.replace('(sheet_instances',new_symbol+'\n(sheet_instances',1)
data=data.replace('Tester18650_V1_asbuilt_R47','Tester18650_V1_real_mosfet_R56')
data=data.replace('AS-BUILT PCB NET AUDIT R47','REAL MOSFET PIN TYPES - AUDIT R56').replace('(rev "R47")','(rev "R56")')
# An explicit same-basename .kicad_pro is required to pick up the project's local Audit symbol library.
import shutil
baseline=d/'Tester18650_V1_asbuilt_R47.kicad_pro'
project=out.with_suffix('.kicad_pro')
if not baseline.exists():raise SystemExit('R47 project missing; refusing to make incomplete R56')
if project.exists():raise SystemExit('R56 project already exists; refusing overwrite')
shutil.copyfile(baseline,project)
out.write_text(data,encoding='utf-8')
print('OK:',out)
print('IRF3205 Q1 uses actual BUZ11 inherited pin geometry and pin types.')
print('Q1 pins:',pins)
print('R56 project configuration copied; Q1 snapped onto KiCad 1.27 mm grid.')
print('Any remaining native-library symbol mismatch must be resolved, not ignored.')
print('R56 is NOT a battery-safe design.')
