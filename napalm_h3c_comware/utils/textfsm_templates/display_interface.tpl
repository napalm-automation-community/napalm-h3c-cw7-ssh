Value Required INTERFACE (\S+)
Value LINK_STATUS (.+)
Value PROTOCOL_STATUS (\S+)
Value MAC_ADDRESS (\S+)
Value DESCRIPTION (.+)
Value BANDWIDTH (\d+)
Value MTU (\d+)
Value SPEED_MODE (\S+)
Value DUPLEX_MODE (\S+)
Value MEDIA_TYPE (\S+(\s+\S+)?)
Value HARDWARE_TYPE (\S+(\s+\S+)?)
Value PVID (\d+)
Value LINK_TYPE (\S+)
Value LAST_FLAPPING (.+)
Value PRIMARY_IPADDR (\d+\.\d+\.\d+\.\d+/\d+)

Start
  # 接口名所在行是一个独立的字符串，以此开始记录
  ^\S+\s*$$ -> Continue.Record
  ^${INTERFACE}\s*$$
  ^(C|c)urrent\s+state:\s+${LINK_STATUS}
  ^(L|l)ine\s+protocol\s+state:\s+${PROTOCOL_STATUS}
  ^IP\s+packet\s+frame\s+type.*hardware\s+address:\s+${MAC_ADDRESS}
  ^Description:\s+${DESCRIPTION}
  ^Bandwidth:\s+${BANDWIDTH}.*
  ^Maximum\s+transmission\s+unit:\s+${MTU}
  ^Media\s+type\s+is\s+${MEDIA_TYPE},\s*port\s+hardware\s+type\s+is\s+${HARDWARE_TYPE}
  ^${SPEED_MODE}-speed mode,\s+${DUPLEX_MODE}-duplex\s+mode
  ^Internet\s+address:\s+${PRIMARY_IPADDR}.*
  ^PVID:\s+${PVID}
  ^Port\s+link-type:\s+${LINK_TYPE}
  ^Last\s+link\s+flapping:\s+${LAST_FLAPPING}
  ^\s*$$