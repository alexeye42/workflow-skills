# task-file-updater

A skill that creates and updates task brief files in the `work/` directory,
providing a lightweight log of what happened during each task session and what
decisions were made.

The skill manages three files:
- **Task file** (`work/YYYYMMDD_task-name.md`) — per-task detail with summary,
  work items, and decisions.
- **LOG.md** — chronological list of all task files (newest first).
- **NOW.md** — current work status: active task, previous tasks, parking lot.

## Setup

Add the following instruction to your `AGENTS.md` (or `CLAUDE.md`):

```markdown
After every file write or edit, invoke task-file-updater skill to create/update task file(s).
```

## Related skills

- **issues-retrospective** — depends on task-file-updater to create task files
  for improvement work.
