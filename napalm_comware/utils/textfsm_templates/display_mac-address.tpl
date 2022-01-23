Value MAC_ADDRESS (\S+)
Value VLAN (\d+)
Value STATE (\S+)
Value INTERFACE (\S+)
Value AGING (\S+)

Start
  ^\s*MAC\s+address
  ^${MAC_ADDRESS}\s+${VLAN}\s+${STATE}\s+${INTERFACE}\s+${AGING} -> Record