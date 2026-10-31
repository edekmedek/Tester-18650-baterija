from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_setpoint_R12.kicad_pcb"
dst=d/"Tester18650_V1_pwm_interface_R13.kicad_pcb"
if not src.exists():raise SystemExit("Missing R12")
if dst.exists():raise SystemExit("R13 already exists")
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):
 a=[v for v in f[ref].Pads() if v.GetNumber()==str(num)]
 assert len(a)==1,(ref,num)
 return a[0]
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
r=pad("R1",1);j=pad("J3",1)
assert r.GetNetname()=="PWM_RAW"
assert not j.GetNetname(),"J3 pad1 already assigned; abort"
j.SetNet(r.GetNet())
def route(a,z):
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(p.F_Cu);t.SetNet(r.GetNet());b.Add(t)
# J3 is a wired interface, NOT a physical ESP32 footprint. J3 pin1 = PWM_RAW.
# x40 corridor is outside active routes; y27 is 2mm inside presumed board edge.
pts=[j.GetPosition(),xy(40,82),xy(40,27),xy(68.0875,27),r.GetPosition()]
for a,z in zip(pts,pts[1:]):route(a,z)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert len(v.GetFootprints())==len(f)
assert next(x for x in next(y for y in v.GetFootprints() if y.GetReference()=="J3").Pads() if x.GetNumber()=="1").GetNetname()=="PWM_RAW"
print("OK:",dst)
print("J3 pin1 wired to R1 pin1 PWM_RAW; physical ESP32 D25 connection remains external/unverified.")
print("Run KiCad DRC. DO NOT connect battery.")
