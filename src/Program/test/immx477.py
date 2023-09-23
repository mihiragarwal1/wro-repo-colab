from jetcam.csi_camera import CSICamera
import cv2

camera = CSICamera(width=960, height=720)


while True:
    frame = camera.read()
    cv2.imshow("cam",frame)

    if cv2.waitKey(1)& 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()