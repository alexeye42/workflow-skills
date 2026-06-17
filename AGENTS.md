# Agent Instructions

## Git commits

After completing an AI generation of any content 
except for program code, skills, rules and other context files,
use `git-commit-flow` skill with author `ai` to commit the result.

If the user signals that they edited a file(s) (e.g., "I reviewed it", 
"check my edits", "commit my changes", etc.), use `git-commit-flow` 
with author `human` to commit user edits before following other instructions.

At the start of every session (before handling the first user message), 
run `git status --short`. If there are uncommitted changes in content files, 
use `git-commit-flow` with author `human/ai` to commit them before doing anything else.

## General workflows

- Before implementing a complex multi-step task, formulate your understanding of 
  a broader goal, ask "Do I get it right?" and wait for user approval or corrections.

- After every file write or edit, invoke task-file-updater skill to create/update task file(s).