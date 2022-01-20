Value IP_ADDRESS (\d+.\d+.\d+.\d+)
Value MAC_ADDRESS (\w+-\w+-\w+)
Value VLAN (\S+|\d+)
Value INTERFACE (\S+)
Value AGING (\d+)
Value TYPE (\S+)

Start
  ^IP\s+address.* -> ARP

ARP
  ^${IP_ADDRESS}\s+${MAC_ADDRESS}\s+${VLAN}\s+${INTERFACE}\s+${AGING}\s+${TYPE} -> Record
  