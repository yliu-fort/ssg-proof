#!/usr/bin/env python3
"""Root agent's verification of the round-19 blind route (routings and the rotor game), from the statements.

 [1] the routing formula: for a positional pair, val(v) = #{acyclic selections routing v to t1} / #{acyclic
     selections}, and the pair is absorbing iff some acyclic selection exists (random stopping and non-stopping games);
 [2] det M = |R| for the integer matrix M (rows 2e_u - e_{u0} - e_{u1} at average, e_v - e_s at controlled vertices),
     and the auditor's factorisation det M = det A_{Vavg} = det A_U det A_{U^c} with A the contracted matrix of
     lem:denominator's proof;
 [3] the rotor identity OUT_n = n h(v0) + sum_u s_u [K_u odd] delta_u + sum_{controlled visits} (h(chosen) - h(v))
     with h = val, and the sandwich |M_rho(n) - n val(v0)| <= A(G)/2 for the exact rotor-game value (backward
     induction over (chips, position, rotor)) on small games; the identity on many runs;
 [4] E1: M(n) = n/2 + 1 for even n <= 10, best positional ceil(n/2);
 [5] RC(m) built as a game: stopping, val = 1/2 - 2^{-(m+1)}, and the schedule 'chip i to u_i (i <= 7), then u_8'
     gives 2 OUT_n > n for every n < 7(2^m - 1) at m = 4, 6, with the minimum excess (7/2) val(q_1);
 [6] exactness over a rotor period: OUT_p / p = val_{sigma,tau}(v0);
 [7] the retyping identity: retyping a controlled vertex as average gives (Z^0 v^0 + Z^1 v^1)/(Z^0 + Z^1).
"""
import sys, os, itertools, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'harness'))
from mycore import G, is_stopping, profile_value, wstar

def det(M):
    n = len(M); A = [list(map(F, r)) for r in M]; d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]; pv = A[c][c]
        for r in range(c + 1, n):
            if A[r][c] != 0:
                f = A[r][c] / pv; A[r] = [A[r][j] - f * A[c][j] for j in range(n)]
    return d

def selections(g, sigma, tau):
    """all selections f (successor index per non-sink) consistent with the pair; yields (f, acyclic?)"""
    avg = g.of('avg')
    base = {}
    for v in range(g.n):
        if g.kinds[v] == 'max': base[v] = g.succ[v].index(sigma[v]) if sigma[v] in g.succ[v] else None
        elif g.kinds[v] == 'min': base[v] = g.succ[v].index(tau[v])
    for bits in itertools.product((0, 1), repeat=len(avg)):
        f = dict(base)
        for u, b in zip(avg, bits): f[u] = b
        nxt = {v: g.succ[v][f[v]] for v in range(g.n)}
        # acyclic iff every vertex reaches a sink
        acyclic = True; end = {}
        for v in range(g.n):
            seen = set(); w = v
            while w < g.n and w not in seen: seen.add(w); w = nxt[w]
            if w < g.n: acyclic = False; break
            end[v] = w
        yield f, acyclic, (end if acyclic else None)

def routing_data(g, sigma, tau):
    R = 0; c = [0] * g.n
    for f, ac, end in selections(g, sigma, tau):
        if not ac: continue
        R += 1
        for v in range(g.n):
            if end[v] == g.T1: c[v] += 1
    return R, c

def absorbing(g, sigma, tau):
    """the chain reaches a sink almost surely from every vertex: no closed set avoiding the sinks"""
    nxt = {}
    for v in range(g.n):
        if g.kinds[v] == 'max': nxt[v] = [sigma[v]]
        elif g.kinds[v] == 'min': nxt[v] = [tau[v]]
        else: nxt[v] = list(g.succ[v])
    good = {g.T0, g.T1}; changed = True
    while changed:
        changed = False
        for v in range(g.n):
            if v not in good and any(u in good for u in nxt[v]): good.add(v); changed = True
    return len(good) == g.N

def matrix_M(g, sigma, tau):
    n = g.n; M = [[0] * n for _ in range(n)]
    for v in range(n):
        if g.kinds[v] == 'avg':
            M[v][v] += 2
            for u in g.succ[v]:
                if u < n: M[v][u] -= 1
        else:
            s = sigma[v] if g.kinds[v] == 'max' else tau[v]
            M[v][v] += 1
            if s < n: M[v][s] -= 1
    return M

def contracted_A(g, sigma, tau):
    """lem:denominator's matrix on Vavg: follow deterministic steps to an average vertex or a sink (bot if a cycle)."""
    avg = g.of('avg'); idx = {u: i for i, u in enumerate(avg)}
    def D(u):
        seen = set(); w = u
        while w < g.n and g.kinds[w] != 'avg':
            if w in seen: return None
            seen.add(w); w = sigma[w] if g.kinds[w] == 'max' else tau[w]
        return w
    A = [[0] * len(avg) for _ in avg]
    for u in avg:
        A[idx[u]][idx[u]] = 2
        for s in g.succ[u]:
            d = D(s)
            if d is not None and d < g.n: A[idx[u]][idx[d]] -= 1
    # U: average vertices from which t1 is reachable in the chain
    reach = set(); frontier = [g.T1]
    pred = {v: [] for v in range(g.N)}
    for v in range(g.n):
        outs = list(g.succ[v]) if g.kinds[v] == 'avg' else [sigma[v] if g.kinds[v] == 'max' else tau[v]]
        for u in outs: pred[u].append(v)
    while frontier:
        w = frontier.pop()
        for v in pred[w]:
            if v not in reach: reach.add(v); frontier.append(v)
    U = [u for u in avg if u in reach]; Uc = [u for u in avg if u not in reach]
    sub = lambda S: [[A[idx[u]][idx[w]] for w in S] for u in S]
    return A, sub(U), sub(Uc)

def random_game(rng, nmax=7):
    n = rng.randint(2, nmax); kinds = [rng.choice(['max', 'min', 'avg', 'avg']) for _ in range(n)]
    succ = [(rng.randrange(n + 2), rng.randrange(n + 2)) for _ in range(n)]
    return G(kinds, succ)

def pairs(g):
    maxv, minv = g.of('max'), g.of('min')
    for sb in itertools.product((0, 1), repeat=len(maxv)):
        for tb in itertools.product((0, 1), repeat=len(minv)):
            yield {v: g.succ[v][sb[i]] for i, v in enumerate(maxv)}, {u: g.succ[u][tb[j]] for j, u in enumerate(minv)}

rng = random.Random(1919)
# [1] + [2]
checked = 0; fact = 0
while checked < 400:
    g = random_game(rng)
    if not g.of('avg'): continue
    for sigma, tau in pairs(g):
        R, c = routing_data(g, sigma, tau); ab = absorbing(g, sigma, tau)
        assert (R > 0) == ab
        if not ab: continue
        pv = profile_value(g, sigma, tau)
        assert all(pv[v] == F(c[v], R) for v in range(g.n)), 'routing formula'
        M = matrix_M(g, sigma, tau); assert det(M) == R, 'det M = |R|'
        A, AU, AUc = contracted_A(g, sigma, tau)
        dA = det(A) if A else F(1); dU = det(AU) if AU else F(1); dUc = det(AUc) if AUc else F(1)
        assert dA == R == dU * dUc, 'factorisation'
        if AUc: fact += 1
        checked += 1
        if checked >= 400: break
print(f'[1][2] routing formula, nonemptiness <=> absorbing, det M = |R| = det A_Vavg = det A_U det A_Uc on {checked} absorbing pairs of random games ({fact} with U^c nonempty)')

# [3] rotor identity and sandwich
def rotor_chip(g, rho, start, choose):
    """one chip; choose(v, rho) returns the successor at a controlled vertex. returns (sink, visits, ctrl_moves)."""
    v = start; visits = {}; moves = []; steps = 0
    while v < g.n:
        steps += 1; assert steps < 10 ** 6
        if g.kinds[v] == 'avg':
            visits[v] = visits.get(v, 0) + 1; i = rho[v]; rho[v] = 1 - i; v = g.succ[v][i]
        else:
            u = choose(v, rho); moves.append((v, u)); v = u
    return v, visits, moves

def identity_check(g, w, rho0, start, n, choose):
    rho = dict(rho0); out = 0; K = {u: 0 for u in g.of('avg')}; ctrl = F(0)
    for _ in range(n):
        sink, visits, moves = rotor_chip(g, rho, start, choose)
        out += sink == g.T1
        for u, k in visits.items(): K[u] += k
        for v, u in moves: ctrl += w[u] - w[v]
    delta = {u: (w[g.succ[u][0]] - w[g.succ[u][1]]) / 2 for u in g.of('avg')}
    s = {u: 1 if rho0[u] == 0 else -1 for u in g.of('avg')}
    rhs = n * w[start] + sum(s[u] * delta[u] for u in g.of('avg') if K[u] % 2 == 1) + ctrl
    return out, rhs

def game_value_rotor(g, w, rho0, start, n):
    """exact value of the n-chip rotor game by backward induction over (chips left, position, rotor)."""
    avg = g.of('avg'); memo = {}
    def rec(k, rho):
        if k == 0: return F(0)
        key = (k, rho)
        if key in memo: return memo[key]
        # one chip from start under optimal adaptive play: a finite game on (position, rho) within the chip
        def chip(v, rho):
            if v == g.T1: return F(1) + rec(k - 1, rho)
            if v == g.T0: return F(0) + rec(k - 1, rho)
            if g.kinds[v] == 'avg':
                i = rho[avg.index(v)]; r2 = list(rho); r2[avg.index(v)] = 1 - i
                return chip(g.succ[v][i], tuple(r2))
            vals = [chip(u, rho) for u in g.succ[v]]
            return max(vals) if g.kinds[v] == 'max' else min(vals)
        res = chip(start, rho); memo[key] = res; return res
    return rec(n, tuple(rho0[u] for u in avg))

wfull = lambda g: (lambda ws: [ws[v] for v in range(g.n)] + [F(0), F(1)])(wstar(g))
ident = 0; sandwich = 0; attained = 0
for _ in range(150):
    g = random_game(rng, 6)
    if not g.of('avg') or not is_stopping(g): continue
    w = wfull(g); start = 0
    Aval = sum(abs(w[g.succ[u][0]] - w[g.succ[u][1]]) for u in g.of('avg'))
    for _ in range(2):
        rho0 = {u: rng.randrange(2) for u in g.of('avg')}
        sigma, tau = rng.choice(list(pairs(g)))
        choose = lambda v, rho: sigma[v] if g.kinds[v] == 'max' else tau[v]
        for n in (1, 3, 6):
            out, rhs = identity_check(g, w, rho0, start, n, choose); assert out == rhs, 'rotor identity'; ident += 1
        if len(g.of('avg')) <= 3:
            for n in (1, 2, 4):
                Mv = game_value_rotor(g, w, rho0, start, n)
                assert abs(Mv - n * w[start]) <= Aval / 2, 'sandwich'; sandwich += 1
                if abs(Mv - n * w[start]) == Aval / 2: attained += 1
print(f'[3] rotor identity on {ident} runs; sandwich |M_rho(n) - n val| <= A/2 on {sandwich} exact rotor-game values ({attained} attained)')

# [4] E1
E1 = G(['max', 'avg', 'avg'], [(1, 2), (4, 3), (4, 3)]); w = wfull(E1); assert is_stopping(E1) and w[0] == F(1, 2)
AE1 = sum(abs(w[E1.succ[u][0]] - w[E1.succ[u][1]]) for u in E1.of('avg')); assert AE1 == 2
for n in (2, 4, 6, 8, 10):
    Mv = game_value_rotor(E1, w, {1: 0, 2: 0}, 0, n); assert Mv == F(n, 2) + 1, (n, Mv)
    best_pos = max(identity_check(E1, w, {1: 0, 2: 0}, 0, n, (lambda v, rho, s=s: s))[0] for s in (1, 2))
    assert best_pos == (n + 1) // 2
print('[4] E1: M(n) = n/2 + 1 = n val + A/2 for n = 2..10 even; best positional play ceil(n/2)')

# [5] RC(m)
def RC(m):
    kinds = ['max'] * 7 + ['avg'] * 8 + ['avg'] * m; n = len(kinds); T0, T1 = n, n + 1
    succ = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14)]
    q = lambda i: 15 + i - 1
    succ += [(q(1), T0)] * 8
    succ += [(T1, q(i + 1)) for i in range(1, m)] + [(T1, T0)]
    return G(kinds, succ)
for m in (3, 4, 5):
    g = RC(m); assert is_stopping(g) and g.N == m + 17
    w = wfull(g); assert w[0] == F(1, 2) - F(1, 2 ** (m + 1)) and all(w[u] == w[0] for u in range(7, 15))
for m in (4, 6):
    g = RC(m); w = wfull(g); vq1 = w[15]; nmax = 8 * 2 ** m
    rho = {u: 0 for u in g.of('avg')}; out = 0; minexcess = None; first_fail = None
    # schedule: chip i (1-based) to leaf u_i for i <= 7, then all to u_8; Max routes the chip down the tree to that leaf
    leaf_path = {}
    for leaf in range(7, 15):
        path = {}; v = leaf
        while v != 0:
            parent = next(p for p in range(7) if v in g.succ[p]); path[parent] = v; v = parent
        leaf_path[leaf] = path
    for i in range(1, nmax + 1):
        leaf = 6 + i if i <= 7 else 14
        sink, _, _ = rotor_chip(g, rho, 0, lambda v, r, lp=leaf_path[leaf]: lp[v])
        out += sink == g.T1
        if i >= 7:
            ex = out - i * w[0]
            minexcess = ex if minexcess is None else min(minexcess, ex)
        if 2 * out <= i and first_fail is None: first_fail = i
    assert first_fail >= 7 * (2 ** m - 1) and minexcess == F(7, 2) * vq1, (m, first_fail, minexcess)
    print(f'[5] RC({m}): N = {g.N}, stopping, val(v0) = {w[0]}; the schedule gives 2 OUT_n > n up to n = {first_fail - 1} >= 7(2^m - 1) = {7 * (2 ** m - 1)}; minimum excess over n >= 7 is (7/2) val(q_1) = {minexcess}')

# [6] period exactness
per = 0
for _ in range(200):
    g = random_game(rng, 6)
    if not g.of('avg') or not is_stopping(g): continue
    sigma, tau = rng.choice(list(pairs(g))); pv = profile_value(g, sigma, tau)
    choose = lambda v, rho: sigma[v] if g.kinds[v] == 'max' else tau[v]
    rho = {u: rng.randrange(2) for u in g.of('avg')}
    seen = {}; hist = []
    while True:
        key = tuple(rho[u] for u in g.of('avg'))
        if key in seen: break
        seen[key] = len(hist)
        sink, _, _ = rotor_chip(g, rho, 0, choose); hist.append(sink == g.T1)
    start_i = seen[key]; p = len(hist) - start_i; outp = sum(hist[start_i:])
    assert F(outp, p) == pv[0], 'period exactness'; per += 1
print(f'[6] exactness over a rotor period on {per} (game, pair, rotor start) instances')

# [7] retyping identity
ret = 0
for _ in range(200):
    g = random_game(rng, 6)
    ctrl = [v for v in range(g.n) if g.kinds[v] != 'avg']
    if not ctrl or not g.of('avg') or not is_stopping(g): continue
    v = rng.choice(ctrl); sigma, tau = rng.choice(list(pairs(g)))
    kinds2 = list(g.kinds); kinds2[v] = 'avg'; g2 = G(kinds2, g.succ)
    if not absorbing(g2, sigma, tau): continue
    pv2 = profile_value(g2, sigma, tau)
    Z = []; V = []
    for a in (0, 1):
        s2 = dict(sigma); t2 = dict(tau)
        if g.kinds[v] == 'max': s2[v] = g.succ[v][a]
        else: t2[v] = g.succ[v][a]
        Ra, ca = routing_data(g, s2, t2); Z.append(Ra); V.append(profile_value(g, s2, t2) if Ra else None)
    if Z[0] + Z[1] == 0: continue
    for x in range(g.n):
        num = sum(Z[a] * V[a][x] for a in (0, 1) if Z[a]); assert pv2[x] == num / (Z[0] + Z[1]), 'retyping'
    ret += 1
print(f'[7] the retyping identity on {ret} instances')
print('FRESH-19 ROUTE: every load-bearing computation reproduced')
