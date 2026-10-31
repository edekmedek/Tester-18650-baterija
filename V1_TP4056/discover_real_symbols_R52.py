from pathlib import Path
import re

d=Path(__file__).resolve().parent
root=Path(r'C:\Program Files\KiCad\10.0\share\kicad\symbols')
out=d/'R52_symbol_discovery.txt'
if not root.is_dir():raise SystemExit('Missing symbol directory: '+str(root))
def balanced(src,start):
 level=0;quoted=False;esc=False
 for i in range(start,len(src)):
  c=src[i]
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':level+=1
  elif c==')':
   level-=1
   if level==0:return src[start:i+1]
 raise RuntimeError('Unclosed s-expression')
def pin_records(symbol):
 records=[]
 for m in re.finditer(r'\(pin\s+(?:input|output|passive|power_in|power_out|open_collector|open_emitter|bidirectional|tri_state|no_connect|unspecified)\b',symbol):
  v=balanced(symbol,m.start())
  num=re.search(r'\(number\s+"([^"]+)"',v)
  name=re.search(r'\(name\s+"([^"]+)"',v)
  if num:records.append((num.group(1),name.group(1) if name else '?',m.group(0)))
 return records
lines=['R52 installed KiCad symbol discovery','Search: MCP6002, IRF3205, MCP600x, generic compatible symbols','']
for library in sorted(root.glob('*.kicad_sym')):
 content=library.read_text(encoding='utf-8',errors='replace')
 names=list(re.finditer(r'\(symbol\s+"([^"]+)"',content))
 hits=[m for m in names if any(k in m.group(1).upper() for k in ('MCP600','IRF3205'))]
 if not hits:continue
 lines.append('LIBRARY '+library.name)
 for match in hits:
  name=match.group(1)
  symbol=balanced(content,match.start())
  parent=re.search(r'\(extends\s+"([^"]+)"',symbol)
  pins=pin_records(symbol)
  lines.append('  SYMBOL '+name+' extends='+str(parent.group(1) if parent else '-')+' local_pin_count='+str(len(pins)))
  for number,pname,kind in pins:lines.append('    '+number+' '+pname+' '+kind)
 lines.append('')
if not any('SYMBOL ' in item for item in lines):
 lines.append('No matching symbols found; must inspect installed libraries before electrical substitutions.')
for library,name in [('Device','R'),('Device','C')]:
 path=root/(library+'.kicad_sym')
 if path.exists():
  content=path.read_text(encoding='utf-8')
  m=re.search(r'\(symbol\s+"'+re.escape(name)+'"',content)
  if m:
   item=balanced(content,m.start())
   lines.append('PASSIVE '+library+':'+name+' pins='+str(pin_records(item)))
report='\n'.join(lines)+'\n'
out.write_text(report,encoding='utf-8')
print(report)
print('Saved:',out)
