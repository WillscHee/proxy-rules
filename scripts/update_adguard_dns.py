#!/usr/bin/env python3
"""Extract domains from AdGuard SDNS Filter into a domains-only list.

Usage: update_adguard_dns.py <source-filter.txt> <destination.txt>
"""
import re
import sys


def extract_domains(lines):
    """Extract clean domains from AdGuard filter rules."""
    domains = set()
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith("!"):
            continue
        # Remove rule modifiers after ^
        if "^" in line:
            line = line.split("^")[0]
        # Remove || prefix
        if line.startswith("||"):
            line = line[2:]
        line = line.strip()
        if not line:
            continue
        # Skip IP addresses
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", line):
            continue
        # Skip lines without a dot (not valid domains for our purpose)
        if "." not in line:
            continue
        domains.add(line.lower())
    return sorted(domains)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source-filter.txt> <destination.txt>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        lines = f.readlines()
    domains = extract_domains(lines)
    header = [
        "! Title: AdGuard DNS Filters - Domains Only",
        "! Description: Extracted domains from AdGuard SDNS Filter (DNS-level ad blocking)",
        "! Source: https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
        "! Auto-updated by GitHub Actions",
        "! Number of entries: " + str(len(domains)),
        "!",
        "",
    ]
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(header + domains) + "\n")
    print(f"wrote {len(domains)} domains to {dst}")


if __name__ == "__main__":
    main()
