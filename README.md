# Network Automation Scripts

A collection of Python automation scripts built to streamline network monitoring, device management, and operational tasks for network engineering and NOC environments. 

## Scripts

| Script | Description |
|---|---|
| [network-interfaces](./network-interfaces.py) | Discovers all network interfaces on the local machine and reports their names, IPv4/IPv6 addresses, MAC addresses, and subnet masks. |
| [interface-status](./interface-status.py) | Pulls operational status, link speed, MTU, and live traffic counters. |
| [network-report](./network-report.py) | Merges interface address data and status into a formatted JSON report. |
| [ping](./ping.py) | Reads a list of IP addresses from ```ips.txt``` and determines if the host are reachable by using _ping_. |
| [ping-trace](./ping-trace.py) | Reads a list of IP addresses from ```devices.txt``` and use tracert to track the path a packet takes to it's destination. Results for each address are assigned to a _.txt_ report  |



