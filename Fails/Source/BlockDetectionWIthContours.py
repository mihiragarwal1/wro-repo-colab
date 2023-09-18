import cv2
import numpy as np


def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def detect_largest_contour():
    # Open video capture
    cap = cv2.VideoCapture('videotestsrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! appsink', cv2.CAP_GSTREAMER)    
    line_color = (0, 255, 0)
    box_color = (0, 0, 255)  # Red

    # Set the desired resolution
    target_width = 320
    target_height = 240

    # Set the desired frame rate for display
    display_fps = 15

    frame_counter = 0

    while True:
        # Read frame from video feed
        ret, frame = cap.read()

        if not ret:
            # Reset the video capture to the beginning of the clip
            # cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Resize the frame to the target resolution
        frame = cv2.resize(frame, (target_width, target_height))

        frame_counter += 1

        if frame_counter % (int(cap.get(cv2.CAP_PROP_FPS)) // display_fps) == 0:
            # Reset the frame counter
            frame_counter = 0

            # Convert the frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for red color in HSV
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])

            # Define the lower and upper bounds for green color in HSV
            lower_green = np.array([40, 50, 50])
            upper_green = np.array([90, 255, 255])

            # Threshold the frame to get only red and green colors
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            mask_green = cv2.inRange(hsv, lower_green, upper_green)

            # Find contours of red and green objects
            contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Calculate the combined area of all red contours
            combined_area_red = 0
            for contour in contours_red:
                combined_area_red += cv2.contourArea(contour)

            # Calculate the combined area of all green contours
            combined_area_green = 0
            for contour in contours_green:
                combined_area_green += cv2.contourArea(contour)

            # Find the largest contour for red color
            largest_contour_red = None
            if len(contours_red) > 0:
                largest_contour_red = max(contours_red, key=cv2.contourArea)

            # Find the largest contour for green color
            largest_contour_green = None
            if len(contours_green) > 0:
                largest_contour_green = max(contours_green, key=cv2.contourArea)

            # Draw the bounding box and center circle for the largest contour
            if largest_contour_red is not None and combined_area_red >= combined_area_green:
                x, y, w, h = cv2.boundingRect(largest_contour_red)
                cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 1)
                center_x = x + w // 2
                center_y = y + h // 2
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), line_color, 1)
            elif largest_contour_green is not None:
                x, y, w, h = cv2.boundingRect(largest_contour_green)
                cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 1)
                center_x = x + w // 2
                center_y = y + h // 2
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
                cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), line_color, 1)

            cv2.imshow("Largest Contours", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_largest_contour()
