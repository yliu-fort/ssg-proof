"""The own-successor test for the HYBRID.

At v in Vmax, Delta_k(v, v^(i)) <= 0 forces val(v) = val(v^(i)) and so proves
v^(i) optimal; dually Delta_k(v^(i), v) <= 0 at v in Vmin.  Non-strict, by
rem:own-successor.  This is the strongest decision test the paper's machinery
supports, so a stopping SSG on which it never fires at any controlled vertex
would be the sharpest refutation available -- and its absence, with a
polynomial round bound, would put SSG-Value in P.
"""
from fractions import Fraction as F
from mycore import (G, wstar, Z01, slack_step, minplus_close, clamp, ones,
                    check_sound, transport_sep, distinguishing)
from zseed import seeds


def hybrid_rounds(g, w, K=25, seeded=True, sink_only=False):
    """Returns, per controlled distinguishing vertex, the first round at which
    the own-successor test fires (or None)."""
    N = g.N
    Z0, Z1 = Z01(g, w)
    L, U, _, _ = seeds(g, w) if seeded else (None, None, None, None)
    D = ones(N)
    if sink_only:
        pairs = []
        for x in range(N):
            pairs += [(g.T0, x), (g.T1, x), (x, g.T0), (x, g.T1)]
    else:
        pairs = [(p, q) for p in range(N) for q in range(N) if p != q]
    dist = distinguishing(g, w)
    first = {v: None for v in dist}
    for k in range(K):
        A = [[clamp(t) for t in r] for r in minplus_close(slack_step(g, D, Z0, Z1), N)]
        M = [[min(D[i][j], A[i][j]) for j in range(N)] for i in range(N)]
        for (p, q), val in transport_sep(g, pairs, D=M, L=L, U=U).items():
            if val is not None:
                M[q][p] = min(M[q][p], val)
        M = [[clamp(t) for t in r] for r in minplus_close(M, N)]
        check_sound(g, M, w, f'r{k+1}')
        D = M
        for v in dist:
            if first[v] is not None:
                continue
            a, b = g.succ[v]
            if g.kinds[v] == 'max':
                # (i) Delta(v,u) <= 0 forces val(v) = val(u), so u is optimal;
                # (ii) Delta(u,v) < 0 proves val(u) < val(v), so u is NOT.
                if (D[v][a] <= 0 or D[v][b] <= 0
                        or D[a][v] < 0 or D[b][v] < 0):
                    first[v] = k + 1
            else:
                if (D[a][v] <= 0 or D[b][v] <= 0
                        or D[v][a] < 0 or D[v][b] < 0):
                    first[v] = k + 1
        if all(first[v] is not None for v in dist):
            break
    return first, dist
