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
Value RX_PKTS (\d+|-)
Value RX_BYTES (\d+|-)
Value RX_UNICAST (\d+|-)
Value RX_BROADCAST (\d+|-)
Value RX_MULTICAST (\d+|-)
Value RX_ERRORS (\d+|-)
Value RX_ABORTS (\d+|-)
Value RX_CRC (\d+|-)
Value TX_PKTS (\d+|-)
Value TX_BYTES (\d+|-)
Value TX_UNICAST (\d+|-)
Value TX_BROADCAST (\d+|-)
Value TX_MULTICAST (\d+|-)
Value TX_ERRORS (\d+|-)
Value TX_ABORTS (\d+|-)

Start
  # 接口名所在行是一个独立的字符串，以此开始记录
  ^\S+\s*$$ -> Continue.Record
  # 路由器某个 Serial 接口后面出现了空格，莫名奇妙的 comware bug
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
  # 如果接口不存在计数信息（例如 Serial），直接开始匹配下一个接口
  ^\s*$$  -> Start
  # 虚拟接口计数匹配
  ^\s?Input:\s*${RX_PKTS}\s+packets,\s+${RX_BYTES}\s+bytes(,\s+\d+\s+buffers)?(,\s+${RX_ABORTS}\s+drops)?
  ^\s?Output:\s*${TX_PKTS}\s+packets,\s+${TX_BYTES}\s+bytes(,\s+\d+\s+buffers)?(,\s+${TX_ABORTS}\s+drops)? -> Start
  # 物理接口计数匹配
  ^\s*Input\s+\(total\) -> INPUT



# for physical interfaces
INPUT
  ^\s*Input\s+\(normal\):\s+${RX_PKTS}\s+packets,\s+${RX_BYTES}\s+bytes
  ^\s*${RX_UNICAST}\s+unicasts,\s+${RX_BROADCAST}\s+broadcasts,\s+${RX_MULTICAST}\s+multicasts,\s+\d+\s+pauses
  ^\s*Input:\s+${RX_ERRORS}\s+input\s+errors,
  ^\s*${RX_CRC}\s+CRC,\s+\d+\s+frame,\s+\d+\s+overruns,\s+${RX_ABORTS}\s+aborts -> OUTPUT

# for physical interfaces
OUTPUT
  ^\s*Output\s+\(normal\):\s+${TX_PKTS}\s+packets,\s+${TX_BYTES}\s+bytes
  ^\s*${TX_UNICAST}\s+unicasts,\s+${TX_BROADCAST}\s+broadcasts,\s+${TX_MULTICAST}\s+multicasts,\s+\d+\s+pauses
  ^\s*Output:\s+${TX_ERRORS}\s+output\s+errors,
  ^\s*${TX_ABORTS}\s+aborts,\s+\d+\s+deferred, -> Start