from imutils import paths
import numpy as np
import imutils
import cv2

def find_marker(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

KNOWN_DISTANCE = 24.0
KNOWN_WIDTH = 11.0

# Load the image that contains an object (red or green block) at KNOWN_DISTANCE from the camera
image = cv2.imread("your_image_path.jpg")  # Replace with your image path

marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

for imagePath in sorted(paths.list_images("images")):  # Replace with your image directory
    image = cv2.imread(imagePath)
    marker = find_marker(image)
    perWidth = marker[1][0]
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, perWidth)

    color = (0, 255, 0)  # Green color
    if inches < 12:
        color = (0, 0, 255)  # Red color

    box = cv2.boxPoints(marker)
    box = np.int0(box)
    
    cv2.drawContours(image, [box], -1, color, 2)
    cv2.putText(image, "%.2fft" % (inches / 12), (image.shape[1] - 200, image.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
    
    cv2.imshow("image", image)
    cv2.waitKey(0)
