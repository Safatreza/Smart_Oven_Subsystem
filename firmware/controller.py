import time
from sensor import TemperatureSensor, SensorNotFoundError
from pid_controller import PIDController
from actuator import Actuator
from logger import Logger

# Configuration
HEATER_PIN = 17  # Example BCM pin
FAN_PIN = 27     # Example BCM pin
PWM_FREQ = 1000  # 1 kHz
LOG_PATH = 'data/temp_logs.csv'
SETPOINT = 100.0
SAFETY_TEMP = 70.0
HYSTERESIS = 2.0


def main():
    # Initialize modules
    logger = Logger(LOG_PATH)
    try:
        sensor = TemperatureSensor()
    except SensorNotFoundError:
        print("Temperature sensor not found. Exiting.")
        return
    pid = PIDController(Kp=2.0, Ki=0.1, Kd=1.0, setpoint=SETPOINT, integral_limit=(0, 100))
    actuator = Actuator(heater_pin=HEATER_PIN, fan_pin=FAN_PIN, pwm_freq=PWM_FREQ)

    overheat_latch = False
    safety_status = "SAFE"
    interval = 1.0
    print("Starting firmware control loop. Press Ctrl+C to stop.")
    try:
        while True:
            temp = sensor.read_temperature()
            if temp is None:
                heater_pwm = 0
                fan_pwm = 0
                safety_status = "SENSOR ERROR"
                actuator.set_heater_pwm(heater_pwm)
                actuator.set_fan_pwm(fan_pwm)
                logger.log_entry(temp, pid.setpoint, heater_pwm, fan_pwm, safety_status)
                print(f"Temp: N/A | Setpoint: {pid.setpoint:.2f}°C | Heater PWM: {heater_pwm}% | Fan PWM: {fan_pwm}% | SAFETY: {safety_status}")
                time.sleep(interval)
                continue
            # Overheat safety with hysteresis
            if overheat_latch:
                if temp < SAFETY_TEMP - HYSTERESIS:
                    overheat_latch = False
                    safety_status = "SAFE"
                else:
                    heater_pwm = 0
                    fan_pwm = 100
                    safety_status = "OVERHEAT"
                    actuator.set_heater_pwm(heater_pwm)
                    actuator.set_fan_pwm(fan_pwm)
                    logger.log_entry(temp, pid.setpoint, heater_pwm, fan_pwm, safety_status)
                    print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | Heater PWM: {heater_pwm}% | Fan PWM: {fan_pwm}% | SAFETY: {safety_status}")
                    time.sleep(interval)
                    continue
            if temp >= SAFETY_TEMP:
                overheat_latch = True
                heater_pwm = 0
                fan_pwm = 100
                safety_status = "OVERHEAT"
                actuator.set_heater_pwm(heater_pwm)
                actuator.set_fan_pwm(fan_pwm)
                logger.log_entry(temp, pid.setpoint, heater_pwm, fan_pwm, safety_status)
                print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | Heater PWM: {heater_pwm}% | Fan PWM: {fan_pwm}% | SAFETY: {safety_status}")
                time.sleep(interval)
                continue
            # Normal operation
            pid.update_setpoint(SETPOINT)
            heater_pwm = int(pid.compute(temp))
            fan_pwm = 100 if temp > SETPOINT + 10 else 0
            safety_status = "SAFE"
            actuator.set_heater_pwm(heater_pwm)
            actuator.set_fan_pwm(fan_pwm)
            logger.log_entry(temp, pid.setpoint, heater_pwm, fan_pwm, safety_status)
            print(f"Temp: {temp:.2f}°C | Setpoint: {pid.setpoint:.2f}°C | Heater PWM: {heater_pwm}% | Fan PWM: {fan_pwm}% | SAFETY: {safety_status}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nControl loop stopped. Cleaning up...")
    finally:
        actuator.cleanup()

if __name__ == "__main__":
    main() 