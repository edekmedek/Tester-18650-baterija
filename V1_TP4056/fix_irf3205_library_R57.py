from pathlib import Path
import re
import shutil

d = Path(__file__).resolve().parent
src = d / "Tester18650_V1_real_mosfet_R56.kicad_sch"
dst = d / "Tester18650_V1_real_mosfet_R57.kicad_sch"
project = dst.with_suffix(".kicad_pro")
local_lib = d / "VerifiedFET.kicad_sym"
table = d / "sym-lib-table"
if not src.exists():
    raise SystemExit("Missing R56 schematic")
for item in (dst, project, local_lib):
    if item.exists():
        raise SystemExit("Refusing to overwrite: " + str(item))
if not table.exists():
    raise SystemExit("Missing symbol library table")
table_text = table.read_text(encoding="utf-8")
if 'name "VerifiedFET"' in table_text:
    raise SystemExit("VerifiedFET library already exists: inspect before proceeding")

def balanced(text, start):
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        ch = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        elif ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise ValueError("Unbalanced s-expression")

s = src.read_text(encoding="utf-8")
matches = list(re.finditer(r'\(symbol\s+"Transistor_FET:IRF3205"', s))
if len(matches) != 1:
    raise SystemExit("Expected one embedded IRF3205 symbol")
original = balanced(s, matches[0].start())
if 'IRF3205_1_1' not in original:
    raise SystemExit("Unexpected flattened BUZ11/IRF3205 symbol")
new_name = "IRF3205_R57"
snapshot = original.replace(
    '"Transistor_FET:IRF3205"', '"VerifiedFET:' + new_name + '"', 1
).replace("IRF3205_", new_name + "_")
local_symbol = snapshot.replace('"VerifiedFET:' + new_name + '"', '"' + new_name + '"', 1)
libdata = ('(kicad_symbol_lib (version 20231120) '
           '(generator "kicad_symbol_editor")\n'
           + local_symbol + '\n)\n')
s = s.replace(original, snapshot, 1)
old_q1 = '(symbol (lib_id "Transistor_FET:IRF3205")'
if s.count(old_q1) != 1:
    raise SystemExit("Expected exactly one Q1 instance")
s = s.replace(old_q1, '(symbol (lib_id "VerifiedFET:' + new_name + '")', 1)
s = s.replace("Tester18650_V1_real_mosfet_R56",
              "Tester18650_V1_real_mosfet_R57")
s = s.replace('(rev "R56")', '(rev "R57")')
if "VerifiedFET:" + new_name not in s:
    raise SystemExit("Replacement failed")
table_text = table_text.rstrip()
if not table_text.endswith(")"):
    raise SystemExit("Unexpected sym-lib-table structure")
entry = ('(lib (name "VerifiedFET") (type "KiCad") '
         '(uri "\${KIPRJMOD}/VerifiedFET.kicad_sym") '
         '(options "") (descr "Verified pin-mapped MOSFET snapshot"))')
new_table = table_text[:-1] + '\n' + entry + '\n)\n'
base_project = src.with_suffix(".kicad_pro")
if not base_project.exists():
    raise SystemExit("Missing R56 .kicad_pro")
local_lib.write_text(libdata, encoding="utf-8")
table.write_text(new_table, encoding="utf-8")
shutil.copyfile(base_project, project)
dst.write_text(s, encoding="utf-8")
print("OK:", dst)
print("LOCAL LIBRARY:", local_lib)
print("R57 Q1 uses a custom pinned snapshot of the verified BUZ11/IRF3205 mapping.")
print("Run ERC and compare netlist against PCB before accepting.")
print("Not an approved electrical design; no battery.")
