# Camera Capture Module

This module is designed to capture images from a Logitech camera connected to a Jetson Nano. The captured images are saved locally in a timestamped format. It uses **OpenCV** for handling the camera feed and image capturing.

## Overview

The script `capture_image.py` initializes the Logitech camera connected to the Jetson Nano, adjusts camera settings, waits for a short delay to allow the camera to stabilize, and captures an image. The image is saved in a designated folder with a unique name based on the current date and time.

### Key Features:

- **Camera Resolution:** Configurable to 640x480 for a balance between image quality and performance.
- **Sleep Delay:** A small 0.5-second pause allows the camera to adjust to the environment before capturing.
- **Image Saving:** Images are saved in the `captured_images` directory with a timestamp, ensuring unique filenames.

## Code Breakdown

### Camera Initialization

The camera is initialized using `cv2.VideoCapture()`. This function opens the camera and allows for capturing images or video streams.

```python
camera = cv2.VideoCapture(1)
```

* `1` is used as the argument because the Logitech camera is connected to `/dev/video1` (the second video device). Using `0` would open the default camera, which in this case is incorrect.

### Camera Settings

Once the camera is successfully initialized, we set the resolution to **640x480** using the following OpenCV commands:

```python
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

These properties ensure the camera captures images at this resolution, which is a good balance between quality and performance, especially for embedded systems like the Jetson Nano.

### Delay for Camera Adjustment

A short delay is introduced to allow the camera to adjust to lighting conditions or focus before capturing an image. This prevents issues like dark or blurry images.

```python
time.sleep(0.5)
```

### Capturing the Image

Once the camera has adjusted, we attempt to capture a single frame (image) using `camera.read()`:

```python
ret, frame = camera.read()
```

* `ret`: A boolean that indicates whether the capture was successful (`True`) or not (`False`).
* `frame`: The actual image captured by the camera as a matrix of pixel values.

If `ret` is `True`, the image is captured successfully, and it is saved to the filesystem.

### Saving the Image

Captured images are saved in the **captured_images** directory. The filename includes a timestamp to ensure that each captured image has a unique name:

```python
img_name = os.path.join(save_dir, f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
cv2.imwrite(img_name, frame)
```

* `datetime.now().strftime('%Y%m%d_%H%M%S')`: Generates a unique timestamp based on the current date and time (format: `YYYYMMDD_HHMMSS`).
* `cv2.imwrite()`: Writes the captured frame to a file in `.jpg` format.

### Cleanup

After the image is captured and saved, the camera is released to free up resources:

```python
camera.release()
```

## Usage Instructions

### Prerequisites

* Jetson Nano with Ubuntu 18.04.
* Logitech USB camera.
* Python 3.6.9 or higher.
* OpenCV library installed (`opencv-python` package).

### Installing OpenCV

If OpenCV is not installed, you can install it using `pip`:

```bash
pip3 install opencv-python
```

### Running the Script

1. Ensure that the camera is connected to the Jetson Nano.
2. Navigate to the `capture_image` directory:

```bash
cd ~/pyProject/capture_image
```

3. Run the Python script:

```bash
python3 capture_image.py
```

4. The captured image will be saved in the `captured_images` folder with a name according to your date and time of running the script,like:

```
image_20241006_153015.jpg
```
