import cv2
import numpy as np
from ultralytics import YOLO

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        else:
            print("Connected to camera.")

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to grab frame from camera")
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
def yolo_detect(frame, model, cond = 0.3):
    results = model(frame)[0]
    


if __name__ == "__main__":
    # สร้างอินสแตนซ์ของ Camera
    camera = Camera(camera_index=0)

    print("Press 'q' to exit camera preview")
    while True:
        frame = camera.read_frame()
        cv2.imshow("Camera Live View", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()

