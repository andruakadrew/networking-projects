# 365 Days of Python Networking Scripts

A daily scripting challenge progressing from networking fundamentals to advanced enterprise automation. Each script is a real-world-applicable tool built to reinforce Python and networking concepts simultaneously.

**Author:** Andru Morales  
**GitHub:** [andruakadrew](https://github.com/andruakadrew)  
**Start Date:** April 6, 2026  
**Target Completion:** April 6, 2027  

---

## About

This folder contains 365 Python scripts, one written per day, that progressively build from foundational network discovery tools to advanced enterprise-grade automation. Scripts are cross-platform (Windows, macOS, Linux). Each level builds on previous concepts while introducing new ones.

---

## Progress Log

| Level | Script | Description | Date |
|-------|--------|-------------|------|
| 1 | `001-net-discovery.py` | Discover all local network interfaces, IPs, MACs, and subnet masks using psutil | 04/05/2026 |
| 2 | `002-interface-status.py` | Pulls the operational status, link speed, and live traffic counters for network interfaces  | 04/06/2026 |
| 3 | `003-network-report.py` | Combines levels 1 and 2 into a structured dictionary, exporting full reports into a JSON file  | 04/07/2026 |


---

## Dependencies

Dependencies are introduced as needed throughout the challenge. Install all current dependencies with:

```bash
pip install -r requirements.txt
```

| Package | First Used | Purpose |
|---------|------------|---------|
| `psutil` | Level 001 | Cross-platform system and network interface data |

---

## Environment

Scripts are developed and tested across:

- Windows 10/11 (PowerShell)
- macOS (Terminal)
- Linux / Debian-based (Bash)

Python version: 3.14
