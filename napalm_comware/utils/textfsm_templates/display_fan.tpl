Value Filldown CHASSIS (\d+)
Value Filldown SLOT (\d+)
Value Required FAN_ID (\d+)
Value STATUS (\S+)


Start
  ^\s*Chassis\s+${CHASSIS} -> CHASSIS_DEVICE
  ^\s*Slot\s+${SLOT} -> NORMAL_DEVICE
  ^\s*Device Info on Slot ${SLOT} -> DEVLOP_TEST

NORMAL_DEVICE
  ^\s*Slot\s+${SLOT}
  ^\s*Fan\s+${FAN_ID}
  ^\s*Stat(e|us)\s+:\s+${STATUS} -> Record

CHASSIS_DEVICE
  ^\s*Chassis\s+${CHASSIS}
  ^\s*Fan(-tray)?\s+${FAN_ID}
  ^\s*Stat(e|us)\s+:\s+${STATUS} -> Record

DEVLOP_TEST
  ^\s*Device Info on Slot ${SLOT}
  ^\s*${FAN_ID}\s+${STATUS} -> Record