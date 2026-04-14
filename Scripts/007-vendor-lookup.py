# ============================================================
# Level 007 - MAC Address Vendor Lookup
# ============================================================
# Takes one or more MAC addresses and identifies the device
# manufacturer by looking up the OUI (first 3 bytes) against
# the IEEE OUI database. Downloads and caches the database
# locally for fast repeated lookups. Handles multiple MAC
# formats (colon, dash, dot, raw) and normalizes them.
#
# Usage:
#   python 007-mac_vendor.py 00:1A:2B:3C:4D:5E
#   python 007-mac_vendor.py DC-A6-32-11-22-33 001A.2B3C.4D5E
#   python 007-mac_vendor.py --update 00:1A:2B:3C:4D:5E
#
# Dependencies: requests
# ============================================================

import argparse
import os
import re
import sys
import requests

OUI_URL = "https://standards-oui.ieee.org/oui/oui.txt"
OUI_CACHE = os.path.join(os.path.expanduser("~"), ".oui_cache.txt")


def normalize_mac(mac):
    """Normalize a MAC address to uppercase colon-separated format."""
    mac_clean = re.sub(r"[.:\-]", "", mac.strip())

    if len(mac_clean) != 12 or not re.match(r"^[0-9A-Fa-f]{12}$", mac_clean):
        return None

    mac_upper = mac_clean.upper()
    return ":".join(mac_upper[i:i+2] for i in range(0, 12, 2))


def download_oui_database():
    """Download the IEEE OUI database and cache it locally."""
    print("  Downloading OUI database from IEEE...")
    try:
        response = requests.get(OUI_URL, timeout=30)
        response.raise_for_status()
        with open(OUI_CACHE, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"  Cached to {OUI_CACHE}")
        return True
    except requests.RequestException as e:
        print(f"  Error downloading OUI database: {e}")
        return False


def parse_oui_database():
    """Parse the cached OUI database into a dictionary."""
    oui_dict = {}

    if not os.path.exists(OUI_CACHE):
        if not download_oui_database():
            return oui_dict

    with open(OUI_CACHE, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(
                r"^\s*([0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2})\s+\(hex\)\s+(.+)$",
                line
            )
            if match:
                oui = match.group(1).replace("-", ":").upper()
                vendor = match.group(2).strip()
                oui_dict[oui] = vendor

    return oui_dict


def lookup_mac(mac, oui_dict):
    """Look up the vendor for a given MAC address."""
    normalized = normalize_mac(mac)

    if not normalized:
        return {"mac": mac, "normalized": None, "vendor": None, "error": "Invalid MAC address format"}

    oui_prefix = normalized[:8]
    vendor = oui_dict.get(oui_prefix)

    return {
        "mac": mac,
        "normalized": normalized,
        "oui": oui_prefix,
        "vendor": vendor if vendor else "Unknown vendor"
    }


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="MAC Address Vendor Lookup - Identify device manufacturers from MAC addresses"
    )
    parser.add_argument(
        "macs",
        nargs="+",
        help="One or more MAC addresses to look up"
    )
    parser.add_argument(
        "-u", "--update",
        action="store_true",
        help="Force re-download of the OUI database"
    )
    return parser.parse_args()


def display_results(results):
    """Display lookup results."""
    print("=" * 60)
    print("  MAC ADDRESS VENDOR LOOKUP")
    print("=" * 60)

    for result in results:
        print()
        if "error" in result:
            print(f"  Input  : {result['mac']}")
            print(f"  Error  : {result['error']}")
        else:
            print(f"  Input  : {result['mac']}")
            print(f"  Normal : {result['normalized']}")
            print(f"  OUI    : {result['oui']}")
            print(f"  Vendor : {result['vendor']}")

    print()
    print(f"  Total lookups: {len(results)}")


if __name__ == "__main__":
    args = parse_args()

    if args.update and os.path.exists(OUI_CACHE):
        os.remove(OUI_CACHE)
        print("  Cleared cached OUI database.")

    print("  Loading OUI database...")
    oui_dict = parse_oui_database()

    if not oui_dict:
        print("  Error: Could not load OUI database.")
        sys.exit(1)

    print(f"  Loaded {len(oui_dict)} vendor entries.\n")

    results = [lookup_mac(mac, oui_dict) for mac in args.macs]
    display_results(results)