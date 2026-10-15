"""Deterministic supervisory state machine for ONE 18650 test slot.

NOT a battery charger, protection circuit or production firmware.
Hardware must independently force charge/load OFF on faults or MCU reset.
"""
from dataclasses import dataclass
from enum import Enum, auto


class State(Enum):
    EMPTY = auto()
    CHECK = auto()
    CHARGE = auto()
    REST1 = auto()
    DISCHARGE = auto()
    REST2 = auto()
    RECHARGE = auto()
    COMPLETE = auto()
    FAULT = auto()


@dataclass(frozen=True)
class Sample:
    cell_present: bool
    polarity_ok: bool
    voltage_v: float
    temp_c: float
    current_a: float
    sensors_ok: bool
    hardware_ok: bool


@dataclass(frozen=True)
class Outputs:
    charge_request: bool = False
    discharge_request: bool = False


class Slot:
    def __init__(self):
        self.state = State.EMPTY
        self.fault_reason = None

    def fault(self, reason: str):
        self.state = State.FAULT
        self.fault_reason = reason

    def step(self, sample: Sample, *, charge_done=False, rest_done=False,
             discharge_done=False, operator_reset=False) -> Outputs:
        # Latching fault; cannot restart with cell installed.
        if self.state is State.FAULT:
            if operator_reset and not sample.cell_present:
                self.state, self.fault_reason = State.EMPTY, None
            return Outputs()
        if self.state is State.EMPTY:
            if sample.cell_present:
                self.state = State.CHECK
            return Outputs()
        if not sample.cell_present:
            self.fault("cell removed during test")
        elif not sample.sensors_ok or not sample.hardware_ok:
            self.fault("sensor or hardware interlock failed")
        elif not sample.polarity_ok:
            self.fault("reverse polarity")
        elif not (0.0 <= sample.voltage_v <= 4.25):
            self.fault("invalid or excessive voltage")
        elif not (0.0 <= sample.temp_c <= 45.0):
            self.fault("temperature out of supervisory envelope")
        elif abs(sample.current_a) > 1.0:
            self.fault("unexpected measured current")
        if self.state is State.FAULT:
            return Outputs()

        if self.state is State.CHECK:
            # Intentionally requires explicit policy authorization by operator
            # or future validated cell qualification logic.
            return Outputs()
        if self.state is State.CHARGE:
            if charge_done:
                self.state = State.REST1
                return Outputs()
            return Outputs(charge_request=True)
        if self.state is State.REST1:
            if rest_done:
                self.state = State.DISCHARGE
            return Outputs()
        if self.state is State.DISCHARGE:
            if discharge_done:
                self.state = State.REST2
                return Outputs()
            return Outputs(discharge_request=True)
        if self.state is State.REST2:
            if rest_done:
                self.state = State.RECHARGE
            return Outputs()
        if self.state is State.RECHARGE:
            if charge_done:
                self.state = State.COMPLETE
                return Outputs()
            return Outputs(charge_request=True)
        return Outputs()

    def authorize_qualified_cell(self):
        # No output activation here. Caller must separately validate
        # chemistry, cell condition and limits, and hardware interlock.
        if self.state is not State.CHECK:
            raise ValueError("cell not awaiting qualification")
        self.state = State.CHARGE
