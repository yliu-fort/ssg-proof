#!/usr/bin/env python3
"""The certificate worlds of ed_cert.py assembled as SSGs through the rational-row gadget of lem:rational-row (rejection
tree, pruned by boundaries, so rows with 291-bit denominators are fine), with a private average entry per incidence
(rem:rational-row), and checked FROM THE GAME with the harness: stopping (mycore.is_stopping), val* on C equal to the
system's (mycore.wstar), nondegenerate at every strategy, and the bit at v0 on the certified side.
  python3 ed_games.py m2      every world of cert_m2_d2.json, fully from the game
  python3 ed_games.py m3 [T]  every gadget of every world of cert_m3_d3.json checked structurally (exit law from the
                              built tree), then the smallest worlds fully from the game for T seconds (default 480)"""
import sys, os, json, math, bisect, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'harness'))
import mycore
HERE = os.path.dirname(os.path.abspath(__file__))

class Builder:
    def __init__(self, m):
        self.m = m; self.kinds = ['max'] * m; self.succ = [None] * m
    def add(self, kind, s=None):
        self.kinds.append(kind); self.succ.append(s); return len(self.kinds) - 1
    def gadget(self, row, targets, T0):
        """row: masses on `targets` (vertex ids), residue to T0; returns the entry vertex of the pruned rejection tree."""
        D = 1
        for x in row: D = D * x.denominator // math.gcd(D, x.denominator)
        K = [0]
        for x in row: K.append(K[-1] + int(x * D))
        if D == 1:   # a unit row or the zero row: no tree
            return targets[next(j for j in range(len(row)) if row[j] == 1)] if K[-1] == 1 else T0
        d = (D - 1).bit_length()
        bounds = sorted(set(K[1:]) | {D})
        def cls(i):   # assignment of leaf i
            if i >= D: return 'entry'
            if i >= K[-1]: return T0
            return targets[bisect.bisect_right(K, i) - 1]
        entry_holder = {}
        def build(lo, span):
            if not any(lo < b < lo + span for b in bounds):
                c = cls(lo); return 'entry' if c == 'entry' else c
            node = self.add('avg'); half = span // 2
            self.succ[node] = (build(lo, half), build(lo + half, half))
            return node
        root = build(0, 1 << d)
        assert root != 'entry'
        # resolve the rejection edges to the root
        for v in range(len(self.kinds)):
            if self.kinds[v] == 'avg' and self.succ[v] is not None and 'entry' in self.succ[v]:
                self.succ[v] = tuple(root if s == 'entry' else s for s in self.succ[v])
        return root

def build_game(rows, m):
    b = Builder(m); n_est = None
    T0 = None
    # sinks are the last two ids (n, n+1); we do not know n yet, so use placeholders and remap at the end
    PT0, PT1 = -1, -2
    for v in range(m):
        ents = []
        for a in (0, 1):
            q, p = rows[(v, a)]
            row = [q] + p; targets = [PT1] + list(range(m))
            keep = [j for j in range(len(row)) if row[j] > 0]
            root = b.gadget([row[j] for j in keep], [targets[j] for j in keep], PT0)
            e = b.add('avg', (root, root)); ents.append(e)   # the private entry
        b.succ[v] = tuple(ents)
    n = len(b.kinds); T0, T1 = n, n + 1
    succ = [tuple(T0 if s == PT0 else T1 if s == PT1 else s for s in sc) for sc in b.succ]
    return mycore.G(b.kinds, succ)

def values_under(g, sig):
    """one-player game, Max frozen at sig (indexed by the first m vertices): the unique solution of the linear system."""
    n = g.n; A = [[F(0)] * n for _ in range(n)]; rhs = [F(0)] * n
    for v in range(n):
        A[v][v] = F(1)
        if g.kinds[v] == 'max':
            s = g.succ[v][sig[v]]
            if s < n: A[v][s] -= 1
            elif s == g.T1: rhs[v] += 1
        else:
            for s in g.succ[v]:
                if s < n: A[v][s] -= F(1, 2)
                elif s == g.T1: rhs[v] += F(1, 2)
    return mycore._lin_solve(A, rhs)

def parse(rows, m):
    R = {}
    for k, v in rows.items():
        i, a = map(int, k.split(',')); vals = [F(x) for x in v]; R[(i, a)] = (vals[0], vals[1:])
    return R

def sys_star(R, m):
    best = None
    for sig in itertools.product((0, 1), repeat=m):
        P = [R[(i, sig[i])][1] for i in range(m)]; q = [R[(i, sig[i])][0] for i in range(m)]
        x = mycore._lin_solve([[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)], q)
        best = x if best is None else [max(a, c) for a, c in zip(best, x)]
    return best

def check_world(rows, m, tag, side):
    R = parse(rows, m); g = build_game(R, m)
    assert mycore.is_stopping(g), (tag, 'not stopping')
    w = mycore.wstar(g)[:g.n]; star = sys_star(R, m)
    assert list(w[:m]) == star, (tag, 'val* differs from the system')
    for sig in itertools.product((0, 1), repeat=m):
        x = values_under(g, sig) + [F(0), F(1)]
        for v in range(m):
            a, c = g.succ[v]; assert x[a] != x[c], (tag, 'tie', sig, v)
            # the successor values are the readings of the rows: the gadget realises the row exactly
            for act, s in ((0, a), (1, c)):
                q, p = R[(v, act)]; assert x[s] == q + sum(p[j] * x[j] for j in range(m)), (tag, 'row not realised', v, act)
    assert (w[0] < F(1, 2)) == (side == 'no'), (tag, 'bit')
    return g.N

def gadget_exit_law(g, entry, m):
    """exit law of the gadget entered at `entry` (an avg vertex): one-pass probabilities by recursion on the pruned tree,
    the rejection edges (back to the root) treated as a 'reject' outcome, then exit = onepass / (1 - reject)."""
    root = g.succ[entry][0]
    memo = {}
    def onepass(v):
        if v in memo: return memo[v]
        if v == root and memo.get('started'): return {'reject': F(1)}
        memo['started'] = True
        out = {}
        for s in g.succ[v]:
            sub = {'reject': F(1)} if s == root else onepass(s) if (s < g.n and g.kinds[s] == 'avg') else {s: F(1)}
            for k, val in sub.items(): out[k] = out.get(k, F(0)) + val / 2
        memo[v] = out; return out
    if g.kinds[root] != 'avg' or root == entry: return {root: F(1)}
    op = onepass(root); rej = op.pop('reject', F(0)); assert rej < F(1, 2)
    return {k: val / (1 - rej) for k, val in op.items()}

part = sys.argv[1] if len(sys.argv) > 1 else 'm2'
if part == 'm2':
    cert = json.load(open(f'{HERE}/cert_m2_d2.json')); sizes = []
    for c in cert:
        sizes.append(check_world(c['no_rows'], 2, ('no', c['queries']), 'no'))
        sizes.append(check_world(c['yes_rows'], 2, ('yes', c['queries']), 'yes'))
    print(f'm=2: all {len(sizes)} worlds of cert_m2_d2.json assembled as SSGs ({min(sizes)} to {max(sizes)} vertices incl. sinks) and verified from the game: stopping, val* equal to the system on C, every row realised exactly, nondegenerate at all 4 strategies, the bit at v0 on the certified side')
else:
    cert = json.load(open(f'{HERE}/cert_m3_d3.json')); worlds = []; ng = 0
    for c in cert:
        for key, side in (('no_rows', 'no'), ('yes_rows', 'yes')):
            R = parse(c[key], 3); g = build_game(R, 3); worlds.append((g.N, c[key], side, c['queries']))
            for v in range(3):
                for a in (0, 1):
                    law = gadget_exit_law(g, g.succ[v][a], 3); q, p = R[(v, a)]
                    want = {g.T1: q, **{j: p[j] for j in range(3)}}; want[g.T0] = 1 - q - sum(p)
                    want = {k: val for k, val in want.items() if val > 0}
                    assert law == want, ('gadget law', c['queries'], side, v, a, law, want); ng += 1
    sizes = [w[0] for w in worlds]
    print(f'm=3: {ng} gadgets of the {len(worlds)} worlds of cert_m3_d3.json built and their exit laws recomputed from the built trees: all exact; games of {min(sizes)} to {max(sizes)} vertices incl. sinks', flush=True)
    import time
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 480.0   # seconds for the full-game checks, smallest worlds first
    worlds.sort(key=lambda w: w[0]); done = 0; t0 = time.time(); largest = 0
    for N, rows, side, qs in worlds:
        if time.time() - t0 > budget: break
        check_world(rows, 3, (side, qs), side); done += 1; largest = N
    print(f'm=3: the {done} smallest worlds ({worlds[0][0]} to {largest} vertices, {int(time.time()-t0)} s) verified fully from the game: stopping, val* equal to the system, rows realised, nondegenerate at all 8 strategies, the bit on the certified side')
