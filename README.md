# Smart Oven Subsystem

A modular, real-time temperature control system for ovens, featuring sensor feedback, PID control, safety logic, and a web dashboard. Includes both hardware and dummy simulation modes for development and testing.

## Features
- Real-time temperature sensing and control
- PID tuning and simulation
- Safety shutoff for overheat and sensor errors (fault detection logic: if sensor reads NaN or temp > 70°C → shutoff)
- Web dashboard for monitoring and control
- Data logging to CSV
- Dummy mode for hardware-free testing
- **Actuator (PWM) graph and setpoint override in dummy dashboard**

## Folder Structure
- `hardware/` — Schematics and setup photos
- `simulation/` — Simulink PID model
- `firmware/` — Python control logic
- `dashboard/` — Web UI (Streamlit)
- `data/` — CSV logs
- `smart-oven-subsystem-demo/` — Dummy version for testing

## Quick Start
See [USER_MANUAL.md](USER_MANUAL.md) for detailed setup and usage instructions.

- The dummy dashboard now allows setpoint override and shows a PWM duty cycle graph.
- Fault detection logic is implemented: if the sensor reads NaN or temperature exceeds 70°C, the heater is shut off.

## Documentation
- [User Manual](USER_MANUAL.md)
- [Project Summary](USER_SUMMARY.md)
