#!/usr/bin/env python3
"""Extract CN/NA DoH domains from HaGeZi DoH-only list.

Filters to China & North America only:
- CN/NA TLDs: .cn .us .ca .hk .tw .mx
- Known CN/NA DoH providers (Cloudflare, Google, Quad9, OpenDNS, NextDNS,
  AdGuard, Aliyun, Tencent, Baidu, NetEase, Huawei, JD, Tsinghua, etc.)
- Excludes Apple Private Relay, ControlD, and non-CN/NA regions

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

# CN/NA TLDs
CN_NA_TLDS = {".cn", ".us", ".ca", ".hk", ".tw", ".mx"}

# Known CN/NA DoH resolver base domains (exact or subdomain match)
KNOWN_PROVIDERS = {
    # Cloudflare
    "cloudflare-dns.com", "cloudflare.com", "cloudflaredns.com",
    "cloudflareresolve.com", "cloudflare-gateway.com", "cloudflareclient.com",
    # Google
    "dns.google", "google-public-dns-a.google.com", "google-public-dns-b.google.com",
    # Quad9
    "quad9.net",
    # OpenDNS
    "opendns.com",
    # NextDNS
    "nextdns.io",
    # AdGuard (official only)
    "adguard.com", "adguard-dns.com", "adguarddns.com",
    # Aliyun
    "aliyun.com", "alidns.com", "aliyuncs.com", "aliyunhttpdns.com",
    # DNSPod (Tencent)
    "dnspod.com",
    # Baidu
    "baidu.com", "baidubce.com", "microbaidu.com",
    # NetEase
    "netease.com", "163.com",
    # Huawei
    "huaweicloud.com", "dbankcloud.cn", "dbankedge.cn",
    # QQ/Tencent
    "qq.com", "wechat.com", "weixin.qq.com", "wechatpay.cn",
    # JD
    "jd.com",
    # Tsinghua
    "tsinghua.edu.cn",
    # 360
    "360.cn",
    # Canadian Shield
    "cira.ca",
    # dnscrypt.ca
    "dnscrypt.ca",
    # UltraDNS (Oracle US)
    "ultradns.com",
    # Comodo
    "dnsbycomodo.com",
    # Fastly (US)
    "fastly-edge.com",
    # Oracle Cloud US
    "oraclecloud.com",
    # IBM Cloud US
    "ibmcloud.com",
}

# Exclude non-CN/NA regions even if provider is global
EXCLUDE_REGIONS = ["eu-", "europe", "london", "frankfurt", "berlin", "paris", "amsterdam"]


def is_cn_na(domain):
    """Check if domain is China or North America related."""
    # Exclude non-CN/NA regions
    if any(r in domain for r in EXCLUDE_REGIONS):
        return False
    # TLD match
    for tld in CN_NA_TLDS:
        if domain.endswith(tld):
            return True
    # Known provider base domain match (exact or subdomain)
    for base in KNOWN_PROVIDERS:
        if domain == base or domain.endswith("." + base):
            return True
    return False


def extract_domains(lines):
    """Extract clean CN/NA domains, excluding Apple Private Relay entries."""
    domains = set()
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue
        domain = line.lower()
        # Skip Apple Private Relay related entries
        if any(p in domain for p in EXCLUDE_PATTERNS):
            continue
        # Skip exact domain exclusions
        if domain in EXCLUDE_DOMAINS:
            continue
        # CN/NA filter
        if not is_cn_na(domain):
            continue
        domains.add(domain)
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
        "# Title: DoH Bypass Whitelist - China & North America",
        "# Description: DoH/DoT/DoQ endpoints in CN/NA. Whitelist to prevent DNS bypass.",
        "# Source: https://hagezi-mirror.dnsbunker.org/wildcard/doh-onlydomains.txt",
        "# Filtered: CN/NA TLDs (.cn/.us/.ca/.hk/.tw/.mx) + known CN/NA providers",
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
