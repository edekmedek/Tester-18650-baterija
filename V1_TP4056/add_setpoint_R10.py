from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_feedback_R09.kicad_pcb"
dst=d/"Tester18650_V1_setpoint_R10.kicad_pcb"
if not src.exists():raise SystemExit("Missing DRC-verified R09 board")
if dst.exists():raise SystemExit("R10 exists; refusing overwrite")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
assert "U1" in f
def net(name):
 for n in b.GetNetInfo().NetsByNetcode().values():
  if n.GetNetname()==name:return n
 n=p.NETINFO_ITEM(b,name);b.Add(n);return n
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def add(ref,value,lib,fp,x,y,n1,n2):
 xfp=p.FootprintLoad(lib,fp)
 if xfp is None:raise RuntimeError("Cannot load footprint "+lib+"/"+fp)
 xfp.SetReference(ref);xfp.SetValue(value);xfp.SetPosition(xy(x,y))
 pads={a.GetNumber():a for a in xfp.Pads()}
 assert set(pads)=={"1","2"},(ref,set(pads))
 pads["1"].SetNet(net(n1));pads["2"].SetNet(net(n2))
 b.Add(xfp)
 return xfp
# Candidate passive network; no ESP32 GPIO assigned. Values require hardware validation.
# 47k PWM input series; 10k pull-down; 10u filter; 1k opamp input isolation.
lib="Resistor_SMD"
add("R1","47k",lib,"R_0805_2012Metric",69,32,"PWM_RAW","PWM_FILTER")
add("R2","10k",lib,"R_0805_2012Metric",75,32,"PWM_FILTER","GND")
add("C1","10u","Capacitor_SMD","C_0805_2012Metric",81,32,"PWM_FILTER","GND")
add("R3","1k",lib,"R_0805_2012Metric",87,32,"PWM_FILTER","CURRENT_SETPOINT")
assert any(x.GetNumber()=="3" and x.GetNetname()=="CURRENT_SETPOINT" for x in f["U1"].Pads())
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert len(v.GetFootprints())==len(f)+4
print("R10 created:",dst)
print("4 passive footprints placed; NOT ROUTED. DRC unconnected expected.")
print("ESP32 PWM GPIO NOT assigned. Battery NOT safe to connect.")
