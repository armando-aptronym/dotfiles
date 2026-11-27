---
name: finish-task
description: Close out a Notion task of any kind. Audits the acceptance criteria against what actually happened, quizzes the user where a criterion is "can explain", updates documentation when the task produced something worth keeping, updates the Notion task and sessions, and proposes follow-up tasks for approval. Sets every session under the task to Done. Use when the user says a task or session is complete, or asks to wrap up or close a ticket.
---

# Finish a task

Close out one task from the Notion Tasks database. Verify instead of assuming, and create nothing without the user's approval.

The `notion-worker` agent does the Notion reading, writing and creating, so the tool schemas stay out of the main context. Do not load or call Notion tools in the main session, except to delete a page the user asks to delete (`notion-delete-pages`, loaded with ToolSearch), because the worker cannot delete.

## Steps

1. **Audit the acceptance criteria.**
   1. Get the task's facts. When this session holds a `GATHER` report for the ticket, use it, updated by any later `EDIT` reports, and send nothing at this step. Otherwise, or when that report lacks the page url, acceptance criteria or sessions, spawn the `notion-worker` agent (Agent tool, `subagent_type: "notion-worker"`) with the message `READ <N>`, where `<N>` is the number after the dash in the ticket ID. Keep the id of the agent that supplied the facts, because later messages continue it with SendMessage, which avoids loading the tool schemas again. If SendMessage is unavailable, spawn a new `notion-worker` agent for each later message.
   2. Gather evidence from whatever the criteria point at. For a repo where this session has run the checks the criteria call for on the current code, use those results and confirm the repo state yourself with read-only commands (git status and log, `gh run list`). For any other repo case, such as finishing in a fresh session, use the evidence sub-agent (the prompt below, `subagent_type: "general-purpose"`, `model: "haiku"`). For produced files or outputs (a render, a document, a deployed page), read them directly. Otherwise the evidence is the conversation, so audit it directly.
   3. Judge each criterion as met or not met, with the evidence. Do not tick anything that has not been verified.
2. **Quiz where a criterion says "can explain".** Ask three or four short questions in the user's own words, grade the answers honestly, and correct gaps. Count the criterion as met only if the understanding is there.
3. **Update the documentation, when the task produced something worth keeping** (knowledge, a decision, a reusable asset). When it is unclear, ask once whether anything is worth writing down, and skip the step on a no. Notes live in the Obsidian vault, and the conventions in `CLAUDE.md` apply (folder note, tags, timeless factual style). Check the existing pages against what was actually done, and add or fix pages where they are out of date. Write each page once, with a single Write, instead of Write followed by Edit.
4. **Update Notion.** Continue the `notion-worker` agent with a `WRITE <N>` message holding the task page url, the verified criteria and plan items to tick, the unmet criteria to leave unticked (or `none`), and any other edits, such as Resources, or `none`. List items verbatim, one per line. The two criteria lists together cover every unticked criterion. The agent reads the current page and sessions, so no `READ` is needed first. If it answers `Page differs`, it has changed nothing: audit the criteria it returns and send `WRITE <N>` again. The agent ticks the boxes, sets every session linked to the task to Done without asking per session, confirms by fetching each session page that none is still To Do, and sets the task to Done last. Do not edit logged or planned hours: `Logged Time (h)` is a formula that counts a session only once it is Done, so marking sessions Done is what logs the time. Report the sessions that were closed, by name, and any Proposed sessions it left as they are (they were never approved; the user decides what to do with them). If the report says `Project complete: yes`, ask whether to set the project Done and, on a yes, continue the agent with `PROJECT DONE <project url>`. Do not fetch pages to verify the updates, because the agent's own check is the only one. If its report ends with a `Degraded:` line, pass that on to the user and go on.
5. **Audit for follow-ups, then ask.** List what is left over: unmet criteria, optional extensions and, when step 3 ran, gaps in the docs. Present them as a numbered list. For each give a proposed task name (Title Case), priority, estimate, Area, project and due date, plus proposed sessions with a short description, type and duration (multiples of 0.5 h, each under 2 h). Area, Type, Domain and project default to the finished task's, from the `GATHER` or `READ` report; the user can correct them. Wait for explicit approval of each item. Then continue the `notion-worker` agent with a `CREATE` message listing only the approved tasks (name, priority, estimate, Area, Type, Domain, project, due date, page content) and their approved sessions (description, type, hours), and leave unapproved ones uncreated. Approved tasks are created as To Do with To Do sessions; the agent names the sessions with the new ticket IDs.

For any other change to the task or its sessions that the user asks for, continue the agent with an `EDIT` message that lists each change with its page url and the exact new text or values.

Choosing the next task is out of scope. The user does that separately.

## Evidence sub-agent prompt

Used for a repo whose checks this session has not run (step 1). It is a general-purpose agent, selected by `subagent_type`.

Fill in the repo path and the criteria verbatim.

```
Gather evidence for these acceptance criteria. Read only: do not edit files, commit, push, or change Notion. Do not judge pass or fail.

Repo: <path>
Criteria:
<criteria, verbatim>

For each criterion, run the minimal read-only commands that show whether it holds: git status and log, gh run list or view, listing files, and running the project's own build, test or lint through its task runner. Return, for each criterion, the commands you ran and a trimmed result of one to three lines, never raw output over 10 lines. Also list anything unexpected: uncommitted changes, unpushed commits, failing or missing CI runs.
```
