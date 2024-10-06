# Capture Image with Logitech Camera

This module captures images using the Logitech camera connected to the Jetson Nano. It allows you to view the live camera feed and capture images when prompted.

## Overview

This script initializes the camera, displays a live camera feed, and allows users to capture images by pressing the 'c' key. It saves the images in a timestamped format inside a specific directory. The script also allows the user to exit the camera feed by pressing the 'q' key.

### Code Walkthrough

#### 1. Importing Libraries
```python
import cv2
import time
import os
```
- `cv2`: OpenCV library used for video and image processing.
- `time`: Used for generating timestamps to save images with unique filenames.
- `os`: Provides functions for interacting with the operating system, like checking if directories exist or creating new directories.

#### 2. Initializing the Camera
```python
camera = cv2.VideoCapture(1)
```
This line initializes the Logitech camera. The argument `1` specifies the device ID for the camera. If your Jetson Nano has multiple cameras, you can change this index based on the camera setup.

#### 3. Defining the Directory for Captured Images
```python
save_dir = '1-capture_image'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
```
- `save_dir`: This string specifies the directory where captured images will be stored. In this case, the directory is named `1-capture_image`.
- The script checks if the directory exists with `os.path.exists(save_dir)`, and if it doesn't, it creates the directory using `os.makedirs(save_dir)`.

#### 4. Capture and Save Image Function
```python
def capture_image():
    ret, frame = camera.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = os.path.join(save_dir, f"image_{timestamp}.jpg")
        cv2.imwrite(file_path, frame)
        print(f"Image saved: {file_path}")
    else:
        print("Failed to capture image")
```
- `camera.read()`: Reads a single frame from the camera. It returns two values: `ret` (a boolean indicating if the frame was captured successfully) and `frame` (the actual image frame).
- If `ret` is `True`, meaning the frame was successfully captured, the script generates a timestamp using `time.strftime("%Y%m%d-%H%M%S")`. This ensures that each captured image has a unique filename.
- `cv2.imwrite(file_path, frame)`: Saves the captured frame (image) to the specified path. The image is saved in .jpg format, with the filename `image_<timestamp>.jpg`.
- If the frame capture fails, the script prints an error message: "Failed to capture image".

#### 5. Main Loop for Camera Feed and Input Handling
```python
if __name__ == "__main__":
    print("Camera is warming up...")
    time.sleep(2)
    
    print("Press 'q' to exit.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Camera Feed", frame)
        key = cv2.waitKey(33)
        
        if key == ord('c'):
            capture_image()
        if key == ord('q'):
            print("Exiting the program.")
            break
```
- Camera Warm-up: The script prints a message and waits for 2 seconds to allow the camera to warm up with `time.sleep(2)`. This helps avoid capturing incomplete or faulty frames right after initialization.
- Main Loop: The script enters a `while True` loop, where it continuously reads frames from the camera.
- `camera.read()`: Reads a frame from the camera. If it fails to capture a frame (`ret == False`), the script exits the loop with an error message.
- Displaying the Feed: The frame is displayed in a window titled "Camera Feed" using `cv2.imshow()`.
- Handling Key Presses: The script checks for key inputs:
  - `cv2.waitKey(33)`: Waits for 33 milliseconds (roughly 30 frames per second) for a key press.
  - If the 'c' key is pressed (`ord('c')`), it calls the `capture_image()` function to capture and save an image.
  - If the 'q' key is pressed (`ord('q')`), the script prints a message and breaks out of the loop, exiting the program.

#### 6. Cleaning Up Resources
```python
camera.release()
cv2.destroyAllWindows()
```
- `camera.release()`: Releases the camera resource when the program exits.
- `cv2.destroyAllWindows()`: Closes any OpenCV windows that were opened during the program execution.

## How to Run the Script

1. Ensure the Logitech camera is connected to your Jetson Nano.
2. Open a terminal and navigate to the directory containing `capture_image.py`.
3. Run the script:
   ```bash
   python3 capture_image.py
   ```
4. The live camera feed will appear in a new window.
5. Press:
   - 'c': To capture an image. The image will be saved in the `1-capture_image/` directory.
   - 'q': To quit the program.

## Dependencies

- OpenCV (version 4.5.5)
- Python 3.6.9 (as per your Jetson Nano setup)

## Notes

- The directory `1-capture_image/` will store all the captured images.
- Ensure you have OpenCV installed:
  ```bash
  sudo apt-get install python3-opencv
  ```
- You can adjust the camera device ID (currently set to 1) if needed, depending on the camera setup.
