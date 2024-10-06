import cv2
import time
import os

# Initialize the camera (Logitech)
camera = cv2.VideoCapture(1)

# Define the directory where captured images will be saved
save_dir = '1-capture_image'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def capture_image():
    ret, frame = camera.read()
    if ret:
        # Generate a timestamp to use in the image filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = os.path.join(save_dir, f"image_{timestamp}.jpg")
        
        # Save the captured image
        cv2.imwrite(file_path, frame)
        print(f"Image saved: {file_path}")
    else:
        print("Failed to capture image")

# Main loop
if __name__ == "__main__":
    print("Camera is warming up...")
    time.sleep(2)  # Give the camera some time to warm up
    
    print("Press 'q' to exit.")
    while True:
        # Read frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            print("Failed to grab frame")
            break

        # Show the frame in a window
        cv2.imshow("Camera Feed", frame)

        # Adding a small delay for the waitKey to correctly detect keys
        key = cv2.waitKey(33)  # Wait 33 milliseconds (~30 frames per second)
        
        # Capture image when 'c' is pressed
        if key == ord('c'):
            capture_image()
        
        # Break the loop when 'q' is pressed
        if key == ord('q'):
            print("Exiting the program.")
            break

    # Release the camera and close windows
    camera.release()
    cv2.destroyAllWindows()

