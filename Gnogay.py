import time
from rtde_control import RTDEControlInterface

rtde_c = RTDEControlInterface("192.168.56.200")
Port = 50002

# activate (เผื่อไว้)
rtde_c.sendCustomScript("rq_activate()\n")
time.sleep(2)

# close
rtde_c.sendCustomScript("rq_move(255, 255, 255)\n")
time.sleep(2)

# open
rtde_c.sendCustomScript("rq_move(0, 255, 255)\n")

rtde_c.stopScript()

#169.254.223.139
#192.168.56.200 ของพี่