---
name: agentic-engineering

description: >
  Autonomous production engineering pipeline implementing Kem's 7-step software factory (Glitch Cat Club;
  Reel DehIT3lNgHC). Operates target-local Markdown Kanban boards (.kanban/), event-driven Listeners,
  Fresh-Context Unbiased Judges, Task Splitters, and multi-model parallel sandboxes.

license: "Proprietary. Complete terms are in the LICENSE file at the repository root."
compatibility: "Requires git. Uses a local model runner for the judge and sandbox tiers."
metadata:
  creator: "kem_glitch"
  source_reel_id: "DehIT3lNgHC"
  source_reel_url: "https://www.instagram.com/reel/DehIT3lNgHC/"
  source_reel_vault_note: "kem_glitch/2026-10-16_agentic_engineering_7_step_loop/notes.md"
allowed-tools: "Bash(python3:*) Bash(git:*) Read Write"
---

# `agentic-engineering` (`agentic`)

A production engineering pipeline implementing **Kem's (Glitch Cat Club) 7-Step Architecture**: moving from conversational chatting to an autonomous, multi-model execution factory.

---

## 🏛️ The 7-Step Architecture

```
[1. Inbound Stream] ──> [2. Kanban Board] ──> [3. The Listener] ──> [4. Report Block & Fresh Judge]
                                                                                │
                                                                   [5. Splitter: Task DAG]
                                                                                │
                                  ┌─────────────────────────────┬───────────────┴─────────────┐
                                  ▼                             ▼                             ▼
                        [6a. Sandbox 1 (Opus)]       [6b. Sandbox 2 (Sonnet)]       [6c. Sandbox 3 (Flash)]
                                  │                             │                             │
                                  └─────────────────────────────┼─────────────────────────────┘
                                                                ▼
                                                     [7. Delivery to YOU]
```

1. **Inbound Task**: Issues or requests flow into the target project's `.kanban/01_new/`.
2. **Kanban State Machine**: Cards track status (`01_new` $\rightarrow$ `02_picked_up` $\rightarrow$ `03_review` $\rightarrow$ `04_done`) with explicit acceptance criteria (`[REQ-XX]`).
3. **The Listener**: Event-driven watcher that automatically detects and claims ready cards without prompt babysitting.
4. **Report Block & Unbiased Judge**:
   - Executes deterministic **Blue Diamond Code Gates** (`gate_lint`, `gate_test`, `gate_evidence`).
   - Invokes a **Fresh-Context Judge** (default: `flash`) with zero prior conversational bias. If criteria fail, Kem's pink arrow (`SENT BACK`) returns the card with a structured rejection delta.
5. **The Splitter**: Partitions approved specs into parallel single-writer task lanes.
6. **Multi-Model Sandboxes**: Executes concurrent lanes across model tiers (Opus, Sonnet, local Genesis 35B) in isolated sandboxes / worktrees.
7. **Delivery to YOU**: Aggregated, verified deliverables presented cleanly for human review.

---

## 🚀 CLI Usage

### 1. Initialize Kanban Board in Target Project
```bash
# Initializes .kanban/ with 01_new/, 02_picked_up/, 03_review/, 04_done/
agentic init [target_dir]
```

### 2. Manage Cards on the Board
```bash
# View ASCII Kanban Board
agentic kanban list

# Add a new task card with acceptance criteria
agentic kanban add "Build Authentication Flow" --req "JWT auth endpoint with refresh rotation"

# Move card between columns manually
agentic kanban move CARD-001 done
```

### 3. Run the Event Listener
```bash
# One-shot poll and dispatch
agentic listen --once

# Background daemon listening on .kanban/01_new/
agentic listen --interval 5 --worker "agentic run {CARD_ID}"
```

### 4. Evaluate with Fresh-Context Judge
```bash
# Spawns clean-slate judge evaluating diff against [REQ-XX] criteria
agentic judge CARD-001 --model flash
```

### 5. Run the Full 7-Step Loop End-to-End
```bash
agentic run CARD-001
```

---

---

## AGENTS.md rule

## Software factory
Work moves through the board, not through chat:
agentic kanban add "<task>" --req "<requirement>"
agentic kanban move <card-id> done
- One card, one verifiable requirement. No card without a done condition.
- A fresh-context judge decides whether the work is done; the author does not grade itself.
- Never merge a card whose gate has not run.
