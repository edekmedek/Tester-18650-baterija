from pathlib import Path
import re
d=Path(__file__).resolve().parent
root=Path(r'C:\Program Files\KiCad\10.0\share\kicad\symbols')
out=d/'R53_resolved_pin_map.txt'
def block(s,start):
 depth=0;quoted=False;escape=False
 for i in range(start,len(s)):
  c=s[i]
  if quoted:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:return s[start:i+1]
 raise RuntimeError('Unbalanced symbol block')
def find_symbol(lib,name):
 text=(root/(lib+'.kicad_sym')).read_text(encoding='utf-8')
 hits=list(re.finditer(r'\(symbol\s+"'+re.escape(name)+r'"',text))
 if len(hits)!=1:raise SystemExit('Unexpected symbol hits '+lib+':'+name+' = '+str(len(hits)))
 return block(text,hits[0].start())
def pins(text):
 records=[]
 for m in re.finditer(r'\(pin\s+(input|output|passive|power_in|power_out|open_collector|open_emitter|bidirectional|tri_state|no_connect|unspecified)\b',text):
  part=block(text,m.start())
  num=re.search(r'\(number\s+"([^"]+)"',part)
  name=re.search(r'\(name\s+"([^"]+)"',part)
  if num:records.append((num.group(1), name.group(1) if name else '?', m.group(1)))
 unique={}
 for n,name,typ in records:
  if n in unique and unique[n]!=(name,typ):raise SystemExit('Inconsistent pin '+n)
  unique[n]=(name,typ)
 return unique
items=[('Amplifier_Operational','MCP6002-xSN','LM2904',set(map(str,range(1,9)))),('Transistor_FET','IRF3205','BUZ11',{'1','2','3'})]
lines=['R53 inherited KiCad symbol pin mapping','']
for lib,part,parent,expected in items:
 candidate=find_symbol(lib,part)
 pm=re.search(r'\(extends\s+"([^"]+)"',candidate)
 if not pm or pm.group(1)!=parent:raise SystemExit('Unexpected inheritance for '+part)
 inherited=find_symbol(lib,parent)
 assigned=pins(inherited)
 if set(assigned)!=expected:raise SystemExit('Unexpected pin count/numbers in '+parent+': '+str(assigned))
 lines.extend([lib+':'+part+' extends '+parent,'Verified electrical pin mapping:'])
 for num in sorted(assigned,key=int):
  name,typ=assigned[num];lines.append('  '+num+' '+name+' '+typ)
 lines.append('')
if pins(find_symbol('Amplifier_Operational','MCP6002-xMC')) and '9' not in pins(find_symbol('Amplifier_Operational','MCP6002-xMC')):
 raise SystemExit('Unexpected MCP6002-xMC pins')
lines+=['This checks installed library pin TYPES and numbers, not real device operating limits.','No battery hookup or fabrication approval.']
out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('Saved:',out)
