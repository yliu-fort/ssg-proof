#!/usr/bin/env python3
"""Root-agent verification of the round-18 one-player-envelope route's OF(D) (ue:onefold, ue:linearise,
ue:cascade, ue:path-not-run, ue:pgf(d)), rebuilt from the STATEMENT, exact arithmetic throughout.

OF(D): non-sinks u1, X0, Y0, F0, H_d (0<=d<D), P_d, X_d, R_d, S_d, S'_d, S''_d, Y_d, F_d (1<=d<=D);
F_0..F_D in Vmax, all others average, Vmin empty; edges
  u1->(t1,t1), X0->(u1,u1), Y0->(t1,t0), F0->(X0,Y0), H_d->(X_d,Y_d), P_d->(F_{d-1},F_{d-1}),
  X_d->(P_d,t0), R_d->(H_{d-1},H_{d-1}), Y_d->(R_d,S_d), F_d->(X_d,Y_d),
  S_d->(S'_d,t0), S'_d->(S''_d,t0), S''_d->(S_{d-1},t0), S_0 := t1.
Damped game OF(D)_rho (def:discount-path): every step out of a non-sink survives with probability rho."""
import sys, os, json, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os; sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness')); sys.path.insert(0, '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/root16')
from mycore import G, is_stopping, wstar, profile_value

def build_OF(D):
    names, kinds, succ = [], [], []
    def add(nm, k, s): names.append(nm); kinds.append(k); succ.append(s)
    add('u1','avg',('t1','t1')); add('X0','avg',('u1','u1')); add('Y0','avg',('t1','t0')); add('F0','max',('X0','Y0'))
    for d in range(D): add(f'H{d}','avg',(f'X{d}',f'Y{d}'))
    for d in range(1, D+1):
        add(f'P{d}','avg',(f'F{d-1}',f'F{d-1}'))
        add(f'X{d}','avg',(f'P{d}','t0'))
        add(f'R{d}','avg',(f'H{d-1}',f'H{d-1}'))
        Sprev = 't1' if d == 1 else f'S{d-1}'
        add(f'S{d}','avg',(f"S'{d}",'t0')); add(f"S'{d}",'avg',(f"S''{d}",'t0')); add(f"S''{d}",'avg',(Sprev,'t0'))
        add(f'Y{d}','avg',(f'R{d}',f'S{d}'))
        add(f'F{d}','max',(f'X{d}',f'Y{d}'))
    n = len(names); idx = {nm: i for i, nm in enumerate(names)}; idx['t0'] = n; idx['t1'] = n+1
    return names, kinds, [(idx[a], idx[b]) for a, b in succ], idx

def damped_values(kinds, succ, rho, sigma=None):
    """Exact values of the damped game by backward induction (the graph is acyclic); sigma: dict max-vertex -> chosen index."""
    n = len(kinds); memo = {}
    def val(v):
        if v == n: return F(0)
        if v == n+1: return F(1)
        if v in memo: return memo[v]
        a, b = succ[v]
        if kinds[v] == 'max':
            r = rho * (max(val(a), val(b)) if sigma is None else val(succ[v][sigma[v]]))
        else:
            r = rho * (val(a) + val(b)) / 2
        memo[v] = r; return r
    return [val(v) for v in range(n)]

def tent(z): return abs(2*z - 1)
def Td(z, d):
    for _ in range(d): z = tent(z)
    return z
def nu2(k):
    c = 0
    while k % 2 == 0: k //= 2; c += 1
    return c

def gated_game(kinds, succ, rho):
    """The damped game as an ordinary SSG: every edge u->w routed through a chain of average vertices
    realising survival rho (binary expansion), the rest to t0. Sinks as sentinels until the end."""
    n = len(kinds); bits = []; r = rho
    while r > 0:
        r *= 2; bits.append(1 if r >= 1 else 0); r -= bits[-1]
    assert len(bits) <= 12
    names = [('v', i) for i in range(n)]; K = {('v', i): kinds[i] for i in range(n)}; S = {}
    def target(w): return 'T0' if w == n else 'T1' if w == n+1 else ('v', w)
    for u in range(n):
        outs = []
        for i, w in enumerate(succ[u]):
            prev = None; first = None
            for j, b in enumerate(bits):
                g = ('g', u, i, j); names.append(g); K[g] = 'avg'
                hit = target(w) if b else 'T0'
                S[g] = [hit, None]
                if prev is not None: S[prev][1] = g
                else: first = g
                prev = g
            S[prev][1] = 'T0'
            outs.append(first)
        S[('v', u)] = outs
    N = len(names); ix = {nm: i for i, nm in enumerate(names)}; ix['T0'] = N; ix['T1'] = N+1
    return G([K[nm] for nm in names], [(ix[S[nm][0]], ix[S[nm][1]]) for nm in names]), N

def check_OF(D, rhos):
    names, kinds, succ, idx = build_OF(D)
    n = len(names)
    assert n == 9*D + 4 and kinds.count('max') == D+1 and kinds.count('min') == 0
    assert all(len(s) == 2 for s in succ)
    g = G(kinds, succ); assert is_stopping(g)
    # (b) tent identity
    for rho in rhos:
        v = damped_values(kinds, succ, rho)
        for d in range(D+1):
            e = (rho/2) * (rho**3/8)**d
            psi = (v[idx[f'X{d}']] - v[idx[f'Y{d}']]) / e
            assert psi == 2*Td(rho, d) - 1, (D, rho, d, psi)
    # (c) breakpoint structure
    M = 2**(D+1)
    signs = []
    for k in range(M):
        vecs = []
        for t in (F(2*k+1, 2*M), F(3*k+1, 3*M)):
            v = damped_values(kinds, succ, t)
            vecs.append(tuple(1 if v[idx[f'X{d}']] > v[idx[f'Y{d}']] else -1 if v[idx[f'X{d}']] < v[idx[f'Y{d}']] else 0 for d in range(D+1)))
        assert vecs[0] == vecs[1] and 0 not in vecs[0], (D, k, vecs)
        signs.append(vecs[0])
    assert len(set(signs)) == M
    assert all(sum(a != b for a, b in zip(signs[k], signs[k+1])) == 1 for k in range(M-1))
    switched = []
    for k in range(1, M):
        v = damped_values(kinds, succ, F(k, M))
        ties = [d for d in range(D+1) if v[idx[f'X{d}']] == v[idx[f'Y{d}']]]
        assert ties == [D - nu2(k)], (D, k, ties)
        switched.append(ties[0])
    distinct = len(set(switched))
    return names, kinds, succ, idx, distinct, M-1

def check_linearise(D, rhos):
    names, kinds, succ, idx = build_OF(D)
    Fs = [idx[f'F{d}'] for d in range(D+1)]
    longest = 0
    for rho in rhos:
        for bits in itertools.product((0, 1), repeat=D+1):
            sigma = {Fs[d]: bits[d] for d in range(D+1)}
            v = damped_values(kinds, succ, rho, sigma)
            eps = [1 if bits[d] == 0 else -1 for d in range(D+1)]
            psi_prev = None
            for d in range(D+1):
                e = (rho/2) * (rho**3/8)**d
                psi = (v[idx[f'X{d}']] - v[idx[f'Y{d}']]) / e
                want = 2*rho - 1 if d == 0 else 2*eps[d-1]*psi_prev - 1
                assert psi == want, (D, rho, bits, d, psi, want)
                psi_prev = psi
        # all-switches from every start
        for bits in itertools.product((0, 1), repeat=D+1):
            sigma = {Fs[d]: bits[d] for d in range(D+1)}; rounds = 0
            while True:
                v = damped_values(kinds, succ, rho, sigma)
                S = [f for f in Fs if v[succ[f][1-sigma[f]]] > v[succ[f][sigma[f]]]]
                if not S: break
                for f in S: sigma[f] = 1 - sigma[f]
                rounds += 1
                assert rounds <= D + 2, (D, rho, bits)
            longest = max(longest, rounds)
    return longest

if __name__ == '__main__':
    rhos = [F(1,3), F(2,7), F(5,11), F(7,9), F(1,2), F(3,8), F(13,16), F(1,100), F(99,100), F(41,97)]
    for D in range(0, 10):
        names, kinds, succ, idx, distinct, steps = check_OF(D, rhos)
        print(f'OF({D}): N={len(names)+2}, m={D+1}, stopping, tent identity at {len(rhos)} rationals, '
              f'breakpoints {steps} = 2^{D+1}-1, Gray walk, level D-nu2(k); distinct switched sets {distinct} of {steps} steps')
    for D in range(0, 6):
        L = check_linearise(D, [F(1,3), F(2,5), F(7,11), F(9,16), F(3,8), F(23,32)])
        print(f'OF({D}): affine cascade under all {2**(D+1)} strategies OK; longest all-switches run {L} <= D+2={D+2}')
    # (d) from the GAME: damped game with rho-gates, values by mycore (brute force over strategies, linear solves)
    for D, rho in [(0, F(1,4)), (1, F(1,4)), (1, F(5,8)), (2, F(3,8)), (2, F(11,16)), (3, F(7,16))]:
        names, kinds, succ, idx = build_OF(D)
        gg, N = gated_game(kinds, succ, rho)
        assert is_stopping(gg)
        w = wstar(gg)
        v = damped_values(kinds, succ, rho)
        assert all(w[i] == v[i] for i in range(len(names))), (D, rho)
        print(f'OF({D})_rho, rho={rho}: gated SSG on {N+2} vertices, stopping, wstar (brute force) == backward induction at all {len(names)} vertices')
    # compare with the route's game files (their graph, my evaluator)
    RD = '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/r18-one-player-envelope'
    for D in (1, 2, 3, 5, 8):
        f = f'{RD}/OF_{D}.json'
        if not os.path.exists(f): continue
        J = json.load(open(f)); names, kinds, succ, idx = build_OF(D)
        assert J['n'] == len(names) and sorted(J['kinds']) == sorted(kinds)
        rho = F(3, 7)
        theirs = damped_values(J['kinds'], [tuple(s) for s in J['succ']], rho)
        mine = damped_values(kinds, succ, rho)
        jn = {nm: i for i, nm in enumerate(J['names'])}
        ok = all(theirs[jn[nm]] == mine[idx[nm]] for nm in names if nm in jn)
        missing = [nm for nm in names if nm not in jn]
        print(f"route's OF_{D}.json: n={J['n']}, values agree by name at rho=3/7: {ok}; names not matched: {len(missing)} (route names S'_d,S''_d as S{D}b/S{D}c)")
    # ue:pgf(d): the four-vertex Min witness
    for rho, want in [(F(2,5), F(8,125)), (F(1,2), F(1,8)), (F(3,5), F(9,50))]:
        assert rho * min(rho/2, rho**2) == want
    assert F(1,8) > (F(8,125) + F(9,50))/2 == F(61,500)
    print('ue:pgf(d): the Min witness values 8/125, 1/8, 9/50 and the chord midpoint 61/500 confirmed (not convex)')
    print('ALL OF CHECKS PASSED')
