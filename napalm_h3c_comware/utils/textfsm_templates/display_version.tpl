Value OS_VERSION (.*)
Value VENDOR (\S+)
Value MODEL (\S+)
Value UPTIME (.*)

Start
  ^.*Comware.*Version\s+[0-9\.]+,\s+${OS_VERSION}
  ^${VENDOR}\s+${MODEL}\s+uptime\s+is\s+${UPTIME} -> Record