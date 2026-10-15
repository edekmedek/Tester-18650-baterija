import unittest
from slot_supervisor import Slot, Sample, State, Outputs

GOOD = Sample(True, True, 3.7, 25.0, 0.0, True, True)


class SlotSupervisorTests(unittest.TestCase):
    def test_insert_stays_off(self):
        s = Slot()
        self.assertEqual(s.step(GOOD), Outputs())
        self.assertEqual(s.state, State.CHECK)
        self.assertEqual(s.step(GOOD), Outputs())

    def test_normal_sequence(self):
        s = Slot()
        s.step(GOOD)
        s.authorize_qualified_cell()
        self.assertEqual(s.step(GOOD), Outputs(charge_request=True))
        self.assertEqual(s.step(GOOD, charge_done=True), Outputs())
        self.assertEqual(s.step(GOOD, rest_done=True), Outputs())
        self.assertEqual(s.step(GOOD), Outputs(discharge_request=True))
        self.assertEqual(s.step(GOOD, discharge_done=True), Outputs())
        self.assertEqual(s.step(GOOD, rest_done=True), Outputs())
        self.assertEqual(s.step(GOOD), Outputs(charge_request=True))
        self.assertEqual(s.step(GOOD, charge_done=True), Outputs())
        self.assertEqual(s.state, State.COMPLETE)

    def test_fault_latched_and_off(self):
        s = Slot()
        s.step(GOOD)
        s.authorize_qualified_cell()
        bad = Sample(True, True, 3.7, 60.0, 0.0, True, True)
        self.assertEqual(s.step(bad), Outputs())
        self.assertEqual(s.state, State.FAULT)
        self.assertEqual(s.step(GOOD), Outputs())
        self.assertEqual(s.state, State.FAULT)
        self.assertEqual(s.step(Sample(False, True, 0, 25, 0, True, True), operator_reset=True), Outputs())
        self.assertEqual(s.state, State.EMPTY)

    def test_removed_cell_stops(self):
        s = Slot()
        s.step(GOOD)
        s.authorize_qualified_cell()
        s.step(Sample(False, True, 0, 25, 0, True, True))
        self.assertEqual(s.state, State.FAULT)

    def test_hardware_fault_stops(self):
        s = Slot()
        s.step(GOOD)
        s.authorize_qualified_cell()
        s.step(Sample(True, True, 3.7, 25, 0, True, False))
        self.assertEqual(s.state, State.FAULT)

    def test_cannot_authorize_empty(self):
        with self.assertRaises(ValueError):
            Slot().authorize_qualified_cell()


if __name__ == "__main__":
    unittest.main()
