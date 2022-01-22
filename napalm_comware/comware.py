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

"""
Napalm driver for H3C ComwareV7 devices.

Read https://napalm.readthedocs.io for more information.
"""

from __future__ import print_function
from operator import itemgetter
from typing import Any, Optional, Dict, List
import re
from netmiko.hp.hp_comware import HPComwareBase
from napalm.base.base import NetworkDriver
from napalm.base.exceptions import (
    ConnectionClosedException,
    ConnectionException,
)
import napalm.base.constants as C
from napalm.base.helpers import (
    textfsm_extractor,
    mac,
)
from napalm.base.netmiko_helpers import netmiko_args
from .utils.helpers import (
    canonical_interface_name_comware,
    parse_time,
    parse_null,
)


class ComwareDriver(NetworkDriver):
    """Napalm driver for H3C/HP Comware7 network devices (using ssh)."""

    def __init__(
            self,
            hostname: str,
            username: str,
            password: str,
            timeout: int = 100,
            optional_args: Optional[Dict] = None):

        self.device = None
        if optional_args is None:
            optional_args = {}
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.netmiko_optional_args = netmiko_args(optional_args)

    def open(self):
        """Open a connection to the device."""
        device_type = "hp_comware"
        self.device: HPComwareBase = self._netmiko_open(
            device_type, netmiko_optional_args=self.netmiko_optional_args
        )

    def close(self):
        self._netmiko_close()

    def send_command(self, command, *args, **kwargs):
        return self.device.send_command(command, *args, **kwargs)

    #

    def is_alive(self):
        if self.device is None:
            return {"is_alive": False}
        else:
            return {"is_alive": self.device.is_alive()}

    def _get_structured_output(self, command: str, template_name: str = None):
        """
        Wrapper for `napalm.base.helpers.textfsm_extractor()`.
        """
        if template_name is None:
            template_name = "_".join(command.split())
        raw_output = self.send_command(command)
        result = textfsm_extractor(self, template_name, raw_output)
        return result

    # ok
    def get_facts(self):
        # default values.
        vendor = "Comware"
        uptime = -1
        serial_number, fqdn, os_version, hostname, fqdn = ("Unknown",) * 5

        # uptime、vender、model
        cmd_sys_info = "display version"
        structured_sys_info = self._get_structured_output(cmd_sys_info)
        if isinstance(structured_sys_info, list) and len(structured_sys_info) == 1:
            structured_sys_info = structured_sys_info[0]
            (uptime_str, vendor, model, os_version) = itemgetter(
                "uptime", "vendor", "model", "os_version"
            )(structured_sys_info)
            uptime = parse_time(uptime_str)

        # os_version. format: `Version.Patch`.
        # Example: "Release 2612P01.2612P01H03"
        # cmd_os_version = "display device"
        # structured_os_version = self._get_structured_output(cmd_os_version)

        # fqdn
        # show_domain = self.send_command("display dns domain")

        # hostname
        hostname = self.device.find_prompt()[1:-1]

        # interfaces
        interface_list = []
        structured_int_info = self._get_structured_output("display interface")
        for interface in structured_int_info:
            interface_list.append(interface.get("interface"))

        # serial number
        cmd_sn = "display device manuinfo"
        structured_sn = self._get_structured_output(cmd_sn)
        if isinstance(structured_sn, list) and len(structured_sn) > 0:
            serial_number = []
            for sn in structured_sn:
                if sn.get("slot_type") == "Slot":
                    # 解析结果为空则跳过记录
                    _sn = sn.get("serial_number")
                    if _sn != "":
                        serial_number.append(_sn)
            if len(serial_number) > 0:
                serial_number = ",".join(serial_number)
            else:
                serial_number = "Unknown"

        return {
            "uptime": uptime,
            "vendor": vendor,
            "os_version": os_version,
            "serial_number": serial_number,
            "model": model,
            "hostname": hostname,
            "fqdn": fqdn,
            "interface_list": interface_list,
        }

    # ok
    def get_interfaces(self):
        interface_dict = {}
        structured_int_info = self._get_structured_output("display interface")

        for interface in structured_int_info:
            # Physical state:
            #   - Administratively DOWN
            #   - DOWN
            #   - UP
            is_enabled = bool("up" in interface.get("link_status").lower())
            # Protocol state:
            #  - UP
            #  - UP (spoofing)
            #  - DOWN
            #  - DOWN(other protocol):such as DOWN(DLDP)、DOWN(LAGG) ...
            is_up = bool("up" in interface.get("protocol_status").lower())

            (description, speed, mtu, mac_address, last_flapped) = itemgetter(
                "description", "bandwidth", "mtu", "mac_address", "last_flapping",
            )(interface)

            # Never flapping: 0
            # No flapping data: -1
            # Last flapping: int(seconds)
            if "never" in last_flapped.lower():
                last_flapped = 0
            else:
                last_flapped = parse_null(last_flapped, -1, parse_time)

            interface_dict[interface.get("interface")] = {
                "is_enabled": is_enabled,
                "is_up": is_up,
                "description": description,
                "speed": parse_null(speed, -1, int),
                "mtu": parse_null(mtu, -1, int),
                "mac_address": parse_null(mac_address, "unknown", mac),
                "last_flapped": last_flapped,
            }
        return interface_dict

    def get_lldp_neighbors(self): ...

    def get_bgp_neighbors(self): ...

    def get_environment(self): ...

    def get_interfaces_counters(self):
        counters = {}
        keys = (
            "tx_errors", "rx_errors", "rx_crc",
            "tx_discards", "rx_discards",
            "tx_octets", "rx_octets",
            "tx_packets", "rx_packets",
            "tx_unicast_packets", "rx_unicast_packets",
            "tx_multicast_packets", "rx_multicast_packets",
            "tx_broadcast_packets", "rx_broadcast_packets",
        )
        structured_int_info = self._get_structured_output("display interface")

        for interface in structured_int_info:
            values = itemgetter(
                "tx_errors", "rx_errors", "rx_crc",
                "tx_aborts", "rx_aborts",
                "tx_bytes", "rx_bytes",
                "tx_pkts", "rx_pkts",
                "tx_unicast", "rx_unicast",
                "tx_multicast", "rx_multicast",
                "tx_broadcast", "rx_broadcast",
            )(interface)

            values = (parse_null(value, -1, int) for value in values)
            counters[interface.get("interface")] = dict(zip(keys, values))

        return counters

    def get_lldp_neighbors_detail(self, interface=""): ...

    def cli(self, commands: List):

        cli_output = dict()

        if type(commands) is not list:
            raise TypeError("Please enter a valid list of commands!")

        for command in commands:
            output = self.device.send_command(command)
            cli_output.setdefault(command, {})
            cli_output[command] = output

        return cli_output

    # ok

    def get_arp_table(self, vrf: str = ""):
        arp_table = []
        if vrf:
            command = "display arp vpn-instance %s" % (vrf)
        else:
            command = "display arp"
        structured_output = self._get_structured_output(command, "display_arp")
        for arp in structured_output:
            entry = {
                'interface': canonical_interface_name_comware(arp.get("interface")),
                'mac': mac(arp.get("mac_address")),
                'ip': arp.get("ip_address"),
                'age': arp.get("aging")
            }
            arp_table.append(entry)
        return arp_table

    def get_interfaces_ip(self): ...

    def get_mac_address_table(self): ...

    def get_route_to(self, destination="", protocol="", longer=False): ...

    def get_config(self, retrieve="all", full=False, sanitized=False): ...

    def get_network_instances(self, name=""): ...

    # ok
    def get_vlans(self):
        """
        Return structure being spit balled is as follows.
            * vlan_id (int)
                * name (text_type)
                * interfaces (list)

        By default, `vlan_name` == `vlan_description`. If both are default or not, \
        use `vlan_name`. If one of them is not the default value, use user-configured \
        value.

        Example::

            {
                1: {
                    "name": "default",
                    "interfaces": ["GigabitEthernet0/0/1", "GigabitEthernet0/0/2"]
                },
                2: {
                    "name": "vlan2",
                    "interfaces": []
                }
            }
        """
        vlans = {}
        command = "display vlan all"
        structured_output = self._get_structured_output(command)
        for vlan in structured_output:
            vlan_name = vlan.get("name")
            vlan_desc = vlan.get("description")
            vlans[int(vlan.get("vlan_id"))] = {
                "name": vlan_desc if "VLAN " not in vlan_desc and "VLAN " in vlan_name else vlan_name,
                "interfaces": vlan.get("interfaces")
            }
        return vlans

    def is_irf(self):
        """
        Returns True if the IRF is setup.
        """
        ...
