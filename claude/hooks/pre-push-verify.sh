#!/usr/bin/env bash
# PreToolUse hook for the Bash tool. Before a `git push`, runs the checks CI runs.
# Applies only to npm projects (package.json and package-lock.json at the repo root).
# Exit 2 blocks the push and shows the failure output to Claude.
set -uo pipefail

input=$(cat)
cmd=$(jq -r '.tool_input.command // empty' <<<"$input")
cwd=$(jq -r '.cwd // empty' <<<"$input")

# Only act on git push.
tok="(([^[:space:]'\"]|'[^']*'|\"[^\"]*\")+)"
push_re="(^|[;&|(])[[:space:]]*git(([[:space:]]+-[cC][[:space:]]+${tok})|([[:space:]]+--[a-z-]+(=${tok})?))*[[:space:]]+push([[:space:]]|\$)"
[[ $cmd =~ $push_re ]] || exit 0

# Work out which directory the push runs in: a git -C path, a leading cd, else the session cwd.
dir="$cwd"
cd_re='(^|[;&|[:space:]])cd[[:space:]]+([^[:space:];&|]+)'
c_re='git[[:space:]]+-C[[:space:]]+([^[:space:]]+)'
if [[ $cmd =~ $cd_re ]]; then dir="${BASH_REMATCH[2]}"; fi
if [[ $cmd =~ $c_re ]]; then dir="${BASH_REMATCH[1]}"; fi
dir="${dir//\"/}"; dir="${dir//\'/}"; dir="${dir/#\~/$HOME}"

root=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null) || exit 0
[[ -f "$root/package.json" && -f "$root/package-lock.json" ]] || exit 0
cd "$root" || exit 0

fail() {
  printf 'Push blocked: %s failed in %s.\n\n' "$1" "$root" >&2
  printf '%s\n' "$2" | tail -n 40 >&2
  exit 2
}

out=$(npm ci --dry-run 2>&1) || fail "npm ci --dry-run (is package-lock.json out of sync? run npm install)" "$(grep -E 'npm error (code|Missing|Invalid|`npm ci`)' <<<"$out" | head -n 12)"

if [[ -f nx.json ]]; then
  out=$(npx nx format:check --all 2>&1) || fail "nx format:check (run nx format:write)" "$out"
  out=$(npx nx run-many -t lint test build typecheck 2>&1) || fail "nx run-many -t lint test build typecheck" "$out"
fi
exit 0
