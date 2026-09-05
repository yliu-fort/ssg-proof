#!/usr/bin/env python3
"""Root agent's verification of the round-19 escape-certificate route, from the statements and the normal form
scripts/blowup/B2_small_nf.json (the level-two game of prop:b2-realised), not from the route's code.

Checked here, all in exact rational arithmetic:
 [1] the drive line of the level-two block {c1,c2,c3,c6} driven by t = y_{c5}: cells, fences (against
     rem:pinned-escape's 13 fences), the refined breakpoints, and that every y_sigma is affine between them;
 [2] the identity A' rho(sigma,t) = (f10(t) - t) + Delta (t - f00(t)) on random parameters, and the second one
     A'' rho = (f11 - t) + Delta'' (t - f01);
 [3] the targets B^2(. xor z): the first-shape tournament (P,Q,R) at every sigma, the inner windows (LOW = the block
     presents B^1 at sigma, HIGH = B^1(. xor e_beta1)), their pruning by the arcs, sup LOW_4 = b, inf HIGH_0 = a,
     LOW inside [0,T];
 [4] the 104 Farkas certificates of the domination lemma, against rows rebuilt here;
 [5] the second-shape level theorem on the route's two games, from the games (values by brute force over all
     positional pairs, outmap, nondegeneracy, stopping), and its tournament / window verdicts for the four z.
"""
import sys, os, json, itertools, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'harness'))
from mycore import G, is_stopping, profile_value
R19 = '/tmp/claude-1000/-data-ssg-proof/c506180a-e393-4ffa-a18f-efc78c98397e/scratchpad/r19-escape-certificate'
nf = json.load(open(os.path.join(HERE, '..', 'blowup', 'B2_small_nf.json')))
den = nf['den']; A = nf['A']; bq = nf['b']; B2 = tuple(nf['target'])
BLOCK = [0, 1, 2, 5]; MAXB = [0, 1, 2]; MINB = 5; DRIVE = 4; ALPHA = 3
pos = {v: i for i, v in enumerate(BLOCK)}
assert all(A[2 * v + a][ALPHA] == 0 for v in BLOCK for a in (0, 1))

def solve(M, rhs):
    n = len(M); Mx = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if Mx[r][c] != 0); Mx[c], Mx[p] = Mx[p], Mx[c]
        pv = Mx[c][c]; Mx[c] = [x / pv for x in Mx[c]]
        for r in range(n):
            if r != c and Mx[r][c] != 0:
                f = Mx[r][c]; Mx[r] = [Mx[r][j] - f * Mx[c][j] for j in range(n + 1)]
    return [Mx[i][n] for i in range(n)]

SIG = list(itertools.product((0, 1), repeat=3))
def sidx(s): return s[0] | (s[1] << 1) | (s[2] << 2)

def affine(sig, tau):
    """y = u + w t for the block frozen at (sig, tau)."""
    acts = {0: sig[0], 1: sig[1], 2: sig[2], 5: tau}
    M = [[F(int(i == j)) for j in range(4)] for i in range(4)]; c0 = []; c1 = []
    for i, v in enumerate(BLOCK):
        row = A[2 * v + acts[v]]
        for j, w in enumerate(BLOCK): M[i][j] -= F(row[w], den)
        c0.append(F(bq[2 * v + acts[v]], den)); c1.append(F(row[DRIVE], den))
    return solve(M, c0), solve(M, c1)
AFF = {(s, tau): affine(s, tau) for s in SIG for tau in (0, 1)}

def y_of(sig, t):
    vals = [[u[i] + w[i] * t for i in range(4)] for (u, w) in (AFF[(sig, 0)], AFF[(sig, 1)])]
    return [min(vals[0][i], vals[1][i]) for i in range(4)]

def read(v, a, y, t):
    row = A[2 * v + a]
    return sum(F(row[w], den) * y[pos[w]] for w in BLOCK) + F(row[DRIVE], den) * t + F(bq[2 * v + a], den)

def outmap(t):
    s = [0] * 8; tied = []
    for sig in SIG:
        y = y_of(sig, t); m = 0
        for i, v in enumerate(MAXB):
            o = read(v, 1 - sig[i], y, t)
            if o > y[pos[v]]: m |= 1 << i
            elif o == y[pos[v]]: tied.append((sig, i))
        s[sidx(sig)] = m
    return tuple(s), tied

# [1] breakpoints: Min crossings and margin roots on each tau-piece
cand = set()
for sig in SIG:
    (u0, w0), (u1, w1) = AFF[(sig, 0)], AFF[(sig, 1)]
    for i in range(4):
        if w0[i] != w1[i]:
            t = (u1[i] - u0[i]) / (w0[i] - w1[i])
            if 0 < t < 1: cand.add(t)
    for tau in (0, 1):
        u, w = AFF[(sig, tau)]
        for i, v in enumerate(MAXB):
            row = A[2 * v + 1 - sig[i]]
            a0 = sum(F(row[x], den) * u[pos[x]] for x in BLOCK) + F(bq[2 * v + 1 - sig[i]], den) - u[pos[v]]
            a1 = sum(F(row[x], den) * w[pos[x]] for x in BLOCK) + F(row[DRIVE], den) - w[pos[v]]
            if a1 != 0:
                t = -a0 / a1
                if 0 < t < 1: cand.add(t)
BP = sorted(cand); BOUNDS = [F(0)] + BP + [F(1)]
# pieces on which every y_sigma is affine: check by a third point
for lo, hi in zip(BOUNDS, BOUNDS[1:]):
    for sig in SIG:
        ya, yb, ym = y_of(sig, lo), y_of(sig, hi), y_of(sig, (lo + hi) / 2)
        assert all(ym[i] == (ya[i] + yb[i]) / 2 for i in range(4)), ('not affine', sig, lo, hi)
        yq = y_of(sig, lo + (hi - lo) / 3); assert all(yq[i] == ya[i] + (yb[i] - ya[i]) / 3 for i in range(4))
# cells of the outmap
cells = []
for lo, hi in zip(BOUNDS, BOUNDS[1:]):
    s, tied = outmap((lo + hi) / 2); assert not tied
    if cells and cells[-1][2] == s: cells[-1] = (cells[-1][0], hi, s)
    else: cells.append((lo, hi, s))
fences = [c[0] for c in cells[1:]]
PAPER_FENCES = [F(47723619, 255897160), F(6856791, 18130160), F(23232377303, 48259671705), F(1368077078, 2659981905), F(3079758983, 5976346345), F(4449774213, 8325926890), F(747670031, 1324418625), F(1175936917, 2026652880), F(10168377, 16341335), F(315968817, 435909343), F(1070103399, 1278421945), F(16114985061, 18836958955), F(2267378637, 2318632595)]
assert len(cells) == 14 and fences == PAPER_FENCES, (len(cells), fences[:3])
B1 = tuple(cells[0][2]); B1T = tuple(cells[8][2])
assert B1 == (0, 1, 3, 6, 7, 4, 5, 2) and B1T == tuple(B1[s ^ 4] for s in range(8))   # B^1 and B^1(. xor e_beta1)
print(f'[1] drive line: 14 cells, the 13 fences of rem:pinned-escape reproduced; {len(BP)} refined breakpoints; every y_sigma affine between consecutive breakpoints; cell 0 = B^1, cell 8 = B^1(. xor e_beta1)')
b_const = PAPER_FENCES[0]; a_const = PAPER_FENCES[7]; T_const = PAPER_FENCES[8]

# [2] the identities on random parameters
rng = random.Random(19)
def rnd_row(k):
    w = [F(rng.randrange(0, 20), 100) for _ in range(k)]; return w
for _ in range(300):
    A_ = F(rng.randrange(1, 100), 128); Ap = F(rng.randrange(1, 100), 128); App = F(rng.randrange(0, 40), 128)
    Ca, Cb, Ra, Rb = rnd_row(4), rnd_row(4), rnd_row(4), rnd_row(4)
    qA, qpA, qB, qpB = [F(rng.randrange(0, 10), 100) for _ in range(4)]
    D = 1 - A_ * Ap; Dpp = 1 - A_ * App
    sig = rng.choice(SIG); t = F(rng.randrange(0, 1000), 1000); y = y_of(sig, t)
    dot = lambda c, y: sum(c[i] * y[i] for i in range(4))
    rho = dot([Ra[i] - Ca[i] for i in range(4)], y) + (qpA - qA) - A_ * t
    f00 = (dot([Ap * Ca[i] + Cb[i] for i in range(4)], y) + Ap * qA + qB) / D
    f10 = dot([Ap * Ra[i] + Cb[i] for i in range(4)], y) + Ap * qpA + qB
    assert Ap * rho == (f10 - t) + D * (t - f00)
    f01 = (dot([App * Ca[i] + Rb[i] for i in range(4)], y) + App * qA + qpB) / Dpp
    f11 = dot([App * Ra[i] + Rb[i] for i in range(4)], y) + App * qpA + qpB
    assert App * rho == (f11 - t) + Dpp * (t - f01)
print('[2] both identities A\' rho = (f10 - t) + Delta (t - f00) and A\'\' rho = (f11 - t) + Delta\'\' (t - f01) hold on 300 random parameter sets')

# [3] the targets. Coordinates: bit i <-> c_{i+1}; alpha = c4 = bit 3, beta = c5 = bit 4.
def target(z):
    return {(sig, (a, b)): B2[(sidx(sig) | (a << 3) | (b << 4)) ^ z] for sig in SIG for a in (0, 1) for b in (0, 1)}
def window(sig, mask):
    """closed cells (as [lo,hi]) on which the block presents `mask` at sigma."""
    return [(lo, hi) for lo, hi, s in cells if s[sidx(sig)] == mask]
def first_shape(z, verbose=False):
    T = target(z); bits = {}
    for sig in SIG:
        P = (T[(sig, (0, 0))] >> 3) & 1; Q = (T[(sig, (0, 0))] >> 4) & 1
        R = (T[(sig, (1, 0))] >> 4) & 1; S = (T[(sig, (0, 1))] >> 3) & 1
        # consistency of the four layers with thm:escape-level's (P,Q,R,S) and w01 = w11
        ok = ((T[(sig, (1, 0))] >> 3) & 1 == 1 - P) and ((T[(sig, (0, 1))] >> 4) & 1 == 1 - Q) and ((T[(sig, (1, 1))] >> 3) & 1 == 1 - S) and ((T[(sig, (1, 1))] >> 4) & 1 == 1 - R)
        tour = (P, Q, R) not in ((1, 0, 1), (0, 1, 0))
        bits[sig] = (P, Q, R, S, ok, tour)
    if not all(v[4] and v[5] for v in bits.values()):
        return bits, None
    # windows per drive: w00 on layer (0,0), w10 on (1,0), w01 on (0,1) (= w11, layer (1,1) must agree)
    W = {}
    for sig in SIG:
        for L in ((0, 0), (1, 0), (0, 1)):
            W[(L, sig)] = window(sig, T[(sig, L)] & 7)
        if (T[(sig, (0, 1))] & 7) != (T[(sig, (1, 1))] & 7): W[((0, 1), sig)] = []
    # prune by the arcs P: w00<w10, Q: w00<w01, R: w10<w01 (bit 1 means the left is smaller)
    def prune():
        changed = False
        for sig in SIG:
            P, Q, R = bits[sig][:3]
            for u, v, bit in ((((0, 0), sig), ((1, 0), sig), P), (((0, 0), sig), ((0, 1), sig), Q), (((1, 0), sig), ((0, 1), sig), R)):
                small, big = (u, v) if bit else (v, u)
                if not W[small] or not W[big]: continue
                hi_big = max(iv[1] for iv in W[big]); lo_small = min(iv[0] for iv in W[small])
                new = [iv for iv in W[small] if iv[0] < hi_big]
                if new != W[small]: W[small] = new; changed = True
                new = [iv for iv in W[big] if iv[1] > lo_small]
                if new != W[big]: W[big] = new; changed = True
        return changed
    while prune(): pass
    return bits, W
for z in (8, 10, 24, 26):
    bits, W = first_shape(z)
    if W is None:
        bad = [sig for sig in SIG if not (bits[sig][4] and bits[sig][5])]
        print(f'[3] z={z}: first shape killed by the tournament / layer consistency at sigma {sorted(map(sidx, bad))} (thm:escape-no-beta)'); continue
    empty = [(L, sidx(sig)) for (L, sig), w in W.items() if not w]
    if empty:
        print(f'[3] z={z}: first shape killed by empty windows at {empty[:6]} (inner reason)'); continue
    def merge(ivs):
        out = []
        for lo, hi in sorted(ivs):
            if out and out[-1][1] == lo: out[-1] = (out[-1][0], hi)
            else: out.append((lo, hi))
        return out
    LOW = {sig: merge(W[((0, 0), sig)]) for sig in SIG}; HIGH = {sig: merge(W[((1, 0), sig)]) for sig in SIG}
    assert all(len(LOW[s]) == 1 and len(HIGH[s]) == 1 for s in SIG), 'not one merged LOW and HIGH window per sigma'
    assert all(merge(W[((0, 1), s)]) == LOW[s] for s in SIG), 'w01 window differs from LOW'
    assert all(LOW[s][0][1] <= T_const for s in SIG) and LOW[(0, 0, 1)][0][1] == b_const and HIGH[(0, 0, 0)][0][0] == a_const
    assert all(bits[s][:3] == (1, 0, 0) for s in SIG if sidx(s) in (1, 3, 7)) and all(bits[s][3] == 0 for s in SIG if sidx(s) in (1, 3, 7))
    print(f'[3] z={z}: first shape survives tournament and inner condition; one LOW and one HIGH window per sigma, w01 in LOW; sup LOW_4 = b, inf HIGH_0 = a, every LOW window inside [0,T]; at sigma in {{1,3,7}}: (P,Q,R,S) = (1,0,0,0), i.e. w01 < w00 < w10 and rho(sigma, w01) < 0')

# [4] the Farkas certificates of the domination lemma, against rows rebuilt here
C = json.load(open(os.path.join(R19, 'ec_minimal_certs.json')))
assert F(C['b']) == b_const and F(C['a']) == a_const and F(C['tmax']) == T_const
PTS = [F(0)] + [t for t in BP if t <= T_const]
assert [F(t) for t in C['points']] == PTS and len(PTS) == 13
NV = 10   # c_lo[0..3], d_lo, c_hi[0..3], d_hi
rows = []
for off in (0, 5):
    for i in range(5):
        r = [F(0)] * NV; r[off + i] = F(-1); rows.append((r, F(0), False))           # x >= 0
    r = [F(0)] * NV
    for i in range(5): r[off + i] = F(1)
    rows.append((r, F(1), True))                                                       # sum < 1
y4 = y_of((0, 0, 1), b_const); r = [F(0)] * NV
for i in range(4): r[i] = y4[i]
r[4] = F(1); rows.append((r, b_const, True))                                           # c_lo.y_4(b) + d_lo < b
y0 = y_of((0, 0, 0), a_const); r = [F(0)] * NV
for i in range(4): r[5 + i] = -y0[i]
r[9] = F(-1); rows.append((r, -a_const, True))                                         # -(c_hi.y_0(a) + d_hi) < -a
file_rows = [([F(v) for v in R['a']], F(R['b']), R['strict']) for R in C['rows']]
assert rows == file_rows, 'the certificate file rows differ from the rows rebuilt here'
nc = 0
for sig in SIG:
    for t in PTS:
        key = f'{sidx(sig)}|{t}'; cert = C['certs'][key]; y = y_of(sig, t)
        obj = [F(0)] * NV
        for i in range(4): obj[i] = -y[i]; obj[5 + i] = y[i]
        obj[4] = F(-1); obj[9] = F(1)                                                  # (c_lo - c_hi).y + d_lo - d_hi > 0  <=>  obj.x < 0
        Am = [q[0] for q in rows] + [obj]; bv = [q[1] for q in rows] + [F(0)]; st = [q[2] for q in rows] + [True]
        lam = [F(v) for v in cert['y']]; assert len(lam) == len(Am) and all(l >= 0 for l in lam)
        for j in range(NV): assert sum(lam[i] * Am[i][j] for i in range(len(Am))) == 0
        lb = sum(lam[i] * bv[i] for i in range(len(Am)))
        assert lb < 0 or (lb == 0 and any(lam[i] > 0 and st[i] for i in range(len(Am)))), key
        nc += 1
# the base system is feasible (so the certificates are not vacuous): c = 0, d_lo = 0, d_hi = (a+1)/2
x = [F(0)] * NV; x[9] = (a_const + 1) / 2
for (r, bb, strict) in rows:
    v = sum(r[j] * x[j] for j in range(NV)); assert v < bb if strict else v <= bb
print(f'[4] {nc} Farkas certificates verified against rows rebuilt here (8 sigma x 13 branch points); the base system is feasible; hence c_lo.y_sigma(t)+d_lo <= c_hi.y_sigma(t)+d_hi on [0,T] for every substochastic pair with Phi_4(lo) < b, Phi_0(hi) > a')
# the maximum of a per-piece affine function over [0,T] sits at a branch point: the branch points are all refined
# breakpoints below T plus 0 (and T itself is a breakpoint)
assert T_const in BP and all(t in PTS for t in BP if t <= T_const)

# [5] the second shape: level theorem on the two games, from the games
def fixed_point(sig, c, d):
    """the unique t with t = c.y_sigma(t) + d (c >= 0, |c|_1 + d < 1), piecewise affine search."""
    for lo, hi in zip(BOUNDS, BOUNDS[1:]):
        ya, yb = y_of(sig, lo), y_of(sig, hi)
        ga = sum(c[i] * ya[i] for i in range(4)) + d - lo; gb = sum(c[i] * yb[i] for i in range(4)) + d - hi
        if ga >= 0 >= gb:
            if ga == gb: return lo
            return lo + (hi - lo) * ga / (ga - gb)
    raise ValueError('no fixed point')
def predict(params):
    A_ = F(params['A']); Ap = F(params['Ap']); App = F(params['App'])
    Ca = [F(x) for x in params['Ca']]; Cb = [F(x) for x in params['Cb']]; Ra = [F(x) for x in params['Ra']]; Rb = [F(x) for x in params['Rb']]
    qA, qpA, qB, qpB = F(params['qA']), F(params['qpA']), F(params['qB']), F(params['qpB'])
    D = 1 - A_ * Ap; Dpp = 1 - A_ * App
    maps = {(0, 0): ([(Ap * Ca[i] + Cb[i]) / D for i in range(4)], (Ap * qA + qB) / D),
            (1, 0): ([Ap * Ra[i] + Cb[i] for i in range(4)], Ap * qpA + qB),
            (0, 1): ([(App * Ca[i] + Rb[i]) / Dpp for i in range(4)], (App * qA + qpB) / Dpp),
            (1, 1): ([App * Ra[i] + Rb[i] for i in range(4)], App * qpA + qpB)}
    for c, d in maps.values(): assert all(x >= 0 for x in c) and d >= 0 and sum(c) + d < 1
    out = [0] * 32
    for sig in SIG:
        w = {L: fixed_point(sig, *maps[L]) for L in maps}
        inner = {L: outmap(w[L])[0][sidx(sig)] for L in maps}
        oa = {(0, 0): w[(0, 0)] < w[(1, 0)], (0, 1): w[(0, 1)] < w[(1, 1)]}; oa[(1, 0)] = not oa[(0, 0)]; oa[(1, 1)] = not oa[(0, 1)]
        ob = {(0, 0): w[(0, 0)] < w[(0, 1)], (1, 0): w[(1, 0)] < w[(1, 1)]}; ob[(0, 1)] = not ob[(0, 0)]; ob[(1, 1)] = not ob[(1, 0)]
        for (a, b) in maps:
            out[sidx(sig) | (a << 3) | (b << 4)] = inner[(a, b)] | (int(oa[(a, b)]) << 3) | (int(ob[(a, b)]) << 4)
    return tuple(out)
def outmap_from_game(g):
    maxv = g.of('max'); minv = g.of('min'); res = {}
    for sig in itertools.product(range(2), repeat=len(maxv)):
        best = None
        for tau in itertools.product(range(2), repeat=len(minv)):
            s = {v: g.succ[v][sig[i]] for i, v in enumerate(maxv)}; tt = {u: g.succ[u][tau[j]] for j, u in enumerate(minv)}
            vals = profile_value(g, s, tt)
            best = vals if best is None else [min(x, y) for x, y in zip(best, vals)]
        res[sig] = best
    return maxv, res
for fn, N in (('EC_SHAPE2_GAME.json', 138), ('EC_SHAPE2B_GAME.json', 149)):
    gj = json.load(open(os.path.join(R19, fn))); g = G(gj['kinds'], [tuple(s) for s in gj['succ']])
    assert g.N == N and is_stopping(g)
    maxv, vals = outmap_from_game(g); assert len(maxv) == 5
    # the Max vertices in the game: which is which? match by the prediction: try to identify c1,c2,c3,alpha,beta by the outmap
    out = [0] * 32; nondeg = True
    for sig, val in vals.items():
        m = 0
        for i, v in enumerate(maxv):
            other = val[g.succ[v][1 - sig[i]]]
            if other > val[v]: m |= 1 << i
            elif other == val[v]: nondeg = False
        out[sum(sig[i] << i for i in range(5))] = m
    assert nondeg
    assert tuple(out) == tuple(gj['outmap']), (fn, 'outmap from the game differs from the file')
    pred = predict(gj['params'])
    assert pred == tuple(out), (fn, 'level theorem prediction differs from the game')
    print(f'[5] {fn}: {N} vertices, stopping, nondegenerate; the outmap from the game (brute force over all 64 pairs) equals the file and equals the second-shape level theorem\'s prediction from the four drives')
# second-shape tournament and windows for the four z
def second_shape(z):
    T = target(z); res = {}
    for sig in SIG:
        bitsL = {L: ((T[(sig, L)] >> 3) & 1, (T[(sig, L)] >> 4) & 1) for L in ((0, 0), (1, 0), (0, 1), (1, 1))}
        # antipodal complementarity and acyclicity of the 4 arcs
        okc = bitsL[(1, 0)][0] == 1 - bitsL[(0, 0)][0] and bitsL[(1, 1)][0] == 1 - bitsL[(0, 1)][0] and bitsL[(0, 1)][1] == 1 - bitsL[(0, 0)][1] and bitsL[(1, 1)][1] == 1 - bitsL[(1, 0)][1]
        arcs = []   # (smaller, larger)
        arcs.append(((0, 0), (1, 0)) if bitsL[(0, 0)][0] else ((1, 0), (0, 0)))
        arcs.append(((0, 1), (1, 1)) if bitsL[(0, 1)][0] else ((1, 1), (0, 1)))
        arcs.append(((0, 0), (0, 1)) if bitsL[(0, 0)][1] else ((0, 1), (0, 0)))
        arcs.append(((1, 0), (1, 1)) if bitsL[(1, 0)][1] else ((1, 1), (1, 0)))
        # acyclic iff no directed 4-cycle: check by topological sort
        nodes = [(0, 0), (1, 0), (0, 1), (1, 1)]; indeg = {n: 0 for n in nodes}
        for s, l in arcs: indeg[l] += 1
        order = []; rem = set(nodes)
        while rem:
            src = [n for n in rem if indeg[n] == 0]
            if not src: break
            n = src[0]; order.append(n); rem.remove(n)
            for s, l in arcs:
                if s == n: indeg[l] -= 1
        acyc = not rem
        wins = {L: window(sig, T[(sig, L)] & 7) for L in nodes}
        res[sig] = (okc, acyc, order, wins)
    return res
for z in (8, 10, 24, 26):
    res = second_shape(z)
    assert all(r[0] and r[1] for r in res.values()), f'z={z}: second-shape tournament fails'
    empties = sum(1 for r in res.values() for w in r[3].values() if not w)
    print(f'[5] z={z}: second shape passes the tournament at every sigma (total orders of the four drives); empty inner windows: {empties} of 32' + ('' if empties else ' -- goes to the certificate: ' + ('w00,w01,w11 LOW, w10 HIGH' if z == 8 else 'w00,w10,w01 LOW, w11 HIGH')))
    if not empties:
        T = target(z)
        for sig in SIG:
            for L in ((0, 0), (1, 0), (0, 1), (1, 1)):
                m = T[(sig, L)] & 7
                assert m in (B1[sidx(sig)], B1T[sidx(sig)])
                is_high = m == B1T[sidx(sig)] and B1[sidx(sig)] != B1T[sidx(sig)]
                if L == ((1, 0) if z == 8 else (1, 1)): assert is_high or B1[sidx(sig)] == B1T[sidx(sig)]
print('ESCAPE-CERTIFICATE ROUTE: every load-bearing computation reproduced from the normal form and the games')
