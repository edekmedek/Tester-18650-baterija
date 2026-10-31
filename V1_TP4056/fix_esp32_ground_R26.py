from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
b=p.LoadBoard(str(d/'Tester18650_V1_esp32_ground_R25.kicad_pcb'))
def mm(v):return (round(p.ToMM(v.x),3),round(p.ToMM(v.y),3))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
matches=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetLayer()==p.B_Cu and t.GetNetname()=='GND' and {mm(t.GetStart()),mm(t.GetEnd())}=={(57.525,74.0),(57.525,50.0)}]
assert len(matches)==1
old=matches[0];net=old.GetNet();b.Remove(old)
for x,y in [(57.525,74),(57.525,50)]:
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
t=p.PCB_TRACK(b);t.SetStart(xy(57.525,74));t.SetEnd(xy(57.525,50));t.SetWidth(p.FromMM(.35));t.SetLayer(p.F_Cu);t.SetNet(net);b.Add(t)
out=d/'Tester18650_V1_esp32_ground_R26.kicad_pcb'
p.SaveBoard(str(out),b)
print('OK:',out,'Run DRC')