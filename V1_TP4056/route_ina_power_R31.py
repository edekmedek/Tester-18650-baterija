from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_ina_power_R30.kicad_pcb'
dst=d/'Tester18650_V1_ina_power_R31.kicad_pcb'
if not src.exists():raise SystemExit('R30 missing')
if dst.exists():raise SystemExit('R31 exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
def pad(ref,num):return next(x for x in f[ref].Pads() if x.GetNumber()==str(num))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def track(a,z,net,layer):
 t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(x,y,net):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
v=pad('J4',1).GetNet();g=pad('J4',2).GetNet()
assert v.GetNetname()=='VCC_3V3' and g.GetNetname()=='GND'
# Connect J4 power from existing B.Cu VCC vertical at x35 y80.
track((35,80),(60,80),v,p.B_Cu)
# Connect J4 GND on F.Cu to existing F.Cu GND vertical at x57.525 y74..50.
track((60,82.54),(63,82.54),g,p.F_Cu)
track((63,82.54),(63,74),g,p.F_Cu)
track((63,74),(57.525,74),g,p.F_Cu)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('J4 3V3 and GND routed. DRC REQUIRED. Verify breakout pin order before connection.')