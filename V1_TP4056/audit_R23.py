from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_opamp_unused_R21.kicad_pcb"
out=d/"R23_mechanical_and_net_audit.txt"
if not src.exists():raise SystemExit("R21 PCB missing")
b=p.LoadBoard(str(src))
bb=b.GetBoardEdgesBoundingBox()
def mm(x):return p.ToMM(x)
xmin,ymin,xmax,ymax=map(mm,(bb.GetLeft(),bb.GetTop(),bb.GetRight(),bb.GetBottom()))
lines=["R23 PCB MECHANICAL AND NET AUDIT",f"Board outline bounds: x={xmin:.2f}..{xmax:.2f} mm, y={ymin:.2f}..{ymax:.2f} mm",f"Board size: {xmax-xmin:.2f} x {ymax-ymin:.2f} mm",""]
outside=[];unassigned=[];close=[]
for f in sorted(b.GetFootprints(),key=lambda x:x.GetReference()):
 for pad in f.Pads():
  pos=pad.GetPosition();x,y=mm(pos.x),mm(pos.y)
  ident=f"{f.GetReference()}.{pad.GetNumber()}"
  if not pad.GetNetname():unassigned.append(ident)
  if not (xmin<=x<=xmax and ymin<=y<=ymax):outside.append((ident,x,y))
  elif min(x-xmin,xmax-x,y-ymin,ymax-y)<1.0:close.append((ident,x,y))
lines.append("UNASSIGNED PADS: "+str(len(unassigned)))
lines+=["  "+x for x in unassigned]
lines.append("PAD CENTERS OUTSIDE BOARD: "+str(len(outside)))
lines += [f"  {name}: {x:.2f}, {y:.2f}" for name,x,y in outside]
lines.append("PAD CENTERS WITHIN 1MM OF BOARD EDGE: "+str(len(close)))
lines += [f"  {name}: {x:.2f}, {y:.2f}" for name,x,y in close]
lines+=["","This is a READ-ONLY audit. Pad-center checks do not replace copper/footprint clearance DRC.","Battery/charger wiring, component SOA, protection and complete ERC are not verified.","Do not connect a cell or fabricate."]
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("\n".join(lines))
