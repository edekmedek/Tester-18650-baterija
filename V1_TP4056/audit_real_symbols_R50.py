from pathlib import Path
import re
d=Path(__file__).resolve().parent
root=Path(r'C:\Program Files\KiCad\10.0\share\kicad\symbols')
out=d/'R50_real_symbols_audit.txt'
def block(src,start):
 depth=0;quoted=False;escaped=False
 for i in range(start,len(src)):
  c=src[i]
  if quoted:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:return src[start:i+1]
 raise SystemExit('Unbalanced symbol file')
def symbol_in(src,name):
 matches=list(re.finditer(r'\(symbol\s+"'+re.escape(name)+r'"',src))
 if len(matches)!=1:raise SystemExit('Expected one '+name+'; found '+str(len(matches)))
 return block(src,matches[0].start())
def pin_blocks(sym):
 p=[]
 for m in re.finditer(r'\(pin\s+(input|output|passive|power_in|power_out|open_collector|open_emitter|bidirectional|tri_state|no_connect|unspecified)\b',sym):
  k=block(sym,m.start())
  number=re.search(r'\(number\s+"([^"]+)"',k)
  name=re.search(r'\(name\s+"([^"]+)"',k)
  at=re.search(r'\(at\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+([0-9.]+)\)',k)
  if number:p.append((number.group(1),name.group(1) if name else '?',m.group(1),at.groups() if at else '?'))
 return p
wanted=[('Device','R'),('Device','C'),('Transistor_FET','IRF3205'),('Amplifier_Operational','MCP6002')]
lines=['R50: real KiCad electrical symbol pin audit','Source: installed KiCad 10 symbol libraries','']
for library,name in wanted:
 path=root/(library+'.kicad_sym')
 if not path.exists():raise SystemExit('Missing KiCad symbol library '+str(path))
 src=path.read_text(encoding='utf-8')
 try:
  sym=symbol_in(src,name)
 except SystemExit:
  if name=='IRF3205' and re.search(r'\(symbol\s+"BUZ11"',src):
   sym=symbol_in(src,'BUZ11')
   lines.append('IRF3205 is not direct symbol: BUZ11 may be an alias; confirm locally.')
  else:raise
 pins=pin_blocks(sym)
 if not pins and name=='IRF3205':
  lines.append('IRF3205 is derived; inherited pins require library parent resolution.')
 lines.append(library+':'+name+' extracted pins='+str(len(pins)))
 for number,pname,ptype,position in pins:lines.append('  '+number+' '+pname+' '+ptype+' '+str(position))
 lines.append('')
report='\n'.join(lines)+'\n'
out.write_text(report,encoding='utf-8')
print(report)
print('Saved:',out)
