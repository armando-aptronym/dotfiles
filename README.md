# dotfiles

Personal setup for macOS: zsh, Starship, VS Code, iTerm2 and Claude Code.

```
zsh/       zshrc, zprofile
starship/  starship.toml
vscode/    settings.json, keybindings.json, extensions.txt
iterm2/    com.googlecode.iterm2.plist
claude/    CLAUDE.md, settings.json, statusline.sh, agents/, hooks/, scripts/, skills/
Brewfile
install.sh
```

## Install

```sh
git clone https://github.com/armando-aptronym/dotfiles ~/Developer/dotfiles
~/Developer/dotfiles/install.sh
```

The script requires [Homebrew](https://brew.sh). It installs the packages in `Brewfile`, symlinks the zsh, Starship, VS Code and Claude Code files (backing up existing ones to `*.bak`) and installs the VS Code extensions listed in `vscode/extensions.txt`.

### Shell
- **Prompt:** [Starship](https://starship.rs), configured in `starship/starship.toml`. Its icons need a Nerd Font in the terminal.
- **Suggestions:** `zsh-autosuggestions` shows a suggestion from history as you type; the right arrow accepts it.
- **History search:** the up and down arrows search history for commands that start with the typed text. History is shared between sessions and stored in `~/.zhistory`.
- **Completion:** Tab completion through `compinit`, plus `gcloud` completion when the SDK is in `~/Developer/google-cloud-sdk`.
- **Highlighting:** `zsh-syntax-highlighting` colors the command line.

`zshrc` also defines aliases. It loads `~/.zshrc.local` when that file exists. The file is untracked and holds machine-specific settings such as `AWS_PROFILE`.

### iTerm2
Settings → General → Settings → tick "Load settings from a custom folder or URL" and choose `iterm2/`. Set "Save changes" to automatically if iTerm2 should write edits back to the repo.

### Claude Code
Only portable config lives here: `CLAUDE.md` (global preferences), `settings.json`, the status line script (needs `jq`), a `git push` pre-check hook (`hooks/pre-push-verify.sh`) the `start-task`, `finish-task` and `session-tally` skills, the `notion-worker` agent (a light-model worker for the skills' Notion reads and writes), and `scripts/session-tally.py` for measuring token usage from a session transcript.

The hook runs the checks CI runs (`npm ci --dry-run`, the Nx format check, and `lint test build typecheck`) before a `git push` that Claude Code runs in an npm project, and blocks the push if one fails. Conversation history, credentials and plugin caches in `~/.claude` are intentionally not tracked.

Plugin marketplaces are added from inside Claude Code, e.g. `/plugin marketplace add anthropics/claude-plugins-official`.

## Notes
- VS Code's `apc.*` settings need the Apc Customize UI++ extension, which patches VS Code's own files and may need re-enabling after updates.
- Fonts used: PT Mono (VS Code), MesloLGS NF (iTerm2).
