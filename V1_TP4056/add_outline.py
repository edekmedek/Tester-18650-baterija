from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
src=d/"Tester18650_V1_gate_R02.kicad_pcb"
dst=d/"Tester18650_V1_outline_R03.kicad_pcb"
if not src.exists(): raise SystemExit("Missing input board: "+str(src))
if dst.exists(): raise SystemExit("Refusing to overwrite "+str(dst))
b=p.LoadBoard(str(src))
assert b is not None
assert not any(x.GetLayer()==p.Edge_Cuts for x in b.GetDrawings()),"Outline already exists"
# Preliminary rectangle covers all current footprints, including the long shunt resistor.
# Coordinates mm; must be reconsidered after real modules and mounting holes selected.
corners=[(25,25),(120,25),(120,110),(25,110)]
for i,(x,y) in enumerate(corners):
    xx,yy=corners[(i+1)%len(corners)]
    line=p.PCB_SHAPE(b)
    line.SetShape(p.SHAPE_T_SEGMENT)
    line.SetStart(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
    line.SetEnd(p.VECTOR2I(p.FromMM(xx),p.FromMM(yy)))
    line.SetLayer(p.Edge_Cuts)
    line.SetWidth(p.FromMM(0.05))
    b.Add(line)
p.SaveBoard(str(dst),b)
v=p.LoadBoard(str(dst))
assert v and len([x for x in v.GetDrawings() if x.GetLayer()==p.Edge_Cuts])==4
print("OK:",dst)
print("Outline: 95 x 85 mm, 4 closed Edge.Cuts segments")
print("Footprints:",len(v.GetFootprints()),"Tracks:",len(v.GetTracks()))
print("PRELIMINARY ONLY: module footprints, schematic, SOA and full DRC not yet verified.")
