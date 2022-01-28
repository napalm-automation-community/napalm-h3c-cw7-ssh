Value CHASSIS (\d+)
Value SLOT ([0-9/]+)
Value SENSOR (\S+\s+\d+)
Value TEMPERATURE (\d+)
Value ALERT (\d+)
Value CRITICAL (\d+)

Start
  ^\s*Chassis -> CHASSIS_DEVICE
  ^\s*Slot -> NORMAL_DEVICE

CHASSIS_DEVICE
 ^\s*${CHASSIS}\s+${SLOT}\s+${SENSOR}\s+${TEMPERATURE}\s+(-)?\d+\s+${ALERT}\s+${CRITICAL} -> Record

NORMAL_DEVICE
 ^\s*${SLOT}\s+${SENSOR}\s+${TEMPERATURE}\s+(-)?\d+\s+${ALERT}\s+${CRITICAL} -> Record