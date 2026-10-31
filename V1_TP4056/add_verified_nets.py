# KiCad 10: add logical nets to known MCP6002 pins only.
# Does NOT connect MOSFET or charger: their pinouts are not yet verified.
from pathlib import Path
import pcbnew as p
folder=Path(__file__).resolve().parent
src=folder/"Tester18650_V1_placement.kicad_pcb"
dst=folder/"Tester18650_V1_nets_R01.kicad_pcb"
if not src.exists(): raise SystemExit("Missing source board: "+str(src))
if dst.exists(): raise SystemExit("Refusing overwrite: "+str(dst))
b=p.LoadBoard(str(src))
fps={f.GetReference():f for f in b.GetFootprints()}
assert set(fps)=={"U1","Q1","RSH1","J1","J2","J3","J4"}
# MCP6002 SOIC-8 pins: 1 OUTA, 2 INA-, 3 INA+, 4 VSS, 5 INB+, 6 INB-, 7 OUTB, 8 VDD.
assign={"1":"OPAMP_A_OUT","2":"CURRENT_SENSE","3":"CURRENT_SETPOINT","4":"GND","8":"VCC_3V3"}
for num,name in assign.items():
    net=b.FindNet(name)
    if net is None:
        net=p.NETINFO_ITEM(b,name)
        b.Add(net)
    pads=[pad for pad in fps["U1"].Pads() if pad.GetNumber()==num]
    assert len(pads)==1,(num,len(pads))
    pads[0].SetNet(net)
# Keep remaining pads unassigned until module and transistor pinouts are verified.
p.SaveBoard(str(dst),b)
check=p.LoadBoard(str(dst))
assert check is not None
for num,name in assign.items():
    pad=next(pad for pad in next(f for f in check.GetFootprints() if f.GetReference()=="U1").Pads() if pad.GetNumber()==num)
    assert pad.GetNetname()==name,(num,pad.GetNetname())
print("OK:",dst)
print("Assigned verified MCP6002 nets:",assign)
print("Tracks:",len(check.GetTracks()))
print("STOP: No physical traces yet. MOSFET, TP4056 and battery wiring remain unverified.")
