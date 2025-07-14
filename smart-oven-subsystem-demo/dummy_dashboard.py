import streamlit as st
import pandas as pd
import os
import time

CSV_FILE = 'dummy_data.csv'

st.set_page_config(page_title="Dummy Smart Oven Dashboard", layout="wide")
st.title("Dummy Smart Oven Real-Time Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
setpoint = st.sidebar.number_input("Setpoint (°C)", min_value=0.0, max_value=300.0, value=25.0, step=0.5)

# Display current values
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    if not df.empty:
        last = df.iloc[-1]
        temp = last['temperature']
        pwm = last['pwm_duty']
        safety_status = "SAFE"
        if temp >= 70:
            safety_status = "OVERHEAT"
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Temp (°C)", f"{temp:.2f}")
        col2.metric("Setpoint (°C)", f"{setpoint}")
        col3.metric("PWM (%)", f"{pwm:.1f}")
        col4.metric("Safety Status", safety_status)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        st.line_chart(df.set_index('timestamp')[['temperature', 'setpoint']], use_container_width=True)
    else:
        st.info("No data to display yet.")
else:
    st.info("Log file not found.")

st.caption("Dummy dashboard. Data updates as dummy_controller.py runs.") 