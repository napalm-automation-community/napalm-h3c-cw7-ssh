Value CHASSIS (\d+)
Value SLOT (\d+)
Value CPU_ID (\d+)
Value FIVE_SEC (\d+)
Value ONE_MIN (\d+)
Value FIVE_MIN (\d+)

Start
  # 单机设备、低端设备等等
  ^\s*CPU -> SINGLE_DEVICE
  # 一般代指支持 irf 特性的盒式设备
  ^\s*Slot -> NORMAL_DEVICE
  # 框式设备
  ^\s*Chassis -> CHASSIS_DEVICE

SINGLE_DEVICE
  ^\s*${CPU_ID}\s+${FIVE_SEC}%\s+${ONE_MIN}%\s+${FIVE_MIN}% -> Record

NORMAL_DEVICE
  ^\s*${SLOT}\s+${CPU_ID}\s+${FIVE_SEC}%\s+${ONE_MIN}%\s+${FIVE_MIN}% -> Record

CHASSIS_DEVICE
  ^\s*${CHASSIS}\s+${SLOT}\s+${CPU_ID}\s+${FIVE_SEC}%\s+${ONE_MIN}%\s+${FIVE_MIN}% -> Record