import time
from rtde_control import RTDEControlInterface

# เชื่อมต่อกับ Robot (IP: 169.254.223.139 ตามในรูปของคุณ)
rtde_c = RTDEControlInterface("169.254.223.139")

print("🚀 กำลังสั่งงาน Gripper...")

# สั่งให้ Gripper ปิด (Grip) 
# พารามิเตอร์: rq_move(ตำแหน่ง, ความเร็ว, แรง)
# 255 = ปิดสุด/เร็วสุด/แรงสุด
rtde_c.sendCustomScript("rq_move(255, 255, 255)\n")

time.sleep(2) # รอให้ Gripper ทำงานเสร็จ

# สั่งให้ Gripper เปิด (Open)
# 0 = เปิดสุด
rtde_c.sendCustomScript("rq_move(0, 255, 255)\n")

print("✅ สั่งงานเรียบร้อย!")
rtde_c.stopScript() # หยุดสคริปต์ที่ค้างอยู่