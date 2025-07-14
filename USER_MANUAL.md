# Smart Oven Subsystem: User Manual

---

## 🔧 Prerequisites

- Raspberry Pi with Raspbian OS
- Python 3.7+
- Breadboard, DS18B20 sensor, 4.7kΩ resistor, optional fan/heater

---

## 📦 Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install pandas flask streamlit w1thermsensor RPi.GPIO
```

---

## 🚀 Running the Dummy Version (No Hardware Required)

1. **Navigate to the demo folder:**
   ```bash
   cd smart-oven-subsystem-demo
   ```
2. **Start the dummy controller (simulates temperature and PID):**
   ```bash
   python3 dummy_controller.py
   ```
3. **In a new terminal, launch the dummy dashboard:**
   ```bash
   streamlit run dummy_dashboard.py
   ```
4. **Open your browser and go to:**
   [http://localhost:8501](http://localhost:8501)

---

## 🔥 Running the Full System (With Hardware)

1. **Connect the DS18B20 sensor and optional fan/heater to your Raspberry Pi as per the hardware schematics.**
2. **Navigate to the firmware folder:**
   ```bash
   cd firmware
   ```
3. **Start the main controller:**
   ```bash
   sudo python3 controller.py
   ```
   > **Note:** `sudo` may be required for GPIO access.
4. **In a new terminal, launch the dashboard:**
   ```bash
   cd ../dashboard
   streamlit run app.py
   ```
5. **Open your browser and go to:**
   [http://localhost:8501](http://localhost:8501)

---

## 📊 Data Logging
- All temperature, setpoint, PWM, and safety events are logged to CSV files in the `data/` directory.

---

## 🛠 Troubleshooting
- Ensure all dependencies are installed and hardware is connected correctly.
- For sensor errors, check wiring and 1-Wire configuration on the Pi.
- For permission errors, try running with `sudo`.
- For more details, see the [README](README.md) and [USER_SUMMARY](USER_SUMMARY.md). 