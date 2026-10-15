import unittest
from dataclasses import replace
from power_budget import Design, budget


class BudgetTests(unittest.TestCase):
    def test_all_charging(self):
        b = budget(Design(charge_active=10, discharge_active=0))
        self.assertAlmostEqual(b["charge_ic_heat_w"], 10)
        self.assertAlmostEqual(b["load_heat_w"], 0)
        self.assertAlmostEqual(b["adapter_min_with_margin_w"], 36.4)

    def test_all_discharging(self):
        b = budget(Design(charge_active=0, discharge_active=10))
        self.assertAlmostEqual(b["load_heat_w"], 21)
        self.assertAlmostEqual(b["adapter_input_w"], 3)

    def test_mixed(self):
        b = budget(Design(charge_active=5, discharge_active=5))
        self.assertAlmostEqual(b["charge_ic_heat_w"], 5)
        self.assertAlmostEqual(b["load_heat_w"], 10.5)

    def test_no_simultaneous_charge_discharge_same_slot(self):
        with self.assertRaises(ValueError):
            budget(Design(charge_active=8, discharge_active=8))

    def test_voltage_envelope(self):
        with self.assertRaises(ValueError):
            budget(replace(Design(), supply_v=4.0))

    def test_negative_current(self):
        with self.assertRaises(ValueError):
            budget(replace(Design(), discharge_a=-0.1))


if __name__ == "__main__":
    unittest.main()
