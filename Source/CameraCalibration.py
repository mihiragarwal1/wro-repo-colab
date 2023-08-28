import numpy as np
import cv2
from imutils import paths
import imutils

# Load your calibration images and gather calibration points

# Define known values for calibration pattern (checkerboard)
pattern_size = (9, 6)  # Change this based on your calibration pattern

# Arrays to store object points and image points from all calibration images
obj_points = []  # 3D points in real-world space
img_points = []  # 2D points in image plane

# Generate object points (calibration pattern in 3D)
objp = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

# Load and process calibration images
for imagePath in sorted(paths.list_images("calibration_images")):
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find calibration pattern corners
    found, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    # If found, add object points and image points
    if found:
        obj_points.append(objp)
        img_points.append(corners)

# Calibrate the camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Now you have the camera matrix (mtx) and distortion coefficients (dist) for undistortion

# Rest of your code
KNOWN_DISTANCE = 24.0
KNOWN_WIDTH = 11.0

for imagePath in sorted(paths.list_images("images")):
    image = cv2.imread(imagePath)
    undistorted = cv2.undistort(image, mtx, dist)
    
    marker = find_marker(undistorted)
    perWidth = marker[1][0]
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, perWidth)

    color = (0, 255, 0)  # Green color
    if inches < 12:
        color = (0, 0, 255)  # Red color

    box = cv2.boxPoints(marker)
    box = np.int0(box)
    
    cv2.drawContours(undistorted, [box], -1, color, 2)
    cv2.putText(undistorted, "%.2fft" % (inches / 12), (undistorted.shape[1] - 200, undistorted.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
    
    cv2.imshow("undistorted", undistorted)
    cv2.waitKey(0)
