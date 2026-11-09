---
name: start-task
description: Start work on a Notion task by ticket ID (for example AIGM-33). Pulls the task, its sessions and the project's progress, asks only the questions the ticket leaves open, and waits for a go-ahead. Use when the user says start, begin or get started on a task, or gives a ticket ID to work on.
---

# Start a task

Start work on one task from the Notion Tasks database. Change nothing until the user says to proceed.

Notion data sources:
- Tasks: `collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd` (`Ticket ID` is an integer, so AIGM-33 is `33`)
- Sessions: `collection://3e62b5c8-41e7-803b-8dac-000b86b4da8a`
- Projects: `collection://3e62b5c8-41e7-807b-9a90-000be3ac55ee`

## Steps

1. **Pull the ticket.** Find the task by ticket ID with a Notion search or a query on the Tasks data source, then fetch the page. Extract the goal and background, acceptance criteria, plan, resources, estimate, priority, type and due date.
2. **Pull its sessions.** Fetch each linked session page. Note the planned duration, the booked time slot, the status, and how far away the next session is.
3. **Check progress on the project.** Fetch the task's project page and query the Tasks data source for every task in that project (`Project` is a JSON array of page URLs, so match with `LIKE`). Summarize which tasks are done and which remain, the hours estimated and logged, the due dates, and which tasks come immediately before and after this one.
4. **Ask only what is still open.** Decide from the ticket and the project which choices are unsettled. Typically: where the work lives, the working mode (the user runs commands and Claude explains, or Claude runs them), tooling, git remote and its visibility, and naming. Do not ask about anything the ticket or project already settles. Ask everything in one message as a numbered list, each item with a recommended default.
5. **State the plan and wait.** Restate the goal and acceptance criteria in a few lines, with the session time and the project context. Say when ready, and do not start until the user confirms.
