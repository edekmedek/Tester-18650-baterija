from pathlib import Path
import re, uuid, shutil

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_real_opamp_R59.kicad_sch'
dst=d/'Tester18650_V1_power_sources_R60.kicad_sch'
project=dst.with_suffix('.kicad_pro')
powerlib=Path(r'C:\Program Files\KiCad\10.0\share\kicad\symbols\power.kicad_sym')
for item in (src,src.with_suffix('.kicad_pro'),powerlib):
 if not item.exists():raise SystemExit('MISSING: '+str(item))
for item in (dst,project):
 if item.exists():raise SystemExit('Refusing overwrite '+str(item))
def block(s,start):
 n=0;q=False;esc=False
 for i in range(start,len(s)):
  c=s[i]
  if q:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':q=False
  elif c=='"':q=True
  elif c=='(':n+=1
  elif c==')':
   n-=1
   if n==0:return s[start:i+1]
 raise ValueError('unbalanced expression')
def one(s,pattern):
 arr=list(re.finditer(pattern,s))
 if len(arr)!=1:raise SystemExit('Expected one '+pattern+', got '+str(len(arr)))
 return block(s,arr[0].start())
def quoted(s):return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'
schematic=src.read_text(encoding='utf-8')
power=powerlib.read_text(encoding='utf-8')
symbol=one(power,r'\(symbol\s+"PWR_FLAG"')
if '(extends ' in symbol:raise SystemExit('PWR_FLAG inherited; inspect before using')
embedded=symbol.replace('(symbol "PWR_FLAG"','(symbol "power:PWR_FLAG"',1)
# KiCad internal symbol names remain PWR_FLAG_x_y; the embedded definition only needs lib namespace.
pin_exprs=list(re.finditer(r'\(pin\s+power_out\b',embedded))
if len(pin_exprs)!=1:raise SystemExit('Unexpected PWR_FLAG power pins: '+str(len(pin_exprs)))
pin=block(embedded,pin_exprs[0].start())
position=re.search(r'\(at\s+(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)\)',pin)
if not position:raise SystemExit('Cannot identify PWR_FLAG pin position')
dx,dy,angle=map(float,position.groups())
# Pin angle controls connection direction, not the pin's origin coordinate.
sym_libs=one(schematic,r'\(lib_symbols\b')
if '(symbol "power:PWR_FLAG"' in sym_libs:raise SystemExit('PWR_FLAG already embedded')
schematic=schematic.replace(sym_libs,sym_libs[:-1]+'\n'+embedded+'\n)',1)
sheet_uuid=re.search(r'\(uuid\s+"([^"]+)"',schematic)
if not sheet_uuid:raise SystemExit('Missing sheet uuid')
sheet_uuid=sheet_uuid.group(1)
def prop(k,v,x,y):
 return '(property '+quoted(k)+' '+quoted(v)+' (at '+str(x)+' '+str(y)+' 0) (effects (font (size 1 1))))'
added=[]
# Pin locations must be on KiCad 1.27mm connection grid.
for ref,net,x,y in [('PF1','VCC_3V3',260.35,151.13),('PF2','GND',260.35,158.75)]:
 # Position symbol such that its pin is exactly on x,y.
 sx=round(x-dx,4);sy=round(y+dy,4)
 item='(symbol (lib_id "power:PWR_FLAG") (at '+str(sx)+' '+str(sy)+' 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid '+quoted(str(uuid.uuid4()))+')'
 item+=prop('Reference',ref,sx,sy-5.08)+prop('Value','PWR_FLAG',sx,sy-2.54)
 item+='(instances (project '+quoted(dst.stem)+' (path '+quoted('/'+sheet_uuid)+' (reference '+quoted(ref)+') (unit 1)))) )'
 item+='(label '+quoted(net)+' (at '+str(x)+' '+str(y)+' 0) (effects (font (size 1 1)) (justify left bottom)) (uuid '+quoted(str(uuid.uuid4()))+'))'
 added.append(item)
schematic=schematic.replace('(sheet_instances','\n'.join(added)+'\n(sheet_instances',1)
schematic=schematic.replace('Tester18650_V1_real_opamp_R59',dst.stem).replace('(rev "R59")','(rev "R60")')
shutil.copyfile(src.with_suffix('.kicad_pro'),project)
dst.write_text(schematic,encoding='utf-8')
print('OK:',dst)
print('PWR_FLAG sources: VCC_3V3 and GND (external ESP32 supply ASSUMED, not electrically verified).')
print('PWR_FLAG is a schematic ERC declaration, NOT a physical protective device.')
print('Run ERC. No battery/fabrication approval.')
