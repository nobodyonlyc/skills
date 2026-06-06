#!/bin/bash
# Blocks dangerous git commands on protected branches

COMMAND="$CLAUDE_TOOL_INPUT_COMMAND"

# Block force push to main/master
if echo "$COMMAND" | grep -qE 'git push.*--force|git push.*-f'; then
  if echo "$COMMAND" | grep -qE '(main|master)'; then
    echo "BLOCKED: Force push to main/master is not allowed." >&2
    exit 1
  fi
fi

# Block hard reset
if echo "$COMMAND" | grep -qE 'git reset --hard'; then
  echo "WARNING: git reset --hard will discard uncommitted changes. Proceed with caution." >&2
fi
