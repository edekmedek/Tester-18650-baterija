from pathlib import Path
import re,shutil
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_real_mosfet_R56.kicad_sch'
dst=d/'Tester18650_V1_real_mosfet_R58.kicad_sch'
project=dst.with_suffix('.kicad_pro')
libfile=d/'VerifiedFET58.kicad_sym'
table=d/'sym-lib-table'
for path in (src,table):
 if not path.exists():raise SystemExit('MISSING: '+str(path))
for path in (dst,project,libfile):
 if path.exists():raise SystemExit('REFUSE OVERWRITE: '+str(path))
def block(s,start):
 depth=0;quoted=False;esc=False
 for i in range(start,len(s)):
  c=s[i]
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:return s[start:i+1]
 raise RuntimeError('Unbalanced S expression')
sch=src.read_text(encoding='utf-8')
hits=list(re.finditer(r'\(symbol\s+"Transistor_FET:IRF3205"',sch))
if len(hits)!=1:raise SystemExit('Expected one embedded IRF3205; got '+str(len(hits)))
original=block(sch,hits[0].start())
old_instance='(symbol (lib_id "Transistor_FET:IRF3205")'
if sch.count(old_instance)!=1:raise SystemExit('Expected exactly one Q1 instance')
name='IRF3205_R58'
nested=original.replace('IRF3205_0_1',name+'_0_1').replace('IRF3205_1_1',name+'_1_1')
if nested==original:raise SystemExit('Expected nested symbol units not found')
embedded=nested.replace('"Transistor_FET:IRF3205"','"VerifiedFET58:'+name+'"',1)
local=embedded.replace('"VerifiedFET58:'+name+'"','"'+name+'"',1)
assert embedded.count('"VerifiedFET58:'+name+'"')==1
assert local.count('(symbol "'+name+'"')==1
sch=sch.replace(original,embedded,1).replace(old_instance,'(symbol (lib_id "VerifiedFET58:'+name+'")',1)
sch=sch.replace('Tester18650_V1_real_mosfet_R56','Tester18650_V1_real_mosfet_R58')
sch=sch.replace('(rev "R56")','(rev "R58")')
if sch.count('VerifiedFET58:'+name)!=2:raise SystemExit('Expected embedded and instance library IDs')
tab=table.read_text(encoding='utf-8')
if 'name "VerifiedFET58"' in tab:raise SystemExit('Table already has VerifiedFET58')
if not tab.rstrip().endswith(')'):raise SystemExit('Invalid sym-lib-table ending')
entry='(lib (name "VerifiedFET58") (type "KiCad") (uri "${KIPRJMOD}/VerifiedFET58.kicad_sym") (options "") (descr "Pinned MOSFET symbol"))'
newtab=tab.rstrip()[:-1]+'\n'+entry+'\n)\n'
libdata='(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+local+'\n)\n'
proj=src.with_suffix('.kicad_pro')
if not proj.exists():raise SystemExit('Missing R56 project')
libfile.write_text(libdata,encoding='utf-8')
table.write_text(newtab,encoding='utf-8')
shutil.copyfile(proj,project)
dst.write_text(sch,encoding='utf-8')
print('OK:',dst)
print('R58 custom symbol library ID VerifiedFET58:'+name)
print('R57 broken output left untouched. R58 still requires KiCad ERC.')
print('No battery connection or fabrication approval.')
