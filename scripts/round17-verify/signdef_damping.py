#!/usr/bin/env python3
"""Root agent's own check of the paper auditor's counterexample to rem:signdef's claim
that the sign-definite class (def:signdef) is closed under def:damping.

def:signdef: for v in Vmax, d^v := (p^{v^(1)} - p^{v^(0)})|_C where p^u is the first-passage
law from u onto C u {t0,t1} (C = controlled vertices), and the game is sign-definite if every
d^v is componentwise >= 0 or componentwise <= 0.
def:damping: G_m replaces EVERY edge u->w by a chain g_1..g_m of average vertices,
g_i -> {w, g_{i+1}} (i<m), g_m -> {w, t0}, each with probability 1/2.
Everything in exact rational arithmetic, written from the definitions (not from the auditor's code)."""
from fractions import Fraction as F

def first_passage(kinds, succ, C, start):
    """P[first vertex of C u {t0,t1} hit, starting from `start`]; if start is in C or a sink it
    is hit immediately. Only average vertices are traversed (the token stops at C)."""
    targets = list(C) + ['t0', 't1']
    if start in targets:
        return {t: F(int(t == start)) for t in targets}
    inter = [x for x in kinds if kinds[x] == 'avg' and x not in C]
    idx = {x: i for i, x in enumerate(inter)}
    n = len(inter)
    out = {}
    for t in targets:
        # x_i = 1/2 sum over successors (x_w if w interior, [w==t] otherwise)
        A = [[F(0)] * n for _ in range(n)]; b = [F(0)] * n
        for x in inter:
            i = idx[x]; A[i][i] += 1
            for w in succ[x]:
                if w in idx: A[i][idx[w]] -= F(1, 2)
                elif w == t: b[i] += F(1, 2)
        # Gaussian elimination
        Mx = [A[i][:] + [b[i]] for i in range(n)]
        for c in range(n):
            p = next(r for r in range(c, n) if Mx[r][c] != 0)
            Mx[c], Mx[p] = Mx[p], Mx[c]
            pv = Mx[c][c]; Mx[c] = [y / pv for y in Mx[c]]
            for r in range(n):
                if r != c and Mx[r][c] != 0:
                    f = Mx[r][c]; Mx[r] = [Mx[r][k] - f * Mx[c][k] for k in range(n + 1)]
        out[t] = Mx[idx[start]][n]
    return out

def dvecs(kinds, succ, C):
    res = {}
    for v in C:
        if kinds[v] != 'max': continue
        p1 = first_passage(kinds, succ, C, succ[v][1]); p0 = first_passage(kinds, succ, C, succ[v][0])
        res[v] = {w: p1[w] - p0[w] for w in C}
    return res

def sign_definite(d):
    return all((all(x >= 0 for x in dv.values()) or all(x <= 0 for x in dv.values())) for dv in d.values())

def damp(kinds, succ, m):
    K = dict(kinds); S = {}
    cnt = 0
    for u in list(succ):
        new = []
        for w in succ[u]:
            chain = [f'g{cnt}_{i}' for i in range(1, m + 1)]; cnt += 1
            for i, g in enumerate(chain):
                K[g] = 'avg'
                S[g] = (w, chain[i + 1]) if i + 1 < m else (w, 't0')
            new.append(chain[0])
        S[u] = tuple(new)
    return K, S

def is_stopping(kinds, succ):
    """largest trap U (set of non-sinks with t1 unreachable... ) via lem:trapchar: iterate."""
    U = set(kinds)
    changed = True
    while changed:
        changed = False
        for x in list(U):
            ok = all(w in U for w in succ[x]) if kinds[x] == 'avg' else any(w in U for w in succ[x])
            if not ok: U.discard(x); changed = True
    return len(U) == 0

if __name__ == '__main__':
    kinds = {'v': 'max', 'w1': 'max', 'w2': 'max', 'A': 'avg', 'a1': 'avg', 'B': 'avg', 'b1': 'avg'}
    succ = {'v': ('B', 'A'), 'w1': ('t1', 't0'), 'w2': ('t0', 't1'),
            'A': ('a1', 'w2'), 'a1': ('w1', 'w1'), 'B': ('w1', 'b1'), 'b1': ('w2', 't0')}
    C = ['v', 'w1', 'w2']
    print('G stopping:', is_stopping(kinds, succ), ' N =', len(kinds) + 2)
    d = dvecs(kinds, succ, C)
    print('G: d^v =', {v: [str(x) for x in dv.values()] for v, dv in d.items()}, ' sign-definite:', sign_definite(d))
    for m in (1, 2, 3, 4):
        K, S = damp(kinds, succ, m)
        d = dvecs(K, S, C)
        print(f'G_{m}: stopping={is_stopping(K,S)} N={len(K)+2} d^v =', {v: [str(x) for x in dv.values()] for v, dv in d.items()},
              ' sign-definite:', sign_definite(d))
    # the closed form: with lambda = 1 - 2^-m, d^v(G_m) = (0, lam^2(1-lam)/2, -lam^2(2-lam)/4)
    for m in (1, 2, 3, 4):
        lam = 1 - F(1, 2 ** m)
        print(f'  closed form m={m}:', [str(x) for x in (F(0), lam ** 2 * (1 - lam) / 2, -lam ** 2 * (2 - lam) / 4)])
