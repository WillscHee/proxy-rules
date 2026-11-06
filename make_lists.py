#!/usr/bin/env python3
"""Generate sing-box JSON rule sets (format: "source", version 5).

New sing-box (>= main 2026-10) parses "source" rule sets as JSON:
    {"version": 5, "rules": [{"type": "default", "domain_suffix": [...]}]}

Generates:
- lists/*.txt (bare domains, for Shadowrocket) -> lists/singbox/*.json (domain_suffix)
- AWAvenue geosite file -> lists/awavenue-ads.json
  (bare -> domain_suffix, full: -> domain, keyword: -> domain_keyword)
- Hagezi official wildcard mini -> lists/hagezi-pro-plus-mini.json (exact domain)

Run: python3 make_lists.py   (then git add -A && git commit && git push)
"""
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).parent
L = ROOT / "lists"
SB = L / "singbox"
SB.mkdir(exist_ok=True)
SB114 = L / "singbox-v114"
SB114.mkdir(exist_ok=True)

VERSION = 5


def write_rs(path: pathlib.Path, rules):
    path.write_text(json.dumps({"version": VERSION, "rules": rules}, separators=(",", ":")))
    n = sum(len(v) for r in rules for v in r.values() if isinstance(v, list))
    print(f"{path.relative_to(ROOT)}: {n} entries, {path.stat().st_size} bytes")


def write_txt(path: pathlib.Path, lines):
    path.write_text("\n".join(lines) + "\n")
    print(f"{path.relative_to(ROOT)}: {len(lines)} lines, {path.stat().st_size} bytes")


CATS = ["apple", "google", "youtube", "netflix", "primevideo",
        "disney", "social", "finance", "government", "isp", "own"]

for c in CATS:
    lines = [x.strip() for x in (L / f"{c}.txt").read_text().splitlines()
             if x.strip() and not x.startswith("#")]
    write_rs(SB / f"{c}.json", [{"type": "default", "domain_suffix": lines}])
    # v1.14.x text source format: leading dot = suffix match
    write_txt(SB114 / f"{c}.txt", ["." + d if not d.startswith(".") else d for d in lines])

AWA = ("https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/"
       "main/Filters/AWAvenue-Ads-Rule-Geosite-Only.Ads.txt")
raw = urllib.request.urlopen(AWA, timeout=60).read().decode("utf-8", "replace")
suffix, exact, keyword = [], [], []
for line in raw.splitlines():
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    if s.startswith("full:"):
        exact.append(s[5:])
    elif s.startswith("keyword:"):
        keyword.append(s[8:])
    else:
        suffix.append(s)
rules = []
if suffix:
    rules.append({"type": "default", "domain_suffix": suffix})
if exact:
    rules.append({"type": "default", "domain": exact})
if keyword:
    rules.append({"type": "default", "domain_keyword": keyword})
write_rs(L / "awavenue-ads.json", rules)
# v1.14.x text: .suffix / exact / ~keyword
txt = ["." + s if not s.startswith(".") else s for s in suffix] + exact + ["~" + k for k in keyword]
write_txt(SB114 / "awavenue-ads.txt", txt)

HAGEZI = ("https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/"
          "wildcard/pro.plus.mini-onlydomains.txt")
raw = urllib.request.urlopen(HAGEZI, timeout=120).read().decode("utf-8", "replace")
domains = [x.strip() for x in raw.splitlines() if x.strip() and not x.startswith("#")]
write_rs(L / "hagezi-pro-plus-mini.json", [{"type": "default", "domain": domains}])
write_txt(SB114 / "hagezi-pro-plus-mini.txt", domains)
