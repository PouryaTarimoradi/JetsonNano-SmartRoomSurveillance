import os
import time
import cv2
import torch
from torchvision.models.detection import ssd300_vgg16
from send_telegram import send_image_via_telegram, send_message_via_telegram, stop_telegram_worker
from capture_image import initialize_camera, detect_motion
from idle_mode import initialize_idle_mode, system_active_event, exit_event, image_detection_paused
from system_stats import initialize_temperature_monitor

# Load the SSD model
ssd_model = ssd300_vgg16(pretrained=True)
ssd_model.eval()  # Set to evaluation mode

# Set resolution for motion detection
MOTION_DETECTION_RESOLUTION = (320, 240)  # Lower resolution for faster processing

def detect_person(frame, confidence_threshold=0.5):
    """Run SSD detection on a frame and check if a person is detected."""
    transform = torch.nn.functional.interpolate  # Optional: Preprocess the image if needed
    image_tensor = torch.from_numpy(frame).permute(2, 0, 1).float().unsqueeze(0) / 255.0  # Normalize
    predictions = ssd_model(image_tensor)[0]

    person_detected = False
    for box, label, score in zip(predictions['boxes'], predictions['labels'], predictions['scores']):
        if label == 1 and score > confidence_threshold:  # Assuming '1' is the class ID for 'person'
            person_detected = True
            break

    return person_detected, predictions

def main():
    # Initialize the idle mode listener
    initialize_idle_mode()

    # Initialize the temperature monitor
    initialize_temperature_monitor()

    # Initialize the camera
    cap = initialize_camera()
    time.sleep(2)  # Allow the camera to warm up

    # Capture the first frame for motion detection
    ret, previous_frame = cap.read()
    if not ret:
        print("Failed to grab the initial frame")
        send_message_via_telegram("Failed to initialize the camera. Please check the setup and restart.", with_buttons=True)
        return

    # Resize the first frame to the lower resolution for motion detection
    previous_frame_low_res = cv2.resize(previous_frame, MOTION_DETECTION_RESOLUTION)

    # Send initialization message via Telegram with buttons
    initialization_message = (
        "System initialized and ready.\n"
        "Please press the appropriate button to control the system."
    )
    send_message_via_telegram(initialization_message, with_buttons=True)
    print("Initialization message sent to Telegram with buttons.")

    try:
        while True:
            if exit_event.is_set():  # Check if the exit signal is set
                print("Exit signal received. Shutting down...")
                break  # Break the loop to exit

            if system_active_event.is_set() and not image_detection_paused.is_set():
                # System is active and image detection is not paused; perform motion detection
                ret, current_frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    send_message_via_telegram("Camera error: Failed to grab frame. System is stopping.", with_buttons=True)
                    break

                # Resize the current frame for motion detection
                current_frame_low_res = cv2.resize(current_frame, MOTION_DETECTION_RESOLUTION)

                # Perform motion detection on the lower-resolution frames
                if detect_motion(previous_frame_low_res, current_frame_low_res):
                    print("Motion detected, checking for person detection...")

                    # Save the image and perform person detection with SSD (on full resolution)
                    timestamp = time.strftime("%Y%m%d--%H%M%S")
                    save_path = os.path.join("processed_images", f"image_{timestamp}.jpg")
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                    # Run SSD detection on the full-resolution current frame
                    person_detected, detections = detect_person(current_frame)

                    if person_detected:
                        print("Person detected, drawing bounding boxes...")

                        # Draw bounding boxes and save the processed image
                        for box, label, score in zip(detections['boxes'], detections['labels'], detections['scores']):
                            if label == 1 and score > 0.5:  # Assuming '1' is the class ID for 'person'
                                x1, y1, x2, y2 = map(int, box)
                                cv2.rectangle(current_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(current_frame, f"Person: {score:.2f}", (x1, y1 - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Save the processed frame with bounding boxes
                        cv2.imwrite(save_path, current_frame)
                        print(f"Processed image saved with bounding boxes at {save_path}")

                        # Prepare detection details (confidence scores) for Telegram
                        detection_data = "\n".join(
                            [f"Person detected with confidence: {score:.2f}"
                             for box, label, score in zip(detections['boxes'], detections['labels'], detections['scores'])
                             if label == 1 and score > 0.5])

                        # Send image and detection details to Telegram
                        send_image_via_telegram(save_path, detection_data=detection_data)

                    # Avoid continuous capturing
                    time.sleep(2)

                # Update the previous frame for motion detection
                previous_frame_low_res = current_frame_low_res

                # Adding a small delay to reduce CPU usage
                cv2.waitKey(30)
            else:
                # System is idle or image detection is paused; skip motion detection
                print("System is idle or image detection is paused.")
                time.sleep(1)  # Sleep for a while before checking again

    except KeyboardInterrupt:
        print("Process interrupted. Exiting...")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        stop_telegram_worker()  # Stop the Telegram worker thread

if __name__ == "__main__":
    main()
