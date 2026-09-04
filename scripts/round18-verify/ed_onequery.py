#!/usr/bin/env python3
"""ed:one-query: for a one-player stopping harmonic system M over C (rows (q, p) with p supported on C, substochastic,
p_v = 0 on its own vertex not required), a strategy sigma_1, and a strictly switchable vertex v (appeal A of the other
action > xi = val_{sigma_1}(v)), replacing that other action's row by z' = ((A-xi)/(1-xi), ((1-A)/(1-xi)) e_v) gives a
system consistent with the query's data (values at C and all appeals), stopping, with val_{sigma_1[v]}(v) = 1.
Checked on random dyadic systems, exact arithmetic."""
import sys, random, itertools
from fractions import Fraction as F

def solve(Mx, rhs):
    n = len(Mx); T = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if T[r][c] != 0); T[c], T[p] = T[p], T[c]; pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]

def values(rows, sig, m):
    P = [rows[(i, sig[i])][1] for i in range(m)]; q = [rows[(i, sig[i])][0] for i in range(m)]
    A = [[F(int(i == j)) - P[i][j] for j in range(m)] for i in range(m)]
    return solve(A, q)

def stopping(rows, m):
    # a trap: a set U of vertices with, for some choice of actions, every chosen row supported inside U with full mass
    for U in range(1, 1 << m):
        us = [i for i in range(m) if (U >> i) & 1]
        if all(any(rows[(i, a)][0] == 0 and sum(rows[(i, a)][1]) == 1 and all(rows[(i, a)][1][j] == 0 for j in range(m) if not (U >> j) & 1) for a in (0, 1)) for i in us):
            return False
    return True

rng = random.Random(3); trials = 0; ok = 0
while trials < 300:
    m = rng.choice([3, 4]); D = 4
    rows = {}
    for i in range(m):
        for a in (0, 1):
            w = [rng.randrange(0, 2 ** D) for _ in range(m + 1)]
            s = sum(w)
            if s == 0: w[rng.randrange(m + 1)] = 1; s = 1
            tot = rng.randrange(1, 2 ** D)          # total mass tot/2^D < 1 (a strict leak)
            row = [F(x * tot, s * 2 ** D) for x in w]
            rows[(i, a)] = (row[0], row[1:])
    if not stopping(rows, m): continue
    sig = tuple(rng.randrange(2) for _ in range(m)); x = values(rows, sig, m)
    appeal = {(i, a): rows[(i, a)][0] + sum(rows[(i, a)][1][j] * x[j] for j in range(m)) for i in range(m) for a in (0, 1)}
    sw = [i for i in range(m) if appeal[(i, 1 - sig[i])] > x[i]]
    if not sw: continue
    trials += 1
    v = rng.choice(sw); A = appeal[(v, 1 - sig[v])]; xi = x[v]; assert xi < 1
    zq = (A - xi) / (1 - xi); zs = (1 - A) / (1 - xi)
    assert zq > 0 and zs >= 0 and zq + zs == 1
    rows2 = dict(rows); rows2[(v, 1 - sig[v])] = (zq, [zs if j == v else F(0) for j in range(m)])
    assert stopping(rows2, m)
    x2 = values(rows2, sig, m); assert x2 == x
    appeal2 = {(i, a): rows2[(i, a)][0] + sum(rows2[(i, a)][1][j] * x2[j] for j in range(m)) for i in range(m) for a in (0, 1)}
    assert appeal2 == appeal
    sig2 = tuple(1 - sig[i] if i == v else sig[i] for i in range(m)); x3 = values(rows2, sig2, m)
    assert x3[v] == 1
    ok += 1
print(f'ed:one-query: {ok}/{trials} random (system, strategy, strictly switchable vertex) triples at m in {{3,4}}: the lifted row is in the simplex, the system stays stopping, reproduces the query (values and all appeals) and has val_{{sigma_1[v]}}(v) = 1')
