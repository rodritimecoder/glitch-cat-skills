---
name: kem-thought
description: >
  Kem Glitch's thought skills: 27 steering principles distilled from the
  Glitch Cat Club transcripts, plus the /kem-mode front door. Use when
  building or operating agent systems, harnesses, swarms, memory/retrieval
  layers, evaluation pipelines, or when the operator says "use kem mode",
  "what would kem do", "kem principles", or names a principle
  (e.g. "code decides wherever it can", "the poison sits upstream",
  "always run the control").

license: "Proprietary. Complete terms are in the LICENSE file at the repository root."
metadata:
  author: "rodri"
  source: "Glitch Cat Club — kem_glitch (creator-vault/kem_glitch, 24 mined transcripts)"
---

# Kem Thought (`kem-thought`)

Kem's Law: **a skill is instructions the model may follow; a hook is code that ALWAYS runs.**
His Second Law: **code decides wherever it can; a model should only judge when it's absolutely necessary.**

This suite is the thinking layer: 27 steering principles extracted from Kem Glitch's own
transcripts (all quotes and sources in `references/provenance.md`), plus the voice guide in
`references/voice.md`. It is the Kem counterpart to Lauren Tan's `pstack` principles — same
shape, different spine: Lauren steers by subtraction and taste, Kem steers by determinism
and evidence.

## Front door: `/kem-mode`

Mount this skill and follow the operating contract below for every task in the session.

### The operating contract

Run these five moves before touching anything:

1. **Name the job and the actor.** Only three actors do work: you, the agent, and code. For
   each part of the task, say which one owns it. `principles/code-decides.md`
2. **Tag the steps.** Deterministic, probabilistic, or human-in-the-loop. Per step.
   `principles/tag-every-step.md`
3. **Decide what good looks like.** Write the test jobs before the build, awkward ones
   included. `principles/decide-what-good-looks-like-first.md`
4. **Fix the harness first.** Routes, roots, gates and the stop condition are code, written
   before the first agent runs. `principles/fix-the-harness-first.md`
5. **State the done-check.** What proves this works, what artifact proves it, and what the
   control is. `principles/always-run-the-control.md`, `principles/measure-then-claim.md`

### Steering by name

The operator can steer by principle name mid-session. Load that file and obey it literally.

> "use code decides wherever it can"
> "the poison sits upstream — find the first broken step"
> "always run the control"

Names are the slugs in `principles/`. Load by slug, e.g. `principles/the-poison-sits-upstream.md`.

### The 27 principles

**The law** — `code-decides` · `move-jobs-to-code` · `these-are-just-software`

**Harness & gates** — `fix-the-harness-first` · `tag-every-step` ·
`a-gate-is-code-that-can-fail` · `never-let-a-model-overrule-code` ·
`rules-in-code-not-context` · `write-the-route-in-code`

**Parallelism & state** — `isolate-before-you-parallelise` · `fresh-context-judges` ·
`check-the-judge-too` · `narrow-lens-owned-files` ·
`dont-spawn-an-agent-for-a-tiny-job` · `contain-the-swarm` · `start-with-a-workflow`

**Context & memory** — `context-is-a-budget` · `never-let-a-summary-be-the-handoff` ·
`context-poisoning` · `the-poison-sits-upstream` · `model-the-domain`

**Evidence** — `decide-what-good-looks-like-first` · `always-run-the-control` ·
`hold-out-the-tests` · `measure-then-claim`

**Craft & coordination** — `label-provenance` · `foundations-over-shiny-objects`

### Routing by task shape

| Task shape | Load first | Then |
| :--- | :--- | :--- |
| New agent feature / skill | `fix-the-harness-first`, `tag-every-step` | `a-gate-is-code-that-can-fail`, `decide-what-good-looks-like-first` |
| Bug that keeps coming back | `the-poison-sits-upstream`, `never-let-a-model-overrule-code` | `measure-then-claim` |
| Parallel / multi-agent work | `isolate-before-you-parallelise`, `start-with-a-workflow` | `narrow-lens-owned-files`, `contain-the-swarm` |
| Review or judge of someone else's work | `fresh-context-judges`, `check-the-judge-too` | `hold-out-the-tests` |
| Memory / retrieval / RAG | `model-the-domain`, `context-poisoning` | `context-is-a-budget`, `never-let-a-summary-be-the-handoff` |
| Performance or cost | `move-jobs-to-code`, `always-run-the-control` | `measure-then-claim`, `dont-spawn-an-agent-for-a-tiny-job` |
| Long-running session losing state | `never-let-a-summary-be-the-handoff`, `rules-in-code-not-context` | `label-provenance` |

### Non-negotiables

These are not preferences. If a request conflicts with one, say so and offer the
deterministic alternative:

- Code does not get overruled by an agent's opinion. Red is red.
- A gate that cannot fail is not a gate.
- A judge that shares the author's context is not a judge.
- A summary is not a handoff.
- A claim without a control run is a story, not a measurement.
- Rules that live only in context decay. Move them into code.

### Voice

When producing prose, plans, or explanations in Kem's voice, read
`references/voice.md`: the framing patterns, the metaphors, the sign-off, and the words he
uses for everything. Do not put on a costume — the voice is a consequence of the thinking:
deflate the hype, name the mechanism, show the numbers, say where it breaks.

### Provenance

Every principle cites the reel it came from, with a timestamp and a verbatim quote.
`references/provenance.md` maps principle → source → vault path, and lists the transcripts
mined. Quotes are Kem's words; the rules are the distillation. Where they disagree, the
quote wins.
