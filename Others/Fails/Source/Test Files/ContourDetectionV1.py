from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

# Define the lower and upper boundaries of the red and green colors in the HSV color space
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

lower_green1 = np.array([40, 50, 50])
upper_green1 = np.array([70, 255, 255])
lower_green2 = np.array([160, 100, 100])
upper_green2 = np.array([90, 255, 255])

color_ranges = [
    (lower_red1, upper_red1),
    (lower_red2, upper_red2),
    (lower_green1, upper_green1),
    (lower_green2, upper_green2)
]

color_names = ['Red', 'Red', 'Green', 'Green'] 

# Initialize the closest contour variables
closest_contour = None
closest_distance = float("inf")

# Distance calculation function
def calculate_distance(known_width, focal_length, contour_width):
    return known_width * focal_length / contour_width

# If a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
# Otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# Allow the camera or video file to warm up
time.sleep(2.0)

while True:
    # Grab the current frame
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    # If we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # Resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    detected_color = None

    for (lower, upper), color_name in zip(color_ranges, color_names):
        # Construct a mask for the color, then perform a series of dilations and erosions
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in the mask and initialize the current (x, y) center
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Only proceed if at least one contour was found
        if len(cnts) > 0:
            # Find the largest contour in the mask
            c = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            # Calculate the distance using the width of the bounding box
            distance = calculate_distance(7, 0.8, w)

            if distance < closest_distance:  # Update the closest contour
                closest_distance = distance
                detected_color = color_name
                closest_contour = c

    if detected_color:
        print(f"{detected_color} block detected at distance: {closest_distance:.2f} units")

    # Show the frame to our screen
    if closest_contour is not None:
        x, y, w, h = cv2.boundingRect(closest_contour)
        center_x = x + w // 2
        center_y = y + h // 2

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

if not args.get("video", False):
    vs.stop()
else:
    vs.release()

# Close all windows
cv2.destroyAllWindows()
