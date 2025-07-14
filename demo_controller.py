import time
import random

setpoint = 50.0
temperature = 20.0
pwm_duty = 0.0

def dummy_pid(temp, setpoint):
    error = setpoint - temp
    return max(0, min(100, error * 2))  # Simple proportional control

print("Running demo oven controller...")
for _ in range(20):
    temperature += random.uniform(-0.5, 0.5)
    pwm_duty = dummy_pid(temperature, setpoint)
    print(f"Temp: {temperature:.2f}°C | Setpoint: {setpoint}°C | PWM: {pwm_duty:.1f}%")
    time.sleep(1) 