"""Step 2: random-instance verification of thm:bv-affine, thm:bv-lfp,
thm:bv-contract(a),(c),(d), cor:bv-threshold and lem:bv-subst."""
from fractions import Fraction as F
from itertools import product
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bv2 import PGame, freeze, ssg_to_pgame

def rnd_ssg(n, rng, pmax=.3, pmin=.3):
    kinds, succ = [], []
    for v in range(n):
        r = rng.random()
        kinds.append('max' if r < pmax else 'min' if r < pmax+pmin else 'avg')
        succ.append((rng.randrange(n+2), rng.randrange(n+2)))
    return ssg_to_pgame(kinds, succ)

def R(g, u, theta):
    y = freeze(g, u, theta).value()
    a, b = g.succ[u]
    k = g.kinds[u]
    return max(y[a], y[b]) if k == 'max' else min(y[a], y[b]) if k == 'min' else (y[a]+y[b])/2

rng = random.Random(20260827)
THETAS = [F(0), F(1,7), F(1,4), F(1,3), F(1,2), F(5,8), F(3,4), F(1)]

n_aff = n_lfp = n_lfp_ns = n_ctr = n_thr = n_sub = 0
games = 0
stopping_games = 0
while games < 260:
    n = rng.randrange(3, 7)
    g = rnd_ssg(n, rng)
    games += 1
    st = g.is_stopping()
    if st: stopping_games += 1
    w = g.value()
    # --- thm:bv-affine ---------------------------------------------------
    for u in range(n):
        for _ in range(2):
            sigma = [rng.randrange(2) for _ in range(n)]
            tau   = [rng.randrange(2) for _ in range(n)]
            h  = g.hitting(sigma, tau, u)
            al = g.alpha(sigma, tau, u, None)
            for th in THETAS:
                gu = freeze(g, u, th)
                x = gu.evaluate(gu.chain(sigma, tau))
                for v in range(n):
                    assert x[v] == al[v] + h[v]*th, (u,v,th,x[v],al[v],h[v])
                    n_aff += 1
    # --- thm:bv-lfp: val(u) is a fixed point of R_u, and least ----------
    for u in range(n):
        assert R(g, u, w[u]) == w[u], ("not fixed", u, w[u], R(g,u,w[u]))
        n_lfp += 1
        if not st: n_lfp_ns += 1
        # no fixed point strictly below w[u], on a fine grid
        den = 1 << (len(g.avgv) + 3)
        num = 0
        while F(num, den) < w[u]:
            th = F(num, den)
            assert R(g, u, th) != th, ("smaller fixed point", u, th, w[u])
            num += 1
    # --- thm:bv-contract(c),(d) and cor:bv-threshold, stopping only ------
    if st:
        for u in range(n):
            for c in THETAS:
                r = R(g, u, c)
                assert (w[u] >= c) == (r >= c), ("sign test", u, c, w[u], r)
                assert (w[u] <= c) == (r <= c)
                n_ctr += 1
            # cor:bv-threshold at 1/2
            y = freeze(g, u, F(1,2)).value()
            a, b = g.succ[u]
            k = g.kinds[u]
            pred = (y[a] >= F(1,2) or y[b] >= F(1,2)) if k == 'max' else \
                   (y[a] >= F(1,2) and y[b] >= F(1,2)) if k == 'min' else \
                   (y[a] + y[b] >= 1)
            assert pred == (w[u] >= F(1,2)), ("threshold", u, w[u], y[a], y[b])
            n_thr += 1
            # lem:bv-subst
            assert freeze(g, u, w[u]).value()[:n] == w[:n], ("subst", u)
            n_sub += 1

print("games", games, " stopping", stopping_games, " non-stopping", games-stopping_games)
print("bv-affine instances     :", n_aff)
print("bv-lfp (fixed+least)    :", n_lfp, " of which on non-stopping games:", n_lfp_ns)
print("bv-contract sign tests  :", n_ctr)
print("bv-threshold instances  :", n_thr)
print("bv-subst instances      :", n_sub)
print("OK step 2")
