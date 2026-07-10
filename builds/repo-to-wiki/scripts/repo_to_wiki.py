#!/usr/bin/env python3
"""
repo_to_wiki.py — local-first, constitution-governed code wiki generator.

Offline counterpart to Google's CodeWiki. No cloud, no vendor account.
Produces a single WIKI.md: LOC breakdown, architecture notes, dependency map,
recent activity, and a Steward constitution review pass.

Usage:
    python3 repo_to_wiki.py --repo /path/to/repo [--out WIKI.md] [--no-constitution]
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

SKIP_DIRS = ".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party,*.egg-info,.openclaw,obsidian-vault"
IMPORT_RE = re.compile(
    r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)', re.M)
REQUIRE_RE = re.compile(
    r'(?:require|import)\s*\(\s*[\'"]([a-zA-Z0-9_\-\.]+)[\'"]\s*\)')
LOCKIN_SIGNALS = [
    "anthropic.com", "openai.com", "googleapis.com", "gemini",
    "claude", "gpt-", "azure", "aws.amazon.com", "vercel",
]


def run(cmd, cwd):
    try:
        return subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            timeout=60).stdout.strip()
    except Exception as e:  # noqa
        return f"(error: {e})"


def pygount_summary(repo):
    out = run([
        "pygount", "--format=summary",
        "--folders-to-skip=" + SKIP_DIRS, ".",
    ], cwd=repo)
    return out


def git_recent(repo):
    return run([
        "git", "log", "-5", "--pretty=format:%h %an %ad %s",
        "--date=short",
    ], cwd=repo)


def list_top_dirs(repo):
    entries = []
    for name in sorted(os.listdir(repo)):
        if name.startswith(".") and name != ".openclaw":
            continue
        full = os.path.join(repo, name)
        if os.path.isdir(full) and name not in SKIP_DIRS.split(","):
            entries.append(name)
        elif os.path.isfile(full):
            entries.append(name)
    return entries[:25]


def scan_imports(repo, exts=(".py", ".js", ".ts", ".tsx", ".jsx")):
    internal, external = set(), {}
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs
                   if d not in SKIP_DIRS.split(",") and not d.startswith(".git")]
        for f in files:
            if not f.endswith(exts):
                continue
            p = os.path.join(root, f)
            if os.path.getsize(p) > 200_000:
                continue
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:  # noqa
                continue
            for m in IMPORT_RE.finditer(txt):
                mod = m.group(1).split(".")[0]
                # skip stdlib, skip Capitalized component identifiers
                # (e.g. `import { App } from`) which are not packages
                if mod in ("os", "sys", "re", "json", "subprocess", "datetime",
                           "typing", "collections", "math", "pathlib", "argparse",
                           "functools", "itertools", "asyncio"):
                    continue
                if mod and mod[0].isupper():
                    continue
                if mod == "type":  # TS `import type { X }` — not a package
                    continue
                external[mod] = external.get(mod, 0) + 1
            for m in REQUIRE_RE.finditer(txt):
                mod = m.group(1).split("/")[0]
                if mod and mod[0].isupper():
                    continue
                external[mod] = external.get(mod, 0) + 1
    # crude internal-module detection: top-level dirs that are imported
    tops = {d for d in list_top_dirs(repo)
            if os.path.isdir(os.path.join(repo, d))}
    for mod in list(external):
        if mod in tops:
            internal.add(mod)
            external.pop(mod, None)
    return sorted(internal), sorted(external.items(), key=lambda x: -x[1])[:20]


def read_doc(repo, name):
    p = os.path.join(repo, name)
    if os.path.isfile(p):
        try:
            return open(p, encoding="utf-8", errors="ignore").read(4000)
        except Exception:  # noqa
            return ""
    return ""


def extract_principles(repo):
    """Derive the principle vocabulary from the repo's OWN constitution docs.

    Returns (principles, source) where principles is a list of lowercase
    keyword fragments to look for. Falls back to a generic Steward vocabulary
    only when no constitution doc exists (so non-Steward repos still get a
    generic check instead of a false DRIFT).
    """
    const_docs = ["CONSTITUTION.md", "PRINCIPLES.md", "CONSTITUTIONAL_REVIEW.md"]
    const_blob = "".join(read_doc(repo, d) for d in const_docs)
    if not const_blob.strip():
        # no constitution present — use generic fallback vocabulary
        return (
            ["local-first", "consent", "no hidden network", "transparency",
             "no lock-in", "privacy", "accountability", "autonomy",
             "stewardship", "model-agnostic"],
            "fallback-generic",
        )
    # Extract principle names from numbered/bulleted lines like:
    #   "1. **Agency** — ..."  or  "### 1. Agency" or "- **Transparency**"
    found = []
    for line in const_blob.splitlines():
        m = re.search(r'(?:^|\s)(?:#{2,4}\s*)?(?:\d+\.\s*)?[\*\-]?\s*\*\*([A-Z][A-Za-z][\w\- ]{1,30}?)\*\*', line)
        if m:
            name = m.group(1).strip().lower()
            # keep meaningful single words / short phrases
            if 3 <= len(name) <= 24:
                found.append(name)
    # de-dup, keep order
    seen, principles = set(), []
    for f in found:
        if f not in seen:
            seen.add(f)
            principles.append(f)
    return (principles or ["transparency", "consent", "local-first"],
            "repository-constitution")


def constitution_pass(repo):
    verdict = "N/A"
    notes = []
    # Honour the repo's own governance docs, not a hardcoded vocabulary.
    src_docs = ["AGENTS.md", "CONSTITUTION.md", "PRINCIPLES.md",
                "CONSTITUTIONAL_REVIEW.md", "README.md"]
    docs_present = [d for d in src_docs
                    if os.path.isfile(os.path.join(repo, d))]
    has_steward = bool(docs_present) or \
        os.path.isfile(os.path.join(repo, "examples", "research-lab",
                                    "reflection_loop.py"))
    if not has_steward:
        return ("N/A", ["No AGENTS.md / CONSTITUTION.md detected — "
                         "not a Steward-governed repo; skipping principle pass."])
    principles, psrc = extract_principles(repo)
    blob = "".join(read_doc(repo, d) for d in docs_present).lower()
    hits = {p: blob.count(p) for p in principles}
    markers = [p for p, c in hits.items() if c]
    drift = [p for p, c in hits.items() if c == 0]
    lockin = []
    for sig in LOCKIN_SIGNALS:
        if sig in blob:
            lockin.append(sig)
    notes.append(f"Principle vocabulary source: {psrc} "
                 f"({len(principles)} principles)")
    notes.append("Steward markers found: " + (", ".join(markers) or "none"))
    if drift:
        notes.append("Principles not explicitly referenced: "
                     + ", ".join(drift))
    if lockin:
        notes.append("⚠ Lock-in signals in docs: " + ", ".join(lockin))
        verdict = "DRIFT" if drift else "PASS*"
    else:
        verdict = "PASS" if not drift else "DRIFT"
    return (verdict, notes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-constitution", action="store_true")
    a = ap.parse_args()

    repo = os.path.abspath(a.repo)
    if not os.path.isdir(os.path.join(repo, ".git")):
        print(f"ERROR: not a git repo: {repo}", file=sys.stderr)
        sys.exit(1)
    out = a.out or os.path.join(repo, "WIKI.md")
    name = os.path.basename(repo)

    loc = pygount_summary(repo)
    recent = git_recent(repo)
    tops = list_top_dirs(repo)
    internal, external = scan_imports(repo)
    readme = read_doc(repo, "README.md")[:600]
    agents = read_doc(repo, "AGENTS.md")[:400]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = []
    L.append(f"# {name} — Wiki (local-first)\n")
    L.append(f"> Generated {now} by `repo-to-wiki` (offline, no cloud, "
             f"no vendor account). Steward-native counterpart to Google CodeWiki.\n")
    L.append("## At a glance\n")
    L.append("```\n" + (loc or "(pygount unavailable)") + "\n```\n")
    L.append("## Architecture notes\n")
    if readme:
        L.append("From README.md:\n")
        L.append(readme.strip() + "\n")
    elif agents:
        L.append("From AGENTS.md:\n")
        L.append(agents.strip() + "\n")
    else:
        L.append("_No README.md / AGENTS.md found — structure inferred from tree._\n")
    L.append("\nTop-level layout:\n")
    for t in tops:
        L.append(f"- `{t}`")
    L.append("\n## Dependency map (heuristic)\n")
    if internal:
        L.append("**Internal modules referenced across repo:** " +
                 ", ".join(f"`{m}`" for m in internal))
    if external:
        L.append("\n**External packages (top by reference count):**\n")
        for mod, cnt in external:
            L.append(f"- `{mod}` ({cnt})")
    if not internal and not external:
        L.append("_No import/require statements scanned (or unsupported language)._")
    L.append("\n## Recent activity\n")
    if recent:
        for line in recent.splitlines():
            L.append(f"- {line}")
    else:
        L.append("_No git history._")
    L.append("\n## Steward review pass\n")
    if a.no_constitution:
        L.append("_Skipped (--no-constitution)._")
    else:
        verdict, notes = constitution_pass(repo)
        L.append(f"**Verdict: {verdict}**\n")
        for n in notes:
            L.append(f"- {n}")

    body = "\n".join(L) + "\n"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"WROTE {out} ({len(body)} bytes)")
    print("VERDICT:", "skipped" if a.no_constitution else
          constitution_pass(repo)[0])


if __name__ == "__main__":
    main()
