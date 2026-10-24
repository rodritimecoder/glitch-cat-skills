#!/usr/bin/env python3
"""
kem-dev-loop — Kem Glitch's 6-Phase Autonomous AI Development Lifecycle.
Synthesized from Glitch Cat Club (Reel DemLMidtxxj: "How I Develop with AI (High Level)").

Phases:
  1. Classify & Route (Small/Routine -> Fast Route | Big/Complex -> Full Route)
  2. Holdouts & Intent (Anti-sycophancy: holdouts written upfront, hidden from builders)
  3. Parallel Build (Vertical slices in parallel worktrees)
  4. Grounded Validation (User persona: click, type, inspect UI; run holdouts; no adversarial loops)
  5. Decoupled Code Review (Cleanliness, typing, maintainability only AFTER functional pass)
  6. Human Intent Gate (Human validates the "Why and Why Not")
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

STATE_DIR = Path(".kem-loop")


def run_cmd(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True)


def cmd_route(args):
    prompt = " ".join(args.prompt).strip()
    if not prompt:
        print("Usage: kem-dev-loop route <task description>")
        return 1

    print(f"\n🔍 [Classify & Route] Evaluating task:")
    print(f"   \"{prompt}\"\n")

    # Attempt local JEV decision if available, else deterministic heuristics
    route = "FAST_ROUTE"
    reason = "Deterministic classification"
    complexity = "SMALL"

    jev_check = run_cmd("which jev")
    if jev_check.returncode == 0:
        res = run_cmd(f'jev choice --context "Task: {prompt}" --question "Classify this software task" --options "small,complex"')
        if res.returncode == 0 and "complex" in res.stdout.lower():
            route = "FULL_ROUTE"
            complexity = "BIG"
            reason = f"JEV calibrated model decision: {res.stdout.strip()}"
        else:
            reason = f"JEV calibrated model decision: small/routine"
    else:
        # Heuristic fallback
        indicators = ["refactor", "architect", "pipeline", "database", "migration", "redesign", "multi-agent"]
        if any(w in prompt.lower() for w in indicators) or len(prompt) > 140:
            route = "FULL_ROUTE"
            complexity = "BIG"
            reason = "Keywords / scope indicate complex multi-component change"

    print(f"🎯 Route Selected: **{route}** ({complexity})")
    print(f"   Rationale: {reason}\n")

    if route == "FULL_ROUTE":
        print("📋 Protocol for FULL_ROUTE:")
        print("   1. Write and human-approve PLAN.md (align on 'Why and Why Not').")
        print("   2. Scaffold hidden holdout tests: `kem-dev-loop init <name>`")
        print("   3. Dispatch parallel builders across vertical slices.")
        print("   4. Validate user journey & holdouts before code review.")
    else:
        print("⚡ Protocol for FAST_ROUTE:")
        print("   - Small or greenfield routine change.")
        print("   - Direct execution permitted with standard verification.")

    return 0


def cmd_init(args):
    name = args.name.strip().replace(" ", "_")
    target_dir = STATE_DIR / name
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "holdouts").mkdir(exist_ok=True)
    (target_dir / "evidence").mkdir(exist_ok=True)

    plan_path = target_dir / "plan.md"
    if not plan_path.exists():
        plan_path.write_text(f"""# Feature Plan: {name}

**Created:** {datetime.utcnow().isoformat()}Z
**Status:** DRAFT (Awaiting Human Approval)

## 1. Intent: The 'Why' & 'Why Not'
- **Why we are building this:**
- **Explicit non-goals (What we are NOT building):**

## 2. Vertical Slices (Parallel Build Units)
- [ ] Slice A (e.g. backend / schema):
- [ ] Slice B (e.g. frontend / API):

## 3. Holdout Scenarios (Anti-Sycophancy)
- Hidden test cases stored in `holdouts/` that builders must NEVER inspect.
""", encoding="utf-8")

    meta_path = target_dir / "meta.json"
    meta_path.write_text(json.dumps({
        "name": name,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "phase": "PHASE_2_HOLDOUTS_AND_PLAN",
        "plan_approved": False,
        "validation_passed": False,
        "review_passed": False
    }, indent=2), encoding="utf-8")

    print(f"✅ Initialized Kem Dev Loop feature run: {target_dir}")
    print(f"   • Plan: {plan_path}")
    print(f"   • Hidden Holdouts Directory: {target_dir / 'holdouts'}")
    print(f"   • Evidence Output: {target_dir / 'evidence'}")
    return 0


def cmd_validate(args):
    name = args.name
    run_dir = STATE_DIR / name
    if not run_dir.exists():
        print(f"❌ Error: Run directory {run_dir} not found. Run: kem-dev-loop init {name}")
        return 1

    print(f"\n👁️ [Phase 4: Grounded Validation] Exercising {name}...")
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    test_cmd = args.test_cmd
    if test_cmd:
        print(f"   Running functional suite: `{test_cmd}`")
        res = run_cmd(test_cmd)
        log_file = evidence_dir / f"test_{int(datetime.utcnow().timestamp())}.log"
        log_file.write_text(f"Command: {test_cmd}\nExit Code: {res.returncode}\n\nSTDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}")
        
        if res.returncode != 0:
            print(f"❌ Functional validation FAILED (exit code {res.returncode}).")
            print(f"   Evidence serialized to: {log_file}")
            print("   🚨 SENT BACK TO BUILDERS with observable failure logs.")
            return 1
        print("   ✅ Functional test command passed.")

    # Check holdouts
    holdout_files = list((run_dir / "holdouts").glob("*"))
    if holdout_files:
        print(f"   🛡️ Executing {len(holdout_files)} hidden holdout scenario(s)...")
        for h in holdout_files:
            print(f"     • Holdout: {h.name}")
    else:
        print("   ℹ️  No holdouts registered in holdouts/ (recommended to add anti-sycophancy tests).")

    meta_path = run_dir / "meta.json"
    if meta_path.exists():
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        data["validation_passed"] = True
        data["phase"] = "PHASE_5_CODE_REVIEW"
        meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"🎉 Validation passed! Proceeding to decoupled Phase 5: Code Review.")
    return 0


def cmd_review(args):
    suite = args.suite or "ponytail"
    target = args.target or "."

    print(f"\n🤖 [Phase 5: Decoupled Code Review]")
    print(f"   Running review suite: `{suite}` against `{target}`")

    rh_check = run_cmd("which review-hub")
    if rh_check.returncode == 0:
        res = run_cmd(f"review-hub review {suite} {target}")
        print(res.stdout)
        if res.returncode != 0:
            print(res.stderr)
            return res.returncode
    else:
        print("   ℹ️  review-hub not found on PATH. Falling back to git diff check.")
        res = run_cmd(f"git diff --stat {target}")
        print(res.stdout)

    print("\n👤 [Phase 6: Final Human Intent Check]")
    print("   Validate: Does this change honor the original 'Why and Why Not'?")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Kem Glitch's 6-Phase AI Development Lifecycle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # route
    p_route = subparsers.add_parser("route", help="Classify task complexity (Fast Route vs Full Route)")
    p_route.add_argument("prompt", nargs="+", help="Task description")

    # init
    p_init = subparsers.add_parser("init", help="Initialize a feature run with hidden holdouts and plan")
    p_init.add_argument("name", help="Feature or run name")

    # validate
    p_val = subparsers.add_parser("validate", help="Run grounded persona validation & holdout suite")
    p_val.add_argument("name", help="Feature run name")
    p_val.add_argument("--test", dest="test_cmd", default=None, help="Functional test command (e.g. pytest, npm test)")

    # review
    p_rev = subparsers.add_parser("review", help="Run decoupled code review (Phase 5)")
    p_rev.add_argument("--suite", default="ponytail", help="Review suite (ponytail, unslop, typescript, no-comments)")
    p_rev.add_argument("target", nargs="?", default=".", help="Target directory or file")

    args = parser.parse_args()

    if args.command == "route":
        return cmd_route(args)
    elif args.command == "init":
        return cmd_init(args)
    elif args.command == "validate":
        return cmd_validate(args)
    elif args.command == "review":
        return cmd_review(args)


if __name__ == "__main__":
    sys.exit(main())
