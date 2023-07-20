import cv2
import numpy as np

def detect_red_green_contours():
    # Open video capture
    cap = cv2.VideoCapture("C:\DATA\WRO\TESTS\wro2020-fe-POV2-175mm.gif")
    line_color = (0,255,0)
    box_color = (0, 0, 255)  # Red


    while True:
        # Read frame from video feed
        ret, frame = cap.read()

        if not ret:
            # Reset the video capture to the beginning of the clip
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
          # Get the dimensions of the frame
        height, width, _ = frame.shape

        # Calculate the positions of the two lines
        line1_x = width // 3
        line2_x = 2 * width // 3

        # Draw the two lines
        cv2.line(frame, (line1_x, 0), (line1_x, height), (255, 0, 0), 1)
        cv2.line(frame, (line2_x, 0), (line2_x, height), (255, 0, 0), 1)

        # Resize the frame to a width of 500 pixels while maintaining the aspect ratio
        width = 500
        height = int(frame.shape[0] * (width / frame.shape[1]))
        frame = cv2.resize(frame, (width, height))

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for darker shades of red color in HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Define the lower and upper bounds for a wider range of green color in HSV
        lower_green1 = np.array([40, 50, 50])
        upper_green1 = np.array([70, 255, 255])
        lower_green2 = np.array([70, 50, 50])
        upper_green2 = np.array([90, 255, 255])

        # Threshold the frame to get only darker shades of red and wider range of green colors
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        mask_green1 = cv2.inRange(hsv, lower_green1, upper_green1)
        mask_green2 = cv2.inRange(hsv, lower_green2, upper_green2)
        mask_green = cv2.bitwise_or(mask_green1, mask_green2)

        # Find contours of red and green objects
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour for red color
        if len(contours_red) > 0:
             # Filter out contours smaller than 300 pixels in area
            contours_red = [cnt for cnt in contours_red if cv2.contourArea(cnt) > 100]
            if len(contours_red) > 0:
                largest_contour_red = max(contours_red, key=cv2.contourArea)
                x_red, y_red, w_red, h_red = cv2.boundingRect(largest_contour_red)

                # Calculate the moments of the contour
                red_moments = cv2.moments(largest_contour_red)

                # Check if moments are valid and non-zero before computing the center
                if red_moments["m00"] != 0:
                    center_x = int(red_moments["m10"] / red_moments["m00"])
                    center_y = int(red_moments["m01"] / red_moments["m00"])
                    if frame.shape[1]//3 < center_x:
                        # Object is between the lines, set box color to red
                        cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 1)
                    else:
                        # Object is outside the center part, set box color to green
                        cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 255, 0), 1)

                    # cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), box_color, 1)

                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                    # Display a vertical line passing through the center
                    cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (255, 255, 0), 1)

        # Find the largest contour for green color
        if len(contours_green) > 0:
            # Filter out contours smaller than 300 pixels in area
            contours_green = [cnt for cnt in contours_green if cv2.contourArea(cnt) > 100]
            if len(contours_green) > 0:
                largest_contour_green = max(contours_green, key=cv2.contourArea)
                x_green, y_green, w_green, h_green = cv2.boundingRect(largest_contour_green)
                # Calculate the moments of the contour
                green_moments = cv2.moments(largest_contour_green)

                # Check if moments are valid and non-zero before computing the center
                if green_moments["m00"] != 0:
                    center_x = int(green_moments["m10"] / green_moments["m00"])
                    center_y = int(green_moments["m01"] / green_moments["m00"])
                    if center_x <2*frame.shape[1]//3:
                        # Object is between the lines, set box color to red
                        cv2.rectangle(frame, (x_green, y_green), (x_green + w_green, y_green + h_green), (0, 0, 255), 1)

                    else:
                        # Object is outside the center part, set box color to green
                        cv2.rectangle(frame, (x_green, y_green), (x_green + w_green, y_green + h_green), (0, 255, 0), 1)
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                    # Display a vertical line passing through the center
                    cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (255, 255, 0), 1)

        # Display the frame with detected contours, bounding boxes, and center line
        cv2.imshow("Contours", frame)

        # Introduce a delay between frames (50 milliseconds)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


# Call the function to detect red and green contours from the video feed
detect_red_green_contours()
