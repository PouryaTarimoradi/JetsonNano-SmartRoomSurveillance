# AI-Powered Surveillance System with Jetson Nano

## Overview
This project is an AI-powered surveillance system built on the NVIDIA Jetson Nano platform. It integrates motion detection, object recognition, and real-time notification capabilities, designed to detect and alert users when someone enters a monitored space. Captured images are sent to a Telegram bot for easy access.

## Features
- **Motion Detection**: Detects changes in the environment using OpenCV.
- **Object Detection**: Identifies if the detected motion corresponds to a person.
- **Real-Time Notifications**: Sends captured images to a Telegram bot.
- **Fan Control**: Manages the Jetson Nano’s fan based on temperature.
- **System Monitoring**: Displays CPU, GPU usage, and temperature stats.
- **Idle Mode**: Allows the system to pause and resume operations via Telegram commands.

## Project Structure
```
Pro/
├── bot_config.py                  # Configuration for the Telegram bot
├── capture_image.py               # Handles motion detection and image capture using OpenCV
├── ChatID_BotToken.py             # Stores the Telegram Bot token and chat ID
├── description.docx               # Contains the project description and requirements
├── fan_control.py                 # Manages fan speed based on Jetson Nano's temperature
├── idle_mode.py                   # Implements idle mode to pause/resume system functionality
├── main.py                        # Main script integrating all system components
├── message_ids.json               # JSON file to manage message IDs for Telegram bot cleanup
├── send_telegram.py               # Sends images and commands to Telegram bot
├── system_stats.py                # Retrieves system stats like CPU, GPU, and temperature
├── images/                        # Folder to store project-related images
│   ├── setup_diagram.png          # Diagram showing hardware setup
│   ├── telegram_ui.png            # Screenshot of the Telegram bot UI
│   ├── captured_sample.png        # Example of a captured image
│   └── fan_control_working.png    # Screenshot of fan control in action
├── requirements.txt               # Python dependencies
└── README.md                      # Main project documentation
```

## Hardware Requirements
- NVIDIA Jetson Nano (4GB Developer Kit)
- Logitech Camera
- PCA9685 PWM Driver (for servo control, optional for pan-tilt functionality)
- Power supply for Jetson Nano
- USB to Micro-USB cable
- Breadboard, jumper wires, and other electronic components

## Software Requirements
- **Operating System**: Ubuntu 18.04
- **Python Version**: 3.6.9
- **Installed Libraries**:
  - OpenCV: `4.5.5`
  - PyTorch: `1.10.0`
  - TorchVision: `0.11.0`
  - python-telegram-bot: `13.12`
  - Twilio: `7.17.0`
  - Adafruit Blinka: `5.13.0`
  - Adafruit CircuitPython PCA9685: `3.4.15`
  - Adafruit CircuitPython ServoKit: `1.3.0`
  - Jetson.GPIO: `2.0.17`

## Installation

### 1. Update the System
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### 2. Install Python and Pip
Ensure Python 3.6.9 is installed:
```bash
sudo apt-get install python3.6 python3-pip -y
```

### 3. Install Required Libraries
Install the libraries listed in `requirements.txt`:
```bash
pip3 install -r requirements.txt
```
Or install them individually:
```bash
pip3 install opencv-python==4.5.5
pip3 install torch==1.10.0 torchvision==0.11.0a0+fa347eb
pip3 install python-telegram-bot==13.12
pip3 install twilio==7.17.0
pip3 install adafruit-blinka
pip3 install adafruit-circuitpython-pca9685
pip3 install adafruit-circuitpython-servokit
pip3 install jetson-gpio
```

## Setting Up the Telegram Bot
1. Create a bot on Telegram via [BotFather](https://core.telegram.org/bots#botfather).
2. Save the bot token and chat ID in `ChatID_BotToken.py`.
3. Ensure the bot is set up to send and receive commands as outlined in `bot_config.py`.

## Running the Project
1. **Start the system**:
   Run the main script:
   ```bash
   python3 main.py
   ```
2. **Use Telegram commands**:
   - `Start`: Begin receiving motion-detected images.
   - `Stop`: Pause image detection and notifications.
   - `Status`: Check the system status.
   - `Clean`: Delete all Telegram bot images from the last 48 hours.
   - `System`: Retrieve current CPU, GPU, and temperature stats.
   - `Exit`: Stop the program entirely.

## Example Outputs
- **Telegram Bot UI**:
  ![Telegram Bot UI](images/telegram_ui.png)

- **Setup Diagram**:
  ![Setup Diagram](images/setup_diagram.png)

- **Captured Sample**:
  ![Captured Image](images/captured_sample.png)

- **Fan Control Working**:
  ![Fan Control](images/fan_control_working.png)

## Future Enhancements
- Add real-time video streaming capabilities.
- Integrate facial recognition to identify known individuals.
- Support multiple cameras for wider surveillance.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

