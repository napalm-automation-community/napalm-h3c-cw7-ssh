# Copyright 2022 Eric Wu. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Helper functions for the ComwareDriver."""

from napalm.base.helpers import canonical_interface_name

comware_interfaces = {
    "XGE": "Ten-GigabitEthernet",
    "MGE": "M-GigabitEthernet",
    "Vlan": "Vlan-interface",
    "BAGG": "Bridge-Aggregation",
    "RAGG": "Route-Aggregation",
    "Loop": "LoopBack",
    "FGE": "FortyGigE",
    "Ser": "Serial",
    "Dia": "Dialer",
    "Reth": "Reth",
    
}

def canonical_interface_name_comware(interface):
    return canonical_interface_name(
        interface = interface, 
        addl_name_map = comware_interfaces,
        )
