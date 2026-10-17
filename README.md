# 🐱 Glitch Cat Autonomous Engineering Suite (`glitch-cat-skills`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: 8](https://img.shields.io/badge/Skills-8%20Production%20Harnesses-orange.svg)](#-the-8-core-engineering-skills)
[![Architecture: Kem Glitch](https://img.shields.io/badge/Architecture-Kem%20Glitch%20Club-purple.svg)](#-architectural-principles)

A production-grade collection of autonomous AI agent skills implementing the **7-step architecture and engineering principles by Kem (Glitch Cat Club)**. Built for AI coding agents (Claude Code, Antigravity, Roo Code, Pi Agent, and Gemini CLI) to prevent context rot, enforce hard guardrails, orchestrate parallel git worktrees, and self-calibrate token expenditure.

---

## 🏛️ Architectural Principles

```
                     ┌───────────────────────────────────────────────┐
                     │          Task Splitter (Atomic Tasks)         │
                     └───────────────────────┬───────────────────────┘
                                             │
                     ┌───────────────────────▼───────────────────────┐
                     │     Target-Local Markdown Kanban (.kanban/)   │
                     │  [01_new] ──► [02_picked_up] ──► [03_review]  │
                     └───────────────────────┬───────────────────────┘
                                             │
                     ┌───────────────────────▼───────────────────────┐
                     │         Multi-Agent Worktree Harness          │
                     │   Section Claims ──► Parallel Worktrees       │
                     └───────┬───────────────────────────────┬───────┘
                             │                               │
             ┌───────────────▼──────────────┐ ┌──────────────▼──────────────┐
             │       Guard Hooks (Hooks)    │ │   Context Rot Shield (cgate)│
             │   "Code that ALWAYS runs"    │ │  AST Outline + State Ledger │
             └───────────────┬──────────────┘ └──────────────┬──────────────┘
                             │                               │
                     ┌───────▼───────────────────────────────▼───────┐
                     │            Fresh-Context Judge                │
                     │       Clean Sandbox ──► Verification Gate     │
                     └───────────────────────┬───────────────────────┘
                                             │ [04_done]
                                             ▼
```

1. **Kem's Law**: *"A skill is instructions the model may follow; a hook is code that ALWAYS runs."* Guardrails, file immutability, and destructive command blockers belong in deterministic pre-execution hooks, never in soft system prompts.
2. **Fresh-Context Unbiased Judges**: Never let the model that authored the code evaluate its own correctness in the same context window. An unbiased judge runs in a clean context with isolated memory.
3. **Target-Local Kanban (`.kanban/`)**: Human-readable, git-versioned task cards (`CARD-001.md`) that persist progress across context flushes.
4. **Zero-Degradation Long Context**: Active structured state ledgers (`.agent_state.json` and `STATE.md`) paired with context-gated retrieval (`cgate`) protect 100% of facts across 660,000+ token sessions without LLM summary hallucinations.
5. **Parallel Worktree Isolation**: Autonomous subagents work in isolated Git worktrees with deterministic section claims to eliminate race conditions.

---

## 🛠️ The 8 Core Engineering Skills

| Skill | Source Reel | Description | Primary CLI Commands |
| :--- | :---: | :--- | :--- |
| **[`projects-harness`](./projects-harness/)** | [`DejvUBotWJD`](https://www.instagram.com/reel/DejvUBotWJD/) | Multi-agent coordination CLI: 3-way routing, dual-provenance envelopes, 200-line memory cap, rule clash detection, queue. | `projects-harness startup`, `projects-harness route`, `projects-harness envelope` |
| **[`worktree-harness`](./worktree-harness/)** | [`DeZUVT1t5vQ`](https://www.instagram.com/reel/DeZUVT1t5vQ/) | Multi-agent parallel Git worktree harness with section claims, quality gates, and automated merge arbitration. | `worktree-harness spawn`, `worktree-harness claim`, `worktree-harness merge` |
| **[`agentic-engineering`](./agentic-engineering/)** | [`DehIT3lNgHC`](https://www.instagram.com/reel/DehIT3lNgHC/) | Kem's 7-step autonomous production pipeline: Markdown Kanban, Event Listeners, Fresh-Context Judges, Task Splitters. | `agentic init`, `agentic split`, `agentic listen`, `agentic judge` |
| **[`guard-hooks`](./guard-hooks/)** | [`DeMSV1jNYem`](https://www.instagram.com/reel/DeMSV1jNYem/) | Deterministic pre-execution guardrails stopping destructive commands (`rm -rf`, force push, drop table) and protected file mutations. | `guard-hooks run`, `guard-hooks verify` |
| **[`state-compactor`](./state-compactor/)** | [`DdyqnietB8C`](https://www.instagram.com/reel/DdyqnietB8C/) | Context rot shield & long-context protocol. Combines state ledgers with `cgate` AST/JPT-4B symbol reader. | `cgate view`, `cgate outline`, `state-compactor record`, `state-compactor compact` |
| **[`parallel-test-lane`](./parallel-test-lane/)** | [`DbSgqTXt-3c`](https://www.instagram.com/reel/DbSgqTXt-3c/) | Test lane partitioning: splits sequential-isolated tests from independent parallel worker lanes to slash test runtime. | `parallel-test-lane run --workers 8` |
| **[`eval-router`](./eval-router/)** | [`DdWLJa2tjq6`](https://www.instagram.com/reel/DdWLJa2tjq6/) | Self-calibrating request router with speculative shadow evaluation and failure harvesting for 30–40% token cost reduction. | `eval-router route`, `eval-router harvest` |
| **[`graph-memory`](./graph-memory/)** | [`DcTIPKyt7Am`](https://www.instagram.com/reel/DcTIPKyt7Am/) | Anti-hallucination knowledge graph (<2ms SQLite k-hop walk) + hybrid BM25/BGE RRF search and exact-quote LLM distillation. | `python3 graph_memory.py ingest`, `python3 graph_memory.py query` |

---

## ⚡ Quick Start

### 1. Context Gating & State Preservation (`state-compactor` & `cgate`)

Stop dumping 500-line files into your LLM prompt. Use `cgate` to extract AST symbols or outline spans:

```bash
# Outline classes, functions, and line ranges via AST
cgate outline src/engine.py

# Extract strictly one class definition without reading the whole file
cgate view src/engine.py --symbol StateMachine

# Record verified facts into the state ledger
state-compactor record --fact "Dual-GPU AMD Radeon operational"
state-compactor record --decision "Use SQLite over Redis for zero dependencies"
state-compactor record --forbidden "Do NOT modify production configs directly"

# Generate zero-loss handover prompt for the next agent
state-compactor compact --out /tmp/handover_prompt.md
```

### 2. Autonomous Markdown Kanban Pipeline (`agentic-engineering`)

Initialize a local Kanban workflow directly inside your repository:

```bash
# Scaffold target-local .kanban directory
agentic init

# Decompose a feature request into atomic cards
agentic split "Implement distributed Raft log compaction"

# Run event listener to dispatch work to subagents
agentic listen --worker-lane parallel

# Invoke the Fresh-Context Judge to verify CARD-001
agentic judge --card .kanban/03_review/CARD-001.md
```

### 3. Multi-Agent Git Worktrees (`worktree-harness`)

Spawn parallel subagents on dedicated branches with file section claims:

```bash
# Spawn 3 isolated worktrees for parallel subagent workers
worktree-harness spawn --branches feature-auth feature-billing feature-metrics

# Claim specific files or sections before editing
worktree-harness claim --agent worker-1 --files src/auth.ts src/session.ts

# Execute quality gates and merge arbitration
worktree-harness merge --branch feature-auth
```

---

## 📦 Installation in Agent Harnesses

Clone this repository into your agent skills directory:

```bash
# For Antigravity / Gemini CLI harness
git clone https://github.com/rodritimecoder/glitch-cat-skills.git ~/.gemini/config/skills/glitch-cat

# For Pi Agent harness
git clone https://github.com/rodritimecoder/glitch-cat-skills.git ~/.pi/agent/skills/glitch-cat
```

Or add symlinks directly to your PATH:
```bash
ln -sf $(pwd)/state-compactor/scripts/cgate.py ~/.local/bin/cgate
ln -sf $(pwd)/state-compactor/scripts/compactor.py ~/.local/bin/state-compactor
ln -sf $(pwd)/agentic-engineering/agentic.py ~/.local/bin/agentic
```

---

## 📄 License

MIT © [rodritimecoder](https://github.com/rodritimecoder). Grounded in the architectural designs of Kem (Glitch Cat Club).
