#!/usr/bin/env python3
"""The one-player, undamped fold proposed by the round-18 novelty auditor of the one-player-envelope route (and implied by
the route's device): X0->(u,u), Y0->(t1,t0), F0=max(X0,Y0) in Vmax, H0=avg(X0,Y0); per level d>=1: S^a_d->(S_{d-1},t0),
S^b_d->(S^a_d,t0), S_d->(S^b_d,t0) with S_0:=t1; X_d->(F_{d-1},t0), Y_d->(H_{d-1},S_d), F_d=max(X_d,Y_d), H_d=avg(X_d,Y_d);
u frozen at payoff theta (thm:fold's reading). Claims: phi_d = |phi_{d-1}|/4 - 8^{-d}/2, psi_d = 2|psi_{d-1}|-1 with
psi_0 = 2theta-1; the response map theta -> val(F_D) is piecewise affine with exactly 2^D+1 pieces of pairwise distinct
slopes; 7D+3 non-sinks besides u; Vmin empty. Exact arithmetic."""
import sys
from fractions import Fraction as F
import os as _os; sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness')); sys.path.insert(0, '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/root16')
from mycore import G, is_stopping, wstar

def build(D):
    names, kinds, succ = [], [], []
    def add(nm, k, s): names.append(nm); kinds.append(k); succ.append(s)
    add('u', 'avg', ('t0', 't1'))            # placeholder; frozen at theta below
    add('X0', 'avg', ('u', 'u')); add('Y0', 'avg', ('t1', 't0')); add('F0', 'max', ('X0', 'Y0')); add('H0', 'avg', ('X0', 'Y0'))
    for d in range(1, D+1):
        Sprev = 't1' if d == 1 else f'S{d-1}'
        add(f'Sa{d}', 'avg', (Sprev, 't0')); add(f'Sb{d}', 'avg', (f'Sa{d}', 't0')); add(f'S{d}', 'avg', (f'Sb{d}', 't0'))
        add(f'X{d}', 'avg', (f'F{d-1}', 't0')); add(f'Y{d}', 'avg', (f'H{d-1}', f'S{d}'))
        add(f'F{d}', 'max', (f'X{d}', f'Y{d}')); add(f'H{d}', 'avg', (f'X{d}', f'Y{d}'))
    n = len(names); idx = {nm: i for i, nm in enumerate(names)}; idx['t0'] = n; idx['t1'] = n+1
    return names, kinds, [(idx[a], idx[b]) for a, b in succ], idx

def values(kinds, succ, idx, theta):
    """backward induction (acyclic), u frozen at theta."""
    n = len(kinds); memo = {idx['u']: theta}
    def val(v):
        if v == n: return F(0)
        if v == n+1: return F(1)
        if v in memo: return memo[v]
        a, b = succ[v]
        r = max(val(a), val(b)) if kinds[v] == 'max' else (val(a) + val(b)) / 2
        memo[v] = r; return r
    return [val(v) for v in range(n)]

def T(z): return abs(2*z - 1)

for D in range(1, 9):
    names, kinds, succ, idx = build(D)
    assert len(names) == 7*D + 5 and kinds.count('max') == D+1 and kinds.count('min') == 0
    g = G(kinds, succ); assert is_stopping(g)
    # the identities at several theta
    for theta in (F(1,3), F(2,7), F(5,11), F(7,9), F(13,16), F(41,97)):
        v = values(kinds, succ, idx, theta)
        psi_prev = None; t = theta
        for d in range(D+1):
            phi = v[idx[f'X{d}']] - v[idx[f'Y{d}']]; e = F(1, 2) * F(1, 8)**d
            psi = phi / e
            assert psi == (2*theta - 1 if d == 0 else 2*abs(psi_prev) - 1), (D, theta, d)
            assert psi == 2*t - 1
            psi_prev = psi; t = T(t)
    # the response map theta -> val(F_D): pieces on the dyadic grid of mesh 2^-(D+4)
    Mg = 2**(D+4); pts = [F(j, Mg) for j in range(Mg+1)]
    R = [values(kinds, succ, idx, t)[idx[f'F{D}']] for t in pts]
    slopes = [(R[j+1] - R[j]) * Mg for j in range(Mg)]
    pieces = 1 + sum(1 for j in range(1, Mg) if slopes[j] != slopes[j-1])
    # affinity inside each grid cell: a third point (the 1/3 point) lies on the chord
    for j in range(Mg):
        t3 = pts[j] + F(1, 3*Mg); r3 = values(kinds, succ, idx, t3)[idx[f'F{D}']]
        assert r3 == R[j] + slopes[j] / (3*Mg), (D, j)
    # the value of u itself: u -> (t0, t1) realises theta = 1/2 only; the frozen reading is thm:fold's
    distinct_slopes = len(set(slopes))
    print(f'D={D}: {len(names)-1} non-sinks besides u, one player, stopping; response map pieces on the grid: {pieces} (2^D+1={2**D+1}); distinct slopes {distinct_slopes}')
    assert pieces == 2**D + 1 and distinct_slopes == 2**D + 1
print('ALL ONE-PLAYER UNDAMPED FOLD CHECKS PASSED (pieces counted on the dyadic grid of mesh 2^-(D+4); breakpoints of T^{D+1} are dyadic of that mesh)')
