from pathlib import Path
import pcbnew as p
d=Path(__file__).resolve().parent
path=d/"Tester18650_V1_feedback_R09.kicad_pcb"
b=p.LoadBoard(str(path))
f={x.GetReference():x for x in b.GetFootprints()}
print("Board:",path.name)
print("Footprints:",len(f),"Tracks/vias:",len(b.GetTracks()))
for ref,pins in {"U1":["1","2","3","4","8"],"Q1":["1","2","3"],"RSH1":["1","2"],"J1":["1","2"]}.items():
 for pin in pins:
  pad=next(x for x in f[ref].Pads() if x.GetNumber()==pin)
  print(f"{ref}.{pin}: {pad.GetNetname() or 'UNASSIGNED'}")
print("0.5 ohm shunt target at 0.25A: 0.125 V, power 0.03125 W")
print("0.5 ohm shunt target at 1.00A: 0.500 V, power 0.500 W")
print("Critical missing: cell connector pin mapping, charger/protection topology, opamp VCC, setpoint DAC/PWM filter, cutoff, reverse polarity protection, thermal sensing, MOSFET DC SOA.")
print("No edits. DRC 0 is not functional validation.")
