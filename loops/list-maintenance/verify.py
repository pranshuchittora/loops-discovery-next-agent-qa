#!/usr/bin/env python3
"""
verify.py — the gate for the list-maintenance loop.

Reads candidate entries, checks each against five conditions, and prints the
survivors as awesome single-line entries grouped by category. Anything that
fails any check is dropped (not queued, not retried).

Usage:
    python verify.py candidates.json [--readme ../../README.md]

candidates.json format:
[
  {"name": "...", "url": "https://...", "desc": "...", "category": "Concepts & Guides", "found": "github topic"},
  ...
]

Exit code 0 always (the loop decides what to do with the output). Survivors are
printed to stdout as markdown; a JSON summary goes to stderr.
"""

import json
import re
import sys
import os
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, "..", "..", "README.md")
REJECTED = os.path.join(HERE, "rejected.txt")
SEEN = os.path.join(HERE, "seen.txt")
MAX_CANDIDATES = 8

VALID_CATEGORIES = {
    "Concepts & Guides", "Origin Posts & Talks", "Loop Patterns", "Templates",
    "Runtimes & Harnesses", "Scheduling & Triggers", "Verification & Guardrails",
    "State & Memory", "Cost Control", "Related Lists", "Communities",
}

LINE_RE = re.compile(r"^- \[.+\]\(https?://[^\)]+\) - .+\.$")


def load_lines(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def host(url):
    try:
        h = urlparse(url).netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


def host_in(h, text):
    """True if host h appears as a domain token in text (not as a substring of a longer domain)."""
    import re as _re
    return bool(_re.search(r"(^|[^a-z0-9.-])" + _re.escape(h) + r"([^a-z0-9.-]|$)", text))


def url_alive(url, timeout=10):
    """HTTP 200 after redirects. HEAD first, fall back to GET."""
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, method=method, headers={"User-Agent": "awesome-agent-loops-bot/1.0"})
            with urlopen(req, timeout=timeout) as resp:
                if 200 <= resp.status < 300:
                    return True
        except HTTPError as e:
            # some servers reject HEAD; let GET decide
            if method == "GET" and 200 <= e.code < 300:
                return True
        except (URLError, ValueError, TimeoutError):
            continue
    return False


def main():
    if len(sys.argv) < 2:
        print("usage: verify.py candidates.json", file=sys.stderr)
        sys.exit(0)

    with open(sys.argv[1], encoding="utf-8") as f:
        candidates = json.load(f)

    readme = load_lines(README).lower()
    rejected = load_lines(REJECTED).lower()
    seen = load_lines(SEEN).lower()

    survivors = []
    report = {"in": len(candidates), "passed": [], "dropped": []}

    for c in candidates:
        url = c.get("url", "").strip()
        name = c.get("name", "").strip()
        desc = c.get("desc", "").strip().rstrip(".") + "."
        cat = c.get("category", "").strip()
        h = host(url)
        line = f"- [{name}]({url}) - {desc}"

        reasons = []
        if not url or not name:
            reasons.append("missing url/name")
        if cat not in VALID_CATEGORIES:
            reasons.append(f"bad category '{cat}'")
        if h and host_in(h, readme):
            reasons.append("host already in README (dupe)")
        if h and host_in(h, rejected):
            reasons.append("host in rejected blacklist")
        if h and host_in(h, seen):
            reasons.append("already seen in a prior run")
        if not LINE_RE.match(line):
            reasons.append("bad awesome format")
        # network check last (slowest)
        if not reasons and not url_alive(url):
            reasons.append("URL not reachable (non-200)")

        if reasons:
            report["dropped"].append({"url": url, "why": reasons})
        else:
            survivors.append({"category": cat, "line": line, "url": url})
            report["passed"].append(url)

    # cap, keeping first MAX (caller should pre-sort by signal strength)
    survivors = survivors[:MAX_CANDIDATES]

    # group by category, print markdown
    by_cat = {}
    for s in survivors:
        by_cat.setdefault(s["category"], []).append(s["line"])
    for cat in sorted(by_cat):
        print(f"\n### {cat}")
        for line in by_cat[cat]:
            print(line)

    # append everything considered to seen.txt
    with open(SEEN, "a", encoding="utf-8") as f:
        for c in candidates:
            u = c.get("url", "").strip()
            if u:
                f.write(u + "\n")

    report["passed_count"] = len(survivors)
    print(json.dumps(report, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
