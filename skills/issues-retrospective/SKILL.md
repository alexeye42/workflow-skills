---
name: issues-retrospective
description: >
  Process accumulated improvement files, detect recurring patterns, and implement skill/rule changes.
  - Use when the user says "retrospective", "retro", "review issues", etc.
  - Use when the user says "implement <file reference>" and the file include `Source: retrospective`
    OR "implement improvements" (then, see RETROSPECTIVE.md for file list). 
    If triggered by "implement", go immediately to Step 5.
---

# Issues Retrospective

Process accumulated workflow issues, identify recurring patterns, and implement
improvements to skills, rules, and context files. This skill acts as the periodical
implementation phase for issues recorded by `issues-recorder`.

## Hard Dependency

This skill **requires** the `task-file-updater` skill to function, as improvements
are considered as tasks.
Before starting Step 1, verify that `task-file-updater` is available to you.
If it is not found, output an error message.

## Multi-Step Process

Follow these steps sequentially.

### Step 1: Gather recent issues/improvements

1. Check for `workflow/RETROSPECTIVE.md` to find the last retrospective date
   (`Last retrospective: YYYY-MM-DD`). If the file does not exist, consider there
   to be no previous retrospective.
2. Search for `YYYY-MM-DD_improvements.md` files in the `workflow/` folder filtering
   only those files that are created **since** the last retrospective date (if any).
3. Inside the eligible files, collect only the issue items that do **NOT** have
   the `[➡️ work]` mark on their heading.

### Step 2: Pattern detection & User approval

4. In improvements files dated **this month** or **last month** only
   (the date may be before the last retrospective date), search for issues:
   a) with no `[➡️ work]` mark AND
   b) with description **similar** to those gathered at Step 1.
   If found, add these similar issues to the list. 
5. Group all the collected issues by similarity to separate them into two lists:
   - **Recurring issues**: Issues that appear 2 or more times. 
   - **Non-recurring issues**: Issues that appear only once. 
6. Output the numbered list of recurring issue groups (title: "Improvements proposed for implementation")
   adding the following to each group: a) "Recurred ... times" b) "Improvement(s): ..."
   (Both issues and improvements must be generalized from the original texts.)
   Ask for approval to implement them (the question is in bold).
   Output non-recurring issues as bullet list titled: "Issues recommended to ignore for now". 
   Stop and wait for the user's response.

> [NOTE] If no recurring issues found, simplify your output (#6) as follows:
> Propose the first 3 issues for implementation in the format above (#6), but without generalization
>   (just copy the issue and improvement(s) from the improvements file).
> If there are more than 3 issues gathered at Step 1, 
>   output "Issues recommended to ignore for now" list as well.

### Step 3: Update RETROSPECTIVE.md

After the user approves/corrects the issues to work on:

7. Write or overwrite `workflow/RETROSPECTIVE.md` file with today's date line:
   `Last retrospective: <YYYY-MM-DD>` (clearing all the previous content of the file).

### Step 4: Create task files for approved issues

For **each** approved issue (task):
1. Create a task file in the `work/` directory named `YYYYMMDD_<topic-slug>.md`
   (e.g., `20260609_fix-linkedin-review.md`; it includes today's date).
2. Use the standard task file format (see `task-file-updater`), but do **NOT**
   include the "Decisions made" section yet. In addition to Created: and Last updated:
   items, add `Source: retrospective <YYYY-MM-DD>` to the list.
3. For the **"What happened"** section, copy the items from the improvement files.
   Format each item as:
   `- <YYYY-MM-DD>. <Issue description>. Context: <Session context>. Proposed improvement(s): <improvement(s)>`
4. For the **"Summary"** section, write a brief generalization of the "What
   happened" items.
5. In the original improvement file(s), append `[➡️ work]` to the heading of
   each issue you copied over.
6. Append the newly created task file name to `workflow/RETROSPECTIVE.md`. 
   All the tasks must form a numbered list there.
7. Output a 1-sentence summary of what you've done and suggest creating a new session (chat) 
   to implement the first task:
   """Let's implement task #1 in a new session to avoid context bloat.
   Just copy this line `Implement <task file relative path>` to a new chat.""".

> [!IMPORTANT] So, you need to modify all 3 files simultaneously: 
> do NOT leave any of those files unchanged when processing an issue.

### Step 5: Implementation loop

Work through the task files **one by one**. For each task:

1. Read the task file focusing on proposed improvements. 
2. Research deeper. Classify the improvements appropriately:
   - **Workflows** (multi-step procedures) belong in **skills**.
   - **General behaviors/preferences** belong in **rules** or `AGENTS.md` / `CLAUDE.md`.
   - **Exclude** project-specific facts or generic engineering advice from skills/rules.
   Analyze potential consequences of the improvements. If possible, propose 2-3 implementation alternatives.
   Present everything to the user and ask for approval/corrections/choice between alternatives.
3. After user response, implement the changes to the relevant skills/rules/context files. 
   - **Constraint**: Ensure a modified skill or rules file is under 150 lines (longer means it's doing too much). For greater line count, propose splitting into two files.
4. As an outline of the implemented changes, write the **"Decisions made"** section 
   in the task file, following the rules of `task-file-updater` 
   (only include reasons if non-obvious or discussed with the user).
5. In the task file, mark the top-level `# Task name` with `[✅ done]` at the end.
6. Suggest committing the changes.
7. After the commit (or if the user refuses), output this again: 
   """Let's implement task #<N> in a new session to avoid context bloat.
   Just copy this line `Implement <task file relative path>` to a new chat."""
