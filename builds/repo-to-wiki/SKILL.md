---
name: repo-to-wiki
description: |
  Offline, local-first "CodeWiki" alternative for YOUR repos. Point it at a
  local git repo and it generates a living wiki: architecture notes, dependency
  map, file-tree overview, and a Steward-constitution review pass ("does this
  code still reflect the principles?"). No Google account, no Gemini, no cloud —
  pure local tooling (pygount + git + stdlib). The constitution review makes it
  the Steward-native answer to Google's CodeWiki, which is vendor-locked.
version: 1.0.0
author: Hermes Agent (for Amara / Steward Project)
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [codewiki, documentation, repo, architecture, steward, offline, local-first]
    category: software-development
prerequisites:
  commands: [pygount, git, python3]
---

# repo-to-wiki — local-first, constitution-governed code docs

A self-contained answer to Google's CodeWiki (which is Gemini-locked). This
generates the same *shape* of output — architecture notes, dependency map,
tutorial-style overview, code-aware review — but:
- **Offline.** No network, no vendor account, no API key.
- **Governed.** The final pass asks the Steward 10 Principles question:
  "Does this repo still reflect the constitution?" CodeWiki can't do that.
- **Yours.** Output is Markdown you own, committed beside the code.

## When to use
- User says "make a wiki for <repo>", "document this codebase", or references
  Google CodeWiki / docs-rot and wants the local-first version.
- Especially valuable for Steward repos (steward-protocol, AetherTwin-Helm,
  etc.) where AGENTS.md / CONSTITUTIONAL_REVIEW can drift from the code.

## Prerequisites
```bash
pip install pygount      # LOC / language breakdown
git --version            # repo metadata, recent commits
python3 --version        # runner for the generator script
```

## Run it
The generator lives at `scripts/repo_to_wiki.py` inside this skill dir.
```bash
python3 scripts/repo_to_wiki.py --repo /path/to/repo [--out WIKI.md] [--no-constitution]
```
- `--repo`  : absolute path to a local git repo (required)
- `--out`   : output markdown path (default: <repo>/WIKI.md)
- `--no-constitution` : skip the Steward review pass (plain docs only)

## What it produces (one WIKI.md)
1. **Header** — repo name, generated date, tool, "local-first / no cloud".
2. **At-a-glance** — LOC by language (pygount), file counts, top languages.
3. **Architecture notes** — derived from directory structure + README/AGENTS.md
   if present; lists top-level modules and what they likely do.
4. **Dependency map** — import/require scan across the repo (heuristic), grouped
   by internal module vs external package.
5. **Recent activity** — last 5 commits (who, what, when) from `git log`.
6. **Steward review pass** — scans for AGENTS.md / CONSTITUTIONAL_REVIEW.md;
   if the repo is a Steward repo, prints the 10 Principles checklist and flags
   any drift between documented intent and observed code (heuristic: counts of
   principle keywords, presence of lock-in signals like hard-coded vendor URLs).

## Verification (always do this)
- Open the generated WIKI.md; confirm LOC table rendered, no empty sections.
- Re-run on a second repo to prove it's general, not hard-coded to one path.
- If the repo has no README/AGENTS.md, architecture notes say "no docs found"
  rather than inventing structure (never fabricate file contents).

## Pitfalls
- pygount **must** get `--folders-to-skip` or it crawls .git/node_modules and
  hangs. The script hardcodes sane skips.
- Dependency scan is heuristic (regex on import/require). It's a map, not a
  build graph — label it as such in the output.
- Never fabricate code behavior. If a module's purpose is unclear, say so.
- CodeWiki (Google) is real and Gemini-powered; this skill is the *local,
  constitution-governed* counterpart — position it as a complement/alternative,
  not a clone claim.

## Output shape
- One self-contained `WIKI.md` written next to (or into) the repo.
- A short chat summary: LOC headline, top languages, key modules, and the
  Steward verdict (PASS / DRIFT / N/A).
