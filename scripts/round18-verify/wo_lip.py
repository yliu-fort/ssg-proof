#!/usr/bin/env python3
"""The weakest-oracle route's admissibility-free Lipschitz bound (prop:wo-gate-lipschitz): for a context H on s vertices
with calls, NOT necessarily admissible, whose composition with a stopping game is stopping, |val_{H<G'>}(v) - val_{H<G>}(v)|
<= (4/3)(s+3)|p'-p| when the plugged-in games are one-player-free chains of values p, p' in [1/4,3/4] (gate data (p,p)).
Random contexts with calls on directed cycles (the excluded class), compositions built explicitly, exact arithmetic."""
import sys, os as _os, random
sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness'))
from fractions import Fraction as F
from mycore import G, is_stopping, wstar

def chain(bits):
    """a chain of average vertices realising survival probability sum bits[j] 2^-(j+1) to 'up', else 'dn' (sentinels)."""
    out = []
    for j, b in enumerate(bits):
        nxt = ('g', j+1) if j < len(bits)-1 else 'dn'
        out.append((('g', j), 'avg', ('up' if b else 'dn', nxt)))
    return out

def compose(ctx_kinds, ctx_succ, bits):
    """ctx: kinds in {max,min,avg,call}; succ over indices 0..s-1 plus 'T0','T1'. Each call replaced by a private chain."""
    s = len(ctx_kinds); names = []; K = {}; S = {}
    def add(nm, k, su): names.append(nm); K[nm] = k; S[nm] = su
    for v in range(s):
        if ctx_kinds[v] != 'call': add(('c', v), ctx_kinds[v], ctx_succ[v])
    for v in range(s):
        if ctx_kinds[v] == 'call':
            e1, e0 = ctx_succ[v]
            for (nm, k, (a, b)) in chain(bits):
                def m(x):
                    if x == 'up': return e1
                    if x == 'dn': return e0
                    return ('c', v, x)
                add(('c', v, nm), k, (m(a), m(b)))
    def fin(x):
        if x == 'T0': return n
        if x == 'T1': return n+1
        if isinstance(x, int): return ix[('c', x)] if ctx_kinds[x] != 'call' else ix[('c', x, ('g', 0))]
        return ix[x]
    n = len(names); ix = {nm: i for i, nm in enumerate(names)}
    succ = [(fin(S[nm][0]), fin(S[nm][1])) for nm in names]
    return G([K[nm] for nm in names], succ), ix

rng = random.Random(7); tested = 0; worst = F(0); nonadm = 0
p0 = [1]                      # 1/2
while tested < 300:
    s = rng.randrange(3, 9)
    kinds = [rng.choice(['max', 'min', 'avg', 'call', 'call']) for _ in range(s)]
    if 'call' not in kinds: continue
    succ = [(rng.choice(list(range(s)) + ['T0', 'T1']), rng.choice(list(range(s)) + ['T0', 'T1'])) for _ in range(s)]
    # composition with a fair coin at every call must be stopping
    g0, ix0 = compose(kinds, succ, p0)
    if not is_stopping(g0): continue
    # admissible? (context stopping with calls read as controlled vertices) -- we want the NON-admissible ones too
    ga = G([('max' if k == 'call' else k) for k in kinds], [(n if x == 'T0' else n+1 if x == 'T1' else x) for x in [] ] or [(s if a == 'T0' else s+1 if a == 'T1' else a, s if b == 'T0' else s+1 if b == 'T1' else b) for a, b in succ])
    adm = is_stopping(ga)
    if not adm: nonadm += 1
    w0 = wstar(g0)
    for bits in ([1, 0, 0, 0, 0, 0, 0, 0, 1], [0, 1, 1], [1, 1]):   # 1/2+2^-9, 3/8, 3/4
        g1, ix1 = compose(kinds, succ, bits)
        assert is_stopping(g1)
        w1 = wstar(g1)
        p = F(1, 2); p1 = sum(F(b, 2**(j+1)) for j, b in enumerate(bits))
        for v in range(s):
            if kinds[v] == 'call': continue
            d = abs(w1[ix1[('c', v)]] - w0[ix0[('c', v)]])
            ratio = d / abs(p1 - p)
            assert ratio <= F(4, 3) * (s + 3), (kinds, succ, bits, v, ratio)
            worst = max(worst, ratio / (s + 3))
    tested += 1
print(f'{tested} random contexts with calls ({nonadm} NOT admissible), each composed with chains of value 1/2 and 1/2+2^-9, 3/8, 3/4: '
      f'|Delta val| <= (4/3)(s+3)|Delta p| in every case; worst observed ratio/(s+3) = {float(worst):.4f} (bound 4/3)')
