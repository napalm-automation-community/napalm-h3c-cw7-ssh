Value Filldown CHASSIS (\d+)
Value Required SLOT (\d+)
Value TOTAL (\d+)
Value USED (\d+)
Value FREE (\d+)
Value SHARED (\d+)
Value BUFFER (\d+)
Value CACHED (\d+)
Value FREE_RATIO ([0-9\-\.]+)


Start
  ^Memory\s+statistics
  ^\s*(Chassis\s+${CHASSIS})?\s*Slot\s+${SLOT}
  ^\s*Mem:\s+${TOTAL}\s+${USED}\s+${FREE}\s+${SHARED}\s+${BUFFER}\s+${CACHED}\s+${FREE_RATIO}% -> Record