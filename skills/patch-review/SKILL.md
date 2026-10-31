---
name: patch-review
description: Propose a batch of file edits as a review page - one card per finding with its reason and diff, Approve/Reject buttons, a summary the human pastes back - then apply only the approved hunks. Use when the human asks to see proposed edits on a review page, to approve edits one by one, or when another skill (an audit, a cleanup) produces four or more independent edits the human should decide on individually. Not for prose the human will rework by hand - leave those edits as an uncommitted diff instead.
---

# patch-review

Nothing changes in the repository until the human has decided. The agent prepares the
edits as a patch, groups its hunks into findings, and shows them on a page; the human
approves or rejects each finding and pastes the page's summary back; the agent applies
exactly the approved part.

The page fits a batch of independent edits to skills, rules, configs, or code, where the
human wants a verdict per edit with its reason in view. It is a poor fit for one to three
edits (ask in chat) and for prose the human will keep editing (an uncommitted diff in the
IDE lets them change the text, not just accept it).

## 1. Make the patch

Work on copies in a scratch folder, never in the repository:

```bash
cd <scratch>
# for every file to change, with its repo-relative path:
mkdir -p a/<dir> b/<dir> && cp <repo>/<path> a/<path> && cp <repo>/<path> b/<path>
# edit the files under b/ (delete one there to propose its deletion; add new files there)
git diff --no-index --src-prefix= --dst-prefix= a b > edits.patch   # exits 1 when there are diffs
```

Make each edit an exact-substring replacement that fails unless it matches once, so an
edit cannot land in the wrong place. Check the patch against the repository before going
on: `git -C <repo> apply --check <scratch>/edits.patch`.

## 2. Write the findings

`findings.json` is a list; the order is the numbering on the page:

```json
[
  {"title": "One instruction file instead of two",
   "why": "Why the edit is right, what was verified, and what it affects. `code` renders as code.",
   "tags": ["high confidence", "verified"],
   "match": ["# Claude Instructions", "AGENTS.md::vice versa"]}
]
```

- `match` — substrings that identify the finding's hunks, searched in their `+`/`-` lines.
  `path::text` limits a key to files whose path ends with `path`. Every hunk belongs to
  exactly one finding; the script stops on an unmatched hunk or an ambiguous key.
- A finding is the unit of decision, so edits that only make sense together (one refers to
  the other, or a rename and its references) go into one finding. Otherwise a rejection can
  leave the files inconsistent.
- An action that is not a text edit (a symlink, a setting outside the repo) is a finding
  with an empty `match`; describe the action in `why` and carry it out on approval.
- `tags` and `group` are optional. `group` defaults to the file of the first hunk.

## 3. Build and show the page

```bash
python3 scripts/review.py build edits.patch findings.json review.html \
  --title "<short name of this review>" --lead "<one paragraph: scope, what is clean>" --lang en
```

`--lang ru` switches the page labels; write `title`, `why`, and `lead` in the language of
the conversation. Publish `review.html` as a private artifact if the agent can (Claude: the
Artifact tool), otherwise open it locally (`open review.html`). Give the human the link and
a few lines on what the findings are; the details are on the page.

## 4. Apply the decision

The pasted summary starts with the review title and lists the findings to approve by
number. Cut the approved part and apply it:

```bash
python3 scripts/review.py select edits.patch findings.json --ids 1,3 -o approved.patch
git -C <repo> apply <scratch>/approved.patch
```

Then carry out the approved no-patch actions, and report what was applied and what was
left out. Committing follows the project's usual rules.
