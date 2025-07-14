import unittest
import sys
import os

# Add project root to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pid_controller import PIDController
from logger import Logger

# Try to import hardware modules, skip if not available
try:
    from sensor import TemperatureSensor, SensorNotFoundError
    from actuator import Actuator
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False

class TestPIDController(unittest.TestCase):
    def test_pid_basic(self):
        pid = PIDController(Kp=2.0, Ki=0.1, Kd=1.0, setpoint=100)
        output = pid.compute(90)
        self.assertIsInstance(output, (int, float))
        self.assertGreaterEqual(output, 0)
        self.assertLessEqual(output, 100)

    def test_pid_hysteresis(self):
        pid = PIDController(Kp=2.0, Ki=0.1, Kd=1.0, setpoint=100, hysteresis=5)
        out1 = pid.compute(98)
        out2 = pid.compute(101)
        self.assertEqual(out1, out2)  # Should hold output within hysteresis

class TestLogger(unittest.TestCase):
    def test_log_entry(self):
        logger = Logger(log_path='tests/test_log.csv')
        logger.log_entry(25.0, 100.0, 50, 0, 'SAFE')
        self.assertTrue(os.path.exists('tests/test_log.csv'))
        with open('tests/test_log.csv') as f:
            lines = f.readlines()
        self.assertGreaterEqual(len(lines), 2)  # header + at least one entry
        os.remove('tests/test_log.csv')

@unittest.skipUnless(HARDWARE_AVAILABLE, "Hardware modules not available")
class TestSensorActuator(unittest.TestCase):
    def test_sensor(self):
        try:
            sensor = TemperatureSensor()
            temp = sensor.read_temperature()
            self.assertTrue(temp is None or isinstance(temp, float))
        except SensorNotFoundError:
            self.assertTrue(True)  # Acceptable if not found

    def test_actuator(self):
        actuator = Actuator(heater_pin=17, fan_pin=27, pwm_freq=1000)
        actuator.set_heater_pwm(50)
        actuator.set_fan_pwm(50)
        actuator.cleanup()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main() 