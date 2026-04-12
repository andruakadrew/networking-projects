# ============================================================
# Level 006 - Ping Sweep Tool
# ============================================================
# Discovers live hosts on a subnet by pinging every usable
# address in the given CIDR range. Uses multithreading to
# sweep hosts concurrently for speed. Reports which hosts
# responded and provides a summary with scan duration.
#
# Usage:
#   python level_006_ping_sweep.py 192.168.1.0/24
#   python level_006_ping_sweep.py 10.0.0.0/22 -w 100 -t 2
#
# Dependencies: None (uses standard library modules)
# ============================================================

import ipaddress
import subprocess
import platform
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Ping Sweep Tool - Discover live hosts on a subnet"
    )
    parser.add_argument(
        "network",
        help="Target subnet in CIDR notation (e.g., 192.168.1.0/24)"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=50,
        help="Number of concurrent threads (default: 50)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds (default: 1)"
    )
    return parser.parse_args()


def ping_host(ip, timeout):
    """Ping a single host and return the result."""
    os_type = platform.system().lower()

    if os_type == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), str(ip)]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), str(ip)]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return {
            "ip": str(ip),
            "alive": result.returncode == 0
        }
    except Exception as e:
        return {
            "ip": str(ip),
            "alive": False,
            "error": str(e)
        }


def sweep_network(network, workers, timeout):
    """Ping all hosts in a subnet using concurrent threads."""
    hosts = list(network.hosts())
    results = {"alive": [], "dead": [], "total": len(hosts)}

    print(f"\n  Sweeping {len(hosts)} hosts with {workers} threads...")
    print(f"  Timeout: {timeout}s per host\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(ping_host, host, timeout): host
            for host in hosts
        }

        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()

            if result["alive"]:
                results["alive"].append(result["ip"])
                print(f"  [+] {result['ip']} is UP")
            else:
                results["dead"].append(result["ip"])

            if completed % 50 == 0 or completed == len(hosts):
                pct = (completed / len(hosts)) * 100
                print(f"  ... {completed}/{len(hosts)} ({pct:.0f}%) complete")

    results["alive"].sort(key=lambda ip: ipaddress.ip_address(ip))
    return results


def display_results(network, results, duration):
    """Display sweep results summary."""
    print("\n" + "=" * 55)
    print("  PING SWEEP RESULTS")
    print("=" * 55)
    print(f"  Target Network : {network}")
    print(f"  Hosts Scanned  : {results['total']}")
    print(f"  Hosts Alive    : {len(results['alive'])}")
    print(f"  Hosts Down     : {len(results['dead'])}")
    print(f"  Sweep Duration : {duration:.2f} seconds")
    print("-" * 55)

    if results["alive"]:
        print(f"\n  Live Hosts:")
        for ip in results["alive"]:
            print(f"    {ip}")
    else:
        print("\n  No live hosts found.")


if __name__ == "__main__":
    args = parse_args()

    try:
        network = ipaddress.ip_network(args.network, strict=False)
    except ValueError as e:
        print(f"  Error: {e}")
        print("  Use CIDR notation like: 192.168.1.0/24")
        exit(1)

    host_count = network.num_addresses - 2
    if host_count > 1024:
        confirm = input(
            f"\n  Warning: {host_count} hosts to scan. Continue? (y/n): "
        )
        if confirm.lower() != "y":
            print("  Sweep cancelled.")
            exit(0)

    start = datetime.now()
    results = sweep_network(network, args.workers, args.timeout)
    duration = (datetime.now() - start).total_seconds()

    display_results(network, results, duration)