---
name: qna-file-creator
description: Implements Flipped Interaction pattern by offloading AI questions and user answers from the chat log into a local markdown file. Use when the user says "ask questions", "create Q&A", "update qna file", "clarify first" and similar phrases.
---

# Q&A File Creator Skill

Analyzes context, generates questions in a file, and requests answers from the user in the same file.

## Objective
Prevent chat window token bloom and context tracking failures during high-uncertainty or discovery phases. Instead of using multi-turn chat dialogues for requirement gathering, you must offload discovery questions to a markdown file (%Q&A File%), halt your execution loop, and resume only upon receiving answers from the user in that file (it may take more than one iteration). 

The file can be appended or corrected. Then, it may be used as a source of truth regarding the task at hand.

## Instructions

### Step 1: Workspace Context Research
* Scan the sources provided in the prompt, as well as workspace files if required by your AGENTS.md or other guidelines. Focus specifically on identifying hidden assumptions, contradictions, and missing information that will become questions.

### Step 2: %Q&A File% Generation
* Formulate clear, actionable, non-redundant questions. Do **not** output these questions to the chat.
* (this is a one-off step at the beginning) Decide on the %Q&A File Name and Location%. Check if any `_qna.md` file exists in that location. 
  - If it doesn't, create your own Q&A File. 
  - If it does, read it and determine if it was created for the current task. If not, create your own Q&A File.
* If a relevant Q&A File already exists, append new subsections/questions to it under a top-level header `# Round 2 Questions` (Round 3 if Round 2 already exists).
* Once the file is written or appended, output a brief message to the user in the chat, for example: 
  > "I have analyzed <context> and generated clarifying questions in `<path_to_qna.md>`. Please review, provide your answers inline, and type "replied" here when done."

### Step 3: Resuming After User Answers

Before generating Round N (N=2+) questions or proceeding with the task:
- Scan for items where `An:` is blank. If **any** answers are missing: ask the user in chat to complete the following blanks in the previous round as well: <list An here>.
- If answers are **unclear or contradictory or reveals new scope to be refined**: write new questions in Round N section.
- If **no more questions remain** AND the user didn't ask for new questions (new round) in the last prompt: close the Q&A loop and proceed with the original task.

## Q&A File

### Q&A File Name and Location

Any Q&A file must end with `_qna.md`.

If the user didn't mention the target file location and name in the prompt, then:

* If there is a file reference in the chat context, use the file's location as the Q&A file location, and consider using the file name as a base when generating the Q&A file name. E.g.:
  - if the file path is `123-agent-skills/draft.md`, the Q&A file is `agent-skills_qna.md`.
  - if the file path is `123-agent-skills/123_draft.md`, the Q&A file is `123_qna.md`. So, if the file name includes something specific, it must become part of the Q&A file name.

* If there is NO file or folder reference in the chat context, generate the file location and name as best you can (the name is usually a 2-word task name in English, ending with `_qna.md`). Use the generated path to create the file but ask the user to correct the file name or location in the chat.

### Q&A File Format Template

```
### <Title (The Task In Question)>
<Brief description of the task context in 1-2 sentences>

## Round 1 Questions (<MM/DD/YYYY>)

### [Section X]

Q1: <Your explanation and your question>
A1: [this is where the user will respond]

Q2: <Your explanation and your question>
A2: 

...

### [Section Y]

Qn: <Your explanation and your question>
An: 

## Round 2 Questions (<MM/DD/YYYY>)

### [Section Y]
...
```

Here:
* An **explanation** is a brief summary of your findings and other context that will simplify answering the question for the user. For example, it could outline a contradiction found: "In conclusion, you didn't mention any continuation of this post, while the `post-enhancer` skill requires a teaser or call-to-action at the end."
* A **question** is either an open question or a question with answer options (see %Skill Options% #2 below). Here are examples of both:
  1. What would you like to say to announce the next post(s)?
  2. What would you prefer as a final paragraph?
     A. The next post will cover the next steps for those who already use Agent Skills. Stay tuned.
     B. Finding public agent skills for the task at hand is not the most efficient way to grow the skill set; I'll explain a better alternative in the next post. 
     C. No teaser, just a call to subscribe.
     D. Something else 


## Skill Options

**Language:** For the Q&A file, use the language of the user's prompt in the chat, unless requested otherwise.

**Question count**
* 3–5 questions: simple, well-scoped tasks with one main unknown.
* 6–10 questions: medium-complexity tasks with multiple independent unknowns.
* More than 10: split into sections; never exceed 12 per round.
* When in doubt, ask fewer — a second round is always possible.

**Question type**
* By default, generate **open questions** avoiding the 'or' conjunction. 
  - In most cases, they must be general questions assuming that the user may answer a question with Yes/OK, so your recommendation or guess must be clear to them. 
  - In addition, the user must be stimulated to provide details. For example: if the explanation is "The 'Registration' epic already mentions some emails: registration confirmation, new user credentials, and a password recovery link.", the question may be as follows: "Should these emails be re-described in this epic? (If yes, how detailed should they be specified?)".
* If the user prompt includes a hint to create **closed questions** ("ask questions with options", etc), prefer generating 3-4 options but use the open question format above for SOME questions where you don't have a clue to generate meaningful options. If the answer options are used for a question:
  - Options must be preceded by A, B, C[, D] for English (use similar letters for another language).
  - The last option must assume an open answer, e.g.: "Other (please specify)".
  - The preceding options must be 4-10 words long.

## Anti-Patterns

- NEVER output questions to the chat while this skill is active.
- NEVER ask multiple questions as one Q&A item even if they are similar.
- NEVER use alternative questions ('or'). Instead, commit to a recommendation and let the user correct it.

> ❌ *"Should the output file go some post folder, or would you prefer it in the project root?"*
> ✅ *"I'll place the output file in the post folder. Is that correct? (If not, specify the preferred location.)"*
