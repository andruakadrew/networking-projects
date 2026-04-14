# 365 Days of Python Networking Scripts

A daily scripting challenge progressing from networking fundamentals to advanced enterprise automation. Each script is a real-world-applicable tool built to reinforce Python and networking concepts simultaneously.

**Author:** Andru Morales  
**GitHub:** [andruakadrew](https://github.com/andruakadrew)  
**Start Date:** April 6, 2026  


## About

This folder contains 365 Python scripts, that progressively build from foundational network discovery tools to advanced enterprise-grade automation. Scripts are cross-platform (Windows, macOS, Linux). Each level builds on previous concepts while introducing new ones.


## Progress Log

| Level | Script | Description | Date |
|-------|--------|-------------|------|
| 1 | `001-net-discovery.py` | Discover all local network interfaces, IPs, MACs, and subnet masks using psutil | 04/05/2026 |
| 2 | `002-interface-status.py` | Pulls the operational status, link speed, and live traffic counters for network interfaces  | 04/06/2026 |
| 3 | `003-network-report.py` | Combines levels 1 and 2 into a structured dictionary, exporting full reports into a JSON file  | 04/07/2026 |
| 4 | `004-dns-tool.py` | DNS Querying and reverse lookups for IPv4 addresses | 04/10/2026 |
| 5 | `005-subnetting-calculator.py` | Takes an IP address with CIDR notation and calculates the subnet | 04/11/2026 |
| 6 | `006-network-mapper.py` | Discover live host on a subnet by pinging usable addresses | 04/12/2026 |
| 7 | `007-vendor-lookup.py` | Takes in MAC addresses, extracts the OUI, and outputs the vendor by utilizing a local OUI database | 04/14/2026 |


## Dependencies

Dependencies are introduced as needed throughout the challenge. Install all current dependencies with:

```bash
pip install -r requirements.txt
```

| Package | First Used | Purpose |
|---------|------------|---------|
| `psutil` | Level 1 | Cross-platform system and network interface data |
| `dnspython` | Level 4 | High level functionality for simple DNS queries |
| `requests` | Level 7 | Allows HTTP transactions with web services |



## Environment

Scripts are developed and tested across:

- Windows 10/11 (PowerShell)
- macOS (Terminal)
- Linux / Debian-based (Bash)

Python version: 3.14
