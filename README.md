# dotfiles

Personal setup for macOS: VS Code, iTerm2 and Claude Code.

```
vscode/   settings.json, keybindings.json, extensions.txt
iterm2/   com.googlecode.iterm2.plist
claude/   CLAUDE.md, settings.json, statusline.sh, hooks/, scripts/, skills/
install.sh
```

## Install

```sh
git clone https://github.com/armando-aptronym/dotfiles ~/Developer/dotfiles
~/Developer/dotfiles/install.sh
```

The script symlinks the VS Code and Claude Code files (backing up existing ones to `*.bak`) and installs the VS Code extensions listed in `vscode/extensions.txt`.

### iTerm2
Settings → General → Settings → tick "Load settings from a custom folder or URL" and choose `iterm2/`. Set "Save changes" to automatically if iTerm2 should write edits back to the repo.

### Claude Code
Only portable config lives here: `CLAUDE.md` (global preferences), `settings.json`, the status line script (needs `jq`), a `git push` pre-check hook (`hooks/pre-push-verify.sh`) the `start-task`, `finish-task` and `session-tally` skills, and `scripts/session-tally.py` for measuring token usage from a session transcript.

The hook runs the checks CI runs (`npm ci --dry-run`, the Nx format check, and `lint test build typecheck`) before a `git push` that Claude Code runs in an npm project, and blocks the push if one fails. Conversation history, credentials and plugin caches in `~/.claude` are intentionally not tracked.

Plugin marketplaces are added from inside Claude Code, e.g. `/plugin marketplace add anthropics/claude-plugins-official`.

## Notes
- VS Code's `apc.*` settings need the Apc Customize UI++ extension, which patches VS Code's own files and may need re-enabling after updates.
- Fonts used: PT Mono (VS Code), MesloLGS NF (iTerm2).
