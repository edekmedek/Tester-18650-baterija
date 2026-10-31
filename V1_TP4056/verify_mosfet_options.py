from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
board=d/"Tester18650_V1_outline_R03.kicad_pcb"
if not board.exists(): raise SystemExit("Missing board: "+str(board))
b=p.LoadBoard(str(board))
parts={x.GetReference():x for x in b.GetFootprints()}
assert "Q1" in parts and "U1" in parts
print("PCB:",board.name)
print("Q1 footprint:",parts["Q1"].GetFPIDAsString())
print("Footprints:",len(parts),"Tracks:",len(b.GetTracks()))
print("AVAILABLE PARTS TO EVALUATE:")
print("IRF3205: TO-220, candidate; needs linear SOA and 3.3V gate-drive test.")
print("SSF7509: TO-220, candidate; needs linear SOA and 3.3V gate-drive test.")
print("CEB4060AL: verify package marking and datasheet before footprint selection.")
print("042N10N: exact suffix/package must be verified before selecting footprint.")
print("5N52K: not preferred for 3.3V drive.")
print("No changes made. No MOSFET is approved for battery connection.")
print("DESIGN ISSUE: 0.5 ohm shunt at 1A = 0.5W; 2W resistor nominal, but cooling and tolerances still need checking.")
print("NEXT: validate datasheet SOA, gate drive and actual parts; only then assign Q1 nets and route.")
