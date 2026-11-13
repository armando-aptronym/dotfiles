---
name: finish-task
description: Close out a Notion task. Audits the acceptance criteria against what actually happened, quizzes the user where a criterion is "can explain", updates the Obsidian notes and the Notion task and session, and proposes follow-up tasks for approval. Sets every session under the task to Done. Use when the user says a task or session is complete, or asks to wrap up or close a ticket.
---

# Finish a task

Close out one task from the Notion Tasks database. Verify instead of assuming, and create nothing without the user's approval.

Do not load or call Notion tools in the main session. The `notion-task` agent does all the Notion reading, writing and creating, so the tool schemas stay out of the main context.

Notion data sources:
- Tasks: `collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd`
- Sessions: `collection://3e62b5c8-41e7-803b-8dac-000b86b4da8a`
- Projects: `collection://3e62b5c8-41e7-807b-9a90-000be3ac55ee`

## Steps

1. **Audit the acceptance criteria.**
   1. Read the task with the `notion-task` agent (Agent tool, `subagent_type: "notion-task"`), with the message `READ <N>`, where `<N>` is the number after the dash in the ticket ID. Keep its agent id, because steps 4 and 5 continue the same agent with SendMessage, which avoids loading the tool schemas again. If SendMessage is unavailable, spawn a new agent and send `READ <N>` again before the write message.
   2. If the task has a repo, gather evidence with an evidence sub-agent (the evidence prompt below, `subagent_type: "general-purpose"`, `model: "haiku"`). Otherwise the evidence is the conversation, so audit it directly.
   3. Judge each criterion as met or not met, with the evidence. Do not tick anything that has not been verified.
2. **Quiz where a criterion says "can explain".** Ask three or four short questions in the user's own words, grade the answers honestly, and correct gaps. Count the criterion as met only if the understanding is there.
3. **Update the documentation.** Notes live in the Obsidian vault, and the conventions in `CLAUDE.md` apply (folder note, tags, timeless factual style). Check the existing pages against what was actually done, and add or fix pages where they are out of date. Write each page once, with a single Write, instead of Write followed by Edit.
4. **Update Notion.** Continue the `notion-task` agent with a `WRITE` message, listing the verified criteria and plan items to tick verbatim, one per line, and any other edits, such as Resources, or `none`. The agent ticks the boxes, sets every session linked to the task to Done without asking per session, confirms with one re-query that none is still To Do, and sets the task to Done last. Do not edit logged or planned hours: `Logged Time (h)` is a formula that counts a session only once it is Done, so marking sessions Done is what logs the time. Report the sessions that were closed, by name. Do not fetch pages to verify the updates, because the agent's re-query is the only check.
5. **Audit for follow-ups, then ask.** List what is left over: unmet criteria, optional extensions, gaps in the docs. Present them as a numbered list. For each give a proposed task name, priority, estimate, project and due date, plus proposed sessions with their types and durations. Wait for explicit approval of each item. Then continue the `notion-task` agent with a `CREATE` message listing only the approved tasks, with their page content, and approved sessions, and leave unapproved ones uncreated.

Choosing the next task is out of scope. The user does that separately.

## Evidence sub-agent prompt

Used when the task has a repo. It stays a general-purpose agent for now, and can later be replaced by a custom code-reviewer agent by changing `subagent_type`.

Fill in the repo path and the criteria verbatim.

```
Gather evidence for these acceptance criteria. Read only: do not edit files, commit, push, or change Notion. Do not judge pass or fail.

Repo: <path>
Criteria:
<criteria, verbatim>

For each criterion, run the minimal read-only commands that show whether it holds: git status and log, gh run list or view, listing files, and running the project's own build, test or lint through its task runner. Return, for each criterion, the commands you ran and a trimmed result of one to three lines, never raw output over 10 lines. Also list anything unexpected: uncommitted changes, unpushed commits, failing or missing CI runs.
```
