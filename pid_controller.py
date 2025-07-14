class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint=0.0, integral_limit=(None, None), hysteresis=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.last_error = 0.0
        self.last_output = 0.0
        self.integral_min, self.integral_max = integral_limit
        self.hysteresis = hysteresis

    def update_setpoint(self, setpoint):
        self.setpoint = setpoint

    def compute(self, current_temp):
        error = self.setpoint - current_temp

        # Hysteresis: if error is within hysteresis band, output stays the same
        if abs(error) < self.hysteresis:
            return self.last_output

        # Proportional
        P = self.Kp * error

        # Integral with clamping (anti-windup)
        self.integral += error
        if self.integral_min is not None:
            self.integral = max(self.integral_min, self.integral)
        if self.integral_max is not None:
            self.integral = min(self.integral_max, self.integral)
        I = self.Ki * self.integral

        # Derivative
        D = self.Kd * (error - self.last_error)
        self.last_error = error

        # PID output
        output = P + I + D
        # Clamp output to 0-100 (PWM duty cycle)
        output = max(0, min(100, output))
        self.last_output = output
        return output 