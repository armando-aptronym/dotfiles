---
name: finish-task
description: Close out a Notion task. Audits the acceptance criteria against what actually happened, quizzes the user where a criterion is "can explain", updates the Obsidian notes and the Notion task and session, and proposes follow-up tasks for approval. Sets every session under the task to Done. Use when the user says a task or session is complete, or asks to wrap up or close a ticket.
---

# Finish a task

Close out one task from the Notion Tasks database. Verify instead of assuming, and create nothing without the user's approval.

Do not load or call Notion tools in the main session. A sub-agent does all the Notion reading and writing, so the tool schemas stay out of the main context.

Notion data sources:
- Tasks: `collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd`
- Sessions: `collection://3e62b5c8-41e7-803b-8dac-000b86b4da8a`
- Projects: `collection://3e62b5c8-41e7-807b-9a90-000be3ac55ee`

## Steps

1. **Audit the acceptance criteria.**
   1. Read the task with a Notion sub-agent (Agent tool, `subagent_type: "general-purpose"`, `model: "haiku"`, prompt A). Keep its agent id, because steps 4 and 5 continue the same agent with SendMessage, which avoids loading the tool schemas again. If SendMessage is unavailable, spawn a new agent with the same tool loading line plus the write prompt.
   2. If the task has a repo, gather evidence with an evidence sub-agent (prompt B, same agent settings). Otherwise the evidence is the conversation, so audit it directly.
   3. Judge each criterion as met or not met, with the evidence. Do not tick anything that has not been verified.
2. **Quiz where a criterion says "can explain".** Ask three or four short questions in the user's own words, grade the answers honestly, and correct gaps. Count the criterion as met only if the understanding is there.
3. **Update the documentation.** Notes live in the Obsidian vault, and the conventions in `CLAUDE.md` apply (folder note, tags, timeless factual style). Check the existing pages against what was actually done, and add or fix pages where they are out of date. Write each page once, with a single Write, instead of Write followed by Edit.
4. **Update Notion.** Continue the Notion sub-agent with prompt C, passing the verified criteria and plan items verbatim and anything the ticket asks to record, such as Resources. It ticks the boxes, sets every session linked to the task to Done without asking per session, confirms with one re-query that none is still To Do, and sets the task to Done last. Do not edit logged or planned hours directly: `Logged Time (h)` is a formula that counts a session only once it is Done, so marking sessions Done is what logs the time. Report the sessions that were closed, by name. Do not fetch pages to verify the updates, because the sub-agent's re-query is the only check.
5. **Audit for follow-ups, then ask.** List what is left over: unmet criteria, optional extensions, gaps in the docs. Present them as a numbered list. For each give a proposed task name, priority, estimate, project and due date, plus proposed sessions with their types and durations. Wait for explicit approval of each item. Then continue the Notion sub-agent with prompt D to create only the approved tasks and sessions, and leave unapproved ones uncreated.

Choosing the next task is out of scope. The user does that separately.

## Sub-agent prompts

Prompt A, read the task. Replace `<N>` with the number after the dash in the ticket ID.

```
Read facts about Notion task AIGM-<N>. Read only for now: change nothing. A follow-up message will give you writes to do, so keep your loaded tools.

1. Load tools with one ToolSearch call: select:mcp__claude_ai_Notion__notion-fetch,mcp__claude_ai_Notion__notion-query-data-sources
2. Query the Tasks data source (collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd): SELECT url, "Task Name", "Status", "Project" FROM "collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd" WHERE "Ticket ID" = ? with params [<N>].
3. Query the Sessions data source (collection://3e62b5c8-41e7-803b-8dac-000b86b4da8a), whose columns are url, "Session Name", "Status" (To Do or Done), "Planned Duration (h)", "Type" and "Task" (a JSON array of task page URLs): SELECT url, "Session Name", "Status" FROM "collection://3e62b5c8-41e7-803b-8dac-000b86b4da8a" WHERE "Task" LIKE ? with params ["%<the task's url from step 2>%"].
4. Fetch the task page (its url from step 2).
The query tool takes a single argument named `data`. Put `mode`, `data_source_urls`, `query` and `params` directly inside it, and do not repeat `data` inside itself.

Return only this, with no commentary: the task url, name and status; the acceptance criteria, plan items and resources, each verbatim; the sessions linked to the task, each with its url, name and status.
```

Prompt B, gather evidence for a code task. Fill in the repo path and the criteria verbatim.

```
Gather evidence for these acceptance criteria. Read only: do not edit files, commit, push, or change Notion. Do not judge pass or fail.

Repo: <path>
Criteria:
<criteria, verbatim>

For each criterion, run the minimal read-only commands that show whether it holds: git status and log, gh run list or view, listing files, and running the project's own build, test or lint through its task runner. Return, for each criterion, the commands you ran and a trimmed result of one to three lines, never raw output over 10 lines. Also list anything unexpected: uncommitted changes, unpushed commits, failing or missing CI runs.
```

Prompt C, update Notion after the audit. Send as a follow-up message to the same agent.

```
Now do these writes. Load the extra tools with one ToolSearch call: select:mcp__claude_ai_Notion__notion-update-page
1. On the task page, tick exactly these boxes with update_content, using a short old_str such as "- [ ] <start of item>" that matches once: <items, verbatim>.
2. Apply these other edits to the task page: <edits, or "none">.
3. For each session you listed that is still To Do, set Status to Done with update_properties. Do not ask per session.
4. Re-query the Sessions data source for rows whose "Task" contains the task's url. Confirm that none is still To Do. If one is, fix it and re-query once.
5. Set the task's Status to Done last.
6. Do not edit any hours. Do not fetch pages to verify anything.
Return one short block: the boxes ticked, the sessions set to Done by name, the task's final status, and any warnings.
```

Prompt D, create approved follow-ups. Send as a follow-up message to the same agent.

```
Create only these approved items. Load the extra tools with one ToolSearch call: select:mcp__claude_ai_Notion__notion-create-pages
Tasks go in the Tasks data source (parent data_source_id 3e62b5c8-41e7-80e7-9415-000bb0c582fd) with these exact property names: "Task Name", "Status", "Priority" (High, Medium or Low), "Estimate (h)", "Type" (["📚 Learning"]), "Area", "Project" (an array of project page URLs), "date:Due Date:start", "date:Due Date:is_datetime" (0). Sessions go in the Sessions data source (parent data_source_id 3e62b5c8-41e7-803b-8dac-000b86b4da8a) with "Session Name", "Status" (To Do), "Planned Duration (h)", "Type" (Deep Work, Admin, Learning or Planning) and "Task" (an array holding the task page URL).
<approved tasks with their page content, and approved sessions>
Return the url of each page you created, and nothing else.
```
