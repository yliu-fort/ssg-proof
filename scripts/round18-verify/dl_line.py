#!/usr/bin/env python3
"""The drive line of the level-two block, recomputed from the paper's normal form (scripts/blowup/B2_small_nf.json,
prop:b2-realised: controlled vertices c1..c6 = seed, alpha_1, beta_1, alpha_2, beta_2, c_min; two rows per vertex over
the six targets and t_1, denominator 512). Block = {c1,c2,c3,c6} (three Max, one Min), driven by t = y_{c5}; no block
row reads c4. For every t the block is a stopping game whose values are affine in t under each (sigma,tau); the
improvement outmap s_B(t) on the 3-cube is computed exactly, all candidate fences (Min switches and margin roots) are
collected, and the maximal cells are reported. Claims (dl:b2-line, dl:drive-flip): 14 cells, 13 fences, every fence
simple (one tied edge pair), the reversed edge combed on the left; cells from B^1 = (0,1,3,6,7,4,5,2) to
B^1(.^e_beta1) = (7,4,5,2,0,1,3,6) in 8 fences = d(B^1, B^1(.^4))."""
import json, itertools, sys, os
from fractions import Fraction as F
nf = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'blowup', 'B2_small_nf.json')))
den = nf['den']; A = nf['A']; b = nf['b']
block = [0, 1, 2, 5]          # c1, c2, c3, c6
drive = 4                     # c5
MAX = [0, 1, 2]; MIN = [5]
assert all(A[2*v + a][3] == 0 for v in block for a in (0, 1)), 'a block row reads c4'
pos = {v: i for i, v in enumerate(block)}

def solve(M, rhs):
    n = len(M); Mx = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if Mx[r][c] != 0); Mx[c], Mx[p] = Mx[p], Mx[c]
        pv = Mx[c][c]; Mx[c] = [x / pv for x in Mx[c]]
        for r in range(n):
            if r != c and Mx[r][c] != 0:
                f = Mx[r][c]; Mx[r] = [Mx[r][j] - f * Mx[c][j] for j in range(n+1)]
    return [Mx[i][n] for i in range(n)]

def affine_values(sig, tau):
    """values of the block under (sigma, tau) as affine functions of t: returns (u, w) with y = u + w t."""
    acts = {0: sig[0], 1: sig[1], 2: sig[2], 5: tau}
    M = [[F(int(i == j)) for j in range(4)] for i in range(4)]; c0 = []; c1 = []
    for i, v in enumerate(block):
        row = A[2*v + acts[v]]
        for j, w in enumerate(block): M[i][j] -= F(row[w], den)
        c0.append(F(b[2*v + acts[v]], den)); c1.append(F(row[drive], den))
    return solve(M, c0), solve(M, c1)

STRATS = list(itertools.product((0, 1), repeat=3))
AFF = {(s, tau): affine_values(s, tau) for s in STRATS for tau in (0, 1)}

def val(sig, t):
    ys = [[u[i] + w[i]*t for i in range(4)] for (u, w) in (AFF[(sig, 0)], AFF[(sig, 1)])]
    return [min(ys[0][i], ys[1][i]) for i in range(4)]

def row_value(v, a, y, t):
    row = A[2*v + a]
    return sum(F(row[w], den) * y[pos[w]] for w in block) + F(row[drive], den) * t + F(b[2*v + a], den)

def outmap(t):
    s = [0] * 8; tied = []
    for sig in STRATS:
        y = val(sig, t); out = 0
        for i, v in enumerate(MAX):
            other = row_value(v, 1 - sig[i], y, t); mine = y[pos[v]]
            if other > mine: out |= 1 << i
            elif other == mine: tied.append((sig, i))
        s[sum(sig[i] << i for i in range(3))] = out      # little-endian: vertex index bit i = coordinate i
    return tuple(s), tied

# candidate fences: Min switches (crossings of the two tau-values) and margin roots on each tau-piece
cands = set()
for sig in STRATS:
    (u0, w0), (u1, w1) = AFF[(sig, 0)], AFF[(sig, 1)]
    for i in range(4):
        if w0[i] != w1[i]:
            t = (u1[i] - u0[i]) / (w0[i] - w1[i])
            if 0 < t < 1: cands.add(t)
    for tau in (0, 1):
        u, w = AFF[(sig, tau)]
        for i, v in enumerate(MAX):
            row = A[2*v + (1 - sig[i])]
            # margin(t) = row.(u + w t) + r t + q - (u_v + w_v t)
            a0 = sum(F(row[x], den) * u[pos[x]] for x in block) + F(b[2*v + 1 - sig[i]], den) - u[pos[v]]
            a1 = sum(F(row[x], den) * w[pos[x]] for x in block) + F(row[drive], den) - w[pos[v]]
            if a1 != 0:
                t = -a0 / a1
                if 0 < t < 1: cands.add(t)
pts = sorted(cands)
cells = []; prev = None; bounds = [F(0)] + pts + [F(1)]
for j in range(len(bounds) - 1):
    mid = (bounds[j] + bounds[j+1]) / 2
    s, tied = outmap(mid); assert not tied, ('degenerate cell', mid)
    if prev is None or s != prev[0]: cells.append([s, bounds[j], bounds[j+1]]); prev = cells[-1]
    else: prev[2] = bounds[j+1]
print(f'{len(cells)} cells, {len(cells)-1} fences')
B1 = (0,1,3,6,7,4,5,2); B1t = tuple(B1[v ^ 4] for v in range(8))
def combed(s, v, k): return (v ^ s[v]) == ((v ^ (1 << k)) ^ s[v ^ (1 << k)])
simple = 0
for j, (s, lo, hi) in enumerate(cells):
    print(f'  cell {j}: {s}  on ({lo}, {hi})' + ('  = B^1' if s == B1 else '') + ('  = B^1(.^e_beta1)' if s == B1t else ''))
    if j + 1 < len(cells):
        t = hi; s2, tied = outmap(t)
        diff = [(v, k) for v in range(8) for k in range(3) if not (v >> k) & 1 and ((s[v] >> k) & 1) != ((cells[j+1][0][v] >> k) & 1)]
        pairs = {(sig, i) for sig, i in tied}
        ok = len(diff) == 1 and len(pairs) == 2 and combed(s, diff[0][0], diff[0][1])
        simple += ok
        print(f'     fence {t}: tied incidences {sorted(pairs)}, edges reversed {diff}, simple & combed: {ok}')
iB1 = [j for j, c in enumerate(cells) if c[0] == B1]; iB1t = [j for j, c in enumerate(cells) if c[0] == B1t]
d = sum(1 for v in range(8) for k in range(3) if not (v >> k) & 1 and ((B1[v] >> k) & 1) != ((B1t[v] >> k) & 1))
print(f'B^1 at cell {iB1}, its translate at cell {iB1t}: {iB1t[0]-iB1[0]} fences apart; d(B^1, B^1(.^4)) = {d}; simple combed fences: {simple} of {len(cells)-1}')
assert len(cells) == 14 and simple == 13 and iB1 == [0] and iB1t == [8] and d == 8
print('DRIVE LINE OF THE LEVEL-TWO BLOCK CONFIRMED')
