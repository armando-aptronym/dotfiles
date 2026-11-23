---
name: start-task
description: Start work on a Notion task by ticket ID (for example TASK-33). A sub-agent gathers the task and its project, then the main session asks only the questions the ticket leaves open, presents a fixed summary and waits for a go-ahead. Use when the user says start, begin or get started on a task, or gives a ticket ID to work on.
---

# Start a task

Start work on one task from the Notion Tasks database. Change nothing until the user says to proceed, apart from the status updates the `GATHER` run makes.

## Steps

1. **Gather with a sub-agent.** Do not gather or call Notion tools in the main session. Spawn the `notion-task` agent (Agent tool, `subagent_type: "notion-task"`) with the message `GATHER <N>`, where `<N>` is the number after the dash in the ticket ID (TASK-33 is `33`). The agent's definition holds its prompt and pins a light model, so pass no model. It reads Notion, sets the ticket to In Progress when it is To Do (and its project to In Progress when that is To Do), and returns a fixed structure. Do not mention these updates in the reply. If its report ends with a `Degraded:` line, show those fields as unknown and go on. If a required field is still missing, fetch just that item yourself. If the agent type is unavailable, Claude Code needs a restart to pick up `~/.claude/agents/`.
2. **Ask only what is still open.** Start from the Open questions in the report, then add any choice the ticket and project leave unsettled: where the work lives, the working mode (the user runs commands and Claude explains, or Claude runs them), tooling, git remote and its visibility, naming. Do not ask about anything already settled. Each question gets a recommended default and an alternative.
3. **Present the summary in the output format below, then wait.** Show the ticket's status as the report gives it. When that status is not To Do or In Progress, put this line first: "Not approved yet (status <status>). Run review-queue first." Do not start the work until the user answers or says "defaults".

## Output format

Use this structure every time, so runs read the same.

```
## TASK-<N>: <task name>

**Ticket:** <type>, <area> area, <priority> priority, due <date>, estimate <h> h, status <status>. <One sentence of background.>

**Acceptance criteria**
- <criterion, verbatim>

**Project: PROJ-<n> <name>** (<start> to <end>, <priority> priority). <X of Y tasks done, Z h estimated.>

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
