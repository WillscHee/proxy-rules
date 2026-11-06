#!/usr/bin/env python3
"""Generate sing-box source-format rule sets.

- lists/*.txt (bare domains, for Shadowrocket) -> lists/singbox/*.txt (domain-suffix:)
- AWAvenue geosite file -> lists/awavenue-ads.txt
  (bare -> domain-suffix:, full: -> domain:, keyword: -> domain-keyword:)

Hagezi is NOT generated here: sing-box subscribes the official
wildcard/pro.plus.mini-onlydomains.txt directly (bare domain = exact match,
which is the intended semantics for a wildcard DNS blocklist).

Run: python3 make_lists.py   (then git add -A && git commit && git push)
"""
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).parent
L = ROOT / "lists"
SB = L / "singbox"
SB.mkdir(exist_ok=True)

CATS = ["apple", "google", "youtube", "netflix", "primevideo",
        "disney", "social", "finance", "government", "isp", "own"]

for c in CATS:
    lines = [x.strip() for x in (L / f"{c}.txt").read_text().splitlines()
             if x.strip() and not x.startswith("#")]
    out = [f"domain-suffix:{x}" for x in lines]
    (SB / f"{c}.txt").write_text("\n".join(out) + "\n")
    print(f"singbox/{c}.txt: {len(out)} entries")

AWA = ("https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/"
       "main/Filters/AWAvenue-Ads-Rule-Geosite-Only.Ads.txt")
raw = urllib.request.urlopen(AWA, timeout=60).read().decode("utf-8", "replace")
out = []
for line in raw.splitlines():
    s = line.strip()
    if not s:
        continue
    if s.startswith("#"):
        out.append(s)
    elif s.startswith("full:"):
        out.append("domain:" + s[5:])
    elif s.startswith("keyword:"):
        out.append("domain-keyword:" + s[8:])
    else:
        out.append("domain-suffix:" + s)
(L / "awavenue-ads.txt").write_text("\n".join(out) + "\n")
print(f"awavenue-ads.txt: {len(out)} entries")
