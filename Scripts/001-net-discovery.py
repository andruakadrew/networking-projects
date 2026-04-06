import psutil
import socket


def discover_interfaces():
    """Discover and display all network interfaces and their addresses"""
    interfaces = psutil.net_if_addrs()

    print("=" * 50)
    print(" NETWORK INTERFACE DISCOVERY")
    print("=" * 50)
    print(f"\nTotal interfaces found: {len(interfaces)}")

    for iface_name, addresses in interfaces.items():
        print(f"\nInterface: {iface_name}")
        print("-" * 40)

        for addr in addresses:
            if addr.family == socket.AF_INET:
                print(f"    IPv4 Address  :  {addr.address}")
                print(f"    Netmask  :  {addr.netmask}")
                print(f"    Broadcast  :  {addr.broadcast}")
            elif addr.family == socket.AF_INET6:
                print(f"    IPv6 Address  :  {addr.address}")
                print(f"    Netmask  :  {addr.netmask}")
            elif addr.family == psutil.AF_LINK:
                print(f"    MAC Address  :  {addr.address}")


if __name__ == "__main__":
    discover_interfaces()
