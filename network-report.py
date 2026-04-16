import psutil
import socket
import json
from datetime import datetime


def format_bytes(b):
    """Convert raw bytes to a human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024
    return f"{b:.2f} PB"


def get_address_info():
    """Collect address information for all interfaces."""
    result = {}
    interfaces = psutil.net_if_addrs()

    for iface_name, addresses in interfaces.items():
        iface_addrs = {"ipv4": [], "ipv6": [], "mac": None}

        for addr in addresses:
            if addr.family == socket.AF_INET:
                iface_addrs["ipv4"].append({
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            elif addr.family == socket.AF_INET6:
                iface_addrs["ipv6"].append({
                    "address": addr.address,
                    "netmask": addr.netmask
                })
            elif addr.family == psutil.AF_LINK:
                iface_addrs["mac"] = addr.address

        result[iface_name] = iface_addrs

    return result


def get_status_info():
    """Collect status and traffic data for all interfaces."""
    result = {}
    stats = psutil.net_if_stats()
    io = psutil.net_io_counters(pernic=True)

    for iface_name, st in stats.items():
        counters = io.get(iface_name)

        iface_info = {
            "is_up": st.isup,
            "speed_mbps": st.speed,
            "mtu": st.mtu,
            "traffic": None
        }

        if counters:
            iface_info["traffic"] = {
                "bytes_sent": counters.bytes_sent,
                "bytes_recv": counters.bytes_recv,
                "bytes_sent_fmt": format_bytes(counters.bytes_sent),
                "bytes_recv_fmt": format_bytes(counters.bytes_recv),
                "packets_sent": counters.packets_sent,
                "packets_recv": counters.packets_recv,
                "errors_in": counters.errin,
                "errors_out": counters.errout,
                "drops_in": counters.dropin,
                "drops_out": counters.dropout
            }

        result[iface_name] = iface_info

    return result


def build_report():
    """Merge address and status data into a single report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    addresses = get_address_info()
    status = get_status_info()

    report = {
        "report_timestamp": timestamp,
        "hostname": socket.gethostname(),
        "interfaces": {}
    }

    all_ifaces = set(list(addresses.keys()) + list(status.keys()))

    for iface_name in sorted(all_ifaces):
        report["interfaces"][iface_name] = {
            "addresses": addresses.get(iface_name, {}),
            "status": status.get(iface_name, {})
        }

    return report

def save_report(report):
    """Save the report to a timestamped JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"net_report_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    return filename


def print_summary(report):
    print("=" * 55)
    print("  NETWORK REPORT SUMMARY")
    print("=" * 55)
    print(f"  Host      : {report['hostname']}")
    print(f"  Timestamp : {report['report_timestamp']}")
    print(f"  Interfaces: {len(report['interfaces'])}")
    print("-" * 55)

    for name, data in report["interfaces"].items():
        status_info = data.get("status", {})
        is_up = status_info.get("is_up", False)
        status = "UP" if is_up else "DOWN"

        addr_info = data.get("addresses", {})
        ipv4_list = addr_info.get("ipv4", [])
        ip = ipv4_list[0]["address"] if ipv4_list else "N/A"

        print(f"  {name:<30} {status:<6} {ip}")


if __name__ == "__main__":
    report = build_report()
    print_summary(report)
    filename = save_report(report)
    print(f"\nFull report saved to: {filename}")
