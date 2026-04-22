import rtde_control
import rtde_receive
import time
import numpy as np
import cv2
import threading
from Detection import Camera
from Detect_color_used import ColorDetect

from rtde_receive import RTDEReceiveInterface #นำเข้า RTDEReceiveInterface จาก rtde_receive
from scipy.spatial.transform import Rotation as R  #นำเข้า Rotation จาก scipy.spatial.transform เพื่อใช้ในการแปลงระหว่างรูปแบบการหมุนต่างๆ

# ฟังก์ชันสำหรับรันกล้องใน thread แยก

def run_color_detection():
    color_detector = ColorDetect()
    color_detector.detect()

#robot_ip = "192.168.1.1"  # IP address

# เริ่ม thread กล้องตั้งแต่แรก (ก่อนเชื่อมหุ่นยนต์)
# camera_thread = threading.Thread(target=run_camera)
# camera_thread.start()

# การเชื่อมต่อกับหุ่นยนต์
# print("Connecting to robot...")
# rtde_c = rtde_control.RTDEControlInterface(robot_ip)
# rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
# print("Connected to robot.")



# รับค่า X, Y, Z, RX, RY, RZ ของ TCP
# pose = rtde_r.getActualTCPpose()
# rot = R.from_rotvec(pose[3:6])
# rpy = rot.as_euler('xyz', degrees=True)

# ตัวอย่างการเซ็ตพิกัด
# waypoint1 = [x, y, z, rx, ry, rz]

# waypoint1 = [0, -1.57, 0, -1.57, 0, 0]
# waypoint2 = [0.1, -1.57, 0, -1.57, 0, 0]


# # สั่งให้เคลื่อนที่ไปตำแหน่งนี้
# #rtde_c.moveL(waypoint1, 0.25, 1.2)

# print("Moving robot to home position...")

# rtde_c.moveL(waypoint2, 0.25, 1.2)

# print("Robot is at home position.")

# # เริ่ม thread สำหรับกล้องหลังจากหุ่นยนต์เคลื่อนที่แล้ว
# camera_thread = threading.Thread(target=run_camera)
# camera_thread.start()

# # รอให้ thread กล้องเสร็จ (またはรันต่อไป)
# camera_thread.join()
if __name__ == "__main__":
    # เลือกว่าจะรันอะไร
    run_color_detection()  # รันการตรวจจับสี