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
from netmiko import ConnectHandler
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
)


MINUTE_SECONDS = 60
HOUR_SECONDS = 60 * MINUTE_SECONDS
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS


class ComwareDriver(NetworkDriver):
    """Napalm driver for HP/H3C Comware7 (using ssh)."""

    def __init__(
            self,
            hostname: str,
            username: str,
            password: str,
            timeout: int = 100,
            optional_args: Optional[Dict] = None):
        """
        :param hostname: (str) IP or FQDN of the device you want to connect to.
        :param username: (str) Username you want to use
        :param password: (str) Password
        :param timeout: (int) Time in seconds to wait for the device to respond.
        :param optional_args: (dict) Pass additional arguments to underlying driver
        :return:
        """
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

    def cli(self, commands: List):

        cli_output = dict()

        if type(commands) is not list:
            raise TypeError("Please enter a valid list of commands!")

        for command in commands:
            output = self.device.send_command(command)
            cli_output.setdefault(command, {})
            cli_output[command] = output

        return cli_output

    #
    def is_alive(self):
        if self.device is None:
            return {"is_alive": False}
        else:
            return {"is_alive": self.device.is_alive()}

    def _get_structured_output(self, command: str, template_name: str = None):
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
            # TODO: 更新一下 textfsm 模板，返回字符串再用 parse_time 解析
            uptime = (
                int(structured_sys_info.get("uptime_weeks")) * WEEK_SECONDS
                + int(structured_sys_info.get("uptime_days")) * DAY_SECONDS
                + int(structured_sys_info.get("uptime_hours")) * HOUR_SECONDS
                + int(structured_sys_info.get("uptime_mins")) * MINUTE_SECONDS
            )
            vendor = structured_sys_info.get("vendor")
            model = structured_sys_info.get("model")
            os_version = structured_sys_info.get("os_version")

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
    def get_vlans(self):
        vlans = {}
        command = "display vlan all"
        structured_output = self._get_structured_output(command)
        for vlan in structured_output:
            # 默认情况下 vlan_name == vlan_description
            #   1. 若两者都是默认值或都不是默认值，优先使用 vlan_name
            #   2. 若两者其中一个不是默认值，优先使用用户自定义的值（非默认值）
            vlan_name = vlan.get("name")
            vlan_desc = vlan.get("description")
            vlans[int(vlan.get("vlan_id"))] = {
                "name": vlan_desc if "VLAN " not in vlan_desc and "VLAN " in vlan_name else vlan_name,
                "interfaces": vlan.get("interfaces")
            }
        return vlans

    # ok
    def get_arp_table(self, vrf=""):
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

    # ok
    def get_interfaces(self):
        """
        """
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
            elif last_flapped == "":
                last_flapped = -1
            else:
                last_flapped = parse_time(last_flapped)

            interface_dict[interface.get("interface")] = {
                "is_enabled": is_enabled,
                "is_up": is_up,
                "description": description,
                "speed": -1 if speed == "" else int(speed),
                "mtu": -1 if mtu == "" else int(mtu),
                "mac_address": "unknown" if mac_address == "" else mac(mac_address),
                "last_flapped": last_flapped,
            }
        return interface_dict

    def is_irf(self):

        ...
