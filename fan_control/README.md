# Fan Control

## Overview
This module manages the Jetson Nano's cooling system by monitoring the device's temperature and controlling the fan accordingly. It ensures the system operates within safe temperature limits, enhancing performance and longevity.

## Features
- Monitors the Jetson Nano's CPU temperature.
- Automatically turns the fan on when the temperature exceeds a specified threshold.
- Turns the fan off once the temperature drops below the threshold.
- Provides console feedback on the current temperature and fan status.

## How It Works
The `fan_control.py` script directly interacts with the Jetson Nano's system files and uses shell commands to control the fan via the PWM interface. Here's the process:

1. **Temperature Monitoring**:
   - Reads the system's temperature from the Jetson Nano's onboard sensors located in `/sys/class/thermal/thermal_zone0/temp`.
   - Converts the raw temperature data (in millidegrees Celsius) into Celsius for readability.

2. **Threshold-Based Fan Control**:
   - If the temperature exceeds the **upper threshold** (60°C), the fan is turned on by setting the PWM value to 255 (maximum speed).
   - If the temperature drops below the **lower threshold** (50°C), the fan is turned off by setting the PWM value to 0.

3. **Shell Command Execution**:
   - The script uses the `os.system()` function to send commands that adjust the fan's PWM values.

## Setup Instructions
1. Ensure the Jetson Nano is equipped with a PWM-controlled fan.
2. Confirm that the fan is connected to the appropriate power and control pins.
3. The fan control interface should be available at `/sys/devices/pwm-fan/target_pwm`. Verify this by running:
   ```bash
   ls /sys/devices/pwm-fan/
   ```
4. No additional Python libraries are required for this script.

## Usage
Run the script to monitor the temperature and control the fan:
```bash
python3 fan_control.py
```

## Code Snippet Breakdown
### Temperature Monitoring
```python
def get_temperature():
    temp_file = "/sys/class/thermal/thermal_zone0/temp"  # Path to the temperature file
    try:
        with open(temp_file, "r") as f:
            temp_str = f.read()
            temp_C = int(temp_str) / 1000.0  # Convert from millidegree Celsius
            return temp_C
    except FileNotFoundError:
        print(f"Temperature file {temp_file} not found")
        return None
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None
```
This function reads the CPU temperature from the system's thermal zone file, handles potential errors, and converts the value to Celsius.

### Fan Control Logic
```python
def control_fan(temperature):
    fan_on_temp = 60.0  # Temperature to turn the fan on (in Celsius)
    fan_off_temp = 50.0  # Temperature to turn the fan off (in Celsius)

    if temperature >= fan_on_temp:
        # Turn on the fan
        os.system("echo 255 > /sys/devices/pwm-fan/target_pwm")  # Max PWM value (255) for full speed
        print("Fan ON")
    elif temperature <= fan_off_temp:
        # Turn off the fan
        os.system("echo 0 > /sys/devices/pwm-fan/target_pwm")  # 0 PWM value to turn off
        print("Fan OFF")
```
This function adjusts the fan's PWM value based on the temperature thresholds.

### Main Execution
```python
# Monitor and control fan based on temperature
temperature = get_temperature()
if temperature is not None:
    print(f"CPU Temperature: {temperature:.2f}°C")
    control_fan(temperature)
```
The script retrieves the current temperature and calls the `control_fan` function to adjust the fan accordingly.

## Example Output
- **Console Logs**:
  ```
  CPU Temperature: 62.50°C
  Fan ON
  CPU Temperature: 48.00°C
  Fan OFF
  ```

## Configuration Example
- **Thresholds**: Adjust the `fan_on_temp` and `fan_off_temp` variables in the script to suit your environment.

## Dependencies
- Python 3.6 or higher
- Access to `/sys/devices/pwm-fan/target_pwm` for fan control

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

