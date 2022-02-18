Value INTERFACE (\S+)
Value List IP_ADDRESS (\d+(\.\d+){3}\/\d+)

Start
  ^\S+\s+current\s+state -> Continue.Record
  ^${INTERFACE}\s+current\s+state  
  ^Internet\s+Address\s+is\s+${IP_ADDRESS}\s+Primary -> Continue
  ^Internet\s+Address\s+is\s+${IP_ADDRESS}\s+Sub -> Continue