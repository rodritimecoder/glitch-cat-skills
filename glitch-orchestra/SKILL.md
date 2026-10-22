---
name: glitch-orchestra

description: >
  Claude Code mods and terminal conductor architecture for multi-session agent supervision (Glitch Cat Club / Kem Glitch;
  Reel Dd_vZqINEtW). Operates the lead assistant as a terminal conductor dispatching tasks to dedicated child sessions,
  tracking active progress without context dilution, and triggering completion audio chimes.

license: "Proprietary. Complete terms are in the LICENSE file at the repository root."
compatibility: "Requires Python 3.10+. No network access needed."
metadata:
  creator: "kem_glitch"
  source_reel_id: "Dd_vZqINEtW"
  source_reel_url: "https://www.instagram.com/reel/Dd_vZqINEtW/"
  source_reel_vault_note: "kem_glitch/2026-10-17_claude_code_mods_and_glitch_orchestra/notes.md"
allowed-tools: "Bash(python3:*) Read Write"
---

# Glitch Orchestra (`glitch-orchestra`)

A terminal conductor architecture built on top of **Claude Code Mods** by **Kem Glitch (Glitch Cat Club)** in Reel [`Dd_vZqINEtW`](https://www.instagram.com/reel/Dd_vZqINEtW/).

---

## 🏛️ Architecture

Instead of a single agent trying to edit every file sequentially while bloating its prompt context:
1. **The Conductor**: Leads the session, decomposes the job, and coordinates child workers.
2. **Child Terminal Sessions**: Run isolated tasks in dedicated virtual terminals.
3. **Completion Alert**: Emits an audible chime/notification upon batch completion.

---

## 🛠️ CLI Quickstart

```bash
ORCHESTRA="python3 /run/media/rodri/AI/skills/glitch-orchestra/glitch_orchestra.py"

# 1. Register a child worker session
$ORCHESTRA register --id worker_01 --task "Refactor authentication middleware" --term tty_01

# 2. Check live conductor status
$ORCHESTRA status

# 3. Mark session complete
$ORCHESTRA complete --id worker_01 --summary "Auth middleware refactored and verified"

# 4. Trigger completion alert
$ORCHESTRA alert --message "All 4 worker tasks successfully completed!"
```

---

---

## AGENTS.md rule

## Conducting
Lead as a conductor, not as a worker:
glitch-orchestra register --id <worker> --task "<task>" --term <tty>
glitch-orchestra complete --id <worker> --summary "<verified summary>"
- Dispatch to a dedicated session; do not hold the work in the lead's context.
- A worker is complete when it says so and its summary is verifiable.
