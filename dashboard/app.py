import streamlit as st
import pandas as pd
import os
import time
from sensor import TemperatureSensor, SensorNotFoundError
from pid_controller import PIDController
from logger import Logger

# Path to log file
LOG_PATH = 'data/temp_logs.csv'

# Initialize logger
logger = Logger(LOG_PATH)

# Streamlit UI
st.set_page_config(page_title="Smart Oven Dashboard", layout="wide")
st.title("Smart Oven Real-Time Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
mode = st.sidebar.selectbox("Mode", ["Auto", "Manual"])
setpoint = st.sidebar.number_input("Setpoint (°C)", min_value=0.0, max_value=300.0, value=100.0, step=0.5)
manual_heater_pwm = st.sidebar.slider("Manual Heater PWM (%)", 0, 100, 0)
manual_fan_pwm = st.sidebar.slider("Manual Fan PWM (%)", 0, 100, 0)

# PID Controller (example values)
pid = PIDController(Kp=2.0, Ki=0.1, Kd=1.0, setpoint=setpoint, integral_limit=(0, 100))

# Try to read temperature
try:
    sensor = TemperatureSensor()
    current_temp = sensor.read_temperature()
    if current_temp is None:
        safety_status = "SENSOR ERROR"
    else:
        safety_status = "SAFE" if current_temp < setpoint + 20 else "OVERHEAT"
except SensorNotFoundError:
    current_temp = None
    safety_status = "SENSOR ERROR"

# Determine PWM values
if mode == "Auto" and current_temp is not None:
    pid.update_setpoint(setpoint)
    heater_pwm = int(pid.compute(current_temp))
    fan_pwm = 100 if current_temp > setpoint + 10 else 0
elif mode == "Manual":
    heater_pwm = manual_heater_pwm
    fan_pwm = manual_fan_pwm
else:
    heater_pwm = 0
    fan_pwm = 0

# Log the entry
logger.log_entry(current_temp, setpoint, heater_pwm, fan_pwm, safety_status)

# Display current values
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Current Temp (°C)", f"{current_temp if current_temp is not None else 'N/A'}")
col2.metric("Setpoint (°C)", f"{setpoint}")
col3.metric("Heater PWM (%)", f"{heater_pwm}")
col4.metric("Fan PWM (%)", f"{fan_pwm}")
col5.metric("Safety Status", safety_status)

# Load log data for chart
if os.path.exists(LOG_PATH):
    df = pd.read_csv(LOG_PATH)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.line_chart(
            df.set_index('timestamp')[['current_temperature', 'setpoint']],
            use_container_width=True
        )
    else:
        st.info("No data to display yet.")
else:
    st.info("Log file not found.")

# Auto-refresh every 2 seconds (for real-time, use st_autorefresh in production)
# from streamlit_autorefresh import st_autorefresh
# st_autorefresh(interval=2000, key="datarefresh")
st.write("\n")
st.caption("Dashboard updates every 2 seconds. (Refresh manually or use st_autorefresh for auto-update)")
time.sleep(2) 