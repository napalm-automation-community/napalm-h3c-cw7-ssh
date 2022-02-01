Value MAC_ADDRESS (\S+)
Value VLAN (\d+)
Value CURRENT_PORT (\S+)
Value SOURCE_PORT (\S+)
Value LAST_MOVE (\d{4}(-\d{2}){2}\s\d\d(:\d\d){2})
Value TIMES (\d+)

Start
  ^\s*MAC\s+address
  ^${MAC_ADDRESS}\s+${VLAN}\s+${CURRENT_PORT}\s+${SOURCE_PORT}\s+${LAST_MOVE}\s+${TIMES} -> Record