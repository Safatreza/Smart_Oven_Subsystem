try:
    from w1thermsensor import W1ThermSensor, SensorNotReadyError, NoSensorFoundError
    W1_AVAILABLE = True
except ImportError:
    W1_AVAILABLE = False

class SensorNotFoundError(Exception):
    """Custom exception for when the temperature sensor is not found."""
    pass

if W1_AVAILABLE:
    class TemperatureSensor:
        def __init__(self):
            try:
                self.sensor = W1ThermSensor()
            except NoSensorFoundError:
                self.sensor = None
                raise SensorNotFoundError("DS18B20 temperature sensor not found.")

        def read_temperature(self):
            if self.sensor is None:
                return None
            try:
                return self.sensor.get_temperature()
            except (SensorNotReadyError, NoSensorFoundError):
                return None
else:
    class TemperatureSensor:
        def __init__(self):
            self.sensor = None
        def read_temperature(self):
            return None 