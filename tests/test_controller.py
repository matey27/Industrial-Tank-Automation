
import unittest

from controller import (
    TankController,
    high_high_interlock
)


class TestTankController(unittest.TestCase):

    def setUp(self):
        self.controller = TankController()

    def test_initial_tank_level(self):
        self.assertEqual(self.controller.level, 35.0)

    def test_tank_level_increases_with_pump(self):
        initial_level = self.controller.level

        new_level = self.controller.update_tank(
            pump_speed=50,
            valve_opening=0
        )

        self.assertGreater(new_level, initial_level)

    def test_tank_level_decreases_with_outlet(self):
        initial_level = self.controller.level

        new_level = self.controller.update_tank(
            pump_speed=0,
            valve_opening=50
        )

        self.assertLess(new_level, initial_level)

    def test_tank_level_never_exceeds_100(self):
        self.controller.level = 99

        new_level = self.controller.update_tank(
            pump_speed=100,
            valve_opening=0
        )

        self.assertLessEqual(new_level, 100)

    def test_tank_level_never_below_zero(self):
        self.controller.level = 1

        new_level = self.controller.update_tank(
            pump_speed=0,
            valve_opening=100
        )

        self.assertGreaterEqual(new_level, 0)

    def test_normal_alarm(self):
        self.controller.level = 50
        self.assertEqual(
            self.controller.get_alarm(),
            "NORMAL"
        )

    def test_high_alarm_at_90(self):
        self.controller.level = 90
        self.assertEqual(
            self.controller.get_alarm(),
            "HIGH LEVEL"
        )

    def test_high_high_alarm_at_95(self):
        self.controller.level = 95
        self.assertEqual(
            self.controller.get_alarm(),
            "HIGH-HIGH LEVEL"
        )

    def test_low_alarm_at_10(self):
        self.controller.level = 10
        self.assertEqual(
            self.controller.get_alarm(),
            "LOW LEVEL"
        )

    def test_pid_output_is_within_limits(self):
        output = self.controller.calculate_pid(60)

        self.assertGreaterEqual(output, 0)
        self.assertLessEqual(output, 100)

    def test_interlock_activates_at_current_threshold(self):
        result = high_high_interlock(
            current_level=95,
            projected_level=96
        )

        self.assertTrue(result)

    def test_interlock_activates_at_projected_threshold(self):
        result = high_high_interlock(
            current_level=94,
            projected_level=95
        )

        self.assertTrue(result)

    def test_interlock_remains_inactive_below_threshold(self):
        result = high_high_interlock(
            current_level=80,
            projected_level=90
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
