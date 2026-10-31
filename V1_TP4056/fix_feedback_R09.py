from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_feedback_R08.kicad_pcb"
dst=d/"Tester18650_V1_feedback_R09.kicad_pcb"
if not src.exists():raise SystemExit("Missing R08")
if dst.exists():raise SystemExit("R09 already exists")
b=p.LoadBoard(str(src))
def mm(v):return round(p.ToMM(v),3)
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def coords(t):return {(mm(v.x),mm(v.y)) for v in (t.GetStart(),t.GetEnd())}
# Move GND x68 vertical F.Cu segment to a right-side x=73 corridor, but
# sense y58 spans x54..79; therefore crossing must be on DIFFERENT layer.
# Instead move sense horizontal y58 to B.Cu using two vias, and keep GND on F.Cu.
sense=[t for t in b.GetTracks() if isinstance(t,p.PCB_TRACK) and t.GetNetname()=="CURRENT_SENSE" and t.GetLayer()==p.F_Cu and coords(t)=={(54.,58.),(79.,58.)}]
assert len(sense)==1,"Unexpected sense horizontal segment"
net=sense[0].GetNet()
b.Remove(sense[0])
for x in (54,79):
 v=p.PCB_VIA(b);v.SetPosition(xy(x,58));v.SetWidth(p.FromMM(.8));v.SetDrill(p.FromMM(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(net);b.Add(v)
t=p.PCB_TRACK(b);t.SetStart(xy(54,58));t.SetEnd(xy(79,58));t.SetWidth(p.FromMM(.25));t.SetLayer(p.B_Cu);t.SetNet(net);b.Add(t)
# NOTE: B.Cu gate route at y55 is parallel to y58, not intersecting.
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len(v.GetFootprints())==8
print("OK:",dst)
print("CURRENT_SENSE horizontal y58 moved to B.Cu using 2 vias.")
print("Run DRC; R09 not approved until no violations.")
