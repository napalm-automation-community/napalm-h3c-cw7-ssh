Value Filldown CHASSIS_ID (\d+)
Value Required SLOT_TYPE (Slot|Subslot|Fan|Power|Chassis)
Value SLOT_ID (\d+|self)
Value DEVICE_NAME (\S+)
Value SERIAL_NUMBER (\S+)
Value MANUFACTURING_DATE (\S+)
Value VENDOR_NAME (\S+)
Value MAC_ADDRESS (\S+)


Start
  ^\s*Chassis\s+${CHASSIS_ID}
  ^\s*${SLOT_TYPE}\s+${SLOT_ID}
  # 一些旧版本的设备不显示 `Slot header`，所以使用 DEVICE_ID 来进行识别
  ^\s*DEVICE_ID\s*:\s*${SLOT_TYPE}\s+ID:\s*${SLOT_ID}
  # 一些风扇/电源模块不支持显示电子标签
  ^\s*The\s+operation\s+is\s+not\s+supported\s+ -> Record Start
  ^\s*DEVICE_NAME\s*:\s*${DEVICE_NAME}
  ^\s*DEVICE_SERIAL_NUMBER\s*:\s*${SERIAL_NUMBER}
  ^\s*MAC_ADDRESS\s*:\s*${MAC_ADDRESS}
  ^\s*MANUFACTURING_DATE\s*:\s*${MANUFACTURING_DATE}
  ^\s*VENDOR_NAME\s*:\s*${VENDOR_NAME} -> Record Start
  ^\s*$$
  ^. -> Error