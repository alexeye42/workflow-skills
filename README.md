# Workflow Skills

Skills and meta-skills to enhance and manage various non-development workflows with AI agents.

## Scrum-Inspired Skills

These skills is an example implementation of a process framework for AI agents (ProF4A), inspired by the Scrum pillars of Transparency, Inspection, and Adaptation. It helps maintain human-in-the-loop oversight and continuous improvement of agent behavior without falling into micromanagement. 

### `qna-file-creator`
**Category:** Transparency / Flipped Interaction

Instead of using multi-turn chat dialogues for requirement gathering (which can lead to context tracking failures), this skill offloads discovery questions to a dedicated Markdown file (`*_qna.md`). It pauses the execution loop and resumes only after you've provided answers directly in the file. This creates a persistent, searchable source of truth for the session.
[View Skill](skills/qna-file-creator/SKILL.md)

### `task-file-updater`
**Category:** Transparency / Task Tracking

To understand what was done in a session and *why* decisions were made, this skill automatically maintains short session briefs in a `work/` directory (`YYYYMMDD_task-name.md`). It records a summary, what happened, and crucial decisions, preventing you from having to read long AI outputs to understand the agent's progress.
[View Skill](skills/task-file-updater/SKILL.md)

### `issues-recorder`
**Category:** Inspection / Session Review

A trigger for the end of a session (or "micro-sprint"). This skill scans the chat log and recent work to identify workflow issues, inefficiencies, or gaps in your agent's current skills. Upon your approval, it records these problems and proposed improvements into a daily file (`workflow/YYYY-MM-DD_improvements.md`), allowing you to defer actual skill modification until later.
[View Skill](skills/issues-recorder/SKILL.md)

### `issues-retrospective`
**Category:** Adaptation / Scheduled Improvement
A tool for scheduled retrospectives. It processes the accumulated issues recorded by the `issues-recorder`, detects recurring patterns, and orchestrates the implementation of improvements to your skills, rules, or system prompts. It acts to clear "process debt," ensuring that you optimize the agent's workflow based on repeating problems rather than random one-off errors.
[View Skill](skills/issues-retrospective/SKILL.md)
