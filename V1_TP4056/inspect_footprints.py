# Run with KiCad 10 bundled Python; read-only inspection of generated placement.
from pathlib import Path
import pcbnew as p
board_path = Path(__file__).resolve().parent / "Tester18650_V1_placement.kicad_pcb"
if not board_path.exists():
    raise SystemExit("PCB missing: " + str(board_path))
board = p.LoadBoard(str(board_path))
if board is None:
    raise SystemExit("Could not open PCB")
for fp in sorted(board.GetFootprints(), key=lambda x:x.GetReference()):
    box=fp.GetBoundingBox(False,False)
    print(f"{fp.GetReference():6} {fp.GetFPIDAsString()} size={p.ToMM(box.GetWidth()):.2f}x{p.ToMM(box.GetHeight()):.2f} mm")
    for pad in sorted(fp.Pads(), key=lambda x:x.GetNumber()):
        pos=pad.GetPosition()
        print(f"  pad {pad.GetNumber():>3} x={p.ToMM(pos.x):.2f} y={p.ToMM(pos.y):.2f} net={pad.GetNetname() or '(none)'}")
print("Tracks:",len(board.GetTracks()),"Nets:",board.GetNetCount())
print("CAUTION: no verified schematic/netlist. Do not route or connect a cell yet.")
