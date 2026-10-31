"""Build a review page for a patch and cut the approved part of it.

  python3 review.py build  <patch> <findings.json> <out.html> --title T [--lead HTML] [--lang en|ru]
  python3 review.py select <patch> <findings.json> --ids 1,3 [-o approved.patch]

<patch>: `git diff --no-index --src-prefix= --dst-prefix= a b` run in a folder with
  a/<repo path> (originals) and b/<repo path> (edited copies); applies with
  `git apply` (-p1) from the repo root.
<findings.json>: list of {"title", "why", "match": [...], "tags": [...]?, "group"?}.
  Findings are numbered in list order. `match` holds substrings that identify the
  finding's hunks, searched in their +/- lines; "path::text" also requires the
  hunk's file path to end with `path`. Every hunk belongs to exactly one finding;
  a finding with an empty `match` has no hunks (an action outside the patch).
  `group` defaults to the file of the finding's first hunk. Backticks render as code.
"""
import argparse, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

L10N = {
    'en': dict(approveAll='Approve all', reset='Reset', copy='Copy summary', copied='Copied',
               copyManual='Selected: copy it manually', approve='Approve', reject='Reject',
               review='Review', approved='Approve', rejected='Reject', open='Undecided',
               cApproved='approved', cRejected='rejected', cOpen='undecided',
               left='Undecided:', allDone='Every finding is decided', fromLine='line',
               noDiff='No patch hunk: the action is described above.'),
    'ru': dict(approveAll='Одобрить все', reset='Сбросить', copy='Скопировать итог', copied='Скопировано',
               copyManual='Выделено: скопируйте вручную', approve='Одобрить', reject='Отклонить',
               review='Ревью', approved='Одобрить', rejected='Отклонить', open='Не решено',
               cApproved='одобрено', cRejected='отклонено', cOpen='не решено',
               left='Не решено:', allDone='Все находки отмечены', fromLine='строка',
               noDiff='Без hunk\'а в патче: действие описано выше.'),
}


def parse(patch):
    """Split a git patch into file blocks: {'head': [...], 'file': path, 'hunks': [...]}."""
    files, cur, hunk = [], None, None
    for line in patch.split('\n'):
        if line.startswith('diff '):
            cur, hunk = {'head': [line], 'file': None, 'hunks': []}, None
            files.append(cur)
        elif cur is None:
            continue
        elif hunk is None and not line.startswith('@@'):
            cur['head'].append(line)
            if line.startswith(('--- ', '+++ ')):
                path = line[4:].split('\t')[0]
                if path != '/dev/null':
                    cur['file'] = path.split('/', 1)[1]
        elif line.startswith('@@'):
            m = re.match(r'@@ -(\d+)', line)
            hunk = {'file': cur['file'], 'old': int(m.group(1)), 'head': line, 'lines': []}
            cur['hunks'].append(hunk)
        elif line[:1] in (' ', '-', '+', '\\'):
            hunk['lines'].append(line)
    return files


def assign(files, findings):
    hunks = [h for f in files for h in f['hunks']]
    owner = {}
    for n, f in enumerate(findings, 1):
        for key in f.get('match', []):
            path, _, text = key.rpartition('::')
            hits = [i for i, h in enumerate(hunks) if h['file'].endswith(path)
                    and any(text in l for l in h['lines'] if l[:1] in '+-')]
            if len(hits) != 1:
                sys.exit(f'#{n} {f["title"]}: key {key!r} matched {len(hits)} hunks')
            if owner.get(hits[0], n) != n:
                sys.exit(f'#{n} {f["title"]}: hunk already belongs to #{owner[hits[0]]}')
            owner[hits[0]] = n
    missing = [f'{h["file"]}:{h["old"]}' for i, h in enumerate(hunks) if i not in owner]
    if missing:
        sys.exit(f'hunks without a finding: {missing}')
    return hunks, owner


def build(a):
    files = parse(open(a.patch, encoding='utf-8').read())
    F = json.load(open(a.findings, encoding='utf-8'))
    hunks, owner = assign(files, F)
    for n, f in enumerate(F, 1):
        f['hunks'] = [{'file': h['file'], 'old': h['old'], 'lines': h['lines']}
                      for i, h in enumerate(hunks) if owner.get(i) == n]
        f.setdefault('group', f['hunks'][0]['file'] if f['hunks'] else '—')
        f.pop('match', None)
    tpl = open(os.path.join(HERE, '..', 'assets', 'template.html'), encoding='utf-8').read()
    js = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    out = (tpl.replace('__TITLE__', html.escape(a.title)).replace('__LEAD__', a.lead)
              .replace('__DATA__', js(F)).replace('__L10N__', js(L10N[a.lang])))
    open(a.out, 'w', encoding='utf-8').write(out)
    print(f'{len(F)} findings, {len(hunks)} hunks -> {a.out}')


def select(a):
    files = parse(open(a.patch, encoding='utf-8').read())
    F = json.load(open(a.findings, encoding='utf-8'))
    hunks, owner = assign(files, F)
    ids = {int(x) for x in a.ids.split(',') if x.strip()}
    keep = {id(h) for i, h in enumerate(hunks) if owner[i] in ids}
    out = []
    for f in files:
        chosen = [h for h in f['hunks'] if id(h) in keep]
        if chosen:
            out += f['head'] + [l for h in chosen for l in [h['head']] + h['lines']]
    text = '\n'.join(out) + '\n' if out else ''
    if a.o:
        open(a.o, 'w', encoding='utf-8').write(text)
        print(f'{len(keep)} hunks of findings {sorted(ids)} -> {a.o}')
    else:
        sys.stdout.write(text)


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest='cmd', required=True)
b = sub.add_parser('build')
b.add_argument('patch'); b.add_argument('findings'); b.add_argument('out')
b.add_argument('--title', required=True); b.add_argument('--lead', default='')
b.add_argument('--lang', choices=sorted(L10N), default='en')
s = sub.add_parser('select')
s.add_argument('patch'); s.add_argument('findings')
s.add_argument('--ids', required=True); s.add_argument('-o')
a = p.parse_args()
build(a) if a.cmd == 'build' else select(a)
