# napalm-h3c-cw7-ssh

![](https://img.shields.io/pypi/v/napalm-h3c-comware?style=flat-square)
![](https://img.shields.io/pypi/pyversions/napalm-h3c-comware?style=flat-square)
![](https://img.shields.io/pypi/dm/napalm-h3c-comware?style=flat-square)

[English](README.md) | [中文](README_CN.md)

本仓库同步发布在 https://github.com/napalm-automation-community/napalm-h3c-cw7-ssh 

## NAPALM

[NAPALM](https://github.com/napalm-automation/napalm) (Network Automation and Programmability Abstraction Layer with Multivendor support) 是一个实现了使用统一的 API 来与多厂商网络设备交换的 Python 库。它支持使用多种方法来连接到设备、操作设备、读取数据等。


## napalm-h3c-cw7-ssh

`napalm-h3c-cw7-ssh` 是一个基于 SSH 的 H3C Comware V7 的网络设备驱动，是 Netmiko 的高级封装。

# 支持的设备

本驱动支持 S5100、S5500、S6800、S12500 等系列的数据中心交换机，一些功能也适用于路由器设备。

一般来说，只要是 V7 的设备都支持，期待你的测试和反馈 :)。


# 支持的功能

- :white_check_mark: is_alive()：检查当前是否与设备连接
- :white_check_mark: get_facts()：获取设备基础信息，如型号、软件版本、序列号等
- :white_check_mark: get_interfaces()：获取所有接口列表
- :white_check_mark: get_interfaces_ip()：获取当前存在 IP 地址的接口列表，目前只支持 IPv4
- :white_check_mark: get_interfaces_counters()：获取接口的计数信息，包括收发包、收发字节、错包、丢包、CRC 等
- :white_check_mark: get_lldp_neighbors()：获取 LLDP 邻居信息
- :white_check_mark: get_lldp_neighbors_detail()：获取 LLDP 的详细信息，包括对端的系统名称及描述、接口名称及描述等
- :white_check_mark: get_environment()：获取设备运行信息，包括 CPU、内存、电源、风扇、温度等状态
- :white_check_mark: cli()：在设备上执行命令
- :white_check_mark: get_arp_table()：获取 ARP 表
- :white_check_mark: get_mac_address_move_table()：获取 MAC 地址漂移表
- :white_check_mark: get_mac_address_table()：获取 MAC 地址表
- :white_check_mark: get_vlans()：获取 VLAN 信息，包括 VLAN 及其成员接口
- :white_check_mark: get_config()：获取设备配置，包括运行时配置和启动配置
- :white_check_mark: get_irf_config()：获取 IRF 配置信息
- :white_check_mark: is_irf()：判断是否为 IRF 设备


# 快速开始

## 安装

```shell
pip install napalm-h3c-comware
```

## 升级

```shell
pip install napalm-h3c-comware -U
```

## 使用

简单使用：

```python
from napalm import get_network_driver

driver = get_network_driver("h3c_comware")
driver = driver("192.168.56.20", "netdevops", "NetDevops@01",)
driver.open()
ret = driver.is_alive()
print(ret)
```

如果需要自定义连接参数，例如连接到设备的 SSH 端口, 请使用 `optional_args` 参数，它支持 netmiko 初始化时的所有参数：

```python
from napalm import get_network_driver

driver = get_network_driver("h3c_comware")
conn_args = {
    "port": 2222
}
driver = driver("192.168.56.21", "netdevops", "NetDevops@01",optional_args=conn_args)
driver.open()
ret = driver.is_alive()
print(ret)
```

如果需要通过原生的 netmiko 来执行命令，可以使用 `send_command`, 它和 `netmiko.send_command` 完全一样，支持所有参数：

```python
from napalm import get_network_driver

driver = get_network_driver("h3c_comware")
driver = driver("192.168.56.20", "netdevops", "NetDevops@01",)
driver.open()
# you can use any options that supported by netmiko.send_command
ret = driver.send_command("display clock", use_textfsm=True)
print(ret)
```