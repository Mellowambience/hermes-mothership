# Skills registry

This directory is the **registry** of reusable procedures the agent maintains
at home. Each entry points to a live skill under the agent's skill space
(`%LOCALAPPDATA%\hermes\skills\`).

| Skill | What it does |
|---|---|
| `repo-to-wiki` | Offline, constitution-governed code-docs generator (the local-first CodeWiki) |
| `thread-reply-card` | Turn a "thoughts?" thread into a screenshot-ready Steward card |
| `mothership-deploy` | Dock an artifact on a mothership (used to dock this home's builds) |
| `social/thread-reply-card` | (alias) reply-to-thread card builder |

## Docked builds (under `builds/`)
| Build | What it is |
|---|---|
| `steward-card/` | Claude Projects vs My Hermes Stack — one-glance local-first case |
| `repo-to-wiki/` | Offline, constitution-governed code-docs generator (local CodeWiki) |
| `loop-engineering/` | Relay Packet/Seed + loop_guard, merged into j-space-bloodway (supersedes standalone spec) |
| `thread-reply-card/` | Turn a "thoughts?" thread into a screenshot-ready Steward card |

## Home tooling (under `scripts/`)
| Tool | What it does |
|---|---|
| `sync_home.py` | Self-maintenance: detects dock drift (docked vs live skill) + constitutional lock-in review. `HOME_STATUS: CLEAN\|DRIFT`. |

New skills are added here when a procedure proves reusable. Each links to its
source so the home stays transparent.
