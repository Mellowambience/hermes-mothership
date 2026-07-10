# Build: repo-to-wiki

Offline, constitution-governed code-docs generator — the **local-first answer to
Google's CodeWiki** (which is Gemini-locked and needs a vendor account).

## Source
- Built this session, directly responding to an X post about Google CodeWiki.
- Method: Python (stdlib) + `pygount` + `git`. No cloud, no vendor account,
  no API key. The constitution review pass is what CodeWiki *cannot* do.
- Tested on 2 local repos: `AetherTwin-Helm` → **DRIFT** (AGENTS.md references
  zero Steward principles); `aetherproof` → **N/A** (not a Steward repo).
- Bugs fixed before ship: capitalized component identifiers and TS
  `import type` leaking into the dependency map as fake "packages".

## Files
- `SKILL.md` — the skill (when/how to use, pitfalls)
- `scripts/repo_to_wiki.py` — the generator

## Usage
```bash
python scripts/repo_to_wiki.py --repo /path/to/repo [--out WIKI.md] [--no-constitution]
```

## Principle check
- Local-first ✓ (offline) · No lock-in ✓ (no vendor) · Transparency ✓ (this README) · Yours ✓ (lives in your home)
