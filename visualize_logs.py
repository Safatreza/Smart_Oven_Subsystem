import matplotlib.pyplot as plt
import pandas as pd
import os

# List available CSV log files
def list_log_files():
    log_files = []
    if os.path.exists('data'):
        log_files += [os.path.join('data', f) for f in os.listdir('data') if f.endswith('.csv')]
    demo_log = 'smart-oven-subsystem-demo/dummy_data.csv'
    if os.path.exists(demo_log):
        log_files.append(demo_log)
    return log_files

def main():
    log_files = list_log_files()
    if not log_files:
        print("No log files found.")
        return
    print("Available log files:")
    for i, f in enumerate(log_files):
        print(f"[{i}] {f}")
    idx = int(input(f"Select log file [0-{len(log_files)-1}]: "))
    log_file = log_files[idx]
    df = pd.read_csv(log_file)
    if 'timestamp' in df.columns:
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        except Exception:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    else:
        print("No 'timestamp' column found in log.")
        return
    # Plot temperature and setpoint
    plt.figure(figsize=(12, 6))
    if 'current_temperature' in df.columns:
        plt.plot(df['timestamp'], df['current_temperature'], label='Temperature (°C)')
        plt.plot(df['timestamp'], df['setpoint'], label='Setpoint (°C)')
    elif 'temperature' in df.columns:
        plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)')
        plt.plot(df['timestamp'], df['setpoint'], label='Setpoint (°C)')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature and Setpoint Over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()
    # Plot PWM
    plt.figure(figsize=(12, 4))
    if 'heater_pwm' in df.columns:
        plt.plot(df['timestamp'], df['heater_pwm'], label='Heater PWM (%)')
    if 'fan_pwm' in df.columns:
        plt.plot(df['timestamp'], df['fan_pwm'], label='Fan PWM (%)')
    if 'pwm_duty' in df.columns:
        plt.plot(df['timestamp'], df['pwm_duty'], label='PWM Duty (%)')
    plt.xlabel('Time')
    plt.ylabel('PWM (%)')
    plt.title('PWM Output Over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()
    # Plot safety status if available
    if 'safety_status' in df.columns:
        plt.figure(figsize=(12, 2))
        plt.plot(df['timestamp'], df['safety_status'], 'o-', label='Safety Status')
        plt.xlabel('Time')
        plt.title('Safety Status Over Time')
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    main() 