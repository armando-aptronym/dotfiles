#!/bin/bash
# Status line: dir | model | context | usage
input=$(cat)

dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // ""')
dir="${dir/#$HOME/~}"

model=$(echo "$input" | jq -r '.model.display_name // "unknown"')

ctx_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
ctx_size=$(echo "$input" | jq -r '.context_window.context_window_size // empty')
if [ -n "$ctx_pct" ]; then
  ctx=$(printf "ctx %.0f%%" "$ctx_pct")
  [ -n "$ctx_size" ] && ctx="$ctx of $((ctx_size / 1000))k"
else
  ctx="ctx 0%"
fi

five=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
week=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
usage=""
[ -n "$five" ] && usage="5h $(printf '%.0f' "$five")%"
[ -n "$week" ] && usage="${usage:+$usage }7d $(printf '%.0f' "$week")%"
[ -z "$usage" ] && usage="usage n/a"

echo "$dir | $model | $ctx | $usage"
