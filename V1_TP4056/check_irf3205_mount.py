# Read-only verification of current KiCad board and IRF3205 TO-220 pin numbering.
from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
path=d/"Tester18650_V1_outline_R03.kicad_pcb"
b=p.LoadBoard(str(path))
q=next(f for f in b.GetFootprints() if f.GetReference()=="Q1")
print("PCB:",path.name)
print("Q1 footprint:",q.GetFPIDAsString())
for pad in sorted(q.Pads(),key=lambda x:x.GetNumber()):
    xy=pad.GetPosition()
    print("Q1 pad",pad.GetNumber(),"x",round(p.ToMM(xy.x),2),"y",round(p.ToMM(xy.y),2))
print("IRF3205 TO-220 FRONT VIEW (text facing you): 1 Gate, 2 Drain, 3 Source.")
print("Metal tab is Drain. Four devices on common bare heatsink may share Drain.")
print("CHECK: insulating pads and shoulder washers, continuity between each tab and heatsink.")
print("Do not wire cells or assign Q1 nets until isolation, gate drive and DC SOA are verified.")
