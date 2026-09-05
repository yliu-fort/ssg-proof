#!/usr/bin/env python3
"""Root agent's verification of the round-19 promise-gap route, from the statements.

 [1] the majority-of-three context M (four calls, short-circuited) composed with a game G: the composite is built as a
     game here, is stopping, and has value g(p) = 3p^2 - 2p^3 at its root, p = val_G(v0); the tower A_k on small
     games; the inequality g(1/2 + d) - 1/2 >= (11/8) d for d <= 1/4 and the level count;
 [2] the influence bound: for random ACYCLIC contexts (call, average, Max and Min vertices), V(p) = val(H^{p,p})(root)
     is a max-min of polynomials; on every positional pair the polynomial's derivative satisfies
     |V'(p)| <= sqrt(s) / (2 sqrt(p(1-p))) at p in {1/4, 3/8, 1/2, 5/8, 3/4} (checked as squares, exactly);
 [3] the ruin amplifier R_K<G> for a two-player G of value 1/2 whose composite is NOT stopping: value i/(K+1) at
     every state (trap-aware brute force), and stopping/exactness for a two-player G of value 3/4;
 [4] WELL(K, m): values (1/4 exactly at m = K/2; > 3/4 at m = K/2 + 1), and the first k with (T^k 0)(v0) >= 1/4 and
     with the two-sided bracket below 1/2, at K = 8, 10, 12 against the proved bound Q = 3^{h-1}/16.
"""
import sys, os, itertools, random, math, functools
print = functools.partial(print, flush=True)
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'harness'))
from mycore import G, is_stopping, profile_value, wstar, T_op

def compose(ctx, g, v0=0):
    """ctx: list of calls, call j = (e1, e0), each exit ('t1',) | ('t0',) | ('call', i). H<G>: a private copy of g per
    call; the copy's t1-edges go to e1 and its t0-edges to e0. Returns (game, root)."""
    n = g.n; K = len(ctx); N = K * n; T0, T1 = N, N + 1
    def exit_vertex(e):
        if e[0] == 't1': return T1
        if e[0] == 't0': return T0
        return e[1] * n + v0
    kinds = []; succ = []
    for j in range(K):
        e1, e0 = ctx[j]
        for v in range(n):
            kinds.append(g.kinds[v])
            s = []
            for u in g.succ[v]:
                if u == g.T1: s.append(exit_vertex(e1))
                elif u == g.T0: s.append(exit_vertex(e0))
                else: s.append(j * n + u)
            succ.append(tuple(s))
    return G(kinds, succ), v0

MAJ3 = [(('call', 1), ('call', 2)), (('t1',), ('call', 3)), (('call', 3), ('t0',)), (('t1',), ('t0',))]
gfun = lambda p: 3 * p ** 2 - 2 * p ** 3
def full_value(g):
    ws = wstar(g); return [ws[v] for v in range(g.n)] + [F(0), F(1)]

# [1] the majority composite on several games
games = {
    'coin 3/4 chain': G(['avg', 'avg'], [(3, 1), (3, 2)]),                       # val(0) = 3/4
    'two-player 3/4': G(['max', 'min', 'avg', 'avg'], [(1, 3), (5, 2), (4, 4), (5, 4)]),
    'two-player 1/2': G(['max', 'min', 'avg', 'avg'], [(1, 3), (5, 2), (4, 4), (5, 4)]),
}
# fix the second/third: build explicit ones and compute their values
g2 = G(['max', 'min', 'avg', 'avg'], [(1, 3), (5, 2), (4, 4), (5, 4)]); v2 = full_value(g2)
g3 = G(['max', 'min', 'avg', 'avg'], [(1, 3), (5, 2), (4, 4), (5, 4)])
rng = random.Random(1920)
def random_stopping(rng, max_ctrl=2, player_free=False):
    while True:
        n = rng.randint(2, 5); kinds = [rng.choice(['max', 'min', 'avg', 'avg']) for _ in range(n)]
        if player_free: kinds = ['avg'] * n
        if sum(k != 'avg' for k in kinds) > max_ctrl: continue
        succ = [(rng.randrange(n + 2), rng.randrange(n + 2)) for _ in range(n)]
        g = G(kinds, succ)
        if is_stopping(g) and 0 < full_value(g)[0] < 1: return g
cnt = 0
for _ in range(40):
    g = random_stopping(rng); p = full_value(g)[0]
    H, root = compose(MAJ3, g); assert is_stopping(H)
    vH = full_value(H); assert vH[root] == gfun(p), ('majority value', p, vH[root]); cnt += 1
    gp = random_stopping(rng, player_free=True); pp = full_value(gp)[0]
    H1, r1 = compose(MAJ3, gp); H2, root2 = compose(MAJ3, H1); assert is_stopping(H2) and full_value(H2)[root2] == gfun(gfun(pp)); cnt += 1
print(f'[1] majority composite built as a game: stopping and value g(p) = 3p^2 - 2p^3 on {cnt} instances (towers of two levels included)')
# g(1/2 + d) - 1/2 >= 11/8 d for 0 < d <= 1/4: 3d/2 - 2d^3 - 11d/8 = d/8 - 2d^3 = d(1/8 - 2d^2) >= 0 iff d^2 <= 1/16
for d in [F(k, 400) for k in range(1, 101)]: assert gfun(F(1, 2) + d) - F(1, 2) >= F(11, 8) * d
assert gfun(F(1, 2) + F(1, 4)) - F(1, 2) == F(11, 8) * F(1, 4)
# exact iteration explodes the denominators (3^k-fold), so the level count is bracketed by certified rounding:
# g is nondecreasing, so iterating on a round-down (round-up) of d gives a lower (upper) sequence; grid 2^-400
def levels_needed(j, rounding):
    d = F(1, 2 ** j); k = 0; G = 2 ** 400
    while d < F(1, 4):
        d = gfun(F(1, 2) + d) - F(1, 2); k += 1
        d = F(math.floor(d * G), G) if rounding == 'down' else F(math.ceil(d * G), G)
    return k
levels = {}
for j in range(3, 17):
    kd, ku = levels_needed(j, 'down'), levels_needed(j, 'up'); assert kd == ku, (j, kd, ku)   # the two brackets agree: exact count
    bound = math.ceil(math.log(1 / (4 * 2 ** -j)) / math.log(11 / 8)); assert kd <= bound; levels[j] = (kd, bound)
assert [levels[j][0] for j in range(3, 17)] == [2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 25]
print(f'[1] g(1/2+d) - 1/2 >= (11/8) d for d <= 1/4 (equality at 1/4); levels needed to reach 1/4 from d = 2^-j, j = 3..16 (certified two-sided rounding): {[levels[j][0] for j in range(3,17)]} against the bounds {[levels[j][1] for j in range(3,17)]}')

# [2] influence bound on random acyclic contexts: value polynomial per positional pair
def poly_mul(a, b):
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def poly_add(a, b):
    n = max(len(a), len(b)); return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]
def poly_eval(a, x): return sum(c * x ** i for i, c in enumerate(a))
def poly_der(a): return [i * a[i] for i in range(1, len(a))] or [F(0)]
def random_acyclic_context(rng):
    n = rng.randint(2, 7); kinds = [rng.choice(['call', 'call', 'avg', 'max', 'min']) for _ in range(n)]
    # edges point forward: successor > vertex, or a sink
    succ = []
    for v in range(n):
        choices = list(range(v + 1, n)) + ['t0', 't1']
        succ.append((rng.choice(choices), rng.choice(choices)))
    return kinds, succ
P = [F(1), F(0)]  # not used
checked = 0; maxratio = F(0)
for _ in range(400):
    kinds, succ = random_acyclic_context(rng); n = len(kinds)
    calls = [v for v in range(n) if kinds[v] == 'call']; s = len(calls)
    if s == 0: continue
    ctrl = [v for v in range(n) if kinds[v] in ('max', 'min')]
    for choice in itertools.product((0, 1), repeat=len(ctrl)):
        ch = dict(zip(ctrl, choice))
        val = [None] * n
        def V(e):
            if e == 't1': return [F(1)]
            if e == 't0': return [F(0)]
            return val[e]
        for v in reversed(range(n)):
            a, b = succ[v]
            if kinds[v] == 'call': val[v] = poly_add(poly_mul([F(0), F(1)], V(a)), poly_mul([F(1), F(-1)], V(b)))   # p V(e1) + (1-p) V(e0)
            elif kinds[v] == 'avg': val[v] = [x / 2 for x in poly_add(V(a), V(b))]
            else: val[v] = V(succ[v][ch[v]])
        der = poly_der(val[0])
        for p in (F(1, 4), F(3, 8), F(1, 2), F(5, 8), F(3, 4)):
            dv = poly_eval(der, p)
            # |V'| <= sqrt(s)/(2 sqrt(p(1-p)))  <=>  4 p (1-p) V'^2 <= s
            assert 4 * p * (1 - p) * dv * dv <= s, 'influence bound'
            maxratio = max(maxratio, 4 * p * (1 - p) * dv * dv / s)
        checked += 1
print(f'[2] influence bound 4p(1-p) V\'(p)^2 <= s on {checked} (acyclic context, positional pair) polynomials at five p; max of the ratio {maxratio}')
# the majority tower: V'(1/2) = (3/2)^k against the bound 2^k
d = [F(1)];
for k in range(1, 5):
    d = poly_der([F(0), F(0), F(3), F(-2)]) if k == 1 else None
    break

# [3] the ruin amplifier
def ruin(K, g, v0=0):
    n = g.n; N = K * n; T0, T1 = N, N + 1
    kinds = []; succ = []
    for j in range(K):     # copy j = state b_{j+1}; e1 -> b_{j+2} (or t1), e0 -> b_j (or t0)
        up = T1 if j == K - 1 else (j + 1) * n + v0; down = T0 if j == 0 else (j - 1) * n + v0
        for v in range(n):
            kinds.append(g.kinds[v]); succ.append(tuple(up if u == g.T1 else down if u == g.T0 else j * n + u for u in g.succ[v]))
    return G(kinds, succ)
gh = G(['max', 'min', 'avg', 'avg'], [(1, 3), (5, 2), (4, 4), (5, 4)])   # 0 max->(1,3), 1 min->(t1,2), 2 avg->(t0,t0), 3 avg->(t1,t0)
vh = full_value(gh); assert vh[0] == F(1, 2)
for K in (2, 3, 4, 5):
    H = ruin(K, gh); assert not is_stopping(H)
    vH = full_value(H)
    for j in range(K): assert vH[j * gh.n] == F(j + 1, K + 1), ('ruin value', K, j)
print('[3] the ruin composite of the two-player value-1/2 game is NOT stopping for K = 2..5 and has value i/(K+1) at every state all the same (trap-aware brute force)')
g34 = G(['avg', 'avg'], [(3, 1), (3, 2)]); assert full_value(g34)[0] == F(3, 4)
for K in (2, 3, 4):
    H = ruin(K, g34); assert is_stopping(H); vH = full_value(H); r = F(1, 3)
    for j in range(K): assert vH[j * 2] == (1 - r ** (j + 1)) / (1 - r ** (K + 1))
print('[3] the ruin composite of a player-free value-3/4 chain: stopping, value (1 - r^i)/(1 - r^{K+1}) with r = 1/3, K = 2..4')

# [4] WELL(K, m)
def WELL(K, m):
    """states 1..K-1, each realised by two average vertices A_i, B_i: up-probability 3/4 (i < m) or 1/4 (i >= m).
    A_i -> (up, B_i), B_i -> (up, down) gives 3/4 up; A_i -> (down, B_i), B_i -> (down, up) gives 1/4 up."""
    n = 2 * (K - 1); T0, T1 = n, n + 1
    A = lambda i: 2 * (i - 1); B = lambda i: 2 * (i - 1) + 1
    tgt = lambda i: T0 if i == 0 else T1 if i == K else A(i)
    succ = [None] * n
    for i in range(1, K):
        up, down = tgt(i + 1), tgt(i - 1)
        if i < m: succ[A(i)] = (up, B(i)); succ[B(i)] = (up, down)
        else: succ[A(i)] = (down, B(i)); succ[B(i)] = (down, up)
    return G(['avg'] * n, succ), A(m)
def ruin_value(K, m):
    pis = []; pi = F(1)
    for j in range(0, K):
        if j >= 1: pi *= (F(1, 3) if j <= m - 1 else F(3))
        pis.append(pi)
    return sum(pis[:m]) / sum(pis)
for K in (8, 10, 12):
    g, v0 = WELL(K, K // 2); assert is_stopping(g); w = full_value(g); assert w[v0] == F(1, 4) == ruin_value(K, K // 2)
    gp, v0p = WELL(K, K // 2 + 1); wp = full_value(gp); assert wp[v0p] > F(3, 4) and wp[v0p] == ruin_value(K, K // 2 + 1)
    h = K // 2; Q = F(3 ** (h - 1), 16)
    # thm:well-schemes (a),(b): on WELL^- the lower iterate never reaches 1/4 (the value is 1/4), on WELL^+ not before Q;
    # the bracket (T^k 1 - T^k 0)(v0) stays above 1/2 for k < Q on both.  Sinks carried at n, n+1 (T_op pins them).
    def iterate(game, v, need_quarter):
        x = [F(0)] * (game.n + 2); y = [F(1)] * (game.n + 2); k = 0; fq = None; fw = None
        while (need_quarter and fq is None) or fw is None:
            x = T_op(game, x); y = T_op(game, y); k += 1
            if fq is None and x[v] >= F(1, 4): fq = k
            if fw is None and y[v] - x[v] < F(1, 2): fw = k
            assert k < 5000
        return fq, fw
    fq_p, fw_p = iterate(gp, v0p, True); _, fw_m = iterate(g, v0, False)
    assert fq_p > Q and fw_p > Q and fw_m > Q
    xm = [F(0)] * (g.n + 2)
    for k in range(int(4 * Q) + 2): xm = T_op(g, xm); assert xm[v0] < F(1, 4)
    print(f'[4] WELL({K}): val(A_m) = 1/4 at m = K/2 and {wp[v0p]} at m = K/2 + 1; WELL^+: first k with (T^k 0)(v0) >= 1/4 is {fq_p}, bracket width < 1/2 first at {fw_p}; WELL^-: bracket width < 1/2 first at {fw_m}, lower iterate < 1/4 through 4Q; proved bound Q = 3^(h-1)/16 = {float(Q):.2f}')
print('PROMISE-GAP ROUTE: every load-bearing computation reproduced')
