#!/usr/bin/env python3
"""Root agent's verification of the round-19 fold-feedback route (batch G), from the statements, in exact arithmetic.

 [1] thm:ff-bmap in the abstract model: for random gains mu_d >= 2, drives t and sign vectors eps (one and two players),
     the strictly switchable levels are exactly {d : eps_d != B(eps,i)_d} with i the first mismatch against the greedy
     itinerary of t, and the new sign vector is B(eps,i); when eps = gamma(t) nothing is switchable.
 [2] the route's games FF1(D), FF2(D), D = 1..4 (FF_games.json; kinds and successors only): stopping by the trap test;
     the cascade coefficients (c_d, a_d, b_d), s, q_0 = 1/2 read off the game by first-passage laws; every gain mu_d = 2;
     the exact all-switches runs from every start (Min optimal at every profile, componentwise minimum over the Min
     strategies), maxrun = D = m-1; at every nondegenerate round the identities psi_0 = 2t-1, psi_d = mu_d eps psi - 1
     (resp. with (.)_+) and the B-map prediction of the switched set hold; the runs recorded by the route for D <= 2 agree.
 [3] prop:ff-blowup: the walk 4,3,5,1,0 of B(1-cube) = (0,1,3,6,7,4,5,2) is a B-map path under exactly 2 of the 48
     relabellings (mismatch levels 0,0,2,1), the other maximal walk 6,3,5,1,0 under 4 (levels 1,0,2,1 and 1,0,1,2);
     the walk 12,19,13,17,8,16,0,7,1,5,4 of B^2 under none of the 3840.
"""
import sys, os, json, itertools, random
from fractions import Fraction as F
M = '/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad'
sys.path.insert(0, f'{M}/root16'); from auso import ba_trace, is_uso, is_acyclic
def say(*a): print(*a, flush=True)
def sign(x): return (x > 0) - (x < 0)

def Bmap(eps, i):
    m = len(eps); out = list(eps); out[i] = -eps[i]; prod = 1
    for d in range(i + 1, m):
        out[d] = -prod; prod *= eps[d]
    return out
def greedy(t, mu):
    psi = [2 * t - 1]
    for d in range(1, len(mu) + 1): psi.append(mu[d - 1] * abs(psi[-1]) - 1)
    return psi
def cascade(t, mu, eps, two):
    psi = [2 * t - 1]
    for d in range(1, len(mu) + 1):
        x = eps[d - 1] * psi[-1]
        psi.append(mu[d - 1] * (max(x, 0) if two else x) - 1)
    return psi

# ---------------------------------------------------------------- [1]
rng = random.Random(19); tested = 0; halts = 0
for _ in range(6000):
    m = rng.randint(1, 6); mu = [F(rng.randint(2, 5)) + F(rng.randint(0, 7), 8) for _ in range(m - 1)]
    t = F(rng.randint(0, 4096), 4096); eps = [rng.choice((1, -1)) for _ in range(m)]; two = rng.random() < 0.5
    psi = cascade(t, mu, eps, two)
    if any(p == 0 for p in psi): continue
    tested += 1
    switch = [d for d in range(m) if eps[d] != sign(psi[d])]           # F_d strictly switchable iff eps_d != sign psi_d
    gam = [sign(p) for p in greedy(t, mu)]
    mism = [d for d in range(m) if eps[d] != gam[d]]
    if not mism: assert not switch; halts += 1; continue
    i = mism[0]; B = Bmap(eps, i)
    assert switch == [d for d in range(m) if eps[d] != B[d]] and min(switch) == i
    assert [eps[d] if d not in switch else -eps[d] for d in range(m)] == B
say(f'[1] B-map: {tested} nondegenerate random (mu, t, eps) cases, m <= 6, one and two players: the switched set is {{d: eps_d != B(eps,i)_d}} with min i, the new signs are B(eps,i); {halts} cases with eps = gamma(t) and nothing switchable')

# ---------------------------------------------------------------- [2] the games
G = json.load(open(f'{M}/r19-fold-feedback/FF_games.json'))
def solve(Mx, rhs):
    n = len(Mx); T = [list(Mx[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if T[r][c] != 0); T[c], T[p] = T[p], T[c]
        pv = T[c][c]; T[c] = [x / pv for x in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [T[r][j] - f * T[c][j] for j in range(n + 1)]
    return [T[i][n] for i in range(n)]
for name, g in G.items():
    kinds, succ, idx = g['kinds'], g['succ'], g['idx']; n = len(kinds); T0, T1 = idx['T0'], idx['T1']; assert {T0, T1} == {n, n + 1}
    D = int(name.split('_D')[1]); two = name.startswith('FF2'); m = D + 1
    Fs = [idx[f'F{d}'] for d in range(m)]; Xs = [idx[f'X{d}'] for d in range(m)]; Ys = [idx[f'Y{d}'] for d in range(m)]
    Zs = [idx[f'H{d}'] if f'H{d}' in idx else idx[f'G{d}'] for d in range(D)]; u = idx['u0']
    assert all(kinds[f] == 'max' for f in Fs) and all(succ[f] == [Xs[d], Ys[d]] or succ[f] == [Ys[d], Xs[d]] for d, f in enumerate(Fs))
    assert all(kinds[z] == ('min' if two else 'avg') for z in Zs) and all(sorted(succ[z]) == sorted([Xs[d], Ys[d]]) for d, z in enumerate(Zs))
    mins = [v for v in range(n) if kinds[v] == 'min']; assert (len(mins) == D) if two else (not mins)
    # stopping: greatest trap
    T = set(range(n))
    while True:
        drop = {v for v in T if (kinds[v] == 'avg' and any(w not in T for w in succ[v])) or (kinds[v] != 'avg' and all(w not in T for w in succ[v]))}
        if not drop: break
        T -= drop
    assert not T and g['stopping']
    # cascade coefficients by first-passage laws (targets: the F's, the Z's, u, the sinks)
    targets = set(Fs) | set(Zs) | {u, T0, T1}
    def law(v, avoid_start=True, _memo={}):
        key = (name, v)
        if key in _memo: return _memo[key]
        out = {}
        def rec(x, p, depth):
            assert depth < 200
            if x in targets: out[x] = out.get(x, F(0)) + p; return
            assert kinds[x] == 'avg', (name, x)
            for w in succ[x]: rec(w, p / 2, depth + 1)
        for w in succ[v]: rec(w, F(1, 2), 0)        # v itself is an average vertex: its law is the mean of its successors' laws
        _memo[key] = out; return out
    c = [None] * m; a = [None] * m; b = [None] * m
    lx0 = law(Xs[0]); ly0 = law(Ys[0])
    assert set(lx0) <= {u, T0, T1} and set(ly0) <= {T0, T1}
    s_seed = lx0.get(u, F(0)); p0 = lx0.get(T1, F(0)); q0 = ly0.get(T1, F(0)); assert s_seed > 0 and q0 == F(1, 2) and p0 - q0 == -s_seed / 2
    e = [s_seed / 2]; mu = []
    for d in range(1, m):
        lx, ly = law(Xs[d]), law(Ys[d])
        assert set(lx) <= {Fs[d - 1], T0, T1} and set(ly) <= {Zs[d - 1], T0, T1}
        c[d] = lx.get(Fs[d - 1], F(0)); assert ly.get(Zs[d - 1], F(0)) == c[d] and c[d] > 0
        a[d] = lx.get(T1, F(0)); b[d] = ly.get(T1, F(0)); e.append(b[d] - a[d]); assert e[-1] > 0
        mu.append((c[d] / 2 if not two else c[d]) * e[d - 1] / e[d])
    assert all(x == 2 for x in mu), (name, mu)
    # values under (sigma, tau)
    def values(sig, tau):
        act = {}
        for d, f in enumerate(Fs): act[f] = Xs[d] if sig[d] == 1 else Ys[d]
        for j, z in enumerate(mins): act[z] = succ[z][tau[j]]
        Mx = [[F(int(i == j)) for j in range(n)] for i in range(n)]; r = [F(0)] * n
        for v in range(n):
            ws = [act[v]] if v in act else succ[v]; p = F(1, len(ws))
            for w in ws:
                if w == T1: r[v] += p
                elif w == T0: pass
                else: Mx[v][w] -= p
        return solve(Mx, r)
    taus = list(itertools.product((0, 1), repeat=len(mins)))
    def val(sig):
        vs = [values(sig, tau) for tau in taus]
        return [min(v[i] for v in vs) for i in range(n)]
    def step(sig):
        x = val(sig); sw = []
        for d, f in enumerate(Fs):
            cur, oth = (Xs[d], Ys[d]) if sig[d] == 1 else (Ys[d], Xs[d])
            if x[oth] > x[cur]: sw.append(d)
        return x, sw
    maxrun = 0; rounds = 0; degenerate = 0; recorded = 0
    for start in itertools.product((1, -1), repeat=m):
        sig = list(start); run = [tuple(sig)]; drives = []; switched = []
        while True:
            x, sw = step(sig); drives.append(x[u])
            t = x[u]; psi = [(x[Xs[d]] - x[Ys[d]]) / e[d] for d in range(m)]
            assert psi[0] == 2 * t - 1
            for d in range(1, m):
                y = sig[d - 1] * psi[d - 1]; assert psi[d] == mu[d - 1] * (max(y, 0) if two else y) - 1
            if any(p == 0 for p in psi): degenerate += 1
            else:
                gam = [sign(p) for p in greedy(t, mu)]; mism = [d for d in range(m) if sig[d] != gam[d]]
                if not mism: assert not sw
                else:
                    B = Bmap(sig, mism[0]); assert sw == [d for d in range(m) if sig[d] != B[d]], (name, sig, sw, B)
                rounds += 1
            if not sw: break
            switched.append(sw)
            for d in sw: sig[d] = -sig[d]
            run.append(tuple(sig))
        maxrun = max(maxrun, len(run) - 1)
        if D <= 2:      # compare with the route's recorded runs: start as 0/1 bits (1 = X), switched as F indices, drives
            # the route's encoding: start bit 0 = first successor (X), switched = indices of the F vertices, drives as strings
            rec = next(r for r in g['runs'] if [0 if b == 1 else 1 for b in start] == r['start'])
            assert rec['length'] == len(run) - 1, (name, start, rec['length'], len(run) - 1)
            assert [F(dv) for dv in rec['drives']] == drives, (name, start, rec['drives'], [str(x) for x in drives])
            assert [[Fs[d] for d in sw] for sw in switched] == rec['switched'], (name, start, rec['switched'], switched)
            recorded += 1
    assert maxrun == D == g['maxrun']
    say(f'[2] {name}: n={n}, m={m}, {"two players" if two else "one player"}, stopping; s={s_seed}, q_0=1/2, c_d={[str(x) for x in c[1:]]}, e_d={[str(x) for x in e]}, all gains 2; maxrun over {2**m} starts = {maxrun} = m-1; B-map identity at {rounds} nondegenerate rounds ({degenerate} degenerate skipped); route-recorded runs matched: {recorded}')

# ---------------------------------------------------------------- [3] the blow-up walks as B-map paths
def bmap_path_relabellings(walk, m):
    hits = []
    for perm in itertools.permutations(range(m)):
        for cmask in range(1 << m):
            epss = [[1 if (((v >> perm[d]) & 1) ^ ((cmask >> d) & 1)) else -1 for d in range(m)] for v in walk]
            levels = []; ok = True
            for k in range(len(walk) - 1):
                e1, e2 = epss[k], epss[k + 1]; mism = [d for d in range(m) if e1[d] != e2[d]]
                if not mism or e2 != Bmap(e1, mism[0]): ok = False; break
                levels.append(mism[0])
            if ok:
                # cor:ff-level0's constraint: the values eps_0 takes AFTER the level-0 rounds are nondecreasing (sign(t_k - 1/2), t_k nondecreasing)
                set0 = [epss[k + 1][0] for k in range(len(walk) - 1) if levels[k] == 0]
                hits.append((perm, cmask, levels, all(set0[j] <= set0[j + 1] for j in range(len(set0) - 1))))
    return hits
B1 = (0, 1, 3, 6, 7, 4, 5, 2); assert is_uso(B1, 3) and is_acyclic(B1, 3)
w4 = ba_trace(B1, 4); w6 = ba_trace(B1, 6); assert w4 == [4, 3, 5, 1, 0] and w6 == [6, 3, 5, 1, 0]
h4 = bmap_path_relabellings(w4, 3); h6 = bmap_path_relabellings(w6, 3)
assert len(h4) == 2 and all(h[2] == [0, 0, 2, 1] for h in h4) and len(h6) == 4 and sorted(h[2] for h in h6) == [[1, 0, 1, 2], [1, 0, 1, 2], [1, 0, 2, 1], [1, 0, 2, 1]]
assert sorted(h[3] for h in h4) == [False, True]
say(f'[3] B(1-cube): the walk 4,3,5,1,0 is a B-map path under {len(h4)} of 48 relabellings, mismatch levels {h4[0][2]}, exactly one of the two compatible with a nondecreasing drive at level 0; the walk 6,3,5,1,0 under {len(h6)}, levels {sorted(set(tuple(h[2]) for h in h6))}')
B2 = (7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18)
assert is_uso(B2, 5) and is_acyclic(B2, 5) and ba_trace(B2, 12) == [12, 19, 13, 17, 8, 16, 0, 7, 1, 5, 4]
h2 = bmap_path_relabellings(ba_trace(B2, 12), 5); assert not h2
say('[3] B^2: the walk 12,19,13,17,8,16,0,7,1,5,4 is a B-map path under none of the 3840 relabellings')
say('FOLD-FEEDBACK ROUTE: [1]-[3] reproduced from the statements')
