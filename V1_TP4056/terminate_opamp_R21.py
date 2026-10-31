from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/'Tester18650_V1_decoupling_R19.kicad_pcb'
dst=d/'Tester18650_V1_opamp_unused_R21.kicad_pcb'
if not src.exists(): raise SystemExit('R19 missing')
if dst.exists(): raise SystemExit('R21 already exists')
b=p.LoadBoard(str(src))
f={x.GetReference():x for x in b.GetFootprints()}
u={x.GetNumber():x for x in f['U1'].Pads()}
assert all(not u[k].GetNetname() for k in ('5','6','7'))
g=u['4'].GetNet()
u['5'].SetNet(g)
n=p.NETINFO_ITEM(b,'OPAMP_B_FB');b.Add(n)
u['6'].SetNet(n);u['7'].SetNet(n)
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def trace(a,z,net,layer=p.F_Cu):
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.25));t.SetLayer(layer);t.SetNet(net);b.Add(t)
def via(x,y,net):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,y));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
trace(u['6'].GetPosition(),u['7'].GetPosition(),n)
trace(u['5'].GetPosition(),xy(65,48),g)
via(65,48,g)
trace(xy(65,48),xy(57.525,48),g,p.B_Cu)
via(57.525,48,g)
trace(xy(57.525,48),u['4'].GetPosition(),g)
p.SaveBoard(str(dst),b)
print('OK:',dst)
print('U1.5 GND; U1.6 tied to U1.7. Run DRC. No battery.')