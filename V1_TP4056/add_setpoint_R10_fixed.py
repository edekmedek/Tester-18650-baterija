from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_feedback_R09.kicad_pcb"
dst=d/"Tester18650_V1_setpoint_R10.kicad_pcb"
if not src.exists():raise SystemExit("Missing R09")
if dst.exists():raise SystemExit("R10 exists; refusing overwrite")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def net(name):
 for n in b.GetNetInfo().NetsByNetcode().values():
  if n.GetNetname()==name:return n
 n=p.NETINFO_ITEM(b,name);b.Add(n);return n
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
# KiCad 10 FootprintLoad requires an absolute .pretty directory in standalone Python.
root=Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
def load(kind,name):
 folder=root/(kind+".pretty")
 if not (folder/(name+".kicad_mod")).exists():raise RuntimeError("Footprint missing: "+str(folder/name))
 obj=p.FootprintLoad(str(folder),name)
 if obj is None:raise RuntimeError("FootprintLoad failed: "+str(folder))
 return obj
def add(ref,value,kind,foot,x,y,n1,n2):
 obj=load(kind,foot)
 obj.SetReference(ref);obj.SetValue(value);obj.SetPosition(xy(x,y))
 pads={a.GetNumber():a for a in obj.Pads()}
 assert set(pads)=={"1","2"},(ref,set(pads))
 pads["1"].SetNet(net(n1));pads["2"].SetNet(net(n2))
 b.Add(obj)
add("R1","47k","Resistor_SMD","R_0805_2012Metric",69,32,"PWM_RAW","PWM_FILTER")
add("R2","10k","Resistor_SMD","R_0805_2012Metric",75,32,"PWM_FILTER","GND")
add("C1","10u","Capacitor_SMD","C_0805_2012Metric",81,32,"PWM_FILTER","GND")
add("R3","1k","Resistor_SMD","R_0805_2012Metric",87,32,"PWM_FILTER","CURRENT_SETPOINT")
assert any(a.GetNumber()=="3" and a.GetNetname()=="CURRENT_SETPOINT" for a in f["U1"].Pads())
p.SaveBoard(str(dst),b)
assert len(p.LoadBoard(str(dst)).GetFootprints())==len(f)+4
print("OK:",dst)
print("Four footprints placed. Not routed; no ESP32 GPIO assigned. Do not connect battery.")
