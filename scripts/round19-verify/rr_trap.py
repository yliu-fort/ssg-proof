#!/usr/bin/env python3
"""The trap hypothesis of rem:rational-row for the readout system of thm:readout-realise(a).

Claim (proved by hand in the round-19 README and in the paper): for a STOPPING SSG G with Max set Vmax, the pieces of
lem:readout(a) -- for each incidence (v,a) and each positional Min strategy tau, the first-passage law (q; p) from v^(a)
onto Vmax u {t1} when Min plays tau, Max vertices absorbing -- satisfy the hypothesis
   (T)  no nonempty U <= Vmax has at each of its vertices v an action a and a tau whose law has q = 0 and
        sum_{u in U} p_u = 1 (mass one inside U; 'supp(p) <= U' alone would not do -- an action into t0 has q = 0).
Proof: if such U, (a_v, tau_v) existed, W := U u (the union over v in U of the vertices visited with positive
probability from v^(a_v) under tau_v before hitting Vmax) would be a trap of G in the sense of lem:trapchar: every
average vertex of W has both successors in W, every Min vertex of W has its tau_v-successor in W, every Max vertex of
W lies in U and has its a_v-successor in W, and W meets no sink since the law puts no mass on t1 and none on t0.
Here: the pieces are computed exactly and (T) is tested on random two-player games, stopping and not; on every
stopping game (T) must hold; on non-stopping games violations may or may not occur (T is implied by stopping, not
equivalent to it), and every violation found is turned into the trap W and W is verified to be a trap.
"""
import sys, os, random, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'harness'))
from mycore import G, is_stopping

def lin_solve(A, b):
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]; pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [M[r][j] - f * M[c][j] for j in range(n + 1)]
    return [M[i][n] for i in range(n)]

def first_passage(g, start, tau):
    """Law of the first hit of Vmax u {t0, t1} from `start` when Min plays tau, Max absorbing; returns
    (law: dict target -> prob, visited: set of transient vertices reached with positive probability).
    Transient vertices from which no target is reachable lose their mass (only in non-stopping games)."""
    targets = set(g.of('max')) | {g.T0, g.T1}
    if start in targets: return {start: F(1)}, set()
    # successor distribution of transient vertices
    dist = {}
    for v in range(g.n):
        if v in targets: continue
        if g.kinds[v] == 'min': dist[v] = {tau[v]: F(1)}
        else:
            d = {}
            for u in g.succ[v]: d[u] = d.get(u, F(0)) + F(1, 2)
            dist[v] = d
    # reachable transient set from start
    seen = {start}; stack = [start]
    while stack:
        v = stack.pop()
        for u in dist[v]:
            if u not in targets and u not in seen: seen.add(u); stack.append(u)
    # vertices that can reach a target
    good = set()
    changed = True
    while changed:
        changed = False
        for v in seen:
            if v not in good and any(u in targets or u in good for u in dist[v]): good.add(v); changed = True
    idx = {v: i for i, v in enumerate(sorted(good))}
    law = {}
    for t in targets:
        # h_v = P(first hit at t)  =  sum_u dist[v][u] * (1[u==t] if u target else h_u)
        n = len(idx); A = [[F(int(i == j)) for j in range(n)] for i in range(n)]; b = [F(0)] * n
        for v, i in idx.items():
            for u, pr in dist[v].items():
                if u in targets: b[i] += pr * (1 if u == t else 0)
                elif u in idx: A[i][idx[u]] -= pr
        if n == 0:
            law[t] = F(0); continue
        h = lin_solve(A, b); assert h is not None
        law[t] = h[idx[start]] if start in idx else F(0)
    return {t: p for t, p in law.items() if p != 0}, seen

def pieces(g):
    """(v,a) -> list over tau of (law, visited)."""
    mins = g.of('min'); out = {}
    for v in g.of('max'):
        for a in (0, 1):
            L = []
            for choice in itertools.product((0, 1), repeat=len(mins)):
                tau = {u: g.succ[u][c] for u, c in zip(mins, choice)}
                L.append(first_passage(g, g.succ[v][a], tau))
            out[(v, a)] = L
    return out

def violation(g, P):
    """The smallest U violating (T), with a witness (a_v, law, visited) per v, or None."""
    Vmax = g.of('max')
    for r in range(1, len(Vmax) + 1):
        for U in itertools.combinations(Vmax, r):
            Us = set(U); wit = {}
            for v in U:
                for a in (0, 1):
                    for law, vis in P[(v, a)]:
                        if g.T1 not in law and g.T0 not in law and set(law) <= Us and sum(law.values()) == 1:
                            wit[v] = (a, law, vis); break
                    if v in wit: break
                if v not in wit: break
            if len(wit) == len(U): return Us, wit
    return None

def is_trap(g, W):
    if not W or g.T0 in W or g.T1 in W: return False
    for v in W:
        if g.kinds[v] == 'avg':
            if not all(u in W for u in g.succ[v]): return False
        else:
            if not any(u in W for u in g.succ[v]): return False
    return True

def random_game(rng):
    m = rng.randint(2, 4); k = rng.randint(1, 3); a = rng.randint(1, 6)
    kinds = ['max'] * m + ['min'] * k + ['avg'] * a; rng.shuffle(kinds)
    n = len(kinds); N = n + 2
    succ = [(rng.randrange(N), rng.randrange(N)) for _ in range(n)]
    return G(kinds, succ)

rng = random.Random(19)
stats = {'stopping': 0, 'stopping_viol': 0, 'nonstopping': 0, 'nonstopping_viol': 0, 'trap_confirmed': 0}
for it in range(3000):
    g = random_game(rng)
    if not any(k == 'max' for k in g.kinds): continue
    st = is_stopping(g); P = pieces(g); vio = violation(g, P)
    if st:
        stats['stopping'] += 1
        if vio: stats['stopping_viol'] += 1; print('VIOLATION ON A STOPPING GAME', g.kinds, g.succ, vio)
    else:
        stats['nonstopping'] += 1
        if vio:
            stats['nonstopping_viol'] += 1
            U, wit = vio
            W = set(U)
            for v, (a, law, vis) in wit.items(): W |= vis
            assert is_trap(g, W), ('W is not a trap', g.kinds, g.succ, W)
            stats['trap_confirmed'] += 1
print(stats)
assert stats['stopping_viol'] == 0 and stats['stopping'] >= 300
# a non-stopping example: the violation found is the singleton U = {0} (action 0 of vertex 0 returns to 0 surely under
# the Min choice 2 -> 6), and W = {0, 2, 3, 6} is the trap. (The root agent's auditor: with one Min vertex a single tau
# always serves every vertex of U; a configuration needing two different tau_v was not found in 40000 games with two
# Min vertices -- the proof handles it, whether or not it occurs.)
#   0: max -> (3, t0); 1: max -> (4, t0); 3: avg -> (2, 2); 4: avg -> (2, 2); 2: min -> (5, 6); 5: avg -> (1, 1); 6: avg -> (0, 0)
g = G(['max', 'max', 'min', 'avg', 'avg', 'avg', 'avg'], [(3, 7), (4, 7), (5, 6), (2, 2), (2, 2), (1, 1), (0, 0)])
P = pieces(g); vio = violation(g, P); assert vio is not None and not is_stopping(g)
U, wit = vio; W = set(U)
for v, (a, law, vis) in wit.items(): W |= vis
print('hand example: U =', sorted(U), 'laws', {v: dict(w[1]) for v, w in wit.items()}, 'W =', sorted(W), 'trap:', is_trap(g, W))
assert is_trap(g, W)
print('TRAP HYPOTHESIS (T) HOLDS ON EVERY STOPPING GAME TESTED; every violation on a non-stopping game yields the trap W')
