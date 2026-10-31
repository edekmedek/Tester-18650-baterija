# R12 pin audit — confirmed gaps and next engineering gates

Source: actual R12 pcbnew pin/net printout, 2026-10-31. DRC reported 0 violations and 0 unconnected, but several pads have NO net assignment and are not checked as unconnected.

Confirmed:
- J1 BATTERY pads 1,2: unassigned.
- J2 TP4056_MODULE_INTERFACE pads 1..6: unassigned.
- J3 ESP32_INTERFACE pads 1..8: unassigned.
- J4 INA219_INTERFACE pads 1..4: unassigned.
- Q1 IRF3205 pad 2 Drain: unassigned.
- U1 MCP6002 pin 8 VCC_3V3: assigned but no other pad on this net; not physically powered.
- U1 pins 5,6,7 unused second amplifier; require datasheet-compliant termination, not left floating without review.
- R1 pad 1 PWM_RAW: net exists but has no driving source.
- CURRENT_SENSE, OPAMP_A_OUT, CURRENT_SETPOINT and GND are routed.

Provisional discharge topology (NOT approved to route until connector and charger are verified):
cell positive -> load MOSFET Drain (Q1 pad2), MOSFET Source (Q1 pad3) -> 0.5-ohm shunt pad1 -> shunt pad2 GND -> cell negative. If INA219 is inserted into discharge path, exact module wiring and measurement range must be designed first. Do not connect TP4056 charge module to load path without reviewing its battery/protection/output terminals and common ground. Charging and discharging should be interlocked.

Critical: the 0.5-ohm shunt at 1 A dissipates 0.5 W; the MOSFET in linear mode may dissipate several watts and its 3.3 V gate drive and DC SOA are unverified. Ensure a fail-safe discharge disable and independent undervoltage/overtemperature cutoff before using a cell.

Next: obtain exact physical ESP32 board and TP4056 board pin labels/photos or existing verified schematic, then finalize pin mapping and add full netlist. No PCB revision is safe to fabricate yet.
