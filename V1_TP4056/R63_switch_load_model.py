from pathlib import Path
import csv

# Off-line, proposed switched-resistor discharge load model.
# NOT a schematic or certification. This is not a constant-current load.
R=4.7
P_RATED=10.0
CELL_V=[4.2,4.0,3.7,3.5,3.2,3.0]
rows=[]
for v in CELL_V:
    i=v/R
    p=v*v/R
    rows.append((v,round(i,4),round(p,4),round(p/P_RATED*100,1)))
assert max(r[2] for r in rows)<P_RATED
output=Path(__file__).resolve().parent/'R63_switched_load_model.csv'
with output.open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f)
    w.writerow(['Cell voltage (V)','Ideal current (A)','Load resistor power (W)','Share of resistor nominal rating (%)'])
    w.writerows(rows)
print('R63: external resistive load candidate 4.7 ohm / nominal 10 W')
print('WARNING: switched resistive load, NOT constant current. INA219 current must be integrated over time.')
print('Nominal 4.2V: 0.894 A, 3.753 W in resistor; 3.0V: 0.638 A, 1.915 W.')
print('A 10W resistor can run extremely hot; confirm mounting and datasheet derating.')
print('Must use logic-level MOSFET verified fully enhanced with actual gate voltage; IRF3205 NOT approved.')
print('Requires independent undervoltage and overtemperature cutoff, fuse, protected output return, charger/load interlock.')
print('No battery connection or PCB fabrication approval.')
print('CSV:',output)
