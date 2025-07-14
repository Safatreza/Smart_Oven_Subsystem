import streamlit as st
import pandas as pd
import time
import os

CSV_FILE = 'temperature_log.csv'

st.set_page_config(page_title="Smart Oven Dashboard", layout="centered")
st.title("Smart Oven Control Dashboard")

# Sidebar controls
st.sidebar.header("Control Panel")
mode = st.sidebar.radio("Mode", ["Auto", "Manual"])
setpoint = st.sidebar.slider("Setpoint (°C)", min_value=15.0, max_value=35.0, value=25.0, step=0.1)
manual_pwm = st.sidebar.slider("Manual PWM (%)", min_value=0, max_value=100, value=0, step=1, disabled=(mode=="Auto"))

# Save setpoint and mode for controller (in real system, would communicate to controller)
# For demo, just display
st.sidebar.write(f"Current Mode: {mode}")
st.sidebar.write(f"Setpoint: {setpoint:.1f}°C")
if mode == "Manual":
    st.sidebar.write(f"Manual PWM: {manual_pwm}%")

# Main dashboard
st.subheader("Real-Time Data")

# Function to read latest data
def read_latest_data():
    if not os.path.exists(CSV_FILE):
        return None
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        return None
    latest = df.iloc[-1]
    return latest, df

placeholder = st.empty()
plot_placeholder = st.empty()

# Real-time update loop
for _ in range(300):  # Run for 5 minutes (adjust as needed)
    result = read_latest_data()
    if result is None:
        placeholder.warning("Waiting for data...")
        time.sleep(1)
        continue
    latest, df = result
    temp = latest['temperature']
    sp = latest['setpoint']
    pwm = latest['pwm_duty']
    timestamp = latest['timestamp']
    with placeholder.container():
        st.metric("Temperature (°C)", f"{temp:.2f}")
        st.metric("Setpoint (°C)", f"{sp:.2f}")
        st.metric("PWM Duty (%)", f"{pwm:.1f}")
        st.write(f"Timestamp: {timestamp:.0f}")
    with plot_placeholder.container():
        st.line_chart(df[['temperature', 'setpoint']])
    time.sleep(1)

st.success("Session ended. Refresh to restart.") 