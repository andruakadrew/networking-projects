# ============================================================
# Level 002 - Network Interface Status & Traffic Monitor
# ============================================================
# Pulls operational status (up/down), link speed, MTU, and
# live traffic counters (bytes, packets, errors, drops) for
# every network interface. Provides a snapshot of interface
# health and utilization similar to what feeds enterprise
# monitoring dashboards.
#
# Usage:
#   python level_002_interface_monitor.py
#
# Dependencies: psutil
# ============================================================


import psutil


def format_bytes(b):
    """Convert raw bytes to a human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024
    return f"{b:.2f} PB"


def monitor_interfaces():
    """Display status and traffic counters for all network interfaces."""
    stats = psutil.net_if_stats()
    io = psutil.net_io_counters(pernic=True)

    print("=" * 55)
    print("  NETWORK INTERFACE STATUS & TRAFFIC MONITOR")
    print("=" * 55)
    print(f"\nTotal interfaces: {len(stats)}")


    for iface_name, st in stats.items():
        counters = io.get(iface_name)
        status = "UP" if st.isup else "DOWN"

        print(f"\nInterface: {iface_name}")
        print("-" * 45)
        print(f"  Status  : {status}")
        print(f"  Speed   : {st.speed} Mbps")
        print(f"  MTU     : {st.mtu}")

        if counters:
            print(f"  Sent    : {format_bytes(counters.bytes_sent)}")
            print(f"  Recv    : {format_bytes(counters.bytes_recv)}")
            print(f"  Packets : {counters.packets_sent} sent / {counters.packets_recv} recv")
            print(f"  Errors  : {counters.errin} in / {counters.errout} out")
            print(f"  Drops   : {counters.dropin} in / {counters.dropout} out")
        else:
            print("  Traffic : No counter data available")



if __name__ == "__main__":
    monitor_interfaces()
