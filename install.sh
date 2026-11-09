#!/usr/bin/env bash
# Link these dotfiles into place on a new macOS machine. Existing files are
# moved aside to <name>.bak before linking. Safe to re-run.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"

link() {  # link <source> <target>
  mkdir -p "$(dirname "$2")"
  if [ -e "$2" ] && [ ! -L "$2" ]; then mv "$2" "$2.bak"; fi
  ln -sfn "$1" "$2"
  echo "linked $2"
}

# VS Code
VSCODE="$HOME/Library/Application Support/Code/User"
link "$REPO/vscode/settings.json"    "$VSCODE/settings.json"
link "$REPO/vscode/keybindings.json" "$VSCODE/keybindings.json"
if command -v code >/dev/null; then
  xargs -L1 code --install-extension < "$REPO/vscode/extensions.txt"
else
  echo "VS Code 'code' command not found: run 'Shell Command: Install code command in PATH', then re-run."
fi

# Claude Code
link "$REPO/claude/settings.json"  "$HOME/.claude/settings.json"
link "$REPO/claude/statusline.sh"  "$HOME/.claude/statusline.sh"

# iTerm2: preferences are loaded from this folder (see README)
echo "iTerm2: Settings > General > Settings > 'Load settings from a custom folder or URL' -> $REPO/iterm2"
