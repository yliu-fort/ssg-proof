#!/usr/bin/env python3
"""Root agent's own check of the round-17 parametric-path route's family BP(D) (labels pp:), rebuilt
from the STATEMENT's successor lists (not from the route's code). G_beta has operator beta*T: every
step out of a non-sink is diverted to t0 with probability 1-beta. BP(D) is acyclic, so w_beta and the
optimal pair are exact backward inductions; everything in Fractions."""
from fractions import Fraction as F
import itertools, sys, json

def build_BP(D):
    kinds = {}; succ = {}
    def add(name, kind, s0, s1): kinds[name] = kind; succ[name] = (s0, s1)
    add('F0', 'avg', 'f1', 'f1'); add('f1', 'avg', 't1', 't1')       # F_0: a deterministic chain of length 2
    G = {0: 't0'}; Fv = {0: 'F0'}
    add('c1', 'avg', 't0', 't1')
    for d in range(2, D + 1):
        add(f'w1_{d}', 'avg', 't0', f'w2_{d}'); add(f'w2_{d}', 'avg', 't0', f'w3_{d}'); add(f'w3_{d}', 'avg', f'c{d-1}', f'c{d-1}')
        kinds[f'c{d}'] = kinds[f'w1_{d}']; succ[f'c{d}'] = succ[f'w1_{d}']; del kinds[f'w1_{d}'], succ[f'w1_{d}']
    for d in range(1, D + 1):
        add(f'P{d}', 'avg', Fv[d-1], Fv[d-1]); add(f'Q{d}', 'avg', G[d-1], G[d-1]); add(f'B{d}', 'avg', f'c{d}', f'c{d}')
        add(f'X{d}', 'avg', f'P{d}', 't0'); add(f'Y{d}', 'avg', f'Q{d}', f'B{d}')
        add(f'F{d}', 'max', f'X{d}', f'Y{d}'); add(f'G{d}', 'min', f'X{d}', f'Y{d}')
        Fv[d] = f'F{d}'; G[d] = f'G{d}'
    return kinds, succ

def values(kinds, succ, beta):
    """w_beta by backward induction (the game must be acyclic); returns (w, tied set, optimal choices)"""
    w = {'t0': F(0), 't1': F(1)}; tied = set(); choice = {}
    def val(v):
        if v in w: return w[v]
        a, b = (val(succ[v][0]), val(succ[v][1]))
        if kinds[v] == 'avg': r = beta * (a + b) / 2
        else:
            r = beta * (max(a, b) if kinds[v] == 'max' else min(a, b))
            if a == b: tied.add(v)
            else: choice[v] = 0 if (a > b) == (kinds[v] == 'max') else 1
        w[v] = r; return r
    for v in kinds: val(v)
    return w, tied, choice

def tent(z): return abs(2 * z - 1)

for D in range(1, 9):
    kinds, succ = build_BP(D)
    N = len(kinds) + 2; assert N == 10 * D + 2, (D, N)
    # the tent identity at random rationals
    for beta in [F(j, 97) for j in range(1, 97, 7)]:
        w, tied, ch = values(kinds, succ, beta)
        assert not tied
        for d in range(1, D + 1):
            e_d = beta * (beta ** 3 / 4) ** d; phi = w[f'F{d}'] - w[f'G{d}']
            z = beta
            for _ in range(d): z = tent(z)
            assert phi == z * e_d, (D, d, beta)
            assert w[f'c{d}'] == (beta / 2) * (beta ** 3 / 4) ** (d - 1)
    # the breakpoints: ties exactly at k/2^D, two tied vertices each, pairs distinct on the 2^D intervals
    bps = []
    for k in range(1, 2 ** D):
        w, tied, ch = values(kinds, succ, F(k, 2 ** D))
        v2 = 0; kk = k
        while kk % 2 == 0: kk //= 2; v2 += 1
        d = D - v2                                      # k/2^D is an odd multiple of 2^-d
        assert tied == {f'F{d}', f'G{d}'}, (D, k, tied)
        bps.append(F(k, 2 ** D))
    pairs = []
    for k in range(2 ** D):
        for off in (F(1, 5), F(1, 2), F(4, 5)):     # three interior points per interval: no change inside
            w, tied, ch = values(kinds, succ, (k + off) / 2 ** D)
            assert not tied
            p = tuple(ch[f'F{d}'] for d in range(1, D + 1)) + tuple(ch[f'G{d}'] for d in range(1, D + 1))
            if off == F(1, 2): pairs.append(p)
            else: assert p == pairs[-1] if off == F(4, 5) else True
            if off == F(1, 5): first = p
            if off == F(1, 2): assert p == first
    assert len(set(pairs)) == 2 ** D and all(pairs[i] != pairs[i + 1] for i in range(2 ** D - 1))
    # the itinerary
    for k in range(2 ** D):
        beta = (2 * k + 1) / F(2 ** (D + 1)); z = beta; it = []
        for d in range(1, D + 1):
            it.append(0 if z > F(1, 2) else 1); z = tent(z)      # F_d takes X_d (choice 0) iff T^{d-1}(beta) > 1/2
        assert tuple(it) == pairs[k][:D], (D, k)
    print(f'BP({D}): N = {N}, tent identity at 14 rationals for every level, breakpoints exactly {{k/2^{D}}} ({2**D - 1}), '
          f'two tied vertices each, {2**D} pairwise distinct optimal pairs = the tent itinerary', flush=True)

# the route's OS instances: one Max vertex u, val(u_0) - val(u_1) = c * beta^K * prod_i (beta - r_i) with the
# file's own roots r_i (OS2.json carries roots {1/4,1/2}; the statement's OS_2 with roots {1/2,3/4} is not dumped)
for fn in sys.argv[1:]:
    d = json.load(open(fn)); roots = [F(r) for r in d['roots']]
    kinds = {i: k for i, k in enumerate(d['kinds'])}; n = len(kinds)
    succ = {i: tuple(('t0' if s == n else 't1' if s == n + 1 else s) for s in d['succ'][i]) for i in range(n)}
    u = [v for v in kinds if kinds[v] == 'max']; assert len(u) == 1; u = u[0]
    cK = None; pattern = []
    pts = sorted(set([F(1, 97)] + roots + [(roots[i] + roots[i + 1]) / 2 for i in range(len(roots) - 1)] + [F(1, 3), F(2, 3), F(5, 7), F(11, 13), F(19, 20), (roots[0]) / 2, (1 + roots[-1]) / 2]))
    for beta in pts:
        w, tied, ch = values(kinds, succ, beta)
        diff = w[succ[u][0]] - w[succ[u][1]]
        if beta in roots: assert diff == 0 and tied == {u}; continue
        assert diff != 0 and not tied
        q = diff
        for r in roots: q /= (beta - r)
        # q must be c * beta^K: pin (c, K) from the first point and check the rest
        if cK is None:
            for K in range(0, 60):
                c = q / beta ** K
                if c.denominator & (c.denominator - 1) == 0 and c.numerator == 1 or True:
                    pass
            cK = (q, beta)
        else:
            q0, b0 = cK
            # q/q0 = (beta/b0)^K for an integer K
            ratio = q / q0; K = 0; t = F(1)
            while t != ratio and K < 80: t *= beta / b0; K += 1
            assert t == ratio, (fn, beta, ratio)
            Kfound = K
        pattern.append((beta, 0 if diff > 0 else 1))
    K = Kfound; c = cK[0] / cK[1] ** K
    seq = [p[1] for p in pattern]
    print(f'{fn.split("/")[-1]}: {n + 2} vertices, roots {[str(r) for r in roots]}: val(u_0)-val(u_1) = {c} * beta^{K} * prod(beta - r_i) at {len(pts)} rationals; '
          f'ties exactly at the roots; optimal action along beta: {"".join(map(str, seq))} ({len(set(zip(seq, seq[1:])))} changes pattern)')
