---
name: task-file-updater
description: >
  Create and update task files that outline what was done and what decisions were made. 
  Use when the user says "save task file", "update task file", or similar.
  Also can fire after a file write or edit if configured in AGENTS.md (see `task-file-updater/README.md`).
---

# Task File Updater

Create and update task files. Make the work done on a task readable for
the user by describing it as briefly as possible without losing essential
information (WHAT was done and WHY).

## Core Concept

A **task** is the work done during **one session** unless the next session is
restored from the previous one — then the task continuation goes in the same
task file.

## Files Managed

This skill manages three files in the `work/` directory.

### 1. Task file: `work/YYYYMMDD_task-name.md`

`task-name` is an agent-generated 2–4 word English slug (the user can correct it).

Format:

```markdown
# Task name (same as in file name)
- Created: <YYYY-MM-DD H24:MI>
- Last updated: <YYYY-MM-DD H24:MI>

## Summary
1 paragraph about what happened and what decisions were made.

## What happened
Bullet list of work items done and issues encountered (if any).

## Decisions made
Numbered list of ESSENTIAL decisions about the task at hand made by agent or user.
```

> [!IMPORTANT]
> **"Last updated" must reflect the current time on every write or edit.**
> Every time the task file is created or modified, set "Last updated" to the current timestamp. 

#### Writing the "Decisions made" section

- Record decisions about the task at hand (rules, scope, trade-offs, etc.).
- Do NOT record workflow-related decisions here if issues-recorder skill is available.
- Include the reason (the "why") **only when** the reason was actually discussed
  OR (was made by you AND is non-obvious). Omit reasons that are self-evident (e.g., "user preference").
- Format: `N. <Decision statement>.` — optionally followed by the reason on the
  same line only if it adds real information.

Good examples:
```
1. Task files live in `work/`, named `YYYYMMDD_task-name.md`.
2. Renamed session-file-updater → task-file-updater. Reason: the file tracks
   a task (which can span sessions), not necessarily a single session.
3. issues-recorder and issues-retrospective replace `refine` as a two-phase
   alternative. Reason: separating detection from implementation allows pattern
   accumulation and scheduled retrospectives.
```

Bad examples (avoid as too self-evident):
```
1. Task files live in `work/`. Reason: user preference for project-root-level visibility.
2. Task-file-updater manages 3 files: task file, LOG.md, NOW.md. Reason: provides both per-task detail and project-level overview.
```

### 2. Work log: `work/LOG.md`

Bullet list of all task files (newest first), **no heading**.
Each line: `- <file name>: <summary paragraph>`

### 3. Work status: `work/NOW.md`

```markdown
# Current work
Last updated: <YYYY-MM-DD H24:MI>

## Active task
<file name>: <summary paragraph> for the task in progress

## Previous tasks
<file name>: <summary paragraph> for what was active before (≤3 tasks, newest first)

## Parking lot
Bullet list of free-form work items discussed as "out of scope" or "in future".
Items removed when recorded in a task file (semantic similarity match).
```

## Update Rules

| File | When updated | Action |
|---|---|---|
| Task file | After every artifact change (Write/Edit tools) | If current task doesn't exist in NOW.md (Active or Previous), create new file. Otherwise reconcile content with what happened since last update. |
| LOG.md | Only when a **new** task file is created | Add new task as top item. |
| NOW.md | Only when active task **changes** (new file created or previous task restored) | Move old active → Previous; add new Active; trim Previous to ≤3. Update "Last updated" timestamp. |

## Key Behaviors

### Task matching

Analyze ONLY `work/NOW.md`. If a semantically similar task exists among active
and previous tasks, use that task file; otherwise create a new one.

### Session restoration

If the user starts a new session with a task matching a Previous task in NOW.md,
move it back to Active (former Active becomes Previous) and continue updating the same task file.

### Parking lot cleanup

When a new task file semantically matches a parking lot item, remove that item from NOW.md.

### No "done" marking

Completed tasks stay in Previous (pushed out naturally when the list exceeds 3).

## Anti-Patterns

- NEVER leave "Last updated" unchanged after modifying a task file or NOW.md.
- NEVER fabricate reasons for decisions that were not discussed.
- NEVER add "Reason: ..." to every decision mechanically.

