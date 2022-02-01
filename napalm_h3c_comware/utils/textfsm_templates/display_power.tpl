Value Filldown CHASSIS (\d+)
Value Filldown SLOT (\d+)
Value Required POWER_ID (\d+)
Value STATUS (\S+)
Value MODE (\S+)
Value CURRENT ([0-9\-\.]+)
Value VOLTAGE ([0-9\-\.]+)
Value POWER ([0-9\-\.]+)


Start
  ^\s*Chassis\s+${CHASSIS} -> CHASSIS_DEVICE
  # for S68xx S51xx S55xx 等盒式设备
  ^\s*Slot\s+${SLOT}
  ^\s*${POWER_ID}\s+${STATUS}\s+${MODE}\s+${CURRENT}\s+${VOLTAGE}\s+${POWER} -> Record


# for S125xx S75xx 等框式设备
CHASSIS_DEVICE
  ^\s*Chassis\s+${CHASSIS}
  ^\s*Power\s+supply\s*policy
  ^\s*PowerID
  ^\s*${POWER_ID}\s+${STATUS}\s+\S+\s+${CURRENT}\s+${VOLTAGE}\s+${POWER} -> Record