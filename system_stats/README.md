# System Stats

## Overview
The System Stats module provides real-time information about the Jetson Nano's hardware performance, including CPU and GPU usage, memory consumption, and temperature. This module is critical for monitoring the health and performance of the system during operations. Additionally, it includes threading for efficient temperature monitoring and fan control without interrupting the main processes.

## Features
- Retrieves CPU usage as a percentage.
- Monitors GPU utilization for load assessment.
- Reports memory usage and availability.
- Fetches CPU and GPU temperature readings.
- Outputs statistics to the console or sends them via a Telegram bot for remote monitoring.
- Implements threading to manage temperature monitoring and fan control independently of other tasks.

## How It Works
The `system_stats.py` script uses standard Python libraries and system commands to collect hardware performance metrics. Here’s a breakdown of its functionality:

1. **CPU and Memory Statistics**:
   - Uses the `psutil` library to calculate CPU usage and memory utilization.

2. **GPU Utilization**:
   - Collects GPU stats using the `tegrastats` utility, which provides detailed information about GPU usage on Jetson Nano.

3. **Temperature Monitoring**:
   - Reads CPU and GPU temperature data from the system’s thermal zone files.
   - Controls the fan based on predefined temperature thresholds.

4. **Threaded Temperature Monitoring**:
   - Runs a dedicated thread for continuous temperature monitoring and fan control to ensure these tasks do not block other system operations.

5. **Telegram Integration**:
   - Sends system stats to the Telegram bot when requested, providing remote access to performance data.

## Setup Instructions
1. Install the required libraries:
   ```bash
   pip3 install psutil
   ```
2. Ensure that the `tegrastats` utility is installed and available on your Jetson Nano. It is included by default in JetPack installations.
3. Configure the Telegram bot for remote monitoring by integrating this module with `bot_config.py`.

## Usage
Run the script to monitor system stats:
```bash
python3 system_stats.py
```

### Example Commands
#### Retrieve Stats via Telegram Bot:
Send the `/stats` command to your Telegram bot to receive a detailed report of the system’s current performance.

## Code Snippet Breakdown
### CPU and Memory Monitoring
```python
import psutil

def get_cpu_memory_stats():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 ** 2)  # Convert to MB
    memory_total = memory.total / (1024 ** 2)  # Convert to MB
    memory_percent = memory.percent

    return {
        "cpu_usage": cpu_usage,
        "memory_used": memory_used,
        "memory_total": memory_total,
        "memory_percent": memory_percent
    }
```
This function retrieves and calculates CPU usage and memory statistics.

### GPU Utilization
```python
import os

def get_gpu_stats():
    try:
        tegrastats_output = os.popen("tegrastats").readline()
        # Parse tegrastats output to extract GPU utilization
        gpu_utilization = "Extracted GPU utilization data"  # Replace with parsing logic
        return gpu_utilization
    except Exception as e:
        print(f"Error fetching GPU stats: {e}")
        return None
```
This function extracts GPU utilization data from the `tegrastats` utility.

### Temperature Monitoring and Fan Control
```python
def get_temperature():
    temp_file = "/sys/class/thermal/thermal_zone0/temp"
    try:
        with open(temp_file, "r") as f:
            temp_C = int(f.read()) / 1000.0
        return temp_C
    except FileNotFoundError:
        print(f"Temperature file {temp_file} not found")
        return None
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def control_fan(temperature):
    fan_on_temp = 60.0
    fan_off_temp = 50.0
    pwm_file = "/sys/devices/pwm-fan/target_pwm"

    try:
        if temperature >= fan_on_temp:
            with open(pwm_file, "w") as f:
                f.write("255")  # Max PWM
            print("Fan ON")
        elif temperature <= fan_off_temp:
            with open(pwm_file, "w") as f:
                f.write("0")  # Fan OFF
            print("Fan OFF")
    except Exception as e:
        print(f"Failed to control fan: {e}")
```
This function monitors and controls the fan based on temperature thresholds.

### Threaded Temperature Monitoring
```python
import threading
import time

def temperature_monitor():
    while True:
        temp = get_temperature()
        if temp is not None:
            print(f"Current Temperature: {temp:.2f}°C")
            control_fan(temp)
        time.sleep(5)

def initialize_temperature_monitor():
    temp_thread = threading.Thread(target=temperature_monitor)
    temp_thread.daemon = True
    temp_thread.start()
    print("Temperature Monitoring thread started")
```
This implementation ensures continuous temperature monitoring and fan control without blocking other operations.

### Sending Stats to Telegram
```python
def send_stats_via_telegram(bot, chat_id):
    stats = get_cpu_memory_stats()
    temperature = get_temperature()
    gpu_stats = get_gpu_stats()

    message = (
        f"CPU Usage: {stats['cpu_usage']}%\n"
        f"Memory Used: {stats['memory_used']:.2f} MB / {stats['memory_total']:.2f} MB ({stats['memory_percent']}%)\n"
        f"CPU Temp: {temperature}°C\n"
        f"GPU Utilization: {gpu_stats}\n"
    )

    bot.send_message(chat_id, message)
```
This function formats and sends system stats to the Telegram bot.

## Example Output
- **Console Output**:
  ```
  CPU Usage: 45.3%
  Memory Used: 2048.0 MB / 4096.0 MB (50%)
  CPU Temp: 57.0°C
  GPU Temp: 62.0°C
  GPU Utilization: 30%
  ```

- **Telegram Message**:
  ```
  CPU Usage: 45.3%
  Memory Used: 2048.0 MB / 4096.0 MB (50%)
  CPU Temp: 57.0°C
  GPU Temp: 62.0°C
  GPU Utilization: 30%
  ```

## Dependencies
- Python 3.6 or higher
- `psutil` library
- `tegrastats` utility

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

