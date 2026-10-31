# PCB GPT pilot — tester 18650 (NO PCB CHANGES)

## Objective
Determine whether [tk-king/pcbGPT](https://github.com/tk-king/pcbGPT) reduces manual effort and produces a usable, editable KiCad schematic for a **single-channel** 18650 capacity tester. This is a tool test, not permission to redesign or fabricate the current board.

## Test setup
- Windows 10, existing KiCad 10.0.x.
- pcbGPT Windows release v0.0.3 (2026-10-01): https://github.com/tk-king/pcbGPT/releases/download/v0.0.3/PCBGPT.exe
- Configure an OpenAI-compatible provider in Settings (local Ollama support is NOT yet verified in a real run).
- Existing reference repository: https://github.com/edekmedek/Tester-18650-baterija/tree/tester-v1-tp4056
- Do not overwrite the R42/R60 files; export to separate folder.

## Single test prompt
You are evaluating schematic generation, not manufacturing readiness.

Create one editable KiCad schematic for a **single-cell 18650 capacity tester** using an external ESP32 board, external INA219 current sensor module, an external USB-C TP4056 protection/charger module with pads B+, B-, OUT+, OUT-, **one** logic-level MOSFET driven directly from 3.3 V, and **one external** 4.7 ohm 15 W power resistor. The resistor is an on/off discharge load, **not constant current**. ESP32 integrates measured INA219 current over time for mAh. No separate gate driver or 10 V supply.

Strict requirements:
1. Distinguish TP4056 B− vs OUT−; no bypass of battery protection.
2. Identify how INA219 VIN+ and VIN- enter the real discharge path; include sensor supply and I2C. Do not confuse the INA219 module shunt with a low-side current-control shunt.
3. Provide a separate safe measurement of the **cell voltage** so discharge can stop before excessive depletion. Explain the measurement reference and any divider needed.
4. Default OFF on ESP32 boot/reset; specify physical gate pull-down and gate resistor.
5. Add fusing, reverse-polarity strategy, and verify overtemperature/undervoltage fail-safe as actual circuitry. If these cannot be safely implemented with specified parts, report blockers, not fabricated functionality.
6. State charging/discharging interlock. Never treat simultaneous charger and load operation as safe by default.
7. Use documented physical pinouts of chosen parts; ask questions instead of guessing actual ESP32, INA219, TP4056 board pin order.
8. Produce an **editable .kicad_sch** with named nets, BOM, and ERC report; distinguish pass/fail/warnings, and list all unresolved issues.
9. Do NOT generate manufacturing files or claim the design is battery-safe.

## Success criteria
- App runs on user's Windows machine.
- KiCad opens exported schematic.
- Components and connections are plausible and pinouts are grounded; warnings don't get hidden.
- Run ERC in KiCad; count errors/warnings.
- Record manual interventions and time spent; compare against manual/scripted approach.
- If the tool merely generates a schematic draft but not PCB routing, record that limitation.

## Status
GitHub project inspection and release availability verified. **No actual local pcbGPT run has been performed.**
