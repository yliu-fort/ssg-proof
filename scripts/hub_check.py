"""Step 3: the hub family W(k,r): exact values, class audit, and the
one-vertex boundary reduction run against brute force."""
from fractions import Fraction as F
from itertools import product
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bv2 import PGame, freeze
from hub import (build_W, cycles, kacyclic, maxreach_sccs, escape_exponent_sigma,
                 solve_acyclic, boundary_value, R_of, cycles_exist_through)

def audit(g, u, brute=True):
    n = g.n
    cyc = cycles(g)
    hub_ok = all(u in c for c in cyc)
    rep = {}
    rep['N'] = g.N
    rep['a'] = len(g.avgv)
    rep['|Vmax|'] = len(g.maxv); rep['|Vmin|'] = len(g.minv)
    rep['stopping'] = g.is_stopping()
    rep['#cycles'] = len(cyc)
    rep['every cycle meets u'] = hub_ok
    rep['max-acyclic'] = kacyclic(g, 'max')
    rep['min-acyclic'] = kacyclic(g, 'min')
    rep['avg-acyclic'] = kacyclic(g, 'avg')
    rep['H(G) SCC sizes'] = sorted((len(c) for c in maxreach_sccs(g)), reverse=True)
    if brute:
        w = g.value()
        opt = []
        for sigma in g.strategies('max'):
            if g.val_sigma(sigma)[:n] == w[:n]:
                opt.append(sigma)
        rep['d(G)'] = min(escape_exponent_sigma(g, s) for s in opt)
        rep['#optimal sigma'] = len(opt)
        return rep, w
    return rep, None

for (k, r) in [(1,1),(1,3),(2,3),(2,5),(3,4),(3,6)]:
    g, u = build_W(k, r, consts=[F(1,2) + F((-1)**i * (i+1), 32) for i in range(2*k)])
    rep, w = audit(g, u)
    print("W(k=%d,r=%d)  u=%d" % (k, r, u))
    for kk, vv in rep.items(): print("    %-22s %s" % (kk, vv))
    print("    val(u) = %s   val(v0=u) >= 1/2 : %s" % (w[u], w[u] >= F(1,2)))
    # ---- the frozen game is acyclic, for every theta -------------------
    gu = freeze(g, u, F(1,3))
    assert not cycles(gu), "frozen game must be acyclic"
    # ---- run the new algorithm -----------------------------------------
    tr = []
    got = boundary_value(g, u, solve_acyclic, trace=tr)
    assert got == w[u], (got, w[u])
    # full value vector from lem:bv-subst
    full = solve_acyclic(freeze(g, u, got))
    assert full[:g.n] == w[:g.n], "substitution failed"
    print("    boundary reduction: %d bisection calls, val(u)=%s  MATCHES brute force"
          % (len(tr), got))
    print("    full value vector reproduced from G[u:=val(u)] : OK")
