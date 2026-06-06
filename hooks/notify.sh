#!/bin/bash
# Notifies when Claude finishes a turn
# Customize: replace with your preferred notification method

MESSAGE="${1:-Claude finished}"

# Terminal bell
echo -e "\a"

# Desktop notification (Linux)
if command -v notify-send &>/dev/null; then
  notify-send "Claude Code" "$MESSAGE" --icon=terminal 2>/dev/null
fi

# macOS
if command -v osascript &>/dev/null; then
  osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\""
fi
