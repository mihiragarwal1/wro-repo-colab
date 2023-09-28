'''This script is for collecting images.
1. Specify the path to store images.
2. Specify the size of chessboard for detecting chessboard and displaying detection results.
3. Press 'c' to capture image.
4. Press 'q' to quit.
'''

import cv2
camera = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
ret, img = camera.read()
path = "./cam1_images/"
count = 0
CHESSBOARD_CORNER_NUM_X = 11
CHESSBOARD_CORNER_NUM_Y = 8

while True:
    ret, img = camera.read()
    img2 = img.copy()
    cv2.putText(img2, 'Captured image: {}. Press \'c\' to capture image. Press \'q\' to quit.'.format(count), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (CHESSBOARD_CORNER_NUM_X,CHESSBOARD_CORNER_NUM_Y), flags=cv2.CALIB_CB_FAST_CHECK)
    delay = 10
    if ret == True:
        # Draw and display the corners
        cv2.drawChessboardCorners(img2, (CHESSBOARD_CORNER_NUM_X,CHESSBOARD_CORNER_NUM_Y), corners, ret)
        delay = 10
    cv2.imshow("img", img2)
    key = cv2.waitKey(delay) & 0xFF
    if key == ord('c'):
        name = path + str(count)+".jpg"
        cv2.imwrite(name, img)
        count += 1
    if key == ord('q'):
        break
cv2.destroyAllWindows()