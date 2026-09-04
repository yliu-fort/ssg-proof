"""My own implementation of the RATIO CALCULUS, written from the STATEMENT of
def:np-ratio (round 13, route nonlinear-perron) and not from that route's code.

Entries in [0, +oo], reading   w*(x) <= R(x,y) * w*(y).
R_0 = +oo.  R_{k+1}(x,y) = min of R_k(x,y) with
  0            if x in Z_0
  1            if y in Z_1
  1            if x = y
  (down)  ag^-_y over y's successors: MIN at Vmax, MAX at Vmin, HARMONIC mean
          at Vavg                                             (y a non-sink)
  (up)    ag^+_x over x's successors: MAX at Vmax, MIN at Vmin, ARITHMETIC mean
          at Vavg                                             (x a non-sink)
  composites for non-sinks of the same type:
     two Max:  min_j max_i R(x^i, y^j),  max_i min_j R(x^i, y^j)
     two Min:  min_i max_j R(x^i, y^j),  max_j min_i R(x^i, y^j)
     two Avg:  max_i R(x^i, y^{pi(i)}) for either bijection pi

Exact rationals with an explicit +oo sentinel.
"""
from fractions import Fraction as F

INF = None          # sentinel for +infinity


def _le(a, b):
    if a is INF:
        return b is INF
    if b is INF:
        return True
    return a <= b


def _min(*xs):
    best = INF
    for x in xs:
        if x is INF:
            continue
        if best is INF or x < best:
            best = x
    return best


def _max(*xs):
    if any(x is INF for x in xs):
        return INF
    return max(xs)


def _mean(a, b):
    if a is INF or b is INF:
        return INF
    return (a + b) / 2


def _harm(a, b):
    """2/(1/a + 1/b), with 1/INF = 0 and the convention harm(0,t) = 0."""
    if a is INF and b is INF:
        return INF
    if a == 0 or b == 0:
        return F(0)
    if a is INF:
        return 2 * b
    if b is INF:
        return 2 * a
    return 2 / (1 / a + 1 / b)


def ratio_rounds(g, w, K):
    """Return [R_1, ..., R_K] as lists of lists over 0..N-1."""
    N = g.N
    Z0 = {v for v in range(N) if w[v] == 0}
    Z1 = {v for v in range(N) if w[v] == 1}
    R = [[INF] * N for _ in range(N)]
    out = []
    for _ in range(K):
        new = [[INF] * N for _ in range(N)]
        for x in range(N):
            for y in range(N):
                cands = [R[x][y]]
                if x in Z0:
                    cands.append(F(0))
                if y in Z1:
                    cands.append(F(1))
                if x == y:
                    cands.append(F(1))
                if y < g.n:                                   # (down)
                    y0, y1 = g.succ[y]
                    a, b = R[x][y0], R[x][y1]
                    k = g.kinds[y]
                    cands.append(_min(a, b) if k == 'max' else
                                 (_max(a, b) if k == 'min' else _harm(a, b)))
                if x < g.n:                                   # (up)
                    x0, x1 = g.succ[x]
                    a, b = R[x0][y], R[x1][y]
                    k = g.kinds[x]
                    cands.append(_max(a, b) if k == 'max' else
                                 (_min(a, b) if k == 'min' else _mean(a, b)))
                if x < g.n and y < g.n and g.kinds[x] == g.kinds[y]:
                    x0, x1 = g.succ[x]
                    y0, y1 = g.succ[y]
                    M = [[R[x0][y0], R[x0][y1]], [R[x1][y0], R[x1][y1]]]
                    k = g.kinds[x]
                    if k == 'max':
                        cands.append(_min(_max(M[0][0], M[1][0]),
                                          _max(M[0][1], M[1][1])))
                        cands.append(_max(_min(M[0][0], M[0][1]),
                                          _min(M[1][0], M[1][1])))
                    elif k == 'min':
                        cands.append(_min(_max(M[0][0], M[0][1]),
                                          _max(M[1][0], M[1][1])))
                        cands.append(_max(_min(M[0][0], M[1][0]),
                                          _min(M[0][1], M[1][1])))
                    else:
                        cands.append(_max(M[0][0], M[1][1]))
                        cands.append(_max(M[0][1], M[1][0]))
                new[x][y] = _min(*cands)
        R = new
        out.append([r[:] for r in R])
    return out


def sound(g, R, w):
    """w*(x) <= R(x,y) w*(y) at every entry."""
    bad = 0
    for x in range(g.N):
        for y in range(g.N):
            r = R[x][y]
            if r is INF:
                continue
            if w[x] > r * w[y]:
                bad += 1
    return bad
