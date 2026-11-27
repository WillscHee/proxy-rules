#!/usr/bin/env python3
"""Extract domains from HaGeZi DoH-only list, removing Apple Private Relay entries.

Usage: update_doh.py <source-list.txt> <destination.txt>
"""
import sys

# Patterns to exclude (Apple Private Relay related)
EXCLUDE_PATTERNS = ["apple", "privaterelay", "appleid", "aaplimg", "applewebkit"]

# Exact domains to exclude
EXCLUDE_DOMAINS = {
    # Apple Private Relay
    "mask.icloud.com",
    "mask-h2.icloud.com",
    "mask-canary.icloud.com",
    # ControlD (can't block own service)
    "dns.controld.com",
    "doh.controld.com",
    "freedns.controld.com",
}


def extract_domains(lines):
    """Extract clean domains, excluding Apple Private Relay entries."""
    domains = set()
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue
        # Skip Apple Private Relay related entries
        if any(p in line.lower() for p in EXCLUDE_PATTERNS):
            continue
        # Skip exact domain exclusions
        if line.lower() in EXCLUDE_DOMAINS:
            continue
        domains.add(line.lower())
    return sorted(domains)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source-list.txt> <destination.txt>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        lines = f.readlines()
    domains = extract_domains(lines)
    header = [
        "# Title: DoH Bypass Whitelist (HaGeZi, minus Apple Private Relay)",
        "# Description: Domains that use encrypted DNS (DoH/DoT/DoQ). Whitelist these to prevent DNS bypass.",
        "# Source: https://hagezi-mirror.dnsbunker.org/wildcard/doh-onlydomains.txt",
        "# Auto-updated by GitHub Actions",
        "# Number of entries: " + str(len(domains)),
        "#",
        "",
    ]
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(header + domains) + "\n")
    print(f"wrote {len(domains)} domains to {dst}")


if __name__ == "__main__":
    main()
