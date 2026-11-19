#!/usr/bin/env bash
# Run one sweep headlessly with either agent.
#
#   scripts/sweep.sh            # Claude Code
#   scripts/sweep.sh codex      # Codex
#
# Both get the same instruction and read the same playbook. Point any scheduler
# (cron, launchd, a Codex automation) at this script.
set -euo pipefail
cd "$(dirname "$0")/.."

agent="${1:-claude}"
prompt="Run one sweep of this repository now. Read playbooks/sweep.md and follow it exactly, start to finish, without asking questions. Today is $(date +%F)."

case "$agent" in
  claude)
    # Edits are auto-accepted; shell use is limited to the build, git and date.
    exec claude -p "$prompt" \
      --permission-mode acceptEdits \
      --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Agent,Bash(python3 scripts/build.py:*),Bash(git:*),Bash(date:*)"
    ;;
  codex)
    # --search turns on live web search. The sandbox may write inside this folder
    # and needs network access for git push.
    exec codex --search exec \
      --sandbox workspace-write \
      -c sandbox_workspace_write.network_access=true \
      "$prompt"
    ;;
  *)
    echo "usage: scripts/sweep.sh [claude|codex]" >&2
    exit 2
    ;;
esac
