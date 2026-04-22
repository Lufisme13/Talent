import cv2
import numpy as np


class ColorDetect:
    def __init__(self, camera_index=0):
        # On Windows, CAP_DSHOW often works better for USB webcams.
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError(
                "Cannot open camera. Try closing other apps that use the webcam "
                "or change camera_index to 1."
            )

    def get_single_target(self):
        """
        โชว์ภาพและหาวัตถุที่ใหญ่ที่สุดชิ้นเดียว 
        กด 'c' เพื่อ Capture (เซฟภาพและส่งค่าตัวแปร)
        กด 'q' เพื่อยกเลิก
        """
        print("📷 Camera is running... Press 'c' to capture target, 'q' to quit.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # ===== ตั้งค่า Mask สี =====
            mask_yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([30, 255, 255]))
            mask_red = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255])) + \
                       cv2.inRange(hsv, np.array([160, 100, 100]), np.array([180, 255, 255]))

            # ===== หา Contours =====
            contours_y, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_r, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            best_color = None
            max_area = 500 # กำหนดขนาดขั้นต่ำ
            best_cnt = None

            # หาชิ้นสีเหลืองที่ใหญ่ที่สุด
            if contours_y:
                largest_y = max(contours_y, key=cv2.contourArea)
                if cv2.contourArea(largest_y) > max_area:
                    max_area = cv2.contourArea(largest_y)
                    best_color = "YELLOW"
                    best_cnt = largest_y

            # หาชิ้นสีแดงที่ใหญ่ที่สุด (เทียบกับสีเหลืองเมื่อกี้ด้วย ว่าใครใหญ่กว่ากัน)
            if contours_r:
                largest_r = max(contours_r, key=cv2.contourArea)
                if cv2.contourArea(largest_r) > max_area:
                    max_area = cv2.contourArea(largest_r)
                    best_color = "RED"
                    best_cnt = largest_r

            # ===== วาดกรอบเป้าหมาย "ชิ้นเดียว" =====
            cx, cy = 0, 0
            if best_color is not None:
                x, y, w, h = cv2.boundingRect(best_cnt)
                cx, cy = int(x + w / 2), int(y + h / 2)
                
                # กำหนดสีเส้นที่ใช้วาดตามสีที่จับได้
                draw_color = (0, 255, 255) if best_color == "YELLOW" else (0, 0, 255)
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
                cv2.circle(frame, (cx, cy), 5, draw_color, -1)
                cv2.putText(frame, f"{best_color} ({cx},{cy})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, draw_color, 2)

            cv2.imshow("Camera View", frame)

            # ===== รอรับคำสั่งจาก Keyboard บนหน้าต่าง OpenCV =====
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c'): # กด c เพื่อ Capture
                if best_color is not None:
                    # เซฟรูป
                    cv2.imwrite("captured_target.jpg", frame)
                    print(f"✅ บันทึกภาพแล้ว! เป้าหมายคือ {best_color} พิกัด (X:{cx}, Y:{cy})")
                    self.release()
                    return best_color, cx, cy # **ส่งค่ากลับไปให้โค้ดหุ่นยนต์**
                else:
                    print("⚠️ ไม่พบเป้าหมายในเฟรม")
                    
            elif key == ord('q'): # กด q เพื่อยกเลิก
                self.release()
                return None, None, None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
