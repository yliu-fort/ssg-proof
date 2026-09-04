"""The Mobius family of calculi.

R^beta is the ratio calculus of def:ratio applied to the affine rescaling
G^beta of the game, in which the sinks pay beta and 1+beta.  By
lem:gen-comparison that game has value w* + beta, so the reading is

        w*(x) + beta  <=  R^beta(x,y) . (w*(y) + beta).

beta = 0 is def:ratio; beta -> oo is def:slack, since
(c+beta)/(t+beta) = 1 + (c-t)/beta + O(beta^{-2}) and the harmonic and
arithmetic means agree to first order.

Bases for beta > 0 (all values now lie in [beta, 1+beta], so nothing is 0):
    (1+beta)/beta   always            [the global cap, replacing R_0 = +oo]
    1               if x in Z_0       (value(x) = beta <= value(y))
    1               if y in Z_1       (value(y) = 1+beta >= value(x))
    beta/(1+beta)   if both
    1               if x = y
"""
from fractions import Fraction as F
from ratio import INF, _min, _max, _mean, _harm


def ratio_rounds_beta(g, w, K, beta):
    """[R^beta_1, ..., R^beta_K].  beta = 0 falls back to def:ratio exactly."""
    N = g.N
    Z0 = {v for v in range(N) if w[v] == 0}
    Z1 = {v for v in range(N) if w[v] == 1}
    cap = INF if beta == 0 else (1 + beta) / beta
    R = [[cap] * N for _ in range(N)]
    out = []
    for _ in range(K):
        new = [[cap] * N for _ in range(N)]
        for x in range(N):
            for y in range(N):
                c = [R[x][y], cap]
                if beta == 0:
                    if x in Z0:
                        c.append(F(0))
                    if y in Z1:
                        c.append(F(1))
                else:
                    if x in Z0:
                        c.append(F(1))
                    if y in Z1:
                        c.append(F(1))
                    if x in Z0 and y in Z1:
                        c.append(beta / (1 + beta))
                if x == y:
                    c.append(F(1))
                if y < g.n:
                    y0, y1 = g.succ[y]
                    a, b = R[x][y0], R[x][y1]
                    k = g.kinds[y]
                    c.append(_min(a, b) if k == 'max' else
                             (_max(a, b) if k == 'min' else _harm(a, b)))
                if x < g.n:
                    x0, x1 = g.succ[x]
                    a, b = R[x0][y], R[x1][y]
                    k = g.kinds[x]
                    c.append(_max(a, b) if k == 'max' else
                             (_min(a, b) if k == 'min' else _mean(a, b)))
                if x < g.n and y < g.n and g.kinds[x] == g.kinds[y]:
                    x0, x1 = g.succ[x]
                    y0, y1 = g.succ[y]
                    M = [[R[x0][y0], R[x0][y1]], [R[x1][y0], R[x1][y1]]]
                    k = g.kinds[x]
                    if k == 'max':
                        c.append(_min(_max(M[0][0], M[1][0]), _max(M[0][1], M[1][1])))
                        c.append(_max(_min(M[0][0], M[0][1]), _min(M[1][0], M[1][1])))
                    elif k == 'min':
                        c.append(_min(_max(M[0][0], M[0][1]), _max(M[1][0], M[1][1])))
                        c.append(_max(_min(M[0][0], M[1][0]), _min(M[0][1], M[1][1])))
                    else:
                        c.append(_max(M[0][0], M[1][1]))
                        c.append(_max(M[0][1], M[1][0]))
                new[x][y] = _min(*c)
        R = new
        out.append([r[:] for r in R])
    return out


def sound_beta(g, R, w, beta):
    bad = 0
    for x in range(g.N):
        for y in range(g.N):
            r = R[x][y]
            if r is INF:
                continue
            if w[x] + beta > r * (w[y] + beta):
                bad += 1
    return bad
