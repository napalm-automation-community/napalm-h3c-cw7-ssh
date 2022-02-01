Value Filldown LOCAL_INTERFACE (\S+)
Value Required INDEX (\d+)
Value REMOTE_UPTIME (.*)
Value REMOTE_CHASSIS_ID (.*)
Value REMOTE_PORT (.*)
Value REMOTE_PORT_DESC (.*)
Value REMOTE_SYSTEM_NAME (.*)
Value List REMOTE_SYSTEM_DESC (.*)
Value REMOTE_SYSTEM_CAPAB (.*)
Value REMOTE_SYSTEM_ENABLED_CAPAB (.*)

Start
  ^The\s+LLDP\s+service\s+is\s+not\s+running -> EOF
  ^There\s+is\+no\s+neighbor -> EOF
  ^LLDP\s+neighbor-information\s+of\s+port\s+\d+\[${LOCAL_INTERFACE}\]
  ^\s*LLDP\s+neighbor\s+index\s+:\s+${INDEX}
  ^\s*Update\s+time\s+:\s*${REMOTE_UPTIME}
  ^\s*Chassis\s+ID\s+:\s+${REMOTE_CHASSIS_ID}
  ^\s*Port\s+ID\s+:\s+${REMOTE_PORT}
  ^\s*Port\s+description\s+:\s+${REMOTE_PORT_DESC}
  ^\s*System\s+name\s+:\s+${REMOTE_SYSTEM_NAME}
  ^\s*System\s*description\s+:\s+${REMOTE_SYSTEM_DESC} -> Continue
  ^\s{3,}${REMOTE_SYSTEM_DESC} -> Continue
  ^\s*System\s+capabilities\s+supported\s+:\s+${REMOTE_SYSTEM_CAPAB}
  ^\s*System\s+capabilities\s+enabled\s+:\s+${REMOTE_SYSTEM_ENABLED_CAPAB} -> Record Start