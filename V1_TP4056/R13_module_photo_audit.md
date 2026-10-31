# R13 — verified module identification from user photographs (2026-10-31)

## ESP32
Photo shows IdeaSpark ESP-WROOM-32 board with OLED display, USB micro-B, EN and BOOT buttons. Silkscreen on right row, from top to bottom as photographed: D23, D22, TX0, RX0, D21, D19, D18, D5, TX2, RX2, D4, D2, D15, GND, 3V3. Left row includes EN, VP, VN, D34, D35, D32, D33, D25, D26, D27, D14, D12, D13, GND, VIN (some upper labels require close-up before final wiring).

Candidate PWM pin: GPIO25 / silkscreen D25, provisionally selected because it is a general-purpose output and not a boot strapping pin. **Not connected**; verify that onboard OLED or other circuitry does not use this pin, and confirm board-specific pin mapping before routing.

## TP4056
Photo depicts compact USB-C TP4056-style charger module, about 28 mm long, with distinct pads marked B+, B-, OUT+, OUT-. A USB input and protection IC appear present, but actual protection configuration and polarity must be confirmed on physical unit. Image orientation is rotated; use silkscreen labels, not positional assumptions.

## Critical PCB mismatch
Existing J2 is a generic six-pin 2.54 mm header; module exposes separate pads for B+/B-/OUT+/OUT- and is NOT a six-pin plug-in header. J3 is an 8-pin generic interface; ESP32 board has two long pin rows and is NOT a matching 8-pin module footprint. Do not solder either directly to J2/J3.

## Next design actions
1. Design J2 as explicit four-net wired interface with pads labelled TP_B+, TP_B-, TP_OUT+, TP_OUT-; keep any extra pads unassigned or replace footprint in next layout revision.
2. Design J3 as explicit wired 8-pin control interface, after identifying required GPIO25 PWM, 3V3, GND, SDA/SCL for INA219, cell voltage ADC, enable/disable, temperature input. Never assume physical board header matches J3.
3. Define discharge circuit and charger/load isolation; verify MOSFET linear DC SOA and hard fail-safe cutoff.
4. Confirm display GPIO assignments, USB power distribution and ADC input divider before assigning any pin.
5. Current R12 0 DRC errors does NOT validate these interfaces or battery safety.
