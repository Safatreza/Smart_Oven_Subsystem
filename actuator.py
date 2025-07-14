import RPi.GPIO as GPIO

class Actuator:
    def __init__(self, heater_pin, fan_pin, pwm_freq=1000):
        self.heater_pin = heater_pin
        self.fan_pin = fan_pin
        self.pwm_freq = pwm_freq

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.heater_pin, GPIO.OUT)
        GPIO.setup(self.fan_pin, GPIO.OUT)

        self.heater_pwm = GPIO.PWM(self.heater_pin, self.pwm_freq)
        self.fan_pwm = GPIO.PWM(self.fan_pin, self.pwm_freq)

        self.heater_pwm.start(0)
        self.fan_pwm.start(0)

    def set_heater_pwm(self, duty_cycle):
        # Clamp duty cycle between 0 and 100
        duty_cycle = max(0, min(100, duty_cycle))
        self.heater_pwm.ChangeDutyCycle(duty_cycle)

    def set_fan_pwm(self, duty_cycle):
        # Clamp duty cycle between 0 and 100
        duty_cycle = max(0, min(100, duty_cycle))
        self.fan_pwm.ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        self.heater_pwm.stop()
        self.fan_pwm.stop()
        GPIO.cleanup() 