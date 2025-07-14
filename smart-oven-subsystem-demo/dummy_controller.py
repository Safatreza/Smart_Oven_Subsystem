import time
import csv
import random
import math
import os

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
        output = max(self.output_limits[0], min(self.output_limits[1], output))
        self._last_error = error
        self._last_time = now
        return output

def random_walk(temp, pwm, ambient=22.0):
    # Simulate heating/cooling effect
    if pwm > 0:
        temp += 0.1 * (pwm / 100.0) + random.uniform(-0.05, 0.05)
    else:
        temp += (ambient - temp) * 0.01 + random.uniform(-0.05, 0.05)
    return temp

CSV_FILE = 'dummy_data.csv'
SETPOINT_FILE = 'setpoint_override.txt'

with open(CSV_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'temperature', 'setpoint', 'pwm_duty'])

def main():
    pid = PID(Kp=2.0, Ki=0.1, Kd=1.0, setpoint=25.0, output_limits=(0, 100))
    temp = 22.0
    interval = 1.0
    print("Starting dummy control loop. Press Ctrl+C to stop.")
    try:
        while True:
            # Allow setpoint override from dashboard
            if os.path.exists(SETPOINT_FILE):
                try:
                    with open(SETPOINT_FILE, 'r') as f:
                        new_setpoint = float(f.read().strip())
                        pid.setpoint = new_setpoint
                except Exception:
                    pass
            pwm = pid.compute(temp)
            temp = random_walk(temp, pwm)
            # Fault detection: shut off if temp is NaN or >70°C
            if math.isnan(temp) or temp > 70.0:
                pwm = 0
                print(f"FAULT: Temp={temp} (NaN or >70°C). Heater shut off.")
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([time.time(), temp, pid.setpoint, pwm])
            print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | PWM: {pwm:.1f}%")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nDummy control loop stopped.")

if __name__ == "__main__":
    main() 