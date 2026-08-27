"""Step 4: does the transport LP of sec:transport supply the offset delta
that the average step of the boundary-value recursion needs?

For u in Vavg with successors u0,u1, G_u := G[u:=1/2], y := val_{G_u}:
   val_G(u) >= 1/2   iff   y(u0) + y(u1) >= 1                (cor:bv-threshold)
and delta is CORRECT iff
   [ y(u0) >= 1/2+delta  and  y(u1) >= 1/2-delta ]  <->  y(u0)+y(u1) >= 1,
i.e. iff  1/2 - y(u1) <= delta <= y(u0) - 1/2   whenever that interval is
nonempty (when it is empty every delta is correct).
"""
from fractions import Fraction as F
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bv2 import PGame, freeze
from lp_exact import check_feasible
import lp2


def q_rows(g, L=None, U=None):
    """Rows of Q(g;L,U) for a payoff game.  Coefficients ACCUMULATED."""
    N = g.N
    rows = []
    def add(pairs, sense, rhs):
        dd = {}
        for k, v in pairs:                       # LIST, never a dict literal:
            dd[k] = dd.get(k, F(0)) + v          # accumulate (rule 6-i)
        dd = {k: v for k, v in dd.items() if v != 0}
        rows.append((dd, sense, F(rhs)))
    for j in range(g.m):
        add([(g.n + j, F(1))], '=', g.pay[j])
    for v in range(g.n):
        a, b = g.succ[v]
        k = g.kinds[v]
        if k == 'max':
            add([(v, F(1)), (a, F(-1))], '>=', 0)
            add([(v, F(1)), (b, F(-1))], '>=', 0)
        elif k == 'min':
            add([(v, F(1)), (a, F(-1))], '<=', 0)
            add([(v, F(1)), (b, F(-1))], '<=', 0)
        else:
            add([(v, F(1)), (a, F(-1, 2)), (b, F(-1, 2))], '=', 0)
    for v in range(N):
        add([(v, F(1))], '<=', 1 if U is None else U[v])
        if L is not None and L[v] != 0:
            add([(v, F(1))], '>=', L[v])
    return rows


def lp_bounds(g, targets, L=None, U=None, check=None):
    """(min, max) of x(t) over Q(g;L,U) for each t in targets."""
    rows = q_rows(g, L, U)
    if check is not None:
        check_feasible(rows, check, "Q feasibility of the true value vector")
    out = {}
    for t in targets:
        lo, _ = lp2.solve(g.N, rows, {t: F(1)}, maximise=False)
        hi, _ = lp2.solve(g.N, rows, {t: F(1)}, maximise=True)
        lp2.certify(g.N, rows, {t: F(1)}, lo, maximise=False)
        lp2.certify(g.N, rows, {t: F(1)}, hi, maximise=True)
        out[t] = (lo, hi)
    return out


def delta_data(g, u, L=None, U=None):
    """Everything the question needs at an average vertex u."""
    assert g.kinds[u] == 'avg'
    gu = freeze(g, u, F(1, 2))
    y = gu.value()
    u0, u1 = g.succ[u]
    bounds = lp_bounds(gu, [u0, u1], L, U, check=y)
    (m0, M0), (m1, M1) = bounds[u0], bounds[u1]
    ans = (y[u0] + y[u1] >= 1)
    lo_ok, hi_ok = F(1, 2) - y[u1], y[u0] - F(1, 2)      # correct-delta window
    return dict(y0=y[u0], y1=y[u1], answer=ans, window=(lo_ok, hi_ok),
                m0=m0, M0=M0, m1=m1, M1=M1, gu=gu, y=y)


def correct(d, delta):
    """Is this delta a correct split for this instance?"""
    conj = (d['y0'] >= F(1, 2) + delta) and (d['y1'] >= F(1, 2) - delta)
    return conj == d['answer']
