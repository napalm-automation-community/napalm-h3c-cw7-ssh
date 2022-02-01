# napalm-h3c-cw7-ssh

## NAPALM

[NAPALM](https://github.com/napalm-automation/napalm) (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python library that implements a set of functions to interact with different router vendor devices using a unified API.

NAPALM supports several methods to connect to the devices, to manipulate configurations or to retrieve data.

## napalm-h3c-cw7-ssh

NAPALM driver for H3C Comware V7 network devices, over ssh.

# Supported devices

S5100、S5500、S6800、S12500 Series Data Center Switches.

# Supported functions

- :white_check_mark: is_alive()
- :white_check_mark: get_facts()
- :white_check_mark: get_interfaces()
- :white_check_mark: get_lldp_neighbors()
- :white_check_mark: get_environment()
- :white_check_mark: get_interfaces_counters()
- :white_check_mark: get_lldp_neighbors_detail()
- :white_check_mark: cli()
- :white_check_mark: get_arp_table()
- :white_check_mark: get_mac_address_move_table()
- :white_check_mark: get_mac_address_table()
- :white_check_mark: get_vlans()
- :white_check_mark: get_config()
- :white_check_mark: get_interfaces()
- :white_check_mark: get_irf_config()
- :white_check_mark: is_irf()


# Getting Started

## Install

```shell
pip install napalm-h3c-comware
```

## Upgrading

```shell
pip install napalm-h3c-comware -U
```

## Use

```python
from napalm import get_network_driver

driver = get_network_driver("h3c_comware")
driver = driver("192.168.56.20", "netdevops", "NetDevops@01",)
driver.open()
ret = driver.is_alive()
print(ret)
```