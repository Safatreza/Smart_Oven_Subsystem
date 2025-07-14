import time
import csv
import random

# PID Controller class
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class PID:
    def __init__(self, Kp, Ki, Kd, setpoint=25.0, output_limits=(0, 100)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits
        self._last_error = 0.0
        self._integral = 0.0
        self._last_time = None

    def compute(self, measurement):
        now = time.time()
        error = self.setpoint - measurement
        dt = 1.0
        if self._last_time is not None:
            dt = now - self._last_time
        self._integral += error * dt
        derivative = 0.0
        if self._last_time is not None:
            derivative = (error - self._last_error) / dt
        output = (
            self.Kp * error +
            self.Ki * self._integral +
            self.Kd * derivative
        )
        output = clamp(output, *self.output_limits)
        self._last_error = error
        self._last_time = now
        return output

# Simulate DS18B20 temperature reading
def read_temperature():
    # Replace with actual sensor code if on Raspberry Pi
    # Return None to simulate sensor failure occasionally
    if random.random() < 0.05:
        return None
    return 20.0 + random.uniform(-2, 2)  # Simulate around 20°C

# Simulate PWM output (replace with GPIO code for real hardware)
def set_pwm_duty_cycle(duty_cycle):
    # For demo, just print or pass
    print(f"PWM Duty Cycle: {duty_cycle:.1f}%")

# Logging setup
CSV_FILE = 'temperature_log.csv'

with open(CSV_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'temperature', 'setpoint', 'pwm_duty', 'safety_status'])

# Safety parameters
SAFETY_TEMP = 70.0
HYSTERESIS = 2.0

# Main loop
def main():
    pid = PID(Kp=2.0, Ki=0.1, Kd=1.0, setpoint=25.0, output_limits=(0, 100))
    interval = 1.0  # seconds
    print("Starting control loop. Press Ctrl+C to stop.")
    safety_status = "SAFE"
    overheat_latch = False
    try:
        while True:
            temp = read_temperature()
            # Sensor failure check
            if temp is None:
                pwm = 0
                safety_status = "SENSOR ERROR"
                set_pwm_duty_cycle(pwm)
                with open(CSV_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([time.time(), temp, pid.setpoint, pwm, safety_status])
                print(f"Temp: N/A | Setpoint: {pid.setpoint:.2f}°C | PWM: {pwm:.1f}% | SAFETY: {safety_status}")
                time.sleep(interval)
                continue
            # Overheat safety with hysteresis
            if overheat_latch:
                if temp < SAFETY_TEMP - HYSTERESIS:
                    overheat_latch = False
                    safety_status = "SAFE"
                else:
                    pwm = 0
                    safety_status = "OVERHEAT"
                    set_pwm_duty_cycle(pwm)
                    with open(CSV_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([time.time(), temp, pid.setpoint, pwm, safety_status])
                    print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | PWM: {pwm:.1f}% | SAFETY: {safety_status}")
                    time.sleep(interval)
                    continue
            if temp >= SAFETY_TEMP:
                overheat_latch = True
                pwm = 0
                safety_status = "OVERHEAT"
                set_pwm_duty_cycle(pwm)
                with open(CSV_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([time.time(), temp, pid.setpoint, pwm, safety_status])
                print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | PWM: {pwm:.1f}% | SAFETY: {safety_status}")
                time.sleep(interval)
                continue
            # Normal operation
            pwm = pid.compute(temp)
            safety_status = "SAFE"
            set_pwm_duty_cycle(pwm)
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([time.time(), temp, pid.setpoint, pwm, safety_status])
            print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | PWM: {pwm:.1f}% | SAFETY: {safety_status}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nControl loop stopped.")

if __name__ == "__main__":
    main() 