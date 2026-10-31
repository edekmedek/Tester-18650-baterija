from pathlib import Path
import re
import shutil

d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_real_mosfet_R58.kicad_sch'
out=d/'Tester18650_V1_real_opamp_R59.kicad_sch'
libfile=d/'VerifiedOpAmp59.kicad_sym'
table=d/'sym-lib-table'
project=out.with_suffix('.kicad_pro')
baseline=src.with_suffix('.kicad_pro')
for path in (src,table,baseline):
 if not path.exists():raise SystemExit('MISSING '+str(path))
for path in (out,libfile,project):
 if path.exists():raise SystemExit('REFUSING OVERWRITE '+str(path))
def balanced(s,start):
 depth=0;quoted=False;escaped=False
 for i in range(start,len(s)):
  ch=s[i]
  if quoted:
   if escaped:escaped=False
   elif ch=='\\':escaped=True
   elif ch=='"':quoted=False
  elif ch=='"':quoted=True
  elif ch=='(':depth+=1
  elif ch==')':
   depth-=1
   if depth==0:return s[start:i+1]
 raise RuntimeError('Unbalanced s-expression')
def getblock(s,regex):
 hits=list(re.finditer(regex,s))
 if len(hits)!=1:raise SystemExit('Expected one block '+regex+', got '+str(len(hits)))
 return balanced(s,hits[0].start())
sch=src.read_text(encoding='utf-8')
audit=getblock(sch,r'\(symbol\s+"Audit:Pads_8"')
original=getblock(sch,r'\(symbol\s+\(lib_id\s+"Audit:Pads_8"')
if '(reference "U1")' not in original:raise SystemExit('Expected Audit 8-pin U1')
# Check installed real MCP6002 LM2904 compatible pin functions confirmed in R53.
pin_types={'1':('output','OUT_A'),'2':('input','IN_A_MINUS'),'3':('input','IN_A_PLUS'),
           '4':('power_in','V_MINUS'),'5':('input','IN_B_PLUS'),
           '6':('input','IN_B_MINUS'),'7':('output','OUT_B'),'8':('power_in','V_PLUS')}
name='MCP6002_R59'
new_embedded=audit.replace('"Audit:Pads_8"','"VerifiedOpAmp59:'+name+'"',1)
new_embedded=new_embedded.replace('Pads_8_0_1',name+'_0_1').replace('Pads_8_1_1',name+'_1_1')
for num,(typ,pname) in pin_types.items():
 pattern=r'\(pin passive line \([^)]+\) \(length 2\.54\) \(name "'+re.escape(num)+r'"'
 matches=list(re.finditer(pattern,new_embedded))
 if len(matches)!=1:raise SystemExit('Pin '+num+' not found or not unique')
 m=matches[0]
 original_prefix=m.group(0)
 updated=original_prefix.replace('(pin passive line','(pin '+typ+' line',1).replace('(name "'+num+'"','(name "'+pname+'"',1)
 new_embedded=new_embedded[:m.start()]+updated+new_embedded[m.end():]
assert new_embedded.count('(pin ')==8
local_symbol=new_embedded.replace('"VerifiedOpAmp59:'+name+'"','"'+name+'"',1)
libtext='(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+local_symbol+'\n)\n'
libblock=getblock(sch,r'\(lib_symbols\b')
sch=sch.replace(libblock,libblock[:-1]+'\n'+new_embedded+'\n)',1)
updated_instance=original.replace('(lib_id "Audit:Pads_8")','(lib_id "VerifiedOpAmp59:'+name+'")',1)
sch=sch.replace(original,updated_instance,1)
sch=sch.replace('Tester18650_V1_real_mosfet_R58','Tester18650_V1_real_opamp_R59')
sch=sch.replace('(rev "R58")','(rev "R59")')
assert sch.count('VerifiedOpAmp59:'+name)==2
tab=table.read_text(encoding='utf-8')
if 'name "VerifiedOpAmp59"' in tab:raise SystemExit('Already registered')
if not tab.rstrip().endswith(')'):raise SystemExit('Unexpected sym-lib-table')
entry='(lib (name "VerifiedOpAmp59") (type "KiCad") (uri "${KIPRJMOD}/VerifiedOpAmp59.kicad_sym") (options "") (descr "Verified MCP6002 pin functions"))'
newtab=tab.rstrip()[:-1]+'\n'+entry+'\n)\n'
libfile.write_text(libtext,encoding='utf-8')
table.write_text(newtab,encoding='utf-8')
shutil.copyfile(baseline,project)
out.write_text(sch,encoding='utf-8')
print('OK:',out)
print('MCP6002 U1 pin types:',pin_types)
print('R59 pin geometry and assigned nets preserved from R58. Run ERC and PCB netlist comparison.')
print('NOT an electrically validated charger or battery tester.')
