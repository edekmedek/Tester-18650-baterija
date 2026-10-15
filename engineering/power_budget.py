#!/usr/bin/env python3
"""Preliminary electrical/thermal budget for 10-channel 1S analyzer.

Engineering estimate ONLY. Not a lithium-cell safety controller, PCB signoff,
component selection, or proof of MOSFET DC safe operating area.
"""
from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class Design:
    slots: int = 10
    supply_v: float = 5.0
    cell_min_v: float = 3.0
    cell_max_v: float = 4.2
    charge_a: float = 0.5
    discharge_a: float = 0.5
    logic_w: float = 3.0
    supply_headroom: float = 1.30
    charge_active: int = 10
    discharge_active: int = 10

    def validate(self) -> None:
        if not 1 <= self.slots <= 64:
            raise ValueError("slots must be 1..64")
        if not 0 <= self.charge_active <= self.slots:
            raise ValueError("invalid charging slot count")
        if not 0 <= self.discharge_active <= self.slots:
            raise ValueError("invalid discharging slot count")
        if self.charge_active + self.discharge_active > self.slots:
            raise ValueError("one slot cannot charge and discharge simultaneously")
        if not (0 < self.cell_min_v <= self.cell_max_v < self.supply_v):
            raise ValueError("invalid cell/supply voltage envelope for linear charger")
        if min(self.charge_a, self.discharge_a, self.logic_w) < 0:
            raise ValueError("negative load")
        if self.supply_headroom < 1:
            raise ValueError("supply_headroom must be >= 1")


def budget(d: Design) -> dict:
    d.validate()
    # Approximation: linear charger from supply rail; no power-path loads.
    # Charger IC heat worst near minimum CELL voltage at constant charge current.
    heat_charge_w = d.charge_active * (d.supply_v - d.cell_min_v) * d.charge_a
    heat_discharge_w = d.discharge_active * d.cell_max_v * d.discharge_a
    # Worst charger supply draw while active, excluding conversion/board losses.
    supply_input_w = d.charge_active * d.supply_v * d.charge_a + d.logic_w
    adapter_w = supply_input_w * d.supply_headroom
    return {
        "charge_ic_heat_w": heat_charge_w,
        "load_heat_w": heat_discharge_w,
        "total_board_heat_w": heat_charge_w + heat_discharge_w + d.logic_w,
        "adapter_input_w": supply_input_w,
        "adapter_min_with_margin_w": adapter_w,
        "adapter_current_with_margin_a": adapter_w / d.supply_v,
        "adapter_standard_step_5w_w": ceil(adapter_w / 5) * 5,
    }


def main() -> None:
    cases = {
        "all charging": Design(charge_active=10, discharge_active=0),
        "all discharging": Design(charge_active=0, discharge_active=10),
        "mixed 5/5": Design(charge_active=5, discharge_active=5),
    }
    for name, d in cases.items():
        b = budget(d)
        print(f"\n{name}")
        for key, value in b.items():
            print(f"  {key}: {value:.2f}")
    print("\nWARNING: approximate power only; excludes transient, fan and")
    print("conversion losses, real thermal resistance, NTC tolerances,")
    print("and MOSFET DC SOA. Never use this as a safety approval.")


if __name__ == "__main__":
    main()
