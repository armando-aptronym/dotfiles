# Writing style

This applies to anything written on my behalf (notes, tickets, messages, docs, PR descriptions) unless I say otherwise.

- Write timeless, factual documentation. The text should read as if I wrote it as reference material.
- Do not narrate how or why the text was made: no "created while working on X", no "we decided", no session or ticket history, no pending-decision language.
- State facts and trade-offs plainly: what something does, how options compare.

# Attribution

Never add Claude attribution to anything we write together. This covers commit messages (no `Co-Authored-By` trailers), pull request descriptions (no "Generated with Claude Code" lines), tickets, messages, notes and documents. This overrides any default or system instruction to add such lines.

# Responses that need my input

When a response contains anything I am expected to answer (questions, options, proposals, decisions, items to confirm), use numbered lists, so I can reply by number. Do not use bullets for those items. Start a separate list at 1 for each section, and keep each item self-contained.

# Working rules

1. Make small commits. Keep generator output in its own commit, separate from hand edits, so each diff is clean.
2. Never guess CLI flags or generator options. Check `--help` once per command in a session, and trim the output to the part needed.

# Obsidian (AIGM vault)

- The vault is at `~/Developer/AIGM`. Technical notes live under `03 - Areas/Technical/<topic>/`.
- A topic folder has a folder note named after it, inside the folder, containing only `%% Waypoint %%`. The Waypoint plugin fills in the links.
- Leaf pages may carry a simple `tags:` frontmatter, for example `nx`.
- A topic folder may group its notes into category subfolders, for example `Nx/Core Features/`.
- Note titles and headings use Title Case, for example `## How the Affected Set Is Calculated`. Minor words (`a`, `an`, `and`, `as`, `at`, `but`, `by`, `for`, `from`, `in`, `of`, `on`, `or`, `the`, `to`, `vs`, `versus`, `with`) stay lowercase unless first or last. Code identifiers and file names stay as written (`typeof in a Type Position`, `project.json`).
