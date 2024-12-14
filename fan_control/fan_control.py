import os

def get_temperature():
    temp_file = "/sys/class/thermal/thermal_zone0/temp"  # Replace with correct thermal zone
    try:
        with open(temp_file, "r") as f:
            temp_str = f.read()
            temp_C = int(temp_str) / 1000.0
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
    
    if temperature >= fan_on_temp:
        # Turn on the fan
        os.system("echo 255 > /sys/devices/pwm-fan/target_pwm")  # Max PWM value (255) for full speed
        print("Fan ON")
    elif temperature <= fan_off_temp:
        # Turn off the fan
        os.system("echo 0 > /sys/devices/pwm-fan/target_pwm")  # 0 PWM value to turn off
        print("Fan OFF")

# Monitor and control fan based on temperature
temperature = get_temperature()
if temperature is not None:
    print(f"CPU Temperature: {temperature:.2f}°C")
    control_fan(temperature)

