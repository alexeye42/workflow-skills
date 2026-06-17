---
name: git-diff-analyzer
description: >
  Analyze human edits to AI-generated content by comparing two git commits, distill patterns into actionable skill improvements, and update the relevant skill(s) (optionally via skill-creator and skill-judge). Use when the user says "analyze my edits", "analyze diff", "learn from git", "extract patterns", "what did I fix". Typically run after the user has manually corrected an AI output.
---

# git-diff-analyzer

Closes the feedback loop between your manual corrections and the agent's future behavior:
compares two commits, extracts patterns from your edits, and updates the relevant skill.

Uses git for reliability, as LLM-based comparisons are unreliable. In addition, git reliably
handles cases when a content was modified in multiple sessions.

## Prerequisites

The typical setup is handled by the `git-commit-flow` skill.
For this skill to learn the right lessons, each pair of commits should represent:
- **commit A** — AI-generated output (pre-edit)
- **commit B** — human-corrected version (post-edit)

## Workflow

### Step 1: Capture uncommitted edits and identify commits

Before anything else, check for uncommitted changes:

```bash
git status --short
```

If there are uncommitted changes in content files (see `git-commit-flow` skill for 
what counts as content), use `git-commit-flow` with author `human` to commit them. 

If the user did not specify both commits, identify the commit(s) yourself:

```bash
git log --oneline -10
```
The last human commit in this log is **commit B**.

To identify **commit A** (AI output), find the most recent `fix(...): ai` or `feat(...): ai` commit 
that matches commit B by **location overlap**: same folder scope (text in parentheses) AND overlapping 
files or sections named in the description (text after `:`). Ask the user to confirm if ambiguous. 

> [!NOTE]
> Skip `human/ai` commits when searching for pairs — these contain mixed authorship
> and cannot serve as either commit A (pure AI output) or commit B (pure human corrections).

### Step 2: Get the diff

```bash
git diff <commit-A> <commit-B> -- '*.md' '*.mkd'
```

Adjust the pathspec to the file types relevant to the task (default: markdown).

### Step 3: Analyze the diff and chat context

Read the diff. Classify every change into one of two buckets, considering user prompts in the chat:

**Significant** — changes that reveal a reusable instruction for the agent:
- Structural or formatting patterns added/removed throughout
- Recurring word or phrase substitutions (AI slop, awkward constructs)
- Tone or register adjustments applied consistently
- Reusable content decisions: what was added, cut, or reordered and why
- Anything the agent should do differently next time (this is based on the user feedback in the chat)

**Trivial** — changes not worth encoding as rules:
- Single typo fixes unlikely to recur
- Proper noun corrections (names, titles) even if they are repeating
- One-off factual updates with no stylistic implication
- Formatting of a single element

### Step 4: Present findings

Present two lists in chat:

**Proposed conclusions** (significant edits, ranked by importance):
> List each as a concise, actionable instruction in imperative form, e.g.:
> 1. "Avoid starting sentences with 'Additionally' or 'Furthermore'."
> 2. "Keep section headers under 6 words."
> 3. "Do not use em-dash as a sentence connector; use a period or semicolon."

**Skipped edits** (bulleted list of trivial edit groups):
> - <very short description of what was changed and why it was skipped>
> - ...
> - Minor vocabulary modifications

Ask the user:
```
1. Do you want to drop or rephrase any of the proposed conclusions? 
2. Should any skipped edit be promoted to a conclusion?
If you agree with my conclusions, just type 'ok' or 'no'.

By default, I will apply them to <a skill or a list of skills>
```

To get the list of skills, if no skills calls exist in the chat history 
(meaning that a new session was started),
use your best guess based on the skills available to the agent.

Wait for the user's response before proceeding.

### Step 5: Update the skill

Once the user confirms the final list of conclusions and the target skill:

1. **Update the skill(s)**: Use the `skill-creator` meta-skill to automatically update the target skill(s) based on the conclusions confirmed by the user. *Fallback (if `skill-creator` is not available)*:
   - Read the current `SKILL.md` of the target skill.
   - Integrate the conclusions as concise additions — append to an existing relevant section or create a new **"Patterns to avoid"** / **"Style rules"** section if no similar section exists.
   - Keep additions minimal: one bullet per conclusion, imperative form, no redundancy with existing instructions.
2. **Invoke `skill-judge` (if available)**: After the skill(s) are updated, use the `skill-judge` meta-skill to evaluate the modified skill(s) to verify they meet quality and design standards. If it's not available, do nothing.

> **Note**: If multiple skills should receive different subsets of the conclusions,
> handle each skill in sequence.

### Step 6: Commit (optional)

Offer to commit the updated skill(s). If the user approved, commit as follows:

```bash
git commit -m "fix(skills): ai updated <skill name(s) and a summary of what was improved; one line per skill>"
```

If some meta-skills were used to update the skill(s), mention them in the commit message, e.g.:
`fix(skills): ai (skill-creator, skill-judge) added edge cases to git-commit-flow`

## Notes

- Focus on **patterns**, not individual fixes. A correction that appears once
  and has no generalization potential belongs in the "skipped" bucket.
- When in doubt whether something is significant, ask the user rather than guessing!
- Do not update project context files and rule files without an explicit permission from the use 
  — only update skill files by default. 
