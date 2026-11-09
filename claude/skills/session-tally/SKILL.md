---
name: session-tally
description: Measure the token cost of a Claude Code session, a skill run inside a session, or a sub-agent run, using the session transcript on disk. Use when the user asks what a skill or session cost, wants a token-efficiency audit, or wants to compare two runs.
---

# Session tally

Report token usage from transcripts. The numbers come from each API call's usage record, so measure instead of estimating.

## Steps

1. **Identify what to measure.** A named session (`~/.claude/scripts/session-tally.py --list` shows names), a session id, or a transcript path. A sub-agent's transcript is the `output_file` path in the Agent result. Pass it to the script, and never Read or tail it, because it is large.
2. **Run the script** with `python3 -I ~/.claude/scripts/session-tally.py <session>`. To isolate one skill run inside a longer session, add `--from "<text>"`, where the text appears in the user message that started it (for example `--from /finish-task`). Add `--json` for machine-readable output.
3. **Report** in this order: the totals (API calls, new context written to cache, context re-read, output), the context size at the start and end of the range, the largest tool results, and the models used. Name the biggest costs and what drives them: tool-schema loads show up as a large cache write right after a tool search, and re-reads grow with context size and with the number of calls.
4. **Compare** with an earlier run when the user has one, side by side, and say which change moved which number.

## Reading the numbers

- Cache re-reads are cheaper per token than new writes, but they repeat on every call, so extra context is paid for on every later turn.
- With `--from`, re-reads include the session's earlier context. Treat cache writes and the context added in the range as the run's own footprint, and re-reads as the cost of the session's length.
- Do not convert to dollars unless asked. Rates change, so get current ones from the `claude-api` skill first.
