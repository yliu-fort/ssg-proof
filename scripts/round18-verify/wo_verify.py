#!/usr/bin/env python3
"""Root-agent verification of the round-18 weakest-oracle route: wo:free-pair (the sink-adjacent blocks H, M, L of a
reduced stopping game and the free strict pair), wo:free-blind (FB(L)+-, two games differing in one edge with the same
free layer and opposite decisions at the Max vertex), wo:gate-lipschitz's amplifier RUIN(K) (values and slopes), and
wo:any-set's copies. Everything rebuilt from the statements; exact arithmetic."""
import sys, random, itertools
from fractions import Fraction as F
import os as _os; sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'harness')); sys.path.insert(0, '/tmp/claude-1000/-data-ssg-proof/296b18c1-9dc5-4a0b-94cf-9bde3946ecfe/scratchpad/root16')
from mycore import G, is_stopping, wstar, T_op

def random_game(n, rng):
    kinds = [rng.choice(['max', 'min', 'avg', 'avg']) for _ in range(n)]
    succ = [(rng.randrange(n+2), rng.randrange(n+2)) for _ in range(n)]
    return G(kinds, succ)

def reduce(g, w):
    """delete {w=0} and {w=1}, redirect edges into them to t0 / t1 (the reduction of wo:free-pair / thm:top)."""
    keep = [v for v in range(g.n) if 0 < w[v] < 1]
    idx = {v: i for i, v in enumerate(keep)}; n2 = len(keep)
    def m(u):
        if u == g.T1 or (u < g.n and w[u] == 1): return n2+1
        if u == g.T0 or (u < g.n and w[u] == 0): return n2
        return idx[u]
    return G([g.kinds[v] for v in keep], [(m(a), m(b)) for v in keep for (a, b) in [g.succ[v]]]), keep

def blocks(g):
    H, M, L = [], [], []
    for v in range(g.n):
        if g.kinds[v] != 'avg': continue
        a, b = g.succ[v]; s = {a, b}
        if s == {g.T0, g.T1}: M.append(v)
        elif g.T1 in s and not (a == g.T1 and b == g.T1) and g.T0 not in s: H.append(v)
        elif g.T0 in s and not (a == g.T0 and b == g.T0) and g.T1 not in s: L.append(v)
    return H, M, L

def free_pair(g):
    H, M, L = blocks(g)
    if H and (L or M): return (H[0], (L+M)[0])
    if not H and L and M: return (M[0], L[0])
    if not H and not L: return 'all equal'
    return None   # (H nonempty, L u M empty) or (L nonempty, H u M empty): excluded by (b)

def check_free_pair(trials, seed):
    rng = random.Random(seed); stats = dict(reduced=0, pair=0, alleq=0, Hn=0, Mn=0, Ln=0)
    for _ in range(trials):
        g = random_game(rng.randrange(3, 11), rng)
        if not is_stopping(g): continue
        w = wstar(g)
        r, keep = reduce(g, w)
        if r.n == 0: continue
        assert is_stopping(r)
        w2 = wstar(r)
        assert all(w2[i] == w[keep[i]] for i in range(r.n)) and all(0 < x < 1 for x in w2[:r.n])
        stats['reduced'] += 1
        H, M, L = blocks(r)
        assert all(w2[v] > F(1,2) for v in H) and all(w2[v] == F(1,2) for v in M) and all(w2[v] < F(1,2) for v in L)
        assert (H or M) and (L or M), 'clause (b) violated'
        if not H and not L: assert all(x == F(1,2) for x in w2[:r.n]), 'clause (c) violated'
        stats['Hn'] += len(H); stats['Mn'] += len(M); stats['Ln'] += len(L)
        fp = free_pair(r)
        assert fp is not None
        if fp == 'all equal': stats['alleq'] += 1; assert all(x == F(1,2) for x in w2[:r.n])
        else:
            x, y = fp; assert w2[x] > w2[y]; stats['pair'] += 1
            # the bracket (T^N 1_{t1}, T^N (1 - 1_{t0})) decides it
            def Tmine(z):
                out = list(z)
                for v in range(r.n):
                    a, b = r.succ[v]
                    out[v] = max(z[a], z[b]) if r.kinds[v] == 'max' else min(z[a], z[b]) if r.kinds[v] == 'min' else (z[a] + z[b]) / 2
                return out
            lo = [F(0)]*r.n + [F(0), F(1)]; hi = [F(1)]*r.n + [F(0), F(1)]
            for _ in range(r.N):
                lo2, hi2 = Tmine(lo), Tmine(hi)
                assert all(lo2[v] >= lo[v] for v in range(r.n)) and all(hi2[v] <= hi[v] for v in range(r.n))
                lo, hi = lo2, hi2
            assert lo[x] > hi[y], (lo[x], hi[y])
    return stats

def build_FB(L, sign):
    """FB(L)+-: chains p_1..p_L (bits 1 0^{L-2} 1) and q_1..q_L (bits 0 1^{L-1}), m->(t0,t1), B->(m,m),
    A->(p_1,m) in FB+ and A->(q_1,m) in FB-, v in Vmax with v->(A,B)."""
    names = []; kinds = {}; S = {}
    def add(nm, k, s): names.append(nm); kinds[nm] = k; S[nm] = s
    pb = [1] + [0]*(L-2) + [1]; qb = [0] + [1]*(L-1)
    for tag, bits in (('p', pb), ('q', qb)):
        for j in range(1, L+1):
            nxt = f'{tag}{j+1}' if j < L else 't0'
            add(f'{tag}{j}', 'avg', ('t1' if bits[j-1] else 't0', nxt))
    add('m', 'avg', ('t0', 't1')); add('B', 'avg', ('m', 'm'))
    add('A', 'avg', ('p1' if sign > 0 else 'q1', 'm')); add('v', 'max', ('A', 'B'))
    n = len(names); ix = {nm: i for i, nm in enumerate(names)}; ix['t0'] = n; ix['t1'] = n+1
    return G([kinds[nm] for nm in names], [(ix[S[nm][0]], ix[S[nm][1]]) for nm in names]), ix

def check_FB(L):
    gp, ip = build_FB(L, +1); gm, im = build_FB(L, -1)
    assert gp.kinds == gm.kinds and sum(a != b for a, b in zip(gp.succ, gm.succ)) == 1
    wp, wm = wstar(gp), wstar(gm)
    for g, w in ((gp, wp), (gm, wm)):
        assert is_stopping(g) and all(0 < x < 1 for x in w[:g.n])
    assert blocks(gp) == blocks(gm) and free_pair(gp) == free_pair(gm)
    H, M, Lb = blocks(gp); assert (len(H), len(M), len(Lb)) == (L-1, 3, L-1)
    v = ip['v']; A, B = gp.succ[v]
    assert wp[A] - wp[B] == F(1, 2**(L+1)) and wm[A] - wm[B] == -F(1, 2**(L+1))
    assert sorted(wp[:gp.n]) != sorted(wm[:gm.n])
    return gp.n

def ruin(K, theta_bits):
    """RUIN(K) with every call replaced by a dyadic chain of value theta (bits), t1-exit i+1, t0-exit i-1."""
    names = []; kinds = {}; S = {}
    def add(nm, k, s): names.append(nm); kinds[nm] = k; S[nm] = s
    for i in range(1, K+1):
        up = f'c{i+1}_1' if i < K else 't1'; dn = f'c{i-1}_1' if i > 1 else 't0'
        for j, b in enumerate(theta_bits, start=1):
            nxt = f'c{i}_{j+1}' if j < len(theta_bits) else dn
            add(f'c{i}_{j}', 'avg', (up if b else dn, nxt))
    n = len(names); ix = {nm: i for i, nm in enumerate(names)}; ix['t0'] = n; ix['t1'] = n+1
    g = G([kinds[nm] for nm in names], [(ix[S[nm][0]], ix[S[nm][1]]) for nm in names])
    assert is_stopping(g)
    w = wstar(g); theta = sum(F(b, 2**j) for j, b in enumerate(theta_bits, start=1))
    r = (1 - theta) / theta
    for i in range(1, K+1):
        want = F(i, K+1) if r == 1 else (1 - r**i) / (1 - r**(K+1))
        assert w[ix[f'c{i}_1']] == want, (K, i)
    return w, ix, theta

if __name__ == '__main__':
    st = check_free_pair(6000, 18)
    print('wo:free-pair on random stopping games:', st, '-- (a),(b),(c),(d),(e) hold in every case')
    for L in range(3, 10):
        n = check_FB(L)
        print(f'FB({L})+-: {n} non-sinks (2L+4={2*L+4}), one differing edge, same blocks (L-1,3,L-1), same free pair, gaps +-2^-(L+1), non-isomorphic')
    for K in (1, 2, 3, 5, 7, 9, 11):
        w0, ix0, t0 = ruin(K, [1]);  wp, ixp, tp = ruin(K, [1, 0,0,0,0,0,0,0,0,0, 1])   # theta = 1/2 and 1/2 + 2^-11
        i = (K+1)//2
        slope = (wp[ixp[f'c{i}_1']] - w0[ix0[f'c{i}_1']]) / (tp - t0)
        exact = F(2*i*(K+1-i), K+1)
        print(f'RUIN({K}): ruin formula exact; start {i}: secant slope {float(slope):.4f} vs derivative 2i(K+1-i)/(K+1) = {float(exact):.4f}; bound (4/3)(K+3) = {4*(K+3)/3:.3f}')
    # wo:any-set copies: P_i -> (t1,p), Q -> (t1,q) tied copies inside H
    rng = random.Random(5); done = 0
    while done < 200:
        g = random_game(rng.randrange(4, 10), rng)
        if not is_stopping(g): continue
        w = wstar(g); r, keep = reduce(g, w)
        if r.n < 2: continue
        p, q = rng.sample(range(r.n), 2)
        kinds = list(r.kinds) + ['avg']*3; succ = [(r.T1+3 if a == r.T1 else r.T0+3 if a == r.T0 else a, r.T1+3 if b == r.T1 else r.T0+3 if b == r.T0 else b) for a, b in r.succ]
        n2 = r.n + 3; succ += [(n2+1, p), (n2+1, p), (n2+1, q)]
        g2 = G(kinds, succ); assert is_stopping(g2); w2 = wstar(g2)
        assert w2[:r.n] == wstar(r)[:r.n]
        assert w2[r.n] == w2[r.n+1] == (1 + w2[p])/2 and w2[r.n+2] == (1 + w2[q])/2
        H, M, L = blocks(g2); assert {r.n, r.n+1, r.n+2} <= set(H)
        done += 1
    print('wo:any-set: 200 reductions -- copies tied, inside H, old values unchanged, stopping')
    print('ALL WO CHECKS PASSED')
