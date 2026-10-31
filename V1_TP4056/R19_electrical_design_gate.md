# R19 — electrical design gate (2026-10-31)

## Verified
- User ran KiCad DRC on Tester18650_V1_decoupling_R19.kicad_pcb: 0 violations, 0 unconnected pads, 0 footprint errors.
- C2 100nF is assigned and routed between VCC_3V3 and GND.
- J3 pin1 PWM_RAW, J3 pin2 VCC_3V3 are routed.
- These results validate **only assigned nets**. The PCB is NOT fabrication-ready or battery-safe.

## Unresolved electrical issues (blocking fabrication)
1. J1 BATTERY pins 1/2 are unassigned.
2. J2 TP4056_MODULE_INTERFACE pins 1–6 are unassigned. Actual photographed USB-C TP4056 board exposes B+, B-, OUT+, OUT-; no verified mechanical or pin mapping.
3. J3 ESP32_INTERFACE pins 3–8 are unassigned; J3 is a generic wired header, NOT the photographed IdeaSpark ESP32/OLED footprint. Confirm 3V3 supply and GPIO25 PWM pin multiplexing.
4. J4 INA219_INTERFACE pins 1–4 are unassigned; actual breakout pin order and measurement location must be confirmed.
5. Q1 IRF3205 drain (pad2) unassigned. Check pinout against physical component, linear-mode SOA, thermal protection, and whether 3.3V MCP6002 can provide adequate gate voltage.
6. U1 MCP6002 unused op-amp pins 5,6,7 unassigned; must configure stable termination per datasheet.
7. Validate battery/charger/protection/load topology, undervoltage cutoff, fail-safe load-off on controller reset, independent current limit, reverse-polarity, and simultaneous charging/discharging safety.
8. Current shunt 0.5 ohm 2W; ensure accuracy, Kelvin sense, power/temperature margin, appropriate fuse and copper widths.
9. Verify PWM RC divider and output setpoint against real 3.3V logic and calibrated reference; do not assume 0..100% maps to safe load current.
10. Run full ERC on source schematic and check PCB footprint assignments, 3D mechanical fit, silkscreen, mounting holes and board outline. R19 DRC excluded several checks.

## Next engineering action
- Obtain verified module pinout/dimensions and complete schematic before adding unassigned high-current connections.
- Do not fabricate or attach an 18650 cell yet.
