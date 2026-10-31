from pathlib import Path

d=Path(__file__).resolve().parent
out=d/'R62_thermal_gate_assessment.txt'
if out.exists():raise SystemExit('R62 report already exists')
v_cell_max=4.2
v_cell_min=3.0
v_pwm=3.3
r_top=47000.0
r_bottom=10000.0
r_shunt=0.5
rth_ja=62.0
ambient=25.0
v_ref=v_pwm*r_bottom/(r_top+r_bottom)
i_design=v_ref/r_shunt
cases=[0.25,0.5,0.75,1.0,i_design]
lines=['R62: 18650 discharge MOSFET gate drive and thermal preliminary check',
       'Source PCB: R42 (MCP6002 at 3.3 V, RSH1 0.5 ohm, IRF3205).',
       'IRF3205 manufacturer: https://www.infineon.com/assets/row/public/documents/24/49/infineon-irf3205-datasheet-en.pdf',
       'Reference parameters: VGS(th) 2-4V at 250uA; RthJA maximum 62 K/W without external heatsink.',
       'Note: VGS(th) is NOT the required gate voltage for 1A operation.',
       'Figure 8 SOA is single-pulse up to 10 ms; NOT sufficient to approve continuous linear operation.',
       'The MOSFET power model ignores connector/wiring/INA219 voltage drops and uses the 4.2 V cell upper bound.',
       'Vref max at 3.3V PWM: %.3f V; nominal max current: %.3f A'%(v_ref,i_design),
       'Thermal-only estimate, no heatsink, 25C ambient:',
       'Current A | Shunt W | MOSFET W at 4.2V cell | Tj estimated C']
for i in cases:
 shunt=i*i*r_shunt
 v_d=max(0.0,v_cell_max-i*r_shunt)
 watt=i*v_d
 tj=ambient+watt*rth_ja
 lines.append('%.3f | %.3f | %.3f | %.1f'%(i,shunt,watt,tj))
lines.extend([
 'Values above are theoretical steady-state estimates, NOT a safe operating envelope.',
 'Thermal estimate does NOT account for MOSFET linear-mode hotspots or DC SOA.',
 'Do not use IRF3205 in this circuit for continuous linear discharge until DC SOA and gate-drive/headroom are verified.',
 'Do not assume a heatsink solves insufficient gate voltage or DC SOA.',
 'DESIGN GATE: choose a component with documented DC linear-mode SOA and suitable gate drive, or redesign switched load.',
 'Also required: verified power-path protection, overtemp cutout, undervoltage cutout and charge/discharge interlock.',
 'NOT APPROVED: battery connection, charging/discharging or PCB fabrication.'])
out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('Saved:',out)
