#!/usr/bin/env python3
"""Root agent's own checks of the round-17 order-lattice route (labels ol:), written from the
statements, not from the route's code. Exact rational arithmetic throughout.
  (1) ol:unique  -- exhaustive over ALL total preorders on the letters A = Vavg u {t0,t1} of random
                    small stopping games, every tie-breaking of the decode: the only consistent
                    preorder is the one induced by w*, and its decode is w*.
  (2) ol:lift-cycles -- OL3.json rebuilt: stopping, the eight profile values against thm:cyclic-uso's
                    table (Min's two actions exchanged), profile-nondegeneracy, w*, the antipodal walk's
                    3-cycle, and the order lift from the coarsest preorder (first-successor tie-break).
  (3) ol:small-C -- random separated profile-nondegenerate stopping games with one Max and one Min
                    vertex: the antipodal walk never cycles, reaches the sink within 3 steps."""
import sys, json, random, itertools
from fractions import Fraction as F

class Game:
    def __init__(self, kinds, succ):
        self.kinds = list(kinds); self.succ = [tuple(s) for s in succ]; self.n = len(kinds)
        self.t0, self.t1 = self.n, self.n + 1
        self.C = [v for v in range(self.n) if kinds[v] in ('max', 'min')]
        self.A = [v for v in range(self.n) if kinds[v] == 'avg'] + [self.t0, self.t1]
    def is_stopping(self):
        # G is stopping iff no nonempty set U of NON-SINKS has every average vertex of U with both
        # successors in U and every controlled vertex of U with some successor in U (lem:trapchar)
        U = set(range(self.n)); ch = True
        while ch:
            ch = False
            for x in list(U):
                ok = all(w in U for w in self.succ[x]) if self.kinds[x] == 'avg' else any(w in U for w in self.succ[x])
                if not ok: U.discard(x); ch = True
        return not U
    def value(self, choice):
        """exact value vector of the positional profile `choice` (dict v -> 0/1 over C); sinks appended"""
        n = self.n; A = [[F(0)] * n for _ in range(n)]; b = [F(0)] * n
        for v in range(n):
            A[v][v] += 1
            if self.kinds[v] == 'avg':
                for w in self.succ[v]:
                    if w < n: A[v][w] -= F(1, 2)
                    elif w == self.t1: b[v] += F(1, 2)
            else:
                w = self.succ[v][choice[v]]
                if w < n: A[v][w] -= 1
                elif w == self.t1: b[v] += 1
        Mx = [A[i][:] + [b[i]] for i in range(n)]
        for c in range(n):
            p = next(r for r in range(c, n) if Mx[r][c] != 0)
            Mx[c], Mx[p] = Mx[p], Mx[c]; pv = Mx[c][c]; Mx[c] = [y / pv for y in Mx[c]]
            for r in range(n):
                if r != c and Mx[r][c] != 0:
                    f = Mx[r][c]; Mx[r] = [Mx[r][k] - f * Mx[c][k] for k in range(n + 1)]
        return [Mx[i][n] for i in range(n)] + [F(0), F(1)]
    def wstar(self):
        maxs = [v for v in self.C if self.kinds[v] == 'max']; mins = [v for v in self.C if self.kinds[v] == 'min']
        best = None
        for sm in itertools.product((0, 1), repeat=len(maxs)):
            worst = None
            for tm in itertools.product((0, 1), repeat=len(mins)):
                ch = dict(zip(maxs, sm)); ch.update(zip(mins, tm))
                x = self.value(ch)
                worst = x if worst is None else [min(a, b) for a, b in zip(worst, x)]
            best = worst if best is None else [max(a, b) for a, b in zip(best, worst)]
        return best
    def topo_C(self):
        """topological order of the controlled subgraph: successors (in C) before v"""
        order = []; seen = set()
        def visit(v):
            if v in seen: return
            seen.add(v)
            for w in self.succ[v]:
                if w in self.Cset: visit(w)
            order.append(v)
        self.Cset = set(self.C)
        for v in self.C: visit(v)
        return order
    def decode(self, rk, tiebreak):
        """rk: dict letter -> rank (0 = top); tiebreak: dict v -> 0/1 used when R ties; returns (choice, x)"""
        R = {a: -rk[a] for a in self.A}
        choice = {}
        for v in self.topo_C():
            r0, r1 = R[self.succ[v][0]], R[self.succ[v][1]]
            if r0 == r1: c = tiebreak[v]
            elif self.kinds[v] == 'max': c = 0 if r0 > r1 else 1
            else: c = 0 if r0 < r1 else 1
            choice[v] = c; R[v] = R[self.succ[v][c]]
        return choice, self.value(choice)
    def decode_all(self, rk):
        """every tie-breaking of the decode, branching only where a tie occurs: list of (choice, x)"""
        R0 = {a: -rk[a] for a in self.A}; order = self.topo_C(); out = []
        def go(i, R, choice):
            if i == len(order):
                out.append((dict(choice), self.value(choice))); return
            v = order[i]; r0, r1 = R[self.succ[v][0]], R[self.succ[v][1]]
            if r0 == r1: cs = (0, 1)
            elif self.kinds[v] == 'max': cs = (0,) if r0 > r1 else (1,)
            else: cs = (0,) if r0 < r1 else (1,)
            for c in cs:
                R[v] = R[self.succ[v][c]]; choice[v] = c; go(i + 1, R, choice)
            R.pop(v, None); choice.pop(v, None)
        go(0, dict(R0), {}); return out
    def induced(self, x):
        vals = sorted({x[a] for a in self.A}, reverse=True)
        return {a: vals.index(x[a]) for a in self.A}
    def outset(self, choice, x):
        """s_C(pi) for a SEPARATED game (successors of controlled vertices are letters)"""
        s = set()
        for v in self.C:
            other = x[self.succ[v][1 - choice[v]]]; cur = x[v]
            if other == cur: return None   # degenerate
            if (self.kinds[v] == 'max' and other > cur) or (self.kinds[v] == 'min' and other < cur): s.add(v)
        return s

def preorders(A):
    """all total preorders on A as rank functions (surjections onto {0..k-1})"""
    for k in range(1, len(A) + 1):
        for ranks in itertools.product(range(k), repeat=len(A)):
            if set(ranks) == set(range(k)): yield dict(zip(A, ranks))

def rand_stopping(n, nmax, nmin, rng, separated=False):
    while True:
        kinds = ['max'] * nmax + ['min'] * nmin + ['avg'] * (n - nmax - nmin)
        succ = []
        for v in range(n):
            if separated and kinds[v] != 'avg':
                succ.append((rng.randrange(nmax + nmin, n + 2), rng.randrange(nmax + nmin, n + 2)))
            else:
                succ.append((rng.randrange(n + 2), rng.randrange(n + 2)))
        g = Game(kinds, succ)
        if g.is_stopping(): return g

def check_unique(games, tag):
    for g in games:
        w = g.wstar(); true_rk = g.induced(w)
        consistent = []
        for rk in preorders(g.A):
            decodes = g.decode_all(rk)
            if any(g.induced(x) == rk for _, x in decodes): consistent.append((rk, [x for _, x in decodes]))
        assert len(consistent) == 1, (tag, len(consistent))
        rk, decodes = consistent[0]
        assert rk == true_rk and all(x == w for x in decodes), tag
    print(f'ol:unique  [{tag}] {len(games)} games (|A| = {sorted(set(len(g.A) for g in games))}, |C| up to {max(len(g.C) for g in games)}): the only consistent preorder is the true one, every tie-breaking decodes to w*', flush=True)

rng = random.Random(17)
games = [rand_stopping(n, nmax, nmin, rng) for n in (4, 5, 6) for nmax in (0, 1, 2) for nmin in (0, 1, 2) if nmax + nmin <= n - 1 for _ in range(4)]
games5 = [g for g in games if len(g.A) <= 5]; games6 = [g for g in games if len(g.A) == 6][:6]
check_unique(games5, 'n=4..6, |A|<=5'); check_unique(games6, 'n=6, |A|=6')
big = [g for g in (rand_stopping(n, 2, 2, rng) for n in (8, 9, 10) for _ in range(40)) if len(g.A) == 6][:6]
check_unique(big, 'n=8..10, |A|=6, 2 Max 2 Min')

# ---------- (2) OL3
g = Game(**{k: v for k, v in json.load(open(sys.argv[1])).items() if k in ('kinds', 'succ')})
print('OL3: n =', g.n, 'non-sinks, C =', g.C, 'stopping =', g.is_stopping())
table = {  # thm:cyclic-uso, profile (a,b,m) -> values (a,b,m)
 (0,0,0): (F(1,4),F(15,64),F(1,8)),   (0,0,1): (F(1,4),F(15,64),F(225,1024)),
 (0,1,0): (F(1,4),F(1,8),F(1,8)),     (0,1,1): (F(1,4),F(1,8),F(15,128)),
 (1,0,0): (F(1,9),F(5,48),F(1,18)),   (1,0,1): (F(128,473),F(120,473),F(225,946)),
 (1,1,0): (F(1,9),F(1,8),F(1,18)),    (1,1,1): (F(169,1024),F(1,8),F(15,128))}
outs = {(0,0,0): set(), (0,0,1): {0,2}, (0,1,0): {1,2}, (0,1,1): {1}, (1,0,0): {0,1}, (1,0,1): {2}, (1,1,0): {0}, (1,1,1): {0,1,2}}
walk = {}
for pi in itertools.product((0, 1), repeat=3):
    ch = dict(zip(g.C, pi)); x = g.value(ch)
    S = (pi[0], pi[1], 1 - pi[2])            # OL3 has Min's actions exchanged
    assert tuple(x[v] for v in g.C) == table[S], (pi, [str(x[v]) for v in g.C])
    s = g.outset(ch, x); assert s is not None and s == outs[S], (pi, s)
    walk[pi] = tuple(pi[i] ^ (1 if g.C[i] in s else 0) for i in range(3))
print('OL3: all 8 profile values and out-sets match thm:cyclic-uso (with m relabelled); profile-nondegenerate')
w = g.wstar(); print('OL3: w*(a,b,m) =', [str(w[v]) for v in g.C])
seq = [(0, 0, 0)]
while walk[seq[-1]] not in seq: seq.append(walk[seq[-1]])
i = seq.index(walk[seq[-1]]); print('OL3: antipodal walk from (0,0,0):', seq, '-> back to', seq[i], '; period', len(seq) - i)
conv = [pi for pi in walk if walk[pi] == pi]; print('OL3: fixed profiles (sinks):', conv)
# the order lift from the coarsest preorder with first-successor tie-breaking
rk = {a: 0 for a in g.A}; orbit = []
for step in range(8):
    ch, x = g.decode(rk, {v: 0 for v in g.C}); prof = tuple(ch[v] for v in g.C)
    orbit.append((prof, tuple(str(x[v]) for v in g.C))); rk = g.induced(x)
print('OL3: order lift from the coarsest preorder:', [o[0] for o in orbit])
print('     profile values along it:', orbit[:4])
# which profiles lead into the cycle
lead = sum(1 for pi in walk if (lambda p: (p := walk[p]) and True)(pi) is not None and walk[pi] != pi and all(True for _ in [0]))
into = 0
for pi in walk:
    p = pi; seen = []
    while p not in seen: seen.append(p); p = walk[p]
    if len(seen) - seen.index(p) == 3: into += 1
print('OL3: profiles whose walk enters the 3-cycle:', into, 'of 8')

# ---------- (3) ol:small-C, one Max and one Min, separated, profile-nondegenerate
cnt = 0; maxsteps = 0
while cnt < 2000:
    g = rand_stopping(rng.randrange(4, 9), 1, 1, rng, separated=True)
    vals = {}; ok = True; wk = {}
    for pi in itertools.product((0, 1), repeat=2):
        ch = dict(zip(g.C, pi)); x = g.value(ch); s = g.outset(ch, x)
        if s is None: ok = False; break
        wk[pi] = tuple(pi[i] ^ (1 if g.C[i] in s else 0) for i in range(2))
    if not ok: continue
    cnt += 1
    for pi in wk:
        p = pi; steps = 0; seen = {p}
        while wk[p] != p:
            p = wk[p]; steps += 1; assert p not in seen, ('CYCLE', g.kinds, g.succ); seen.add(p)
        maxsteps = max(maxsteps, steps)
print(f'ol:small-C: {cnt} random separated nondegenerate 1-Max-1-Min stopping games: no cycle, at most {maxsteps} antipodal steps to the sink')
