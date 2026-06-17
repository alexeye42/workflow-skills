---
name: issues-recorder
description: >
  Record workflow issues and skill gaps at the end of a session.
  Use when the user says "record issues", "save issues", "what went wrong",
  "what can we improve".
---

# Issues Recorder

Record workflow issues that happened during the session. This skill performs
issue analysis only — it does NOT implement any fixes or updates to skills/rules.
When approved/corrected by the user, issues and proposed improvements are written to a file.

## Definitions

- **Workflow issue**: A problem, inefficiency, or gap in the agent's instructions,
  skills, rules, or system prompts. Issues that are specific only to a single
  task or are highly unlikely to recur must be ignored.
- **Skill**: In the context of proposed improvements, a "skill" refers broadly to
  any source of instructions: actual skills, slash commands, rule files, or
  `AGENTS.md` / `CLAUDE.md`.

## Output File Format

Issues & corresponding improvements are stored in the `workflow/` directory.

- **File**: `workflow/YYYY-MM-DD_improvements.md` (use today's date).
- **Header**: `# Workflow improvements — YYYY-MM-DD`
- **Appending**: If the file for today already exists, append new issues to the
  bottom and continue the numbering from the last issue in the file.

### Issue Structure

Each issue must follow this exact format:

```markdown
## N. Issue Title

Issue description: <1-2 sentences>

Session context: <1-2 sentences, relevant to the issue>

Proposed improvements:
- <**skill-name** / **AGENTS.md** / **CLAUDE.md** / **rule-file-name**>: <2-3 sentences about the improvement>
- ...
```

## 3-Step Flow

Follow these steps sequentially. Do NOT skip Step 2.

### Step 1: Generate analysis

Scan the current session's chat log and work for workflow issues encountered.

**Recurrence test**: Before logging an issue, ask: *Would this problem occur again
in a different session on a different topic?* If yes → log it. If only in this
specific task → ignore.

**Include** not only issues discussed with a user (e.g. based on user feedback or corrections) but also issues that led to significant waste of tokens (e.g. 2+ attempts to handle the same sub-task with different methods).

### Step 2: Output to chat

Write a numbered list of the identified issues to the chat. Each item should be
just a 1-2 sentence description of the issue.

At the end of the list, ask the user:
> "I'm about to save these issues for further workflow improvements. Type Yes, No, or a corrected list to continue."

**STOP HERE.** Wait for the user to respond before proceeding to Step 3.

### Step 3: Create / Append the improvements file

If the user responds negatively or give you irrelevant prompt, do not proceed.

Otherwise:
1. Incorporate any corrections the user made to your proposed issues (if any).
2. Incorporate any entirely new improvements the user proposed in their response (if any).
3. Read the related skill(s), think and formulate item(s) for the "Proposed improvements" for each issue. But do NOT perform a full research on alternative solutions, as this can be done later via `issues-retrospective`.
4. **Deduplication check**: Before writing each proposed improvement, check if a similar instruction already exists in the target skill, rule, or context file. If it does, propose *strengthening* the existing instruction (e.g. by adding a one-shot example or an anti-pattern) instead of adding a new one.

Write everything to the `workflow/YYYY-MM-DD_improvements.md` file using the %Issue Structure% format.
