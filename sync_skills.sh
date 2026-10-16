#!/usr/bin/env bash
# sync_skills.sh — Synchronize and install glitch-cat-skills
# Installs into ~/.gemini/config/skills and ~/.pi/agent/skills, and links ~/.local/bin launchers.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEMINI_HARNESS="$HOME/.gemini/config/skills"
PI_HARNESS="$HOME/.pi/agent/skills"
BIN_DIR="$HOME/.local/bin"

EXCLUDES=(
    --exclude "__pycache__"
    --exclude "*.pyc"
    --exclude ".venv"
    --exclude "node_modules"
    --exclude ".git"
    --exclude "README.md"
    --exclude ".env"
    --exclude ".env*"
    --exclude ".DS_Store"
    --exclude "Thumbs.db"
)

DO_PUSH=false
DO_PULL=false

for arg in "$@"; do
    case "$arg" in
        --push|-p)
            DO_PUSH=true
            ;;
        --pull|-u)
            DO_PULL=true
            ;;
        --status|-s)
            echo "📊 [glitch-sync] Repository Status:"
            git -C "$SCRIPT_DIR" status --short
            exit 0
            ;;
    esac
done

if [ "$DO_PULL" = true ]; then
    echo "📥 [glitch-sync] Pulling latest updates from GitHub..."
    git -C "$SCRIPT_DIR" pull origin main
fi

echo "🐱 [glitch-sync] Installing Glitch Cat Engineering Skills from $SCRIPT_DIR..."

mkdir -p "$GEMINI_HARNESS" "$PI_HARNESS" "$BIN_DIR"

for skill_dir in "$SCRIPT_DIR"/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        skill_name="$(basename "$skill_dir")"
        echo "  📦 Syncing skill: $skill_name"
        mkdir -p "$GEMINI_HARNESS/$skill_name" "$PI_HARNESS/$skill_name"
        rsync -avu "${EXCLUDES[@]}" "$skill_dir" "$GEMINI_HARNESS/$skill_name/" >/dev/null 2>&1
        rsync -avu "${EXCLUDES[@]}" "$skill_dir" "$PI_HARNESS/$skill_name/" >/dev/null 2>&1
    fi
done

echo "🔗 [glitch-sync] Configuring CLI launchers in $BIN_DIR..."

[ -f "$SCRIPT_DIR/state-compactor/scripts/cgate.py" ] && ln -sf "$SCRIPT_DIR/state-compactor/scripts/cgate.py" "$BIN_DIR/cgate" && chmod +x "$SCRIPT_DIR/state-compactor/scripts/cgate.py"
[ -f "$SCRIPT_DIR/state-compactor/scripts/compactor.py" ] && ln -sf "$SCRIPT_DIR/state-compactor/scripts/compactor.py" "$BIN_DIR/state-compactor" && chmod +x "$SCRIPT_DIR/state-compactor/scripts/compactor.py"
[ -f "$SCRIPT_DIR/agentic-engineering/agentic.py" ] && ln -sf "$SCRIPT_DIR/agentic-engineering/agentic.py" "$BIN_DIR/agentic" && chmod +x "$SCRIPT_DIR/agentic-engineering/agentic.py"
[ -f "$SCRIPT_DIR/guard-hooks/guard_hooks.py" ] && ln -sf "$SCRIPT_DIR/guard-hooks/guard_hooks.py" "$BIN_DIR/guard-hooks" && chmod +x "$SCRIPT_DIR/guard-hooks/guard_hooks.py"
[ -f "$SCRIPT_DIR/parallel-test-lane/parallel_test_lane.py" ] && ln -sf "$SCRIPT_DIR/parallel-test-lane/parallel_test_lane.py" "$BIN_DIR/parallel-test-lane" && chmod +x "$SCRIPT_DIR/parallel-test-lane/parallel_test_lane.py"
[ -f "$SCRIPT_DIR/worktree-harness/scripts/harness.py" ] && ln -sf "$SCRIPT_DIR/worktree-harness/scripts/harness.py" "$BIN_DIR/worktree-harness" && chmod +x "$SCRIPT_DIR/worktree-harness/scripts/harness.py"
[ -f "$SCRIPT_DIR/eval-router/eval_router.py" ] && ln -sf "$SCRIPT_DIR/eval-router/eval_router.py" "$BIN_DIR/eval-router" && chmod +x "$SCRIPT_DIR/eval-router/eval_router.py"

if [ "$DO_PUSH" = true ]; then
    echo "🚀 [glitch-sync] Committing and pushing updates to GitHub..."
    if [ -d "$SCRIPT_DIR/.git" ]; then
        cd "$SCRIPT_DIR"
        if [ -n "$(git status --porcelain)" ]; then
            git add -A
            git commit -m "sync: glitch-cat skills update [$(date -u +'%Y-%m-%dT%H:%M:%SZ')]"
            git push origin main
        else
            echo "✅ Working tree is already clean. Nothing to commit."
        fi
    fi
fi

echo "✅ All Glitch Cat skills synchronized into harnesses and ~/.local/bin."
