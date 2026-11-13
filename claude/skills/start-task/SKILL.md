---
name: start-task
description: Start work on a Notion task by ticket ID (for example AIGM-33). A sub-agent gathers the task, its project and the project's progress, then the main session asks only the questions the ticket leaves open, presents a fixed summary, and waits for a go-ahead. Use when the user says start, begin or get started on a task, or gives a ticket ID to work on.
---

# Start a task

Start work on one task from the Notion Tasks database. Apart from the status updates in step 3, change nothing until the user says to proceed.

## Steps

1. **Gather with a sub-agent.** Do not gather in the main session. Spawn the `notion-task` agent (Agent tool, `subagent_type: "notion-task"`) with the message `GATHER <N>`, where `<N>` is the number after the dash in the ticket ID (AIGM-33 is `33`). The agent's definition holds its prompt and pins a light model, so pass no model. It reads Notion only and returns a fixed structure. If a required field is missing from its result, fetch just that item yourself. If the agent type is unavailable, Claude Code needs a restart to pick up `~/.claude/agents/`.
2. **Ask only what is still open.** From the summary, decide which choices the ticket and the project leave unsettled. Typically: where the work lives, the working mode (the user runs commands and Claude explains, or Claude runs them), tooling, git remote and its visibility, and naming. Do not ask about anything already settled. Each question gets a recommended default and an alternative.
3. **Mark the work as started, silently.** The `GATHER` run already did this: the agent sets the ticket to In Progress and, if the project's status is To Do, the project to In Progress, and leaves a status alone when it is already In Progress or Done. Its report shows the ticket's status after the update, so show that status in the summary. Do not mention these updates in the reply. Do not call Notion tools in the main session.
4. **Present the summary in the output format below, then wait.** Do not start the work until the user answers or says "defaults".

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
