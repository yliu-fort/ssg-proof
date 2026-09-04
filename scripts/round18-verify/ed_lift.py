#!/usr/bin/env python3
"""prop:eval-lift on random data: one-player stopping dyadic systems over C (m=3), data of t=2 random queries,
a random sigma*, c in {1/2, 1}. For each v: S^c_v (nonnegative rows with q + c*sum p = c and the t recorded readings)
is nonempty iff the appeal profile lies in conv{c*1_t, X_u}; both sides decided exactly by vertex enumeration.
When every S^c_v is nonempty and some choice of vertices makes the lifted system M' STOPPING (tested directly: the
correctness auditor showed the route's reachability hypothesis on the replaced rows does not imply it), M'
reproduces the data (same values and appeals at both queries) and has val_{sigma*} = c on all of C. Choices that
satisfy the reachability hypothesis but are not stopping are counted."""
import sys, random, itertools
from fractions import Fraction as F

def solve(Mx, rhs):
    n = len(Mx); T = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None: return None
        T[c], T[p] = T[p], T[c]; pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]

def vertices(E, b, dim):
    """vertices of {z >= 0 : E z = b}, E with k rows: choose k coordinates to be free, the rest zero."""
    k = len(E); out = []
    for S in itertools.combinations(range(dim), k):
        A = [[E[i][j] for j in S] for i in range(k)]; x = solve(A, b)
        if x is None or any(t < 0 for t in x): continue
        z = [F(0)] * dim
        for j, t in zip(S, x): z[j] = t
        if all(sum(E[i][j] * z[j] for j in range(dim)) == b[i] for i in range(k)): out.append(tuple(z))
    return sorted(set(out))

def in_hull(pt, gens):
    """pt in conv(gens) (all in Q^t): some subset of <= t+1 generators carries it with nonneg barycentric weights."""
    t = len(pt)
    for k in range(1, min(len(gens), t + 1) + 1):
        for S in itertools.combinations(range(len(gens)), k):
            E = [[gens[j][i] for j in S] for i in range(t)] + [[F(1)] * k]
            if vertices(E, list(pt) + [F(1)], k): return True
    return False

def values(rows, sig, m):
    P = [rows[(i, sig[i])][1] for i in range(m)]; q = [rows[(i, sig[i])][0] for i in range(m)]
    return solve([[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)], q)

def stopping(rows, m):
    for U in range(1, 1 << m):
        us = [i for i in range(m) if (U >> i) & 1]
        if all(any(rows[(i, a)][0] == 0 and sum(rows[(i, a)][1]) == 1 and all(rows[(i, a)][1][j] == 0 for j in range(m) if not (U >> j) & 1) for a in (0, 1)) for i in us):
            return False
    return True

rng = random.Random(11); m = 3; t = 2; D = 4
stats = {'systems': 0, 'criterion': 0, 'lifted': 0, 'empty': 0, 'no_stopping_choice': 0, 'reach_not_stopping': 0}
while stats['systems'] < 200:
    rows = {}
    for i in range(m):
        for a in (0, 1):
            w = [rng.randrange(0, 2 ** D) for _ in range(m + 1)]; s = sum(w) or 1
            tot = rng.randrange(2 ** D - 3, 2 ** D + 1)      # dense, nearly stochastic rows (the lift lives there)
            row = [F(x * tot, s * 2 ** D) for x in w]; rows[(i, a)] = (row[0], row[1:])
    if not stopping(rows, m): continue
    stats['systems'] += 1
    sigs = rng.sample(list(itertools.product((0, 1), repeat=m)), t)
    X = [values(rows, s, m) for s in sigs]
    A = [{(v, a): rows[(v, a)][0] + sum(rows[(v, a)][1][j] * X[r][j] for j in range(m)) for v in range(m) for a in (0, 1)} for r in range(t)]
    star = rng.choice(list(itertools.product((0, 1), repeat=m))); c = rng.choice([F(1, 2), F(1)])
    choices = {}
    for v in range(m):
        E = [[F(1)] + [c] * m] + [[F(1)] + list(X[r]) for r in range(t)]
        b = [c] + [A[r][(v, star[v])] for r in range(t)]
        V = vertices(E, b, m + 1)
        gens = [tuple([c] * t)] + [tuple(X[r][u] for r in range(t)) for u in range(m)]
        assert (len(V) > 0) == in_hull(tuple(A[r][(v, star[v])] for r in range(t)), gens), 'hull criterion'
        stats['criterion'] += 1
        choices[v] = V
    if any(not choices[v] for v in range(m)): stats['empty'] += 1; continue
    # look for a choice of vertices making M' stopping (tested directly); count reachable-but-not-stopping choices
    found = None
    for pick in itertools.product(*[choices[v] for v in range(m)]):
        rows2 = dict(rows)
        for v in range(m): rows2[(v, star[v])] = (pick[v][0], list(pick[v][1:]))
        q = {v: pick[v][0] for v in range(m)}; supp = {v: [u for u in range(m) if pick[v][1 + u] > 0] for v in range(m)}
        good = {v for v in range(m) if q[v] > 0}; changed = True
        while changed:
            changed = False
            for v in range(m):
                if v not in good and any(u in good for u in supp[v]): good.add(v); changed = True
        reach = len(good) == m; stp = stopping(rows2, m)
        if reach and not stp: stats['reach_not_stopping'] += 1
        if stp and found is None: found = pick
    if found is None: stats['no_stopping_choice'] += 1; continue
    rows2 = dict(rows)
    for v in range(m): rows2[(v, star[v])] = (found[v][0], list(found[v][1:]))
    assert stopping(rows2, m)
    for r in range(t):
        x2 = values(rows2, sigs[r], m); assert x2 == X[r]
        assert all(rows2[(v, a)][0] + sum(rows2[(v, a)][1][j] * x2[j] for j in range(m)) == A[r][(v, a)] for v in range(m) for a in (0, 1))
    assert values(rows2, star, m) == [c] * m
    stats['lifted'] += 1
print(f"prop:eval-lift, m={m}, t={t}: {stats['systems']} random dense systems; hull criterion agreed with vertex enumeration in all {stats['criterion']} fibres; "
      f"{stats['lifted']} lifts built (M' stopping, reproduces both queries, val_(sigma*) = c on C), {stats['empty']} with an empty S^c_v, {stats['no_stopping_choice']} with no stopping choice of vertices; "
      f"{stats['reach_not_stopping']} vertex choices satisfied the route's reachability hypothesis but were NOT stopping")
