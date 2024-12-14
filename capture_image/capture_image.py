import cv2
import time
import os

def initialize_camera():
    
    #this is for initializing the camera we must use 1 for the logitech camera
    cap=cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Can not open the Camera")
        exit()
    return cap

def capture_image(cap, save_path):
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame")
        return None 
    
    #save the capture image
    cv2.imwrite(save_path, frame)
    print(f"Image saved at {save_path}")
    return frame

def detect_motion(previous_frame, current_frame, threshold=25):

    #convert frames to grayscales
    prev_gray= cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    curr_gray= cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    #compute the absolute differences between the current frame and the previous frame
    frame_diff= cv2.absdiff(curr_gray, prev_gray)

    #Apply thresholding to get the regions with significant differences
    _,thresh= cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

    ##calculate the number of non-zero pixels (changes)
    non_zero_count= cv2.countNonZero(thresh)
    return non_zero_count > 500 # we need to adjust this value according to the environment


def main():
    cap = initialize_camera()
    time.sleep(1) #Allow camera to warm up

    #read the first frame
    ret, previous_frame = cap.read()
    if not ret:
        print("failed to grab the initial frame")
        return
   
    try:
        while True:
            ret, current_frame = cap.read()
            if not ret:
                print("failed to grab frame")
                break
            

            if detect_motion(previous_frame,current_frame):
                timestamp = time.strftime("%Y%m%d--%H%M%S")
                save_path = os.path.join("/home/pta/pyProject/Camera Control Security/Motion Detected", f"image_{timestamp}.jpg")

                #ensure the directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok = True)

                #capture and save the image
                capture_image(cap, save_path)

                #adding a delay to avaiod continous capturing
                time.sleep(0.5)

            
            #update the previous frame
            previous_frame = current_frame

            #Adding small delay to reduce CPU Usage
            cv2.waitKey(30)


    except KeyboardInterrupt:  # by pressing Ctrl+C
        print("Exiting...")

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

            
