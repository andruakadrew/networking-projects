# ============================================================
# Level 005 - Subnet Calculator
# ============================================================
# Takes an IP address in CIDR notation and calculates all
# relevant subnet details: network/broadcast addresses,
# subnet and wildcard masks, usable host range, total hosts,
# and a binary breakdown showing the network/host bit boundary.
# Includes an optional membership check to verify whether a
# specific IP falls within the given subnet.
#
# Usage:
#   python level_005_subnet_calculator.py 192.168.1.50/24
#   python level_005_subnet_calculator.py 10.0.4.0/22 --check 10.0.5.37
#
# Dependencies: None (uses standard library ipaddress module)
# ============================================================


import argparse
import ipaddress


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Subnet Calculator - Compute network details from CIDR notation"
    )
    parser.add_argument(
        "network",
        help="IP address in CIDR notation (e.g., 192.168.1.0/24)"
    )
    parser.add_argument(
        "-c", "--check",
        help="Check if this IP address belongs to the subnet",
        default=None
    )
    return parser.parse_args()


def calculate_subnet(cidr_input):
    """Calculate all subnet details from a CIDR notation input."""
    network = ipaddress.ip_network(cidr_input, strict=False)

    subnet_info = {
        "input": cidr_input,
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "subnet_mask": str(network.netmask),
        "wildcard_mask": str(network.hostmask),
        "prefix_length": network.prefixlen,
        "total_addresses": network.num_addresses,
        "usable_hosts": max(network.num_addresses - 2, 0),
        "first_host": None,
        "last_host": None,
        "is_private": network.is_private,
        "version": network.version
    }

    hosts = list(network.hosts())
    if hosts:
        subnet_info["first_host"] = str(hosts[0])
        subnet_info["last_host"] = str(hosts[-1])

    return subnet_info


def get_binary_breakdown(cidr_input):
    """Show the binary representation of the IP and subnet mask."""
    network = ipaddress.ip_network(cidr_input, strict=False)
    ip = ipaddress.ip_address(cidr_input.split("/")[0])

    ip_octets = str(ip).split(".")
    mask_octets = str(network.netmask).split(".")

    ip_binary = ".".join(f"{int(octet):08b}" for octet in ip_octets)
    mask_binary = ".".join(f"{int(octet):08b}" for octet in mask_octets)

    prefix = network.prefixlen
    ip_flat = ip_binary.replace(".", "")
    separator = " " * prefix + "|" + " " * (32 - prefix)
    separator = ".".join(
        separator[i:i+8] for i in range(0, 32, 8)
    )

    return ip_binary, mask_binary, separator


def check_membership(cidr_input, check_ip):
    """Check if a given IP address belongs to the subnet."""
    try:
        network = ipaddress.ip_network(cidr_input, strict=False)
        ip = ipaddress.ip_address(check_ip)
        return {
            "ip": check_ip,
            "belongs": ip in network,
            "network": str(network)
        }
    except ValueError as e:
        return {"ip": check_ip, "error": str(e)}


def display_results(info, binary, membership=None):
    """Display all subnet calculation results."""
    ip_bin, mask_bin, separator = binary

    print("=" * 58)
    print("  SUBNET CALCULATOR")
    print("=" * 58)
    print(f"  Input           : {info['input']}")
    print(f"  IP Version      : IPv{info['version']}")
    print(f"  Private Address : {'Yes' if info['is_private'] else 'No'}")
    print("-" * 58)

    print(f"  Network Address : {info['network_address']}")
    print(f"  Broadcast Addr  : {info['broadcast_address']}")
    print(f"  Subnet Mask     : {info['subnet_mask']}")
    print(f"  Wildcard Mask   : {info['wildcard_mask']}")
    print(f"  CIDR Prefix     : /{info['prefix_length']}")
    print("-" * 58)

    print(f"  Total Addresses : {info['total_addresses']}")
    print(f"  Usable Hosts    : {info['usable_hosts']}")
    if info["first_host"]:
        print(f"  Host Range      : {info['first_host']} - {info['last_host']}")
    else:
        print(f"  Host Range      : N/A (no usable hosts)")
    print("-" * 58)

    print(f"\n  Binary Breakdown")
    print(f"  IP Address  : {ip_bin}")
    print(f"  Subnet Mask : {mask_bin}")
    print(f"  Net | Host  : {separator}")

    if membership:
        print(f"\n  Membership Check")
        print("-" * 58)
        if "error" in membership:
            print(f"  Error: {membership['error']}")
        else:
            status = "BELONGS" if membership["belongs"] else "DOES NOT BELONG"
            print(f"  {membership['ip']} {status} to {membership['network']}")


if __name__ == "__main__":
    args = parse_args()

    try:
        info = calculate_subnet(args.network)
        binary = get_binary_breakdown(args.network)

        membership = None
        if args.check:
            membership = check_membership(args.network, args.check)

        display_results(info, binary, membership)

    except ValueError as e:
        print(f"Error: {e}")
        print("Use CIDR notation like: 192.168.1.0/24")
