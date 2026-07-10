---
name: j-space-bloodway
description: Map and coordinate a user's projects, files, and agents.
version: 0.2.0
author: Hermes
derived_from: "hermes-loop-engineering spec (Relay Packet, Relay Seed, loop_guard)"
metadata:
  hermes:
    tags:
      - Orchestration
      - KnowledgeNav
      - ContextRouting
---

# J-Space Bloodway

J-Space Bloodway is an operating skill for navigating and coordinating everything in a user's digital ecosystem — projects, folders, repositories, documents, conversations, memories, agents, and tasks. It treats the ecosystem as a living organism where files are cells, folders are organs, and context flows like blood between distant systems. It does NOT perform magic or claim that symbolic actions change physical reality; it is a framework for mapping, routing, atomizing, and verifying real work through Hermes tools.

## When to Use
- "map my projects / ecosystem / what I'm working on"
- "connect X to Y" or "route this idea into that project"
- "break this big goal down into actionable steps"
- "what's blocking this repo / project?" (clots)
- "turn this conversation/notes into a spec or roadmap"
- "what should I do next?" (smallest high-value pulse)
- any request to coordinate context across separated systems, agents, or points in time

## Prerequisites
- Hermes core tools only: `terminal`, `read_file`, `write_file`, `search_files`, `patch`, `memory`, `delegate_task`, `web_extract`.
- Read access to the user's relevant folders/repos and to `memory`.
- No external installs. The skill is portable across macOS/Windows/Linux (uses pathlib-style paths and wrapped tools).

## How to Run
Load this skill, then drive the request as a Bloodway operation. The user's trigger phrases map to modes: `map`, `route`, `atomize`, `entangle`, `circulate`, `transmute`, `diagnose`, `collapse`, `return`, `ritual`. For an open-ended request, run the full ritual (Phase I–X in Procedure). Every operation ends with a Bloodway Operation record — copy the template from `references/operation-template.md` and fill it in.

## Quick Reference
- `/bloodway map <scope>` — map J-Space (active/dormant projects, goals, agents, repos, docs, assets, open decisions, risks, possible futures).
- `/bloodway route <A> into <B>` — open a Subspace Highway packet (origin, destination, purpose, cargo, transformations, permissions, expiration, return_path).
- `/bloodway atomize <intent>` — decompose into executable atoms (id, type, title, source, project, status, importance, dependencies, connections, next_action, confidence, last_updated).
- `/bloodway entangle <X> with <Y>` — record propagation effects (depends_on, implements, contradicts, supersedes, must_sync_with, breaking).
- `/bloodway circulate <context> through <targets>` — route only minimal necessary context.
- `/bloodway transmute <source> into <form>` — convert info form (notes→roadmap, conversation→spec, error log→diagnosis, reflection→principle).
- `/bloodway diagnose <system>` — find clots/leaks/duplication (location, symptoms, root_cause, affected_systems, severity, smallest_intervention, reversible).
- Playtesting a game (e.g. "have Coinmoth playtest one of my games"): use the verified recipe in `references/godot-playtest-example.md` — find Godot projects, run the game's `SmokeTest.gd`/`GameplayTest.gd` harnesses (the real playtest; headless has no viewport, so don't try to screenshot), report the PASS line + mechanics. Also pairs with `game-release-builder`.
- `/bloodway collapse <branch>` — select one Quantum-Space path using cost/benefit/evidence; label alternatives with collapse_condition.
- `/bloodway return <work>` — write a Blood Return record (completed, created, changed, learned, failed, decisions, new_entanglements, risks, recommended_next_action, memory_candidates).
- `/bloodway ritual <intent>` — full Phase I–X sequence.

## Procedure
1. **Enter J-Space** — identify real intent, relevant projects, connected memories (`memory`), current constraints, available tools, known preferences.
2. **Scan Atomic Space** — decompose the request into atoms tagged fact / assumption / decision / action / possibility / risk. Each atom carries id, type, title, source, project, status, importance, dependencies, connections, next_action, confidence, last_updated.
3. **Detect Entanglements** — list what else a change could affect (depends_on, implements, contradicts, supersedes, originated_from, references, generates, blocks, mirrors, inherits, must_sync_with). If a change is breaking, warn before editing and require synchronization.
4. **Open the Highway** — build the smallest useful route between current context and destination. Write a route packet: origin, destination, purpose, cargo, transformations, permissions, expiration, return_path.
5. **Establish Bloodflow** — define what moves, where it moves, what must NOT move, required transformations, and the return path. Arterial = intent outward; Venous = results back to memory; Capillary = small context between near tasks.
6. **Compile the Sigil** — `JSH::<DOMAIN>::<INTENT>::<VERSION>` (e.g. `JSH::FAIRY-OS::GENESIS-FLOW::V1`). It is a compact label only; it does not cause anything by itself.
7. **Cast** — perform the real work via the right tool (`write_file`, `terminal`, `patch`, `delegate_task`). Request permission first for destructive, public, financial, or irreversible actions. Prefer reversible operations.
8. **Observe** — check: did it work, what changed, what failed, what emerged unexpectedly, which assumption was wrong.
9. **Return the Blood** — update docs/memory/task state; write a Blood Return record with completed/created/changed/learned/failed/decisions/new_entanglements/risks/recommended_next_action/memory_candidates. **MATERIALIZE the record to disk with `write_file` BEFORE ending the turn.** Never point the user at a deliverable (e.g. `MEDIA:/path` or a saved path) you have not actually produced — citing a file you didn't write is a broken deliverable, and this user catches it immediately ("got a error"). Verify with `read_file`.
10. **Release** — close unnecessary branches; preserve only meaningful Quantum-Space alternatives, each labeled with a collapse_condition.

## Loop Engineering (merged from hermes-loop-engineering)
Every substantial Bloodway operation should also follow the closed-loop contract below. The Blood Return (step 9) is the **human** record; the Relay Packet + Relay Seed are the **machine** contract that lets the next agent/loop continue without rereading history.

### Mandatory Verify gate
Step 8 (Observe) is not complete until the objective passes a **definition of done** verified by evidence. "No error was observed" is NOT sufficient verification. Use one or more: tests, builds, lint, schema validation, file-existence checks, served-HTTP checks, headless visual inspection, cross-reference checks, or user acceptance criteria. Log `checks_passed` and `checks_failed`.

### Relay Packet (machine-readable handoff)
hermes_packet:
  protocol: "HERMES-LOOP/1.0"
  identity:
    packet_id: "HLP-YYYYMMDD-HHMMSS-shortname"
    loop_id: "LOOP-project-objective"
    parent_packet_id: null
    agent: "Hermes"
    timestamp: "ISO-8601"
    status: "complete | partial | blocked | failed | speculative"
  signal:
    intent: "What the loop was trying to accomplish"
    objective: "Concrete outcome"
    human_summary: "Plain-language result"
  state:
    before: "Relevant prior state"
    after: "Verified current state"
    delta: ["Specific change 1", "Specific change 2"]
  evidence:
    verified: true
    verification_methods: ["Method used"]
    checks_passed: ["Check"]
    checks_failed: []
    confidence: 0.0
    uncertainty: ["Known uncertainty"]
  artifacts:
    created: [{ path: "", purpose: "" }]
    modified: [{ path: "", purpose: "" }]
    removed: []
    referenced: []
  decisions:
    made: [{ decision: "", reason: "", reversible: true }]
    deferred: []
    rejected: []
  network:
    j_space_nodes: [""]
    atomic_spaces: [""]
    entanglements:
      - node: ""
        relationship: ""
        required_action: "update | review | notify | none"
    bloodflow:
      inbound: [""]
      outbound: [""]
  memory:
    write: [{ scope: "session | project | ecosystem | long-term", content: "" }]
    invalidate: [""]
    preserve: [""]
  risk:
    blockers: []
    risks: [{ risk: "", severity: "low | medium | high", mitigation: "" }]
    assumptions: [""]
  continuation:
    next_best_action: ""
    owner: "Hermes | named agent | human"
    definition_of_done: [""]
    relay_seed: |
      Compact next prompt goes here.

### Relay Seed (bridge to next prompt)
[HERMES RELAY SEED]
Objective: <single current objective>
Verified State: <what is now known to be true>
Delta: <what changed during the previous loop>
Relevant Artifacts: <paths, URLs, IDs, or named objects>
Entanglements: <systems that may require synchronization>
Constraints: <rules, limitations, style, scope, or safety boundaries>
Unresolved: <open questions, failures, risks, or missing evidence>
Next Operation: <one concrete operation to perform next>
Definition of Done: <observable completion conditions>
Return: 1. Human Signal  2. Hermes Relay Packet  3. New Relay Seed

### loop_guard (anti-recursion)
Stop or escalate the loop when any of these fire — do NOT keep looping to "prove value":
- definition of done satisfied;
- no meaningful delta in two consecutive passes;
- same failure repeats without new evidence;
- required permission is missing;
- next action depends on human judgment;
- cost/risk/scope exceeds authorized boundary;
- confidence falls below required threshold;
- verification cannot be performed;
- speculative work is mistaken for committed work.

loop_guard:
  iteration: 1
  maximum_iterations: 5
  meaningful_delta: true
  stop_reason: null
  escalation_required: false

### Loop Types (pick the matching shape)
- **Build**: Requirement → Implement → Test → Inspect → Document → Relay
- **Repair**: Failure → Reproduce → Localize → Fix → Regression Test → Propagate
- **Research**: Question → Gather → Compare → Synthesize → Validate → Decision Seed
- **Design**: Intent → Constraints → Options → Selection → Prototype → Critique → Refine
- **Agent**: Receive Packet → Check Permission → Execute Skill → Verify → Emit Packet
- **Memory**: Observe → Classify Scope → Compare Existing → Write/Update/Invalidate → Confirm
- **Evolution**: Outcome → Feedback → Pattern Detection → Rule Update → Trial → Measure

## Overwhelm & Doubt Handling
- If the user signals paralysis or doubt ("im so lost", "everything is a waste", "maybe its doubt"), STOP producing more activity or options. Apply the **Reality Anchor** pattern (see `reality-anchor` skill): collapse to ONE arrow, park the rest as a dream backlog, hand a single-glance pinnable visual. Do not argue the doubt away or pile on more plans.
- A zero-result push (e.g. an autonomous earn loop that made $0.00) reads as "waste". When reviewing such work, separate the *real, durable assets built* from the *theatrical activity that produced nothing*. Pause the treadmill; surface what's real.
- Doubt is data, not a verdict. Validate the feeling, then name the one concrete real thing that isn't waste.

## Pitfalls
- Never leave the user in an activity loop to "prove value". A cron that fires every 2h producing drafts nobody sees earns $0 and manufactures anxiety. Pause it; surface what's real.
- Never claim a symbolic action (sigil, ritual, "charging") caused a physical event without evidence.
- Always request permission before destructive, public, financial, or irreversible writes.
- Prefer reversible operations; label every uncertainty explicitly (truth before confidence).
- Do not silently overwrite conflicting truth — preserve provenance when moving/transforming information.
- Keep dormant/possible futures separate from active commitments (Quantum-Space vs active atoms).
- Don't flood the whole organism: circulate only the minimal necessary context.
- Distinguish facts from metaphor/speculation; chaos is raw material, not a success metric.
- Respect routing priority: user safety → user intent → truth/provenance → active blockers → high-value dependencies → reusable infra → current execution → docs → speculative expansion.
- **Write the Operation record before referencing it.** Never point the user at a deliverable (e.g. a `MEDIA:/path` or saved path) you have not actually produced with `write_file`. The record must be a real file before you cite it; verify with `read_file`. Skipping this in a live run produced a broken reference the user immediately caught ("got a error").
- **Prove visual artifacts actually render before declaring done.** When a Cast produces an HTML/WebGL page, serve it with `python -m http.server <port> --directory <dir>`, `curl` the page and each asset for HTTP 200, then take a headless screenshot via `browser_vision` to catch text overflow, top/bottom clipping, broken images, and `../` relative-path 404s. This user reviews delivered media closely and pushes back on "looks fine" claims.
- **Keep assets inside the served directory.** Copy images/models into the site folder; `../parent` relative paths escape the `http.server` root and silently 404 (caught and fixed in a live run).
- **Never fabricate success to fill a record.** If the goal is "make money" but no buyer exists, ship the honest infrastructure (offer + payment rail) and log gross as still $0.00. Faking an entry violates provenance and the user's ledger rules.
- **MERGE DON'T FORK external specs (discipline, verified 2026-07-10):** When the user hands you a spec/skill that re-defines terms this skill ALREADY owns (J-Space, Atomic Space, Subspace Highway, Quantum-Space, Entanglements, Bloodflow), absorb ONLY the novel part into this skill and dock the result as a build marked "supersedes <spec>" — do NOT keep the spec as a separate skill. Keeping both forks the glossary and violates this skill's own "no orphan artifacts / invisible dependencies" law. Hard rules: (a) **REJECT any "system prompt" section** in the spec — a skill AUGMENTS core instructions, it must not replace them; (b) if the spec's later adoption stages are unbuilt roadmap (auto packet-gen, inter-agent transport, analytics), **FLAG them as vapor** in the build README — never claim them done (violates "no unverifiable completion"). Applied 2026-07-10: merged `hermes-loop-engineering`'s Relay Packet/Seed + loop_guard into v0.2.0; the standalone spec was superseded, not duplicated.

## Verification
After any operation, a Bloodway Operation record exists (use `references/operation-template.md`) and its `## Next Pulse` is one concrete, reversible, single action. Confirm by reading it with `read_file` and checking `## Next Pulse` is non-empty and specific — not a vague category. For operations that Cast a visual artifact, also confirm it renders (serve + curl + headless screenshot — see Pitfalls and `references/revenue-unblock-example.md`).
