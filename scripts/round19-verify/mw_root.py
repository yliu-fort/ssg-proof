#!/usr/bin/env python3
"""Root agent's verification of the round-19 m6-walk route (batch F), from the statements, in exact arithmetic.

 [1] mw:flip -- the single-edge reversal criterion, exhaustively at m = 2, 3: reversing the edge {u, u ^ e_i} of a unique
     sink orientation s gives a unique sink orientation iff s(u) ^ s(u') = e_i (iff u ^ s(u) = u' ^ s(u')); then t = s o (u u'),
     the bottom-antipodal successors of the other vertices are unchanged and u, u' acquire z ^ e_i; acyclicity of t iff no
     directed s-path from the tail to the head avoids the edge; 744 USOs, 8928 reversals, 48 acyclic -> cyclic at m = 3;
     the stated 3-cube example, whose directed cycle is 1 -> 5 -> 4 -> 6 -> 2 -> 3 -> 1 (not the route's 1 -> 5 -> 7 -> 3 -> 1).
 [2] mw:twelve-flat -- own enumeration of the acyclic unique sink orientations of the m-cube whose bottom-antipodal walk
     from 0 has length L: a depth-first search over the walk pruned by the backward law, the forward law and the
     Szabo-Welzl condition (all three hold for bottom-antipodal walks of AUSOs by reachability: the walk vertices are in
     topological order), then a bijective Szabo-Welzl completion and an acyclicity test.  (4,7): 48; (5,12): 480, equal
     to the route's list mw_h12_m5.txt; (5,13): none.  Then the partitions (F1)-(F4) of lem:seven-flat for each of the 480:
     240 admit a partition with a nontrivial block, unique, the edge {0, e_x} at the start, one flat incidence (0, x),
     x equidistributed (48 each); at m = 4 the 48 give lem:seven-flat back (24, edge {0,e_x}, incidence (0,x)).
 [3] mw:h13 -- the 418-vertex game H13_m6_WITNESS_GAME.json: one-player, out-degree two, greatest trap empty, the
     average part acyclic, the first-passage rows equal the printed system (denominator 2^14, every row leaking, least
     leak 5), 64 exact value vectors, the printed outmap with no tie and the printed least margin, USO, acyclic,
     Holt-Klee, bottom-antipodal height 13 attained exactly at {25,27,57,59}, the run from 25 and its switched sets as
     printed, the all-switches rule from the values agreeing with the walk, values nondecreasing and somewhere strictly
     increasing at every step, longest run over the 64 starts 13.
 [4] mw:b2-return -- the level-two block of prop:b2-realised (rows scripts/blowup/B2_small_nf.json), driven by t = y_{c5}:
     the 14 cells between the 13 fences of rem:pinned-escape are the route's printed outmaps, every fence ties exactly one
     edge, the edges reversed in order are (4,a1),(3,b1),(0,seed),(0,b1),(1,b1),(2,b1),(4,seed),(0,a1),(3,b1),(1,a1),
     (6,seed),(2,seed),(5,a1) -- {3,7} in direction beta_1 twice -- the flip distance from the first to the last cell is
     11, and every cell is a Holt-Klee AUSO of the 3-cube of the printed height.
"""
import sys, os, json, itertools, time
from fractions import Fraction as F
M = '/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad'
sys.path.insert(0, f'{M}/solo'); sys.path.insert(0, f'{M}/root16')
from my_D import is_holt_klee
from auso import is_uso, is_acyclic, ba_heights, ba_trace
HERE = os.path.dirname(os.path.abspath(__file__))
def say(*a): print(*a, flush=True)

# ---------------------------------------------------------------- [1] the flip criterion
def faces(m):
    out = []
    for J in range(1, 1 << m):
        fixed = [v for v in range(m) if not (J >> v) & 1]
        for bits in itertools.product((0, 1), repeat=len(fixed)):
            base = sum(b << v for b, v in zip(bits, fixed))
            out.append((J, [base | sub for sub in range(1 << m) if sub & ~J == 0]))
    return out
def all_usos(m):
    FACES = faces(m); n = 1 << m
    edges = [(v, v | (1 << k)) for v in range(n) for k in range(m) if not (v >> k) & 1]
    res = []
    for bits in range(1 << len(edges)):
        s = [0] * n
        for i, (a, b) in enumerate(edges):
            if (bits >> i) & 1: s[a] |= a ^ b
            else: s[b] |= a ^ b
        if all(sum(1 for v in verts if s[v] & J == 0) == 1 for J, verts in FACES): res.append(tuple(s))
    return res
def path_avoiding(s, m, a, b):
    seen = {a}; stack = [a]
    while stack:
        u = stack.pop()
        for k in range(m):
            if (s[u] >> k) & 1:
                w = u ^ (1 << k)
                if u == a and w == b: continue
                if w == b: return True
                if w not in seen: seen.add(w); stack.append(w)
    return False
def find_cycle(s, m):
    n = 1 << m; colour = [0] * n; parent = {}
    def dfs(u):
        colour[u] = 1
        for k in range(m):
            if (s[u] >> k) & 1:
                w = u ^ (1 << k)
                if colour[w] == 1:
                    cyc = [w, u]; x = u
                    while x != w: x = parent[x]; cyc.append(x)
                    return cyc[::-1]
                if colour[w] == 0:
                    parent[w] = u; c = dfs(w)
                    if c: return c
        colour[u] = 2; return None
    for v in range(n):
        if colour[v] == 0:
            c = dfs(v)
            if c: return c
for m in (2, 3):
    U = all_usos(m); n = 1 << m; Uset = set(U); rev = 0; ac2cy = 0
    for s in U:
        acyc = is_acyclic(s, m)
        for u in range(n):
            for i in range(m):
                if (u >> i) & 1: continue
                up = u ^ (1 << i); rev += 1
                t = list(s); t[u] ^= 1 << i; t[up] ^= 1 << i; t = tuple(t)
                crit = (s[u] ^ s[up]) == (1 << i)
                assert crit == (u ^ s[u] == up ^ s[up]) and crit == (t in Uset)
                if not crit: continue
                assert t[u] == s[up] and t[up] == s[u]
                z = u ^ s[u]
                assert all(x ^ t[x] == x ^ s[x] for x in range(n) if x not in (u, up)) and u ^ t[u] == z ^ (1 << i) and up ^ t[up] == z ^ (1 << i)
                sink_s = s.index(0); sink_t = t.index(0)
                assert sink_t == (sink_s if sink_s not in (u, up) else (up if sink_s == u else u))
                if acyc:
                    tail, head = (u, up) if (s[u] >> i) & 1 else (up, u)
                    assert (s[tail] >> i) & 1 and not (s[head] >> i) & 1
                    ta = is_acyclic(t, m); assert ta == (not path_avoiding(s, m, tail, head))
                    if not ta: ac2cy += 1
    say(f'[1] m={m}: {len(U)} unique sink orientations, {rev} single-edge reversals; the criterion (a), the transposition and successor clauses (b), the path clause (c) hold throughout; {ac2cy} reversals turn an acyclic orientation cyclic')
    if m == 3: assert len(U) == 744 and rev == 8928 and ac2cy == 48
s = (0, 1, 3, 2, 6, 5, 4, 7); t = (0, 5, 3, 2, 6, 1, 4, 7)
assert is_uso(s, 3) and is_acyclic(s, 3) and ba_heights(s, 3) == [0, 1, 2, 2, 3, 1, 3, 1] and s[1] ^ s[5] == 4
tt = list(s); tt[1] ^= 4; tt[5] ^= 4; assert tuple(tt) == t and is_uso(t, 3) and not is_acyclic(t, 3)
cyc = find_cycle(t, 3); say(f'[1] the example: s=(0,1,3,2,6,5,4,7), edge {{1,5}} in direction 2, t=(0,5,3,2,6,1,4,7) is a cyclic USO; a directed cycle: {" -> ".join(map(str, cyc))}')
def is_dicycle(t, m, cyc):
    return all(cyc[k] ^ cyc[k + 1] in {1 << i for i in range(m)} and (t[cyc[k]] >> (cyc[k] ^ cyc[k + 1]).bit_length() - 1) & 1 for k in range(len(cyc) - 1))
assert is_dicycle(t, 3, [1, 5, 4, 6, 2, 3, 1]) and not is_dicycle(t, 3, [1, 5, 7, 3, 1])
say('[1] 1 -> 5 -> 4 -> 6 -> 2 -> 3 -> 1 is a directed cycle of t; the route\'s 1 -> 5 -> 7 -> 3 -> 1 is not (t(5) = 1 points only to 4)')

# ---------------------------------------------------------------- [2] the walks of length L from 0 and their completions
def enumerate_walk_ausos(m, L):
    n = 1 << m; sig = [0]; S = []; found = []
    def rec(t):
        if t == L:
            # the sink: SW against every earlier vertex is the backward law with t' = L
            if all((sig[L] ^ sig[t0]) & S[t0] for t0 in range(L)): complete()
            return
        for St in range(1, n):
            new = sig[t] ^ St
            if new in sig: continue
            ok = True
            for t0 in range(t):
                d = sig[t] ^ sig[t0]
                if not ((St ^ S[t0]) & d): ok = False; break          # Szabo-Welzl at (sigma_t0, sigma_t)
                if not (d & ~St & (n - 1)): ok = False; break          # forward law: Delta not inside S_t
            if not ok: continue
            for t0 in range(t + 1):
                Sx = S[t0] if t0 < t else St
                if not ((new ^ sig[t0]) & Sx): ok = False; break       # backward law for sigma_{t+1}
            if not ok: continue
            sig.append(new); S.append(St); rec(t + 1); sig.pop(); S.pop()
    def complete():
        s = [None] * n
        for t0 in range(L): s[sig[t0]] = S[t0]
        s[sig[L]] = 0
        assigned = [v for v in range(n) if s[v] is not None]
        free = [v for v in range(n) if s[v] is None]
        used = set(s[v] for v in assigned); avail = [c for c in range(n) if c not in used]
        # most-constrained first: vertices with many assigned neighbours
        free.sort(key=lambda v: -sum(1 for k in range(m) if s[v ^ (1 << k)] is not None))
        def rec2(idx, asg):
            if idx == len(free):
                st = tuple(s)
                if is_uso(st, m) and is_acyclic(st, m):
                    assert ba_trace(st, 0) == sig
                    found.append(st)
                return
            v = free[idx]
            for c in avail:
                if c in used: continue
                if all((c ^ s[w]) & (v ^ w) for w in asg):
                    s[v] = c; used.add(c); asg.append(v)
                    rec2(idx + 1, asg)
                    asg.pop(); used.discard(c); s[v] = None
        rec2(0, list(assigned))
    rec(0)
    return found
t0 = time.time(); W47 = enumerate_walk_ausos(4, 7); say(f'[2] m=4, L=7: {len(W47)} AUSOs with walk from 0 of length 7 ({time.time()-t0:.1f}s)'); assert len(W47) == 48
t0 = time.time(); W512 = enumerate_walk_ausos(5, 12); say(f'[2] m=5, L=12: {len(W512)} AUSOs with walk from 0 of length 12 ({time.time()-t0:.1f}s)'); assert len(W512) == 480
route = set(tuple(int(x) for x in line.split()) for line in open(f'{HERE}/mw_h12_m5.txt') if line.strip())
assert route == set(W512) and len(route) == 480, (len(route), len(route & set(W512)))
say('[2] the 480 coincide with the route\'s list mw_h12_m5.txt; none is Holt-Klee:', all(not is_holt_klee(s, 5)[0] for s in W512))
t0 = time.time(); W513 = enumerate_walk_ausos(5, 13); say(f'[2] m=5, L=13: {len(W513)} ({time.time()-t0:.1f}s)'); assert len(W513) == 0

def admissible_partitions(s, m, sigma0):
    """all partitions of the cube into subcubes with (F1)-(F4) w.r.t. s and the walk from sigma0."""
    n = 1 << m; trace = ba_trace(s, sigma0)
    # candidate blocks: subcubes on which v ^ s(v) is constant
    blocks = []
    for D in range(n):
        for base in range(n):
            if base & D: continue
            cells = [base | sub for sub in range(n) if sub & ~D == 0]
            if len({v ^ s[v] for v in cells}) == 1: blocks.append((D, tuple(cells)))
    by_v = {v: [b for b in blocks if v in b[1]] for v in range(n)}
    parts = []
    def rec(covered, chosen):
        if len(covered) == n: parts.append(list(chosen)); return
        v = min(set(range(n)) - covered)
        for b in by_v[v]:
            if covered & set(b[1]): continue
            chosen.append(b); rec(covered | set(b[1]), chosen); chosen.pop()
    rec(set(), [])
    good = []
    for P in parts:
        D = [0] * n; A = [0] * n
        for k, (Dk, cells) in enumerate(P):
            for v in cells: D[v] = Dk; A[v] = k
        if any(s[v] & D[v] for v in trace): continue                                   # (F2)
        adj = {k: set() for k in range(len(P))}
        for v in range(n):
            for i in range(m):
                if (s[v] >> i) & 1 and not (D[v] >> i) & 1 and A[v ^ (1 << i)] != A[v]: adj[A[v]].add(A[v ^ (1 << i)])
        col = [0] * len(P); cyc = False
        def dfs(x):
            nonlocal cyc
            col[x] = 1
            for y in adj[x]:
                if col[y] == 1 or (col[y] == 0 and dfs(y)): cyc = True; return True
            col[x] = 2; return False
        for x in range(len(P)):
            if col[x] == 0 and dfs(x): break
        if cyc: continue                                                                # (F3)
        ok = True
        for J, verts in faces(m):
            Sset = [v for v in verts if (s[v] & ~D[v]) & J == 0]
            ks = {A[v] for v in Sset}
            if len(ks) != 1 or set(Sset) != set(P[ks.pop()][1]) & set(verts): ok = False; break
        if not ok: continue                                                              # (F4)
        good.append((P, [(t, v) for t in range(len(trace)) for v in range(m) if (D[trace[t]] >> v) & 1]))
    return trace, good
def flat_report(W, m, L, tag):
    nontriv = 0; xs = {}
    for s in W:
        trace, good = admissible_partitions(s, m, 0)
        assert len(trace) == L + 1 and trace[0] == 0
        nt = [(P, inc) for P, inc in good if any(Dk for Dk, _ in P)]
        assert any(all(not Dk for Dk, _ in P) for P, _ in good)              # the all-singleton partition is admissible
        if not nt: continue
        nontriv += 1; assert len(nt) == 1
        P, inc = nt[0]; big = [(Dk, cells) for Dk, cells in P if Dk]
        assert len(big) == 1 and bin(big[0][0]).count('1') == 1 and set(big[0][1]) == {0, big[0][0]}
        x = big[0][0].bit_length() - 1; assert inc == [(0, x)]; xs[x] = xs.get(x, 0) + 1
    say(f'[2] {tag}: {nontriv} of the {len(W)} admit a partition with a nontrivial block, always unique, always the single edge {{0,e_x}} at the start with the one flat incidence (0,x); x-counts {dict(sorted(xs.items()))}')
    return nontriv, xs
nt4, xs4 = flat_report(W47, 4, 7, 'm=4, L=7 (lem:seven-flat)'); assert nt4 == 24
nt5, xs5 = flat_report(W512, 5, 12, 'm=5, L=12 (mw:twelve-flat)'); assert nt5 == 240 and all(xs5[x] == 48 for x in range(5))

# ---------------------------------------------------------------- [3] the height-13 witness from the game
g = json.load(open(f'{HERE}/H13_m6_WITNESS_GAME.json')); kinds = g['kinds']; succ = g['succ']; N = len(kinds); m = 6
assert set(kinds) == {'max', 'avg'} and kinds[:6] == ['max'] * 6 and kinds.count('avg') == 410 and N == 416
assert all(len(su) == 2 and len(set(su)) == 2 and all(0 <= w <= N + 1 for w in su) for su in succ)
T = set(range(N))
while True:
    drop = {u for u in T if (kinds[u] == 'avg' and any(w not in T for w in succ[u])) or (kinds[u] == 'max' and all(w not in T for w in succ[u]))}
    if not drop: break
    T -= drop
assert not T
say('[3] H13 game: 6 Max, 410 average, two sinks (418 vertices), one-player, every non-sink of out-degree two, greatest trap empty: stopping')
targets = list(range(6)) + [N, N + 1]; law = {}; state = {}
def law_of(u):
    if u in law: return law[u]
    if u >= N or kinds[u] == 'max': vec = {u: F(1)}
    else:
        assert state.get(u) != 1, 'cycle in the average part'; state[u] = 1
        vec = {}
        for w in succ[u]:
            for k, p in law_of(w).items(): vec[k] = vec.get(k, F(0)) + p / 2
        state[u] = 2
    law[u] = vec; return vec
rows = {}
for v in range(6):
    for a in (0, 1):
        rows[(v, a)] = law_of(succ[v][a])
# which sink is t_1: match b
for t1 in (N, N + 1):
    if all(rows[(v, a)].get(t1, 0) == F(g['b'][2 * v + a], g['den']) for v in range(6) for a in (0, 1)): break
else: raise AssertionError('no sink matches b')
t0s = N + 1 if t1 == N else N
A = g['A']; den = g['den']; assert den == 2 ** 14
for v in range(6):
    for a in (0, 1):
        r = rows[(v, a)]
        assert all(r.get(j, 0) == F(A[2 * v + a][j], den) for j in range(6)) and r.get(v, 0) == 0
        leak = r.get(t0s, 0); assert leak == 1 - sum(F(x, den) for x in A[2 * v + a]) - F(g['b'][2 * v + a], den) and leak > 0
minleak = min(1 - sum(F(x, den) for x in A[2 * v + a]) - F(g['b'][2 * v + a], den) for v in range(6) for a in (0, 1))
say(f'[3] the average part is acyclic and the first-passage rows over (x_0..x_5, t_1) are exactly the printed system; p^{{v,a}}_v = 0 throughout; least leak {minleak} = 5/2^14: {minleak == F(5, den)}')
def solve(Mx, rhs):
    n = len(Mx); Tm = [list(map(F, Mx[i])) + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if Tm[r][c] != 0); Tm[c], Tm[p] = Tm[p], Tm[c]
        pv = Tm[c][c]; Tm[c] = [x / pv for x in Tm[c]]
        for r in range(n):
            if r != c and Tm[r][c] != 0:
                f = Tm[r][c]; Tm[r] = [Tm[r][j] - f * Tm[c][j] for j in range(n + 1)]
    return [Tm[i][n] for i in range(n)]
P = {(v, a): [F(A[2 * v + a][j], den) for j in range(6)] for v in range(6) for a in (0, 1)}
Q = {(v, a): F(g['b'][2 * v + a], den) for v in range(6) for a in (0, 1)}
X = {}; s_out = [0] * 64; margin = None
for idx in range(64):
    sig = [(idx >> v) & 1 for v in range(6)]
    Mx = [[F(int(i == j)) - P[(i, sig[i])][j] for j in range(6)] for i in range(6)]
    x = solve(Mx, [Q[(i, sig[i])] for i in range(6)]); X[idx] = x
    for v in range(6):
        gap = sum(P[(v, 1 - sig[v])][j] * x[j] for j in range(6)) + Q[(v, 1 - sig[v])] - x[v]
        assert gap != 0
        if gap > 0: s_out[idx] |= 1 << v
        margin = abs(gap) if margin is None else min(margin, abs(gap))
s_out = tuple(s_out); assert s_out == tuple(g['outmap'])
assert margin == F(226793593012712537793143, 3187971438880543888553754624), margin
assert is_uso(s_out, 6) and is_acyclic(s_out, 6) and is_holt_klee(s_out, 6)[0]
h = ba_heights(s_out, 6); assert max(h) == 13 and {v for v in range(64) if h[v] == 13} == {25, 27, 57, 59}
tr = ba_trace(s_out, 25); assert tr == [25, 14, 33, 6, 37, 46, 45, 44, 16, 40, 0, 8, 28, 12]
Ssets = [sorted(v for v in range(6) if ((tr[t] ^ tr[t + 1]) >> v) & 1) for t in range(13)]
assert Ssets == [[0,1,2,4],[0,1,2,3,5],[0,1,2,5],[0,1,5],[0,1,3],[0,1],[0],[2,3,4,5],[3,4,5],[3,5],[3],[2,4],[4]]
# the all-switches rule from the values, and the value monotonicity
def all_switches(idx):
    run = [idx]
    while True:
        sig = [(idx >> v) & 1 for v in range(6)]; x = X[idx]
        sw = [v for v in range(6) if sum(P[(v, 1 - sig[v])][j] * x[j] for j in range(6)) + Q[(v, 1 - sig[v])] > x[v]]
        if not sw: return run
        idx ^= sum(1 << v for v in sw); run.append(idx)
assert all_switches(25) == tr
for t in range(13):
    a, b = X[tr[t]], X[tr[t + 1]]; assert all(b[j] >= a[j] for j in range(6)) and any(b[j] > a[j] for j in range(6))
longest = max(len(all_switches(i)) - 1 for i in range(64)); assert longest == 13
say(f'[3] 64 exact value vectors: the printed outmap, no tie, least margin as printed; USO, acyclic, Holt-Klee; height 13 exactly at {{25,27,57,59}}; run from 25 and its switched sets as printed; the all-switches rule from the values reproduces the walk with nondecreasing values, strictly increasing somewhere at each step; longest run over 64 starts: {longest}')

# ---------------------------------------------------------------- [4] the level-two block's return
nf = json.load(open(os.path.join(HERE, '..', 'blowup', 'B2_small_nf.json'))); den2 = nf['den']; A2 = nf['A']; b2 = nf['b']
block = [0, 1, 2, 5]; drive = 4; MAX = [0, 1, 2]; pos = {v: i for i, v in enumerate(block)}
assert all(A2[2 * v + a][3] == 0 for v in block for a in (0, 1))
def affine_values(sig, tau):
    acts = {0: sig[0], 1: sig[1], 2: sig[2], 5: tau}
    Mx = [[F(int(i == j)) for j in range(4)] for i in range(4)]; c0 = []; c1 = []
    for i, v in enumerate(block):
        row = A2[2 * v + acts[v]]
        for j, w in enumerate(block): Mx[i][j] -= F(row[w], den2)
        c0.append(F(b2[2 * v + acts[v]], den2)); c1.append(F(row[drive], den2))
    return solve(Mx, c0), solve(Mx, c1)
STR = list(itertools.product((0, 1), repeat=3)); AFF = {(sg, tau): affine_values(sg, tau) for sg in STR for tau in (0, 1)}
def val(sg, t):
    ys = [[u[i] + w[i] * t for i in range(4)] for (u, w) in (AFF[(sg, 0)], AFF[(sg, 1)])]
    return [min(ys[0][i], ys[1][i]) for i in range(4)]
def outmap_t(t):
    s = [0] * 8; tied = []
    for sg in STR:
        y = val(sg, t)
        for i, v in enumerate(MAX):
            row = A2[2 * v + (1 - sg[i])]
            other = sum(F(row[w], den2) * y[pos[w]] for w in block) + F(row[drive], den2) * t + F(b2[2 * v + 1 - sg[i]], den2)
            if other > y[pos[v]]: s[sum(sg[k] << k for k in range(3))] |= 1 << i
            elif other == y[pos[v]]: tied.append((sum(sg[k] << k for k in range(3)), i))
    return tuple(s), tied
fences = [F(47723619, 255897160), F(6856791, 18130160), F(23232377303, 48259671705), F(1368077078, 2659981905), F(3079758983, 5976346345),
          F(4449774213, 8325926890), F(747670031, 1324418625), F(1175936917, 2026652880), F(10168377, 16341335), F(315968817, 435909343),
          F(1070103399, 1278421945), F(16114985061, 18836958955), F(2267378637, 2318632595)]
assert fences == sorted(fences)
bounds = [F(0)] + fences + [F(1)]
cells = []
for j in range(14):
    s, tied = outmap_t((bounds[j] + bounds[j + 1]) / 2); assert not tied; cells.append(s)
route_cells = [(0,1,3,6,7,4,5,2),(0,1,3,6,5,4,7,2),(0,1,3,2,5,4,7,6),(1,0,3,2,5,4,7,6),(5,0,3,2,1,4,7,6),(5,4,3,2,1,0,7,6),(5,4,7,2,1,0,3,6),
               (5,4,7,2,0,1,3,6),(7,4,5,2,0,1,3,6),(7,4,5,6,0,1,3,2),(7,6,5,4,0,1,3,2),(7,6,5,4,0,1,2,3),(7,6,4,5,0,1,2,3),(7,6,4,5,0,3,2,1)]
assert cells == route_cells
B1 = (0,1,3,6,7,4,5,2); assert cells[0] == B1 and cells[8] == tuple(B1[v ^ 4] for v in range(8))
names = {0: 'seed', 1: 'alpha_1', 2: 'beta_1'}; reversed_edges = []
for j in range(13):
    s1, s2 = cells[j], cells[j + 1]
    diff = [(v, k) for v in range(8) for k in range(3) if not (v >> k) & 1 and ((s1[v] >> k) & 1) != ((s2[v] >> k) & 1)]
    assert len(diff) == 1 and s1[diff[0][0]] ^ s1[diff[0][0] ^ (1 << diff[0][1])] == 1 << diff[0][1]      # one edge, satisfying the criterion
    _, tied = outmap_t(fences[j]); tied_edges = {(min(v, v ^ (1 << i)), i) for v, i in tied}
    assert tied_edges == {diff[0]}, (j, tied_edges, diff)                                                   # simple fence: exactly that edge ties
    reversed_edges.append(diff[0])
say('[4] level-two block: the 14 cells between the 13 fences of rem:pinned-escape are the route\'s; every fence ties exactly one edge, the one reversed; reversed in order:', ', '.join(f'({v},{names[k]})' for v, k in reversed_edges))
assert reversed_edges == [(4,1),(3,2),(0,0),(0,2),(1,2),(2,2),(4,0),(0,1),(3,2),(1,1),(6,0),(2,0),(5,1)]
assert reversed_edges.count((3, 2)) == 2
fd = sum(bin(cells[0][v] ^ cells[13][v]).count('1') for v in range(8)) // 2; assert fd == 11
hts = [max(ba_heights(c, 3)) for c in cells]; assert all(is_uso(c, 3) and is_acyclic(c, 3) and is_holt_klee(c, 3)[0] for c in cells)
assert hts == [4,3,2,1,2,2,2,3,4,3,3,2,2,3]
say(f'[4] the first fence reverses (4,alpha_1) -- the route printed (4,beta_1); {{3,7}} in direction beta_1 is reversed twice (2nd and 9th fences); flip distance first->last cell {fd} against 13 fences; all 14 cells Holt-Klee AUSOs of heights {hts}')
say('M6-WALK ROUTE: [1]-[4] reproduced from the statements')
