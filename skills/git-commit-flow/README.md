# git-commit-flow

A meta-skill that handles git commits for AI-generated and human-edited content
with a conventional message format (`feat`/`fix` with folder scope, prefixed with `ai`/`human`).

## Why This Skill Exists

1. It drastically decreases the need for manual commits and writing commit messages. 
  It triggers commit every time an eligible file is changed. 

2. For `git-diff-analyzer` to learn from your corrections, every AI-generated
  result needs two commits: one for the raw AI output, one for your edits. This 
  skill standardizes the commit format so `git-diff-analyzer` can reliably find
  and compare the right commit pairs.

## Suggested CLAUDE.md / AGENTS.md Instructions

Place the following in your root project-level context file:

```markdown
## Git commits

After completing an AI generation of any content 
except for program code, skills, rules and other context files,
use `git-commit-flow` skill with author `ai` to commit the result.

If the user signals that they edited a file(s) (e.g., "I reviewed it", 
"check my edits", "commit my changes", etc), use `git-commit-flow` 
with author `human` to commit user edits before following other instructions.

At the start of every session (before handling the first user message), 
run `git status --short`. If there are uncommitted changes in content files, 
use `git-commit-flow` with author `human/ai` to commit them before doing anything else.
```

## Why Not in Every Skill?

Embedding commit instructions in each skill would mean every new or updated
skill must be processed by a `skill-updater` to stay in sync — an unreasonable
maintenance burden. A single project-level instruction that delegates to
`git-commit-flow` is the pragmatic solution.
