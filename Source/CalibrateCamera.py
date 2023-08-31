import numpy as np
import cv2 as cv
import glob
import yaml
from pathlib import Path

CHESSBOARD_CORNER_NUM_X = 11
CHESSBOARD_CORNER_NUM_Y = 8
IMAGE_SRC = "cam1_images"
CAMERA_PARAMETERS_OUTPUT_FILE = "cam1.yaml"

# Get the absolute path of the script's directory
root = Path(__file__).parent.absolute()

# Set path to the images
calib_imgs_path = root.joinpath(IMAGE_SRC)

# Termination criteria for corner refinement
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points for the chessboard corners
objp = np.zeros((CHESSBOARD_CORNER_NUM_X * CHESSBOARD_CORNER_NUM_Y, 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD_CORNER_NUM_X, 0:CHESSBOARD_CORNER_NUM_Y].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane
last_gray = None

# Load images
images = calib_imgs_path.glob('*.jpg')

# Loop through images and find chessboard corners
for fname in images:
    img = cv.imread(str(root.joinpath(fname)))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    last_gray = gray
    
    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (CHESSBOARD_CORNER_NUM_X, CHESSBOARD_CORNER_NUM_Y), None)
    
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        
        # Draw and display the corners
        cv.drawChessboardCorners(img, (CHESSBOARD_CORNER_NUM_X, CHESSBOARD_CORNER_NUM_Y), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
    else:
        print('Failed to find a chessboard in {}'.format(fname))

cv.destroyAllWindows()

if last_gray is not None:
    # Calibrate the camera using the last gray image
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, last_gray.shape[::-1], None, None)

    # Display the results
    print("Camera matrix:\n", mtx)
    print("Distortion coefficients:\n", dist)

    # Calculate mean error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error

    print("Total error: {}".format(mean_error / len(objpoints)))

    # Save camera parameters to YAML file
    data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
    with open(CAMERA_PARAMETERS_OUTPUT_FILE, "w") as f:
        yaml.dump(data, f)
