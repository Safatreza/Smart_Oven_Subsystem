# Smart Oven Subsystem: Project Overview

## 1. Project Purpose
The Smart Oven Subsystem is designed to demonstrate modern embedded control principles for temperature regulation in ovens. By integrating real-time sensing, PID-based control, safety logic, and a user-friendly dashboard, the project showcases how embedded systems can deliver precise, safe, and user-configurable oven operation. This system is relevant for both educational and practical applications in embedded control, IoT, and smart appliance development.

## 2. System Architecture
The system operates in a closed-loop fashion:
- **Sensor**: Reads the oven temperature using a DS18B20 sensor.
- **PID Controller**: Calculates the optimal heater output to reach and maintain the setpoint.
- **Actuator**: Controls the heater and fan via PWM signals. In the dummy system, actuator (PWM) output is visualized as a graph.
- **Logger**: Records all system data for analysis and traceability.
- **Dashboard**: Provides a real-time web interface for monitoring, control, and safety status. The dummy dashboard allows setpoint override and visualizes actuator output.

Data flows from the sensor to the PID controller, which determines actuator commands. All actions and measurements are logged and visualized on the dashboard.

## 3. Folder Structure Overview
- `hardware/`: Schematics, PCB layouts, and setup photos for the oven sensor and control hardware.
- `simulation/`: Simulink or MATLAB models for PID tuning and system simulation.
- `firmware/`: Python scripts implementing the real-time control logic for the oven.
- `dashboard/`: Streamlit-based web UI for real-time monitoring and control.
- `data/`: CSV log files containing historical temperature, setpoint, actuator, and safety data.
- `smart-oven-subsystem-demo/`: Dummy version of the system for safe, hardware-free testing and demonstration.

## 4. Key Features
- **Real-time temperature control** with feedback from a digital sensor
- **PID tuning** for optimal oven performance
- **Safety shutoff** logic for overheat and sensor failure conditions (fault detection: if sensor reads NaN or temp > 70°C → shutoff)
- **Web dashboard** for live monitoring, setpoint adjustment, and safety status
- **Actuator (PWM) graph and setpoint override in dummy dashboard**
- **Data logging** for traceability and analysis

## 5. How to Use This Project
For setup instructions, usage details, and troubleshooting, please refer to the [User Manual](USER_MANUAL.md) and the main [README](README.md) in the project root. 