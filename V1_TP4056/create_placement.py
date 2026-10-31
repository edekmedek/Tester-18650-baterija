# KiCad 10 pcbnew: initial physical placement, no electrical nets yet.
# Run using KiCad bundled python.exe. Does not overwrite existing boards.
import os
from pathlib import Path
import pcbnew as p

root = Path(os.environ.get("KICAD10_FOOTPRINT_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\footprints"))
out = Path(__file__).resolve().parent / "Tester18650_V1_placement.kicad_pcb"
if out.exists():
    raise SystemExit("STOP: output already exists; refusing overwrite: " + str(out))
if not root.is_dir():
    raise SystemExit("Footprint libraries not found: " + str(root))
board = p.BOARD()
# Only library footprints with known geometry. Modules are not represented as bare ICs.
parts = [
    ("U1", "MCP6002", "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", 60, 45),
    ("Q1", "LINEAR_MOSFET_TBD", "Package_TO_SOT_THT.pretty", "TO-220-3_Vertical", 85, 45),
    ("RSH1", "0R5_2W_TBD", "Resistor_THT.pretty", "R_Axial_Power_L25.0mm_W9.0mm_P27.94mm", 83, 65),
    ("J1", "BATTERY", "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x02_P2.54mm_Vertical", 32, 63),
    ("J2", "TP4056_MODULE_INTERFACE", "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x06_P2.54mm_Vertical", 32, 35),
    ("J3", "ESP32_INTERFACE", "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x08_P2.54mm_Vertical", 32, 82),
    ("J4", "INA219_INTERFACE", "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Vertical", 60, 80),
]
for ref, value, library, name, x, y in parts:
    fp = p.FootprintLoad(str(root / library), name)
    if fp is None:
        raise SystemExit("Missing footprint: " + library + "/" + name)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))
    board.Add(fp)
    print(ref, name, "pads:", fp.GetPadCount())
p.SaveBoard(str(out), board)
loaded = p.LoadBoard(str(out))
assert loaded is not None and len(loaded.GetFootprints()) == len(parts)
print("OK: saved and reloaded", out)
print("CAUTION: placeholder connectors; no tracks, nets, safety validation or real module footprints.")
