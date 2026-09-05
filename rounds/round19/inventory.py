#!/usr/bin/env python3
"""Regenerate the result inventory of frontier.tex at HEAD.

Output format (one line per numbered result, grouped under section headers):
  ## L<line> <section title>
  L<line> <env> <label> :: <title>
Run from the repository root:  python3 rounds/round19/inventory.py > rounds/round19/inventory.txt
"""
import re, sys
ENVS = ('theorem','lemma','proposition','corollary','definition','remark','problem','conjecture','example','question','claim','observation')
lines = open('frontier.tex', encoding='utf-8').read().split('\n')
out = []; n = 0
sec_re = re.compile(r'\\(?:sub)*section\*?\{(.*)')
beg_re = re.compile(r'\\begin\{(' + '|'.join(ENVS) + r')\}(?:\[(.*?)\])?')
lab_re = re.compile(r'\\label\{([^}]*)\}')
i = 0
while i < len(lines):
    l = lines[i]
    m = sec_re.match(l.strip())
    if m and not l.strip().startswith('%'):
        t = m.group(1)
        t = re.sub(r'\}\s*\\label\{.*$', '', t); t = re.sub(r'\}\s*$', '', t)
        out.append(f'## L{i+1} {t.strip()}')
    m = beg_re.search(l)
    if m and not l.strip().startswith('%'):
        env, title = m.group(1), m.group(2) or ''
        # the label is on this or one of the next three lines
        lab = ''
        for j in range(i, min(i+4, len(lines))):
            ml = lab_re.search(lines[j])
            if ml: lab = ml.group(1); break
        # a title may run over onto the next line
        if m.group(2) is None:
            mt = re.search(r'\\begin\{' + env + r'\}\s*$', l)
            if mt and i+1 < len(lines) and lines[i+1].lstrip().startswith('['):
                title = lines[i+1].strip()[1:].split(']')[0]
        title = re.sub(r'\s+', ' ', title).strip()
        out.append(f'L{i+1} {env} {lab or "-"} :: {title}'); n += 1
    i += 1
sys.stdout.write('\n'.join(out) + '\n')
print(f'# {n} numbered results, {len(lines)} lines', file=sys.stderr)
