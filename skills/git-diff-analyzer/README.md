# git-diff-analyzer

Closes the feedback loop between your manual corrections and the agent's future output.
Compares two git commits (AI output → human corrections), extracts reusable patterns
from the diff, and applies them to the relevant skill.

## Typical Workflow

1. **AI generates content** → `git-commit-flow` commits with author `ai`
2. **User reviews and edits** the output in their editor
3. **User signals edits** (e.g., "I fixed it", "commit my changes") → `git-commit-flow` commits with author `human`
4. **User triggers analysis** (e.g., "analyze my edits", "what did I fix") → `git-diff-analyzer` runs:
   - Commits uncommitted changes, if any
   - Identifies the commit pair (AI output = commit A, human edits = commit B) by **location overlap**
   - Runs `git diff` between the two commits
   - Classifies each change as **significant** (reusable pattern) or **trivial** (skip)
   - Presents conclusions to the user for review
   - Updates the target skill(s) with confirmed conclusions (optionally via `skill-creator` and `skill-judge`)

## Major Restrictions

### User must signal their edits

The workflow depends on the user telling the agent about their edits (e.g., "I
fixed it", "commit my changes"). If the user edits files silently, those edits
will be bundled into the next AI commit, sometimes polluting the learning loop. 
The session-start `git status` check (see `git-commit-flow`
[README](../git-commit-flow/README.md)) catches stale uncommitted edits between
sessions, but it uses the `human/ai` author, which the analyzer skips.

### No evidence accumulation across multiple diffs

Each analysis run produces conclusions and immediately updates a skill. A pattern
seen once might be noise. There is no staging mechanism to hold observations until
they recur in multiple diffs. Frequent analysis runs on small diffs may lead to
skill bloat.

## Other Known Restrictions And Comments

### Pair matching requires location-based commit descriptions

`git-diff-analyzer` relies on commit descriptions naming
**where** changes happened (which files or sections), not summarizing **what** changed
in the content. If descriptions are too vague (e.g., "edited the article" with no
file/section detail), pair matching becomes ambiguous and the user will be asked
to confirm.

### `human/ai` commits are skipped

Commits with author `human/ai` (typically from session-start uncommitted changes
of unclear origin) cannot serve as either commit A or commit B. The analyzer
skips them when searching for pairs. They are valid git checkpoints but don't
participate in the learning loop.

### Folder-level commits, file-level edits

`git-commit-flow` creates one commit per folder. If the user makes unrelated edits
in different files of the same folder, the analyzer might conflate independent fixes
into a single pattern. The existing rule — "focus on patterns, not individual
fixes" — mitigates this.

### Skill identification is a best guess

When running in a fresh session with no chat context about which skill produced
the AI output, the analyzer guesses the target skill and presents the guess to
the user for confirmation before changes are applied.

### Skill-file commits use a separate convention

The analyzer commits updated skills with `fix(skills): ai ...`, which is outside
the `git-commit-flow` content convention. These commits won't be picked up as
diff-analysis targets.
