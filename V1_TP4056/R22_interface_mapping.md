# R22 — Interface mapping and verification checklist

## Baseline
- R21 PCB: Tester18650_V1_opamp_unused_R21.kicad_pcb
- User-verified KiCad DRC: 0 violations, 0 unconnected, 0 footprint errors.
- MCP6002 channel B terminated: pin 5 GND; pin 6 tied to pin 7.

## Proposed J3 wiring (NOT YET ASSIGNED)
| PCB J3 pin | Proposed function | Physical ESP32 mapping |
|---|---|---|
| 1 | PWM_RAW | Candidate GPIO25 / D25; check OLED and boot pin use |
| 2 | VCC_3V3 | Regulated 3V3 only; confirm module regulator budget |
| 3 | GND | ESP32 GND |
| 4 | I2C_SDA | GPIO TBD |
| 5 | I2C_SCL | GPIO TBD |
| 6 | ADC_BATTERY | GPIO TBD; divider and input limits required |
| 7 | ENABLE/FAULT | GPIO TBD; fail-safe logic required |
| 8 | Spare | leave unassigned until defined |

## Proposed J4 wiring (NOT YET ASSIGNED)
| PCB J4 pin | Function | INA219 breakout label |
|---|---|---|
| 1 | VCC_3V3 | VCC, only after confirming breakout supports 3.3 V |
| 2 | GND | GND |
| 3 | I2C_SDA | SDA |
| 4 | I2C_SCL | SCL |

**IMPORTANT**: This is a proposed *cable mapping*, not a claim about physical order on the user's INA219 breakout. The actual breakout must be inspected before wiring.

## Critical system-level questions
- INA219 current sense is high-side and normally uses its own shunt. The current RSH1 low-side 0.5 ohm is for analog control; do not confuse the two.
- The photographed TP4056 module uses B+/B-/OUT+/OUT- pads; generic J2 six-pin header is not a drop-in module footprint. Must confirm protection circuit and exact wiring.
- Q1 IRF3205 is operated in linear mode; verify DC safe-operating-area and gate drive at 3.3 V. A low Rds(on) spec does not establish suitability.
- Ensure battery disconnect, undervoltage cutoff, overcurrent and thermal protection independent of software. Define charging/load interlock.
- Add a complete schematic with ERC before fabrication. DRC of assigned nets is insufficient.

## Next step
Only after verifying actual module pin labels and chosen ESP32 GPIOs, implement connector net assignments and routing. Do not fabricate or connect a cell yet.
