---
name: start-task
description: Start work on a Notion task by ticket ID (for example AIGM-33). A sub-agent gathers the task, its project and the project's progress, then the main session asks only the questions the ticket leaves open, presents a fixed summary, and waits for a go-ahead. Use when the user says start, begin or get started on a task, or gives a ticket ID to work on.
---

# Start a task

Start work on one task from the Notion Tasks database. Apart from the status updates in step 3, change nothing until the user says to proceed.

## Steps

1. **Gather with a sub-agent.** Do not gather in the main session. Spawn one agent (Agent tool, `subagent_type: "general-purpose"`, `model: "haiku"`) with the prompt below, replacing `<N>` with the number after the dash in the ticket ID (AIGM-33 is `33`). It reads Notion only and returns a fixed structure. If a required field is missing from its result, fetch just that item yourself.
2. **Ask only what is still open.** From the summary, decide which choices the ticket and the project leave unsettled. Typically: where the work lives, the working mode (the user runs commands and Claude explains, or Claude runs them), tooling, git remote and its visibility, and naming. Do not ask about anything already settled. Each question gets a recommended default and an alternative.
3. **Mark the work as started, silently.** Right before presenting the summary, set the ticket's Status to In Progress with `notion-update-page` (`update_properties`, Status only). If the project's status is To Do, set the project to In Progress too. Leave a status alone when it is already In Progress or Done. Show the ticket status as In Progress in the summary. Do not mention these updates in the reply.
4. **Present the summary in the output format below, then wait.** Do not start the work until the user answers or says "defaults".

## Sub-agent prompt

```
Gather facts about Notion task AIGM-<N> and return them in the exact structure at the end. Read only: change nothing in Notion. Be efficient: use the fewest calls you can.

1. Load tools with one ToolSearch call: select:mcp__claude_ai_Notion__notion-fetch,mcp__claude_ai_Notion__notion-query-data-sources
2. Query the Tasks data source (collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd) for every task in the same project as ticket <N>. Columns: url, "Ticket ID" (integer), "Task Name", "Status" (Unplanned, To Do, Blocked, In Progress, Done), "Priority" (High, Medium, Low), "Estimate (h)", "date:Due Date:start", "Type" (JSON array), "Area", "Project" (JSON array of page URLs). Query:
   SELECT "Ticket ID", "Task Name", "Status", "Priority", "Estimate (h)", "date:Due Date:start" AS due, "Type", "Area", "Project", url FROM "collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd" WHERE "Project" = (SELECT "Project" FROM "collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd" WHERE "Ticket ID" = ?) ORDER BY due
   with params [<N>]. The query tool takes a single argument named `data`. Put `mode`, `data_source_urls`, `query` and `params` directly inside it, and do not repeat `data` inside itself. If the task has no project (zero rows), query only the ticket row. Do not fetch the data source schema unless a query errors.
3. In parallel with 4, query the Projects data source (collection://3e62b5c8-41e7-807b-9a90-000be3ac55ee). Columns: url, "Project Name", "Status", "Priority", "date:Start Date:start", "date:End Date:start". Match url to the project URL from step 2.
4. Fetch the ticket's own page (its url from step 2) for its body.

Return only this, with no commentary:
- Ticket: id, name, page url, status, priority, estimate (h), due date, type, area
- Background: two sentences at most
- Acceptance criteria: verbatim list
- Plan and resources: verbatim lists from the page
- Project: name, page url, status, priority, start and end dates
- Project tasks: a table of id, name, status, estimate (h), due date, ordered by due date, with the ticket's own row marked
```

## Output format

Use this structure every time, so runs read the same.

```
## AIGM-<N>: <task name>

**Ticket:** <type>, <area> area, <priority> priority, due <date>, estimate <h> h, status <status>. <One sentence of background.>

**Acceptance criteria**
- <criterion, verbatim>

**Project: <name>** (<start> to <end>, <priority> priority). <X of Y tasks done, Z h estimated.>

| ID | Task | Est. | Due |
| --- | --- | --- | --- |
| <N> | <name> (this one) | <h> | <MM-DD> |
| ... | ... | ... | ... |

<One sentence on what comes before and after this task.>

**Open questions**

1. <question>? Recommended: <default>. Alternative: <option>.
2. ...

**Plan:** <One or two sentences on how the work will go.> Reply with answers by number, or say "defaults". The work does not start until you confirm.
```
