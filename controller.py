
class TankController:
    def __init__(self):
        self.level = 35.0
        self.integral = 0.0
        self.previous_error = 0.0

    def calculate_pid(self, setpoint):
        error = setpoint - self.level

        kp = 3.0
        ki = 0.08
        kd = 0.5

        self.integral += error
        self.integral = max(-500, min(500, self.integral))

        derivative = error - self.previous_error

        output = (
            kp * error
            + ki * self.integral
            + kd * derivative
        )

        self.previous_error = error

        return max(0, min(100, output))

    def update_tank(self, pump_speed, valve_opening):
        inflow = pump_speed * 0.08
        outflow = valve_opening * 0.05

        self.level += inflow - outflow

        # Keep tank level within physical simulation limits
        self.level = max(0, min(100, self.level))

        return self.level

    def get_alarm(self):
        if self.level >= 95:
            return "HIGH-HIGH LEVEL"
        elif self.level >= 90:
            return "HIGH LEVEL"
        elif self.level <= 10:
            return "LOW LEVEL"
        else:
            return "NORMAL"


def high_high_interlock(
    current_level,
    projected_level,
    threshold=95
):
    """
    Returns True when the current or projected tank level
    reaches the high-high safety threshold.
    """
    return (
        current_level >= threshold
        or projected_level >= threshold
    )
