Value OS_VERSION (.*)
Value VENDOR (\S+)
Value MODEL (\S+)
Value UPTIME_WEEKS (\d+)
Value UPTIME_DAYS (\d+)
Value UPTIME_HOURS (\d+)
Value UPTIME_MINS (\d+)

Start
  ^.*Comware.*Version\s+[0-9\.]+,\s+${OS_VERSION}
  ^${VENDOR}\s+${MODEL}\s+uptime\s+is\s+${UPTIME_WEEKS}\s+week(s)?,\s+${UPTIME_DAYS}\s+day(s)?,\s+${UPTIME_HOURS}\s+hour(s)?,\s+${UPTIME_MINS}\s+minute(s)? -> Record