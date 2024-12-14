# AI-Powered Surveillance System

## Overview
The **AI-Powered Surveillance System** is a robust application that uses `main.py` as the entry point to manage and execute its core functionalities. The system employs computer vision and deep learning techniques to detect motion, identify persons, and send real-time alerts via Telegram. The `main.py` script integrates multiple functionalities, including motion detection, object detection using SSD, and Telegram notifications.

## Key Features
- **Motion Detection**: Detects motion efficiently using low-resolution frames.
- **Person Detection**: Leverages an SSD model for real-time detection of persons with high confidence.
- **Real-Time Notifications**: Sends processed images and detection details to Telegram.
- **Dynamic Image Processing**: Annotates images with bounding boxes and confidence scores.
- **Graceful System Control**: Manages system states (e.g., active, idle) and handles termination safely.

## How It Works
### 1. System Initialization
The script initializes the following components:
- **Camera**: Captures the first frame to set up motion detection.
- **Telegram Bot**: Sends an initialization message with control buttons.
- **Idle Mode and Temperature Monitor**: Starts listeners for system commands and temperature monitoring.

#### Example Code
```python
cap = initialize_camera()
time.sleep(2)  # Allow the camera to warm up
ret, previous_frame = cap.read()
if not ret:
    send_message_via_telegram("Failed to initialize the camera. Please restart.", with_buttons=True)
    return
```
Initializes the camera and prepares the first frame for motion detection.

---

### 2. Motion Detection
Motion detection operates on low-resolution frames to reduce computation time. It compares consecutive frames to detect motion.

#### Example Code
```python
if detect_motion(previous_frame_low_res, current_frame_low_res):
    print("Motion detected, checking for person detection...")
```
Triggers further processing when motion is detected.

---

### 3. Person Detection
When motion is detected, the system processes full-resolution frames using the SSD model to identify persons.

#### SSD Model Setup
```python
ssd_model = ssd300_vgg16(pretrained=True)
ssd_model.eval()  # Set the model to evaluation mode
```
The pre-trained SSD model is loaded for person detection.

#### Person Detection Workflow
```python
def detect_person(frame, confidence_threshold=0.5):
    image_tensor = torch.from_numpy(frame).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    predictions = ssd_model(image_tensor)[0]

    for box, label, score in zip(predictions['boxes'], predictions['labels'], predictions['scores']):
        if label == 1 and score > confidence_threshold:
            return True, predictions
    return False, predictions
```
Processes the frame and returns detection results with bounding boxes and scores.

---

### 4. Image Annotation and Notifications
When a person is detected, bounding boxes and confidence scores are drawn on the image. The annotated image is saved and sent to Telegram along with detection details.

#### Example Code
```python
cv2.rectangle(current_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.putText(current_frame, f"Person: {score:.2f}", (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
```
Annotates the frame with bounding boxes and confidence scores.

---

### 5. Telegram Notifications
The processed image and detection details are sent to the user via Telegram.

#### Example Code
```python
send_image_via_telegram(save_path, detection_data=detection_data)
```
Sends the annotated image and detection details.

---

### 6. Graceful Shutdown
Handles safe termination of the system upon receiving an exit signal.

#### Example Code
```python
if exit_event.is_set():
    print("Exit signal received. Shutting down...")
    break
```
Safely terminates the script when the exit signal is triggered.

## Example Output
- **Console Logs**:
  ```
  System initialized and ready.
  Motion detected, checking for person detection...
  Person detected, drawing bounding boxes...
  Processed image saved at processed_images/image_20240101--123456.jpg
  ```

- **Telegram Notifications**:
  ```
  Initialization complete. Use the buttons to control the system.
  Person detected with confidence: 0.89
  ```

## Usage
### Running the System
To start the surveillance system, execute:
```bash
python3 main.py
```

### Customization
- Modify `MOTION_DETECTION_RESOLUTION` to adjust the resolution for motion detection.
- Update confidence thresholds in the `detect_person` function to fine-tune person detection sensitivity.
- Change the SSD model to another supported detection model if required.

## Troubleshooting
- **Camera Initialization Error**:
  Ensure the camera is connected and accessible.
- **Telegram Notifications Not Sent**:
  Verify the bot token and Chat ID in `bot_config.py`.
- **SSD Model Issues**:
  Ensure PyTorch and Torchvision are installed correctly.

## Dependencies
- Python 3.6 or higher
- `OpenCV` for image processing
- `PyTorch` and `Torchvision` for SSD-based person detection
- `python-telegram-bot` for Telegram integration

## License
This project is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

