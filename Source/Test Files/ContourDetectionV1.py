import cv2
import numpy as np

def get_closest_contour(contours):
    if len(contours) == 0:
        return None

    closest_contour = max(contours, key=cv2.contourArea)
    return closest_contour

def detect_closest_contour(frame, hsv, mask_red, mask_green):
    # Find contours of red objects
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find contours of green objects
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the closest contours for red and green
    closest_contour_red = get_closest_contour(contours_red)
    closest_contour_green = get_closest_contour(contours_green)
    
    # Determine which contour is closest overall
    if closest_contour_red is not None and closest_contour_green is not None:
        if cv2.contourArea(closest_contour_red) > cv2.contourArea(closest_contour_green):
            closest_contour = closest_contour_red
            bounding_box_color = (0, 0, 255)  # Red
        else:
            closest_contour = closest_contour_green
            bounding_box_color = (0, 255, 0)  # Green
    elif closest_contour_red is not None:
        closest_contour = closest_contour_red
        bounding_box_color = (0, 0, 255)  # Red
    elif closest_contour_green is not None:
        closest_contour = closest_contour_green
        bounding_box_color = (0, 255, 0)  # Green
    else:
        closest_contour = None
        bounding_box_color = None
    
    if closest_contour is not None:
        x, y, w, h = cv2.boundingRect(closest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), bounding_box_color, 1)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 5, bounding_box_color, -1)
        cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), bounding_box_color, 1)
        return (x, y, w, h)
    else:
        return None

def main():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (320, 240))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for red color in HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Define the lower and upper bounds for green color in HSV
        lower_green1 = np.array([40, 50, 50])
        upper_green1 = np.array([70, 255, 255])
        lower_green2 = np.array([160, 100, 100])
        upper_green2 = np.array([90, 255, 255])

        # Threshold the frame to get only red and green colors
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        mask_green1 = cv2.inRange(hsv, lower_green1, upper_green1)
        mask_green2 = cv2.inRange(hsv, lower_green2, upper_green2)
        mask_green = cv2.bitwise_or(mask_green1, mask_green2)

        detected_bounding_box = detect_closest_contour(frame, hsv, mask_red, mask_green)

        cv2.imshow("Closest Contour Detection", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
