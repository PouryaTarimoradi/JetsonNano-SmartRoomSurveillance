# Fan Control

## Overview
This module manages the Jetson Nano's cooling system by monitoring the device's temperature and controlling the fan accordingly. It ensures the system operates within safe temperature limits, enhancing performance and longevity.

## Features
- Monitors the Jetson Nano's CPU and GPU temperature.
- Automatically turns the fan on when the temperature exceeds a specified threshold.
- Turns the fan off once the temperature drops below the threshold.

## How It Works
The `fan_control.py` script uses the `Jetson.GPIO` library to control the GPIO pin connected to the fan. Here's the process:

1. **Temperature Monitoring**:
   - Reads the system's temperature from the Jetson Nano's onboard sensors.
   - The temperature is retrieved using files located in `/sys/class/thermal`.

2. **Threshold-Based Fan Control**:
   - If the temperature exceeds the **upper threshold** (e.g., 60°C), the fan is turned on.
   - If the temperature drops below the **lower threshold** (e.g., 50°C), the fan is turned off.

3. **GPIO Pin Management**:
   - Configures a specific GPIO pin as output for controlling the fan's power supply.

4. **Logging**:
   - Tracks temperature readings and fan status changes for debugging and monitoring.

## Setup Instructions
1. Install the required library:
   ```bash
   pip3 install Jetson.GPIO
   ```
2. Connect the fan to the appropriate GPIO pin on the Jetson Nano.
3. Update the GPIO pin configuration in the script:
   ```python
   FAN_GPIO_PIN = 18  # Update based on your connection
   ```

## Usage
Run the script to monitor the temperature and control the fan:
```bash
python3 fan_control.py
```

## Code Snippet Breakdown
### GPIO Setup
```python
import Jetson.GPIO as GPIO

# Pin setup
FAN_GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_GPIO_PIN, GPIO.OUT)
```
This initializes the GPIO pin for fan control.

### Temperature Monitoring
```python
def get_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        cpu_temp = int(file.read()) / 1000.0  # Convert from millidegree Celsius
    return cpu_temp
```
Reads the CPU temperature from the Jetson Nano's thermal sensors.

### Fan Control Logic
```python
UPPER_THRESHOLD = 60.0  # Turn fan on
LOWER_THRESHOLD = 50.0  # Turn fan off

def control_fan(temp):
    if temp > UPPER_THRESHOLD:
        GPIO.output(FAN_GPIO_PIN, GPIO.HIGH)  # Turn fan on
    elif temp < LOWER_THRESHOLD:
        GPIO.output(FAN_GPIO_PIN, GPIO.LOW)   # Turn fan off
```
Controls the fan based on temperature thresholds.

### Main Loop
```python
try:
    while True:
        temp = get_temperature()
        control_fan(temp)
        print(f"Temperature: {temp}°C")
        time.sleep(5)  # Check temperature every 5 seconds
except KeyboardInterrupt:
    GPIO.cleanup()
```
Continuously monitors the temperature and adjusts the fan accordingly.

### Cleanup
```python
GPIO.cleanup()
```
Ensures the GPIO pin is released when the script exits.

## Example Output
- **Console Logs**:
  ```
  Temperature: 62.5°C - Fan ON
  Temperature: 48.0°C - Fan OFF
  ```

## Configuration Example
- **Thresholds**: Adjust the temperature thresholds to suit your environment.
- **GPIO Pin**: Update the GPIO pin number based on your setup.

## Dependencies
- Python 3.6 or higher
- Jetson.GPIO library

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.


