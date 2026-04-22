from rtde_receive import RTDEReceiveInterface
from rtde_control import RTDEControlInterface
import time
import keyboard  # อย่าลืม pip install keyboard
import math 

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
    SAFE_JOINT_POS_Waypoint1 = [0.9511861801147461, -1.5639360708049317, 0.0008571783648889664, -1.570834299127096, -2.0329152242481996e-05, 8.201599121093375e-05]
    HOME_JOINT_POS = [0.019417285919189453, -1.5370262426188965, -0.020110130310058594, -1.6604982815184535, 0.0020804405212402344, 0.076226711277319336]

    print("\n--- System is ready for operation ---")
    print(" '1'  Waypoint 1")
    print(" '2'  Home Position")
    print(" 'S'  Emergency Stop")
    print(" 'ESC'  Exit Program\n")

    while True:
        # 1. ตรวจสอบการกดปุ่ม '1' เพื่อเริ่มทำงาน
        if keyboard.is_pressed('1'):
            start_time = time.time() # บันทึกเวลาเริ่มต้น
            print(f"⏱️ Start T1: {start_time}")
            
            # สั่งขยับ (ไม่ใส่ async เพื่อให้ Python รอจนหุ่นถึงที่หมาย)
            rtde_c.moveJ(SAFE_JOINT_POS_Waypoint1, speed=SPEED_RAD, acceleration=ACCEL_RAD) 
            
            end_time = time.time() # บันทึกเวลาสิ้นสุด
            print(f"🏁 End T1: {end_time}")
            print(f"📊 Total Time (1): {end_time - start_time:.4f} seconds\n")
            time.sleep(1) # พักก่อนกดครั้งต่อไป
        
        if keyboard.is_pressed('2'):
            print("🚀 robot moving to Home Position...")
            rtde_c.moveJ(HOME_JOINT_POS, speed=SPEED_RAD, acceleration=ACCEL_RAD, asynchronous=True)
            time.sleep(0.5) # ป้องกันการส่งคำสั่งซ้ำรัวๆ

        # 2. ตรวจสอบการกดปุ่ม 'S' เพื่อหยุด (สำคัญมาก!)
        if keyboard.is_pressed('s'):
            print("🛑 STOP! now")
            rtde_c.stopJ(2.0) # เบรกข้อต่อทันทีด้วยความหน่วง 2.0 rad/s^2
            # เคลียร์คำสั่งที่ค้างอยู่เพื่อให้หุ่นนิ่งจริงๆ
            rtde_c.reuploadScript() 
            print("robot is already stopped.")
            time.sleep(0.5)

        # 3. ตรวจสอบการกด 'ESC' เพื่อจบโปรแกรม
        if keyboard.is_pressed('esc'):
            print("End12...")
            rtde_c.stopScript()
            break

        time.sleep(0.01) # พัก CPU เล็กน้อย

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")
finally:
    # ปิดการเชื่อมต่ออย่างปลอดภัย
    print("ระบบกำลังปิดตัวลง...")