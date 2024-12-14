import os
import psutil
import time
import threading
import subprocess
import re

def get_temperature():
    temp_file = "/sys/class/thermal/thermal_zone0/temp"  # Path to the temperature file
    try:
        with open(temp_file, "r") as f:
            temp_str = f.read()
            temp_C = int(temp_str) / 1000.0  # Convert from millidegrees to degrees
            return temp_C
    except FileNotFoundError:
        print(f"Temperature file {temp_file} not found")
        return None
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def control_fan(temperature):
    fan_on_temp = 60.0  # Temperature to turn the fan on (in Celsius)
    fan_off_temp = 50.0  # Temperature to turn the fan off (in Celsius)
    pwm_file = "/sys/devices/pwm-fan/target_pwm"

    try:
        if temperature >= fan_on_temp:
            # Turn on the fan at full speed
            with open(pwm_file, "w") as f:
                f.write("255")  # Max PWM value (255) for full speed
            print("Fan ON")
        elif temperature <= fan_off_temp:
            # Turn off the fan
            with open(pwm_file, "w") as f:
                f.write("0")  # PWM value 0 to turn off
            print("Fan OFF")
        else:
            # Fan state remains unchanged
            pass
    except PermissionError:
        print(f"Permission denied when writing to {pwm_file}. Try running as root or adjust permissions.")
    except Exception as e:
        print(f"Failed to control fan: {e}")

def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        print(f"Error reading CPU usage: {e}")
        return None

def get_ram_usage():
    try:
        mem = psutil.virtual_memory()
        return mem.percent
    except Exception as e:
        print(f"Error reading RAM usage: {e}")
        return None

def temperature_monitor():
    """
    This is for monitoring the system temperature and controlling the fan accordingly.
    """
    while True:
        temp = get_temperature()
        if temp is not None:
            print(f"Current Temperature: {temp:.2f}ºC")
            control_fan(temp)
        else:
            print("Unable to read temperature.")
        time.sleep(5)

def initialize_temperature_monitor():
    """
    Initializing the temperature monitor in a separate thread.
    """
    # Start temperature monitoring thread
    temp_thread = threading.Thread(target=temperature_monitor)
    temp_thread.daemon = True
    temp_thread.start()
    print("Temperature Monitoring thread started")
