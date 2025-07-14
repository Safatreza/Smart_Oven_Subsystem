import os
import pandas as pd
from datetime import datetime

class Logger:
    def __init__(self, log_path='data/temp_logs.csv'):
        self.log_path = log_path
        self.columns = [
            'timestamp',
            'current_temperature',
            'setpoint',
            'heater_pwm',
            'fan_pwm',
            'safety_status'
        ]
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        # Create file with header if it doesn't exist
        if not os.path.isfile(self.log_path):
            pd.DataFrame(columns=self.columns).to_csv(self.log_path, index=False)

    def log_entry(self, current_temperature, setpoint, heater_pwm, fan_pwm, safety_status):
        timestamp = datetime.now().isoformat()
        entry = {
            'timestamp': timestamp,
            'current_temperature': current_temperature,
            'setpoint': setpoint,
            'heater_pwm': heater_pwm,
            'fan_pwm': fan_pwm,
            'safety_status': safety_status
        }
        df = pd.DataFrame([entry])
        df.to_csv(self.log_path, mode='a', header=False, index=False) 