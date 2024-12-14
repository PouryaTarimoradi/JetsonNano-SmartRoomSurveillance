# Capture Image

## Overview
This module is responsible for detecting motion in the environment using OpenCV and capturing images when changes are detected. The captured images are then passed to other modules, such as object detection or notification modules. This script ensures real-time surveillance by constantly monitoring and reacting to motion in the field of view.

## Features
- **Motion Detection**: Identifies changes in the environment using frame-by-frame analysis.
- **Image Capture**: Captures high-resolution images when motion is detected.
- **Seamless Integration**: Interfaces with object detection and notification modules for further processing.
- **Logging**: Tracks motion events and saves logs for analysis.
- **Configurable Sensitivity**: Allows adjustment of motion detection sensitivity thresholds.
- **Supports Multiple Cameras**: Can handle multiple camera inputs with slight modifications.

## How It Works
The `capture_image.py` script uses OpenCV to analyze live camera feed in real-time. Here's a detailed explanation of its functionality:

1. **Initialize Camera**:
   - The script initializes the camera using OpenCV’s `VideoCapture`.
   - The camera index is set to `0` (default USB camera).

2. **Read Frames**:
   - Continuously captures frames from the camera.
   - Converts frames to grayscale for easier motion analysis.

3. **Detect Motion**:
   - Uses frame subtraction to detect significant changes between consecutive frames.
   - Applies thresholding to isolate motion regions.

4. **Capture Images**:
   - If motion is detected, saves the current frame as an image file.
   - Stores the image in a predefined directory for further processing.
   - Logs the event details, such as timestamp and location.
   - Checks for file management, ensuring the directory does not exceed a predefined limit of images.

5. **Display Feed**:
   - Displays the live feed for real-time monitoring with bounding boxes around motion regions.

6. **Configuration Options**:
   - Includes adjustable settings for motion sensitivity, capture intervals, and frame resizing.
   - Allows enabling/disabling logging and debug display via configuration file.

7. **Threaded Operations**:
   - Implements threading to manage image saving and motion detection separately, ensuring smooth operation without frame drops.

8. **Exit Safely**:
   - Releases the camera and closes all OpenCV windows when the script is stopped.

## Setup Instructions
1. Ensure the camera is connected to the Jetson Nano via USB.
2. Install OpenCV if not already installed:
   ```bash
   pip3 install opencv-python==4.5.5
   ```
3. Update the `capture_image.py` script to set the correct save directory for captured images.
4. (Optional) Modify sensitivity and other settings in the configuration section of the script.

## Usage
Run the script to start motion detection and image capture:
```bash
python3 capture_image.py
```

## Code Snippet Breakdown
### Initialization
```python
import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Error: Camera not accessible")
    exit()
```
This initializes the camera. If the camera cannot be accessed, the script exits with an error message.

### Frame Reading and Processing
```python
ret, frame = camera.read()
if not ret:
    break

# Convert the frame to grayscale
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
Reads frames continuously and converts them to grayscale for motion detection.

### Motion Detection
```python
# Compute the difference between frames
diff = cv2.absdiff(previous_frame, gray_frame)
_, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

# Check for motion
if cv2.countNonZero(thresh) > motion_threshold:
    print("Motion detected!")
    cv2.imwrite(f"{save_directory}/captured_image_{timestamp}.jpg", frame)
    log_event(f"Motion detected at {timestamp}")
```
Uses frame subtraction to detect changes and saves an image if motion is detected. Logs the event for analysis.

### Threaded Image Saving
```python
from threading import Thread

def save_image_threaded(image, path):
    Thread(target=cv2.imwrite, args=(path, image)).start()

save_image_threaded(frame, f"{save_directory}/captured_image_{timestamp}.jpg")
```
Ensures image saving does not block motion detection by using a separate thread.

### Cleanup
```python
camera.release()
cv2.destroyAllWindows()
```
Releases the camera and closes all OpenCV windows on exit.

## Example Output
- Captured images are saved in the specified directory with unique timestamps.
- The console displays messages like "Motion detected!".
- A log file records all motion events with timestamps.

## Configuration Example
A sample JSON configuration for sensitivity and other settings:
```json
{
  "motion_threshold": 500,
  "save_directory": "./captured_images",
  "camera_index": 0,
  "enable_logging": true,
  "debug_display": true
}
```

## Dependencies
- Python 3.6 or higher
- OpenCV (version 4.5.5)
- Threading (built-in Python module)

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

