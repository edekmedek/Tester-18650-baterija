# R10 — ESP32 setpoint design (NOT PCB-approved)

R09 KiCad DRC: 0 violations and 0 unconnected pads (user confirmed). This does not validate the full circuit.

Candidate: ESP32 PWM GPIO -> 47 kOhm -> SETPOINT_FILTER; 10 kOhm and 10 uF from SETPOINT_FILTER to analog GND; SETPOINT_FILTER -> 1 kOhm -> MCP6002 U1 pin3 (CURRENT_SETPOINT). MCP6002 pin8 requires regulated 3.3 V and local 100 nF decoupling to pin4 GND. Confirm actual ESP32 GPIO pin assignment before implementation.

Nominal PWM 3.3 V, 5 kHz. Divider output at 100% = 3.3*10/57 = 0.57895 V. Shunt 0.5 ohm => nominal current 1.158 A maximum. Duty targets: 0.25 A=21.59%, 0.5 A=43.18%, 0.75 A=64.77%, 1.0 A=86.36%. Equivalent filter resistance 8.246 kOhm, RC=82.46 ms, fc=1.93 Hz. PWM resolution depends on ESP32 variant and firmware clock.

Safety gates BEFORE routing:
- Verify actual ESP32 board variant, GPIO availability, boot pin restrictions and power supply.
- Ensure GPIO reset, firmware crash and brownout cannot turn on discharge. Firmware undervoltage cutoff alone is not fail-safe; add independent hardware shutdown as required.
- Check MCP6002 gate drive at 3.3 V, IRF3205 Vgs, linear-mode DC safe operating area, thermal dissipation and heatsink insulation. Switching current rating does NOT establish linear-mode safety.
- Confirm opamp feedback polarity, stability and current-limited bench test.
- Specify battery and TP4056 charger connector polarity, protection, INA219 role, temperature sensing, cutoff and common ground.
- Check shunt 0.5 ohm 2 W tolerance and temperature; 1 A produces 0.5 W.
- Do not connect battery or charger until schematic and staged testing are complete.

Next PCB action: confirm ESP32 pinout and safety architecture; then add footprints, assign nets, route, and run DRC. This file is design documentation, not a fabricated PCB or validated circuit.
