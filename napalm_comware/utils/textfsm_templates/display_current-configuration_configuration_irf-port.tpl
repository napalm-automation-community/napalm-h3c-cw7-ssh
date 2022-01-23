Value MEMBER_ID (\d+)
Value PORT_ID (\d+)
Value List PORT_MEMBER (\S+)

Start
  ^# -> Continue.Record
  ^irf-port\s+${MEMBER_ID}/${PORT_ID}
  ^\s*port\s+group\s+interface\s+${PORT_MEMBER} -> Continue