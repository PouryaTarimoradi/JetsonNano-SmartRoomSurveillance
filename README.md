AI-Powered Smart Surveillance System with Jetson Nano
This project involves building a smart surveillance system using Jetson Nano, a Logitech Camera, and a Pan-Tilt mechanism driven by servo motors controlled via a PCA9685 PWM driver. The system captures images when someone enters the room and sends those images to a mobile phone through Telegram or WhatsApp.

Table of Contents
Project Overview
Features
Hardware Requirements
Software Requirements
Setup Instructions
System Workflow
Code Structure
Future Enhancements
Project Overview
This AI-powered surveillance system is built on the NVIDIA Jetson Nano platform. The system uses a Logitech camera for image capturing and a person detection model. The camera is mounted on a Pan-Tilt mechanism controlled by servo motors, which can adjust the camera's position based on movement in the room.

When motion is detected, the camera captures an image and sends it to the user’s mobile device through Telegram or WhatsApp, providing real-time updates on the room’s status.

Features
Real-time person detection: Detects movement when someone enters the room.
Pan-Tilt Camera Control: Uses servo motors to adjust the camera’s position for a better view.
Image capture and mobile notification: Captures images and sends them to mobile via Telegram or WhatsApp.
Integration with mobile devices: Supports sending images through both Telegram and WhatsApp using APIs.
Customizable alerts: Easily switch between Telegram and WhatsApp notifications.
Hardware Requirements
Jetson Nano (Developer Kit)
Logitech Camera
PCA9685 PWM Driver (for servo control)
Two Servo Motors (for Pan-Tilt functionality)
USB to Micro-USB cable
Power supply for Jetson Nano
Breadboard, jumper wires, etc.
Software Requirements
OS: Ubuntu 18.04
Python version: 3.6.9
Installed libraries:
OpenCV (4.5.5) for image capture and processing
PyTorch (1.10.0) and TorchVision (0.11.0) for person detection
Adafruit Blinka (5.13.0) for CircuitPython compatibility
Adafruit CircuitPython PCA9685 (3.4.15) for controlling servos
Adafruit CircuitPython ServoKit (1.3.0)
python-telegram-bot (13.12) for sending images via Telegram
Twilio (7.17.0) for sending messages via WhatsApp
Jetson.GPIO (2.0.17) for GPIO control
Setup Instructions
Step 1: Jetson Nano Setup
Install Jetson Nano and connect the power supply.
Set up a USB Camera (Logitech) and connect it to the Jetson Nano.
Configure Ubuntu 18.04 on Jetson Nano and ensure it runs with Python 3.6.9.
Step 2: Install Dependencies
bash
Copy code
sudo apt-get update
sudo apt-get install python3-pip
pip3 install opencv-python==4.5.5
pip3 install torch==1.10.0 torchvision==0.11.0a0+fa347eb
pip3 install python-telegram-bot==13.12
pip3 install twilio==7.17.0
pip3 install adafruit-circuitpython-pca9685
pip3 install adafruit-circuitpython-servokit
Step 3: Servo and PCA9685 Setup
Connect the PCA9685 PWM Driver to the Jetson Nano via the I2C bus.
Attach two servo motors to the PCA9685 and install the Pan-Tilt mechanism.
Step 4: Configure Telegram and WhatsApp API
Telegram Bot Setup
Create a bot on Telegram via BotFather and get the API Token.
Install and configure the python-telegram-bot library.
WhatsApp Integration
Create a Twilio account and configure WhatsApp messaging.
Obtain your Twilio Account SID, Auth Token, and WhatsApp number.
System Workflow
Person Detection: The system uses a PyTorch-based model to detect people entering the room.
Pan-Tilt Control: The camera moves to capture a wider range using the servo motors.
Image Capture: Once a person is detected, the Logitech camera captures an image.
Notification: The captured image is sent to the user’s mobile phone via Telegram or WhatsApp.
Code Structure
bash
Copy code
├── src
│   ├── capture_image.py          # Handles image capturing from the Logitech camera
│   ├── detect_person.py          # Detects people using a pre-trained PyTorch model
│   ├── pan_tilt_control.py       # Controls the servo motors for the camera's pan-tilt movement
│   ├── send_telegram.py          # Sends images via Telegram bot
│   ├── send_whatsapp.py          # Sends images via WhatsApp using Twilio
│   └── main.py                   # Main script to integrate person detection, image capture, and notification
├── models                        # Stores any machine learning models used for detection
├── requirements.txt              # List of required Python libraries
└── README.md                     # Documentation (this file)
Important Files:
capture_image.py: Starts the camera and captures an image when motion is detected.
detect_person.py: Runs a lightweight PyTorch model to detect people in the frame.
pan_tilt_control.py: Adjusts the camera’s position using the servo motors controlled by the PCA9685.
send_telegram.py: Sends the captured image via a Telegram bot.
send_whatsapp.py: Sends the captured image via WhatsApp using the Twilio API.
main.py: Integrates all components and runs the full surveillance system.
Future Enhancements
Video streaming: Implement a feature for real-time video streaming to the user’s mobile.
Facial recognition: Add face detection to recognize known individuals.
Multiple camera support: Integrate multiple cameras for wider surveillance coverage.
License
This project is licensed under the MIT License.
