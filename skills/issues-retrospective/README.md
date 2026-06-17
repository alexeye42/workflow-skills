# issues-retrospective

Process accumulated workflow issues, detect recurring patterns, and implement
improvements to skills and rules. This skill acts as the implementation phase
for issues recorded by `issues-recorder`.

## Invocation

Invoke this skill periodically (e.g., weekly or monthly) by saying:
"retrospective", "retro", "review issues".

It's better to implement each improvement in a new session (chat) to avoid context bloat.
To do this, say "implement <reference to a task file from `work` folder>" 
  or "implement improvements" (to implement tasks from `workflow/RETROSPECTIVE.md`).

> **Note:** This skill's execution can also be scheduled externally
> (for example, via Claude Dispatch) to run on a regular basis.

## Related skills

- **task-file-updater** (hard dependency) — used to create and track the
  implementation tasks.
- **issues-recorder** — the source of the daily improvement files that this
  skill processes.
