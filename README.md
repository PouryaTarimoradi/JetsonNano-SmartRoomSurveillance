# Camera Security System with Jetson Nano
![photo_2024-12-14_20-53-26](https://github.com/user-attachments/assets/821170ea-0271-490b-8996-3f2e99ac1788)

## Overview
This project is an AI-powered surveillance system built on the NVIDIA Jetson Nano platform. It integrates motion detection, object recognition, and real-time notification capabilities, designed to detect and alert users when someone enters a monitored space. Captured images are sent to a Telegram bot for easy access.

## Features
- **Motion Detection**: Detects changes in the environment using OpenCV.
- **Object Detection**: Identifies if the detected motion corresponds to a person using SSD.
- **Real-Time Notifications**: Sends captured images to a Telegram bot.
- **Fan Control**: Manages the Jetson Nano’s fan based on temperature.
- **System Monitoring**: Displays CPU, GPU usage, and temperature stats.
- **Idle Mode**: Allows the system to pause and resume operations via Telegram commands.
![Screenshot 2024-12-26 155432](https://github.com/user-attachments/assets/4dd81337-e184-426e-8087-aa7324674fe8)


![Screenshot 2024-12-26 155306](https://github.com/user-attachments/assets/f3054a11-d94a-412a-9d45-2c0fe93a85ee)

![Screenshot 2024-12-26 155532](https://github.com/user-attachments/assets/e231042c-9b33-4afd-8e8b-2dd36940b398)


  

## Project Structure
```
CameraSecuritySystem/
├── ChatID_BotToken/
│   ├── ChatID_BotToken.py             # Stores the Telegram Bot token and chat ID
│   ├── README.md                      # Documentation for ChatID_BotToken
├── bot_config/
│   ├── bot_config.py                  # Configuration for Telegram bot commands
│   ├── README.md                      # Documentation for bot_config
├── capture_image/
│   ├── capture_image.py               # Handles motion detection and image capture
│   ├── README.md                      # Documentation for capture_image
├── send_telegram/
│   ├── send_telegram.py               # Sends images and commands to Telegram bot
│   ├── README.md                      # Documentation for send_telegram
├── system_stats/
│   ├── system_stats.py                # Retrieves system stats (CPU, GPU, temperature)
│   ├── README.md                      # Documentation for system_stats
├── idle_mode/
│   ├── idle_mode.py                   # Implements idle mode for pausing/resuming operations
│   ├── README.md
├── main/
│   ├── main.py                        # Main script to integrate all modules
│   ├── README.md                      # Documentation for idle_mode                       
├── requirements.txt                   # Python dependencies
├── LICENSE                            # Project license
└── README.md                          # Main project documentation
```

## Hardware Requirements
- NVIDIA Jetson Nano (4GB Developer Kit)
- Logitech Camera or similar USB camera
- Power supply for Jetson Nano
- MicroSD card (32GB or higher) for OS
- USB to Micro-USB cable

## Software Requirements
- **Operating System**: Ubuntu 18.04 or JetPack 4.6
- **Python Version**: 3.6.9
- **Installed Libraries**:
  - OpenCV: `4.5.5`
  - PyTorch: `1.10.0`
  - TorchVision: `0.11.0`
  - python-telegram-bot: `13.12`

## Installation

### Step 1: Update the System
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### Step 2: Install Python and Pip
Ensure Python 3.6.9 is installed:
```bash
sudo apt-get install python3.6 python3-pip -y
```

### Step 3: Install Required Libraries
Install the libraries listed in `requirements.txt`:
```bash
pip3 install -r requirements.txt
```
Or install them individually:
```bash
pip3 install opencv-python==4.5.5
pip3 install torch==1.10.0 torchvision==0.11.0
pip3 install python-telegram-bot==13.12
```

### Step 4: Set Up Telegram Bot
1. Create a Telegram bot using [BotFather](https://core.telegram.org/bots#botfather).
2. Save the bot token and chat ID in `ChatID_BotToken.py`.
3. Verify the bot configuration using the `bot_config.py` script.

## Running the Project

### How to Start
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/CameraSecuritySystem.git
  
   ```

2. **Run the Main Script**:
   ```bash
   python3 main.py
   ```

3. **Use Telegram Commands**:
   - **Start**: Begin motion detection and notifications.
   - **Stop**: Pause detection and notifications.
   - **Status**: Check the current system status (active or idle).
   - **Clean**: Delete all previous Telegram messages from the bot.
   - **System**: Retrieve CPU, GPU, and temperature stats.
   - **Exit**: Shut down the system.

### How to Use
- **Monitor the Environment**:
  Once started, the system will detect motion and send a notification if a person is identified.
- **Manage the System**:
  Use Telegram commands to pause, resume, or stop the system as needed.

## Example Outputs
- **Telegram Bot UI**:
  ```
  Initialization complete. Use the buttons to control the system.
  Motion detected. Person detected with confidence: 0.89
  ```

- **Captured Image**:
  The system saves captured images with bounding boxes in the `processed_images/` directory and sends them via Telegram.

## Future Enhancements
- Add real-time video streaming capabilities.
- Integrate facial recognition to identify known individuals.
- Support multiple cameras for wider surveillance.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

