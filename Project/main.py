from rtde_receive import RTDEReceiveInterface
from rtde_control import RTDEControlInterface
from scipy.spatial.transform import Rotation as R
from Detection import Camera
from Detect_color_used import ColorDetect
import threading
import keyboard
import cv2
import numpy as np
import time
import math
from Basic_code_UR  import run_color_detection

def Yellow():
    rtde_c.moveJ(HOME_JOINT_POS, speed=SPEED_RAD, acceleration=ACCEL_RAD)
    rtde_c.moveJ(SAFE_JOINT_POS_Waypoint1, speed=SPEED_RAD, acceleration=ACCEL_RAD) 
    rtde_c.moveJ(SAFE_JOINT_POS_Waypoint2, speed=SPEED_RAD, acceleration=ACCEL_RAD) 
    rtde_c.moveJ(SAFE_JOINT_POS_Waypoint3, speed=SPEED_RAD, acceleration=ACCEL_RAD) 
    rtde_c.moveJ(HOME_JOINT_POS, speed=SPEED_RAD, acceleration=ACCEL_RAD)



ROBOT_IP = "169.254.223.139"
rtde_r = RTDEReceiveInterface(ROBOT_IP)
current_q = rtde_r.getActualQ()
print(f"ค่า Joint (q) คือ: {current_q}")

SPEED_RAD = 60 * (math.pi / 180)      # ประมาณ 1.047
ACCEL_RAD = 80 * (math.pi / 180)      # ประมาณ 1.396

try:
    print(f"Connecting to {ROBOT_IP}...")
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_c = RTDEControlInterface(ROBOT_IP)
    print("✅ Device Connected!")

    # พิกัด Joint ที่คุณอ่านได้ (Safe Point)
    HOME_JOINT_POS = [0.7666654586791992, -1.7334257564940394, 0.21562463441957647, -1.3820694249919434, -1.6330178419696253, 8.20159912109375e-05] 
    SAFE_JOINT_POS_Waypoint1 = [0.5434155464172363, -1.0034750264934083, 1.1601312796222132, -1.7528683147826136, -1.5421722571002405, 1.3339605331420898]
    SAFE_JOINT_POS_Waypoint2 = [0.550137996673584, -1.6423670254149378, 0.4860180060016077, -1.7518850765623988, -1.542112175618307, 1.333864688873291]
    SAFE_JOINT_POS_Waypoint3 = [1.2932119369506836, -1.0348432821086426, 0.8494585196124476, -1.3450268071940918, -1.5377104918109339, 0.5207304954528809]
    
    
    
    print("\n--- System is ready for operation ---")
    print("Press '1' to start color detection and robot movement")
    print(" 'S'  Emergency Stop")
    print(" 'ESC'  Exit Program\n")

    
    while True:
        
        if keyboard.is_pressed('1'):
            print("👁️ เปิดระบบมองเห็น... (กด 'c' เพื่อจับภาพ หรือ 'q' เพื่อยกเลิก)")
            detector = ColorDetect(camera_index=0)
            
            # รอรับค่าสีจากกล้อง
            color, cx, cy = detector.get_single_target() 
            
            # ===== เอาค่าสีที่ได้ มาเข้าเงื่อนไข (แทน if '1' ของเดิม) =====
            if color == "YELLOW":
                print(f"🟡 ตรวจพบสีเหลืองที่ ({cx}, {cy}) -> หุ่นยนต์กำลังไป Waypoint 1")
                start_time = time.time() 
                
                Yellow()
                
                end_time = time.time()
                print(f"📊 ทำงานเสร็จสิ้น ใช้เวลา: {end_time - start_time:.4f} วินาที\n")

            elif color == "RED":
                print(f"🔴 ตรวจพบสีแดงที่ ({cx}, {cy}) -> หุ่นยนต์กำลังกลับ Home")
                rtde_c.moveJ(SAFE_JOINT_POS_Waypoint2, speed=SPEED_RAD, acceleration=ACCEL_RAD)
                
            else:
                print("⚠️ ข้ามการทำงาน เนื่องจากไม่ได้สีที่ต้องการ หรือกดยกเลิก")
                
            time.sleep(0.5) # หน่วงเวลากันกดปุ่มซ้ำ

        
        if keyboard.is_pressed('s'):
            print("🛑 STOP! now")
            rtde_c.stopJ(2.0) 
            rtde_c.reuploadScript() 
            print("robot is already stopped.")
            time.sleep(0.5)

        if keyboard.is_pressed('esc'):
            print("End12...")
            rtde_c.stopScript()
            break
        
    

    time.sleep(0.01) 

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")
finally:
    # ปิดการเชื่อมต่ออย่างปลอดภัย
    print("ระบบกำลังปิดตัวลง...")