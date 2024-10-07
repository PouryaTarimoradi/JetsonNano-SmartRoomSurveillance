import cv2
import os
from datetime import datetime
import time  # To use the sleep function

# Define the camera (index 1 is used because cv2.VideoCapture(0) is not correct for the Logitech camera)
camera = cv2.VideoCapture(1)

# Check if the camera opened correctly
if not camera.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Set camera resolution to 320x240
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Give the camera some time to adjust (1 second sleep)
time.sleep(0.5)

# Define a directory to save captured images
save_dir = os.path.join(os.path.expanduser("~"), "pyProject/1-capture_image/captured_images")
os.makedirs(save_dir, exist_ok=True)

# Capture the image
ret, frame = camera.read()
if ret:
    # Save the image with a timestamp
    img_name = os.path.join(save_dir, f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    cv2.imwrite(img_name, frame)
    print(f"Image saved: {img_name}")
else:
    print("Error: Failed to capture image.")

# Release the camera
camera.release()
