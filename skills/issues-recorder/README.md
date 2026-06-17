# issues-recorder

Record workflow issues at the end of a session. This skill analyzes the session
for recurring or systemic problems with the agent's instructions (skills, rules,
prompts) and records them in a daily improvements file. It does not implement
the fixes itself.

## Invocation

Invoke this skill manually at the end of a session (or when a problem occurs)
by saying something like:
- "record issues"
- "save issues"
- "what went wrong"
- "what can we improve"

## Related skills

- **issues-retrospective** — used periodically to process the accumulated issue
  files and implement the actual improvements to skills and rules.
