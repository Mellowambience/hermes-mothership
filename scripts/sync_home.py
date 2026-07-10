#!/usr/bin/env python3
"""
sync_home.py — keep the Hermes Mothership home self-aware.

Offline. No cloud, no vendor account. Two jobs:

  1. DOCK DRIFT  — for every build under builds/<slug>/SKILL.md, find the
     matching live skill (by name) and compare content. If the live skill
     changed but the docked copy didn't, flag STALE (re-dock needed).
  2. CONSTITUTIONAL REVIEW — grep the home for vendor lock-in signals.

Emits a human report + a machine line `HOME_STATUS: CLEAN|DRIFT ...`.
Exit 0 = clean, 1 = drift (so a cron can detect and report).

Usage:
    python sync_home.py [--home /path/to/hermes-mothership] [--skills /path/to/skills]
"""
import argparse
import hashlib
import os
import re
import sys
from datetime import datetime, timezone

DEFAULT_HOME = r"C:\Users\nator\hermes-mothership"
LOCKIN_SIGNALS = [
    "cdnjs.cloudflare.com", "unpkg.com", "cdn.jsdelivr.net", "jsdelivr.net",
    "anthropic.com", "openai.com", "googleapis.com", "vercel.app",
    "vercel.com",
]
SYNC_EXTS = (".md", ".html", ".py", ".js", ".ts", ".json",
             ".yaml", ".yml", ".css", ".toml")


def find_skills(skills_root):
    """Walk the skills tree; return {name: (relpath, abs_path, description)}."""
    found = {}
    if not skills_root or not os.path.isdir(skills_root):
        return found
    for root, _dirs, files in os.walk(skills_root):
        if "SKILL.md" not in files:
            continue
        p = os.path.join(root, "SKILL.md")
        try:
            txt = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        name = re.search(r"^name:\s*(.+)$", txt, re.M)
        desc = re.search(r"^description:\s*(.+)$", txt, re.M)
        nm = name.group(1).strip() if name else os.path.basename(root)
        ds = desc.group(1).strip() if desc else ""
        found[nm] = (os.path.relpath(root, skills_root), p, ds)
    return found


def sha(path):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()
    except Exception:
        return None


def docked_builds(home):
    """Return list of (slug, build_dir) for each builds/<slug>/ with a SKILL.md."""
    out = []
    bd = os.path.join(home, "builds")
    if not os.path.isdir(bd):
        return out
    for slug in sorted(os.listdir(bd)):
        d = os.path.join(bd, slug)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "SKILL.md")):
            out.append((slug, d))
    return out


def constitutional_review(home):
    hits = []
    for root, dirs, files in os.walk(home):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            if not f.endswith(SYNC_EXTS):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, home)
            # The home's own governance tooling DEFINES the lock-in veto;
            # it is not a deliverable and must never self-flag.
            if rel.startswith("scripts" + os.sep) or f == "repo_to_wiki.py":
                continue
            try:
                lines = open(p, encoding="utf-8", errors="ignore").readlines()
            except Exception:
                continue
            low = [ln.lower() for ln in lines]
            for sig in LOCKIN_SIGNALS:
                for i, ln in enumerate(low):
                    if sig.lower() in ln:
                        # Skip if the line documents the veto as a feature
                        # (e.g. "hard-coded vendor URLs: anthropic.com ...").
                        ctx = " ".join(low[max(0, i-1):i+2])
                        if any(w in ctx for w in
                               ("signal", "veto", "block", "drift",
                                "detection", "lock-in", "lockin")):
                            continue
                        hits.append((rel, sig))
                        break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default=DEFAULT_HOME)
    ap.add_argument("--skills", default=None)
    a = ap.parse_args()
    home = os.path.abspath(a.home)
    skills_root = a.skills or os.path.join(
        os.environ.get("LOCALAPPDATA", ""), "hermes", "skills")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = [f"# Hermes Mothership — Home Sync Report ({now})", ""]

    live = find_skills(skills_root)
    L.append(f"Live skills indexed: {len(live)}")
    L.append(f"Docked builds with SKILL.md: {len(docked_builds(home))}")
    L.append("")

    # 1. Dock drift
    L.append("## Dock drift (docked copy vs live source)")
    stale = 0
    for slug, d in docked_builds(home):
        docked = os.path.join(d, "SKILL.md")
        txt = open(docked, encoding="utf-8", errors="ignore").read()
        nm = re.search(r"^name:\s*(.+)$", txt, re.M)
        key = nm.group(1).strip() if nm else slug
        if key in live:
            src = live[key][1]
            if sha(src) != sha(docked):
                stale += 1
                L.append(f"- ⚠ STALE `{slug}` — live `{key}` changed; "
                         f"re-dock from {src}")
            else:
                L.append(f"- ✓ `{slug}` in sync with live `{key}`")
        else:
            L.append(f"- ? `{slug}` — no matching live skill named `{key}` "
                     f"(manual build, not tracked)")
    if stale == 0:
        L.append("  (no stale docks)")
    L.append("")

    # 2. Constitutional review
    ci = constitutional_review(home)
    if ci:
        L.append("## ⚠ Constitutional review: LOCK-IN SIGNALS DETECTED")
        for path, sig in ci:
            L.append(f"- `{path}` → `{sig}`")
    else:
        L.append("## Constitutional review: CLEAN (no vendor lock-in)")
    L.append("")

    body = "\n".join(L) + "\n"
    drift = (stale > 0) or bool(ci)
    status = "DRIFT" if drift else "CLEAN"
    print(body)
    print(f"HOME_STATUS: {status}  stale_docks={stale} lockin={len(ci)}")
    sys.exit(1 if drift else 0)


if __name__ == "__main__":
    main()
