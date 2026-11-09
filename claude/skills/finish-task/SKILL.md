---
name: finish-task
description: Close out a Notion task. Audits the acceptance criteria against what actually happened, quizzes the user where a criterion is "can explain", updates the Obsidian notes and the Notion task and session, and proposes follow-up tasks for approval. Use when the user says a task or session is complete, or asks to wrap up or close a ticket.
---

# Finish a task

Close out one task from the Notion Tasks database. Verify instead of assuming, and create nothing without the user's approval.

Notion data sources:
- Tasks: `collection://3e62b5c8-41e7-80e7-9415-000bb0c582fd`
- Sessions: `collection://3e62b5c8-41e7-803b-8dac-000b86b4da8a`
- Projects: `collection://3e62b5c8-41e7-807b-9a90-000be3ac55ee`

## Steps

1. **Audit the acceptance criteria.** Check each criterion against the real state of the work: the repo, the commands that ran, CI. Report each as met or not met, with the evidence. Do not tick anything that has not been verified.
2. **Quiz where a criterion says "can explain".** Ask three or four short questions in the user's own words, grade the answers honestly, and correct gaps. Count the criterion as met only if the understanding is there.
3. **Update the documentation.** Notes live in the Obsidian vault at `~/Developer/AIGM`, under `03 - Areas/Technical/<topic>/`.
   - The topic folder has a folder note named after it, containing only `%% Waypoint %%`.
   - Leaf pages carry a simple `tags:` frontmatter.
   - Check the existing pages against what was actually done, and add or fix pages where they are out of date.
   - Write timeless, factual reference material: no narration of how it was made, no "we decided", no ticket or session history.
4. **Update Notion.** Tick the acceptance-criteria and plan boxes that are verified. Fill in anything the ticket asks to record, such as Resources. Set the session or sessions to Done, then the task to Done. Do not change logged or planned hours.
5. **Audit for follow-ups, then ask.** List what is left over: unmet criteria, optional extensions, gaps in the docs. Present them as a numbered list. For each give a proposed task name, priority, estimate, project and due date, plus proposed sessions with their types and durations. Wait for explicit approval of each item. Create only the approved tasks and sessions, and leave unapproved ones uncreated.

Choosing the next task is out of scope. The user does that separately.
