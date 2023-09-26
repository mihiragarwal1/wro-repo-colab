import cv2

cap = cv2.VideoCapture("nvarguscamerasrc sensor_id=0 ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e", cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    # You can now capture frames from the camera using cap.read()
    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Could not read frame.")
            break

        # Process the frame here (e.g., display it or perform some operations)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()