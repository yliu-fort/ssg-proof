#!/usr/bin/env python3
"""dl:escape-level checked on prop:b2-realised's normal form: with the level-two block driven by t = y_{c5} and the outer
pair (alpha, beta) = (c4, c5) whose rest actions read each other (A = 502/512, q_A = 8/512; A' = 509/512, q_B = 0) and
whose other actions read the block (R_alpha = row of c4's action 1, R_beta = row of c5's action 1), the theorem says: the
drive on the layers (0,0),(1,0),(0,1),(1,1) is w00, w10, w01, w01, the inner outmap at (sigma, L) is s_B(w_L(sigma))(sigma),
and the outer bits are P=[w00<w10], Q=[w00<w01], R=[w10<w01], S=[rho(sigma,w01)>0] with O_(0,0)=(P,Q), O_(1,0)=(1-P,R),
O_(0,1)=(S,1-Q), O_(1,1)=(1-S,1-R). The whole 5-cube outmap so assembled must be the paper's B^2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from dl_line import A, b, den, block, drive, MAX, pos, STRATS, AFF, val, outmap

def fixed_point(sig, c, d):
    """the unique t in [0,1] with t = c . y_sigma(t) + d, y_sigma piecewise affine (min over tau of two affine maps)."""
    f = lambda t: sum(F(c[w], den) * val(sig, t)[pos[w]] for w in block) + d
    # candidates: on each tau-piece the equation is affine; solve for both tau and keep the consistent one
    sols = []
    for tau in (0, 1):
        u, w = AFF[(sig, tau)]
        a0 = sum(F(c[x], den) * u[pos[x]] for x in block) + d; a1 = sum(F(c[x], den) * w[pos[x]] for x in block)
        if a1 != 1:
            t = a0 / (1 - a1)
            if 0 <= t <= 1 and f(t) == t: sols.append(t)
    assert len(set(sols)) == 1, (sig, sols)
    return sols[0]

Aq = F(A[6][4], den); qA = F(b[6], den)          # c4 action 0: A y_beta + q_A
Ap = F(A[8][3], den); qB = F(b[8], den)          # c5 action 0: A' y_alpha + q_B
Ralpha = A[7]; qpA = F(b[7], den)                # c4 action 1 reads the block
Rbeta = A[9]; qpB = F(b[9], den)                 # c5 action 1 reads the block
assert all(A[6][w] == 0 and A[8][w] == 0 for w in block) and A[7][3] == A[7][4] == 0 and A[9][3] == A[9][4] == 0
Delta = 1 - Aq * Ap
ehat = (Ap * qA + qB) / Delta                     # C_alpha = C_beta = 0 here (the pinned shape)
D1 = [Ap * F(Ralpha[w], 1) for w in range(6)]     # in units of 1/den
zero = [0]*6
B2 = (7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18)
out = [None]*32; mism = 0
print(f'Theta_w = e-hat = {ehat} (paper: 2036/3313), Theta_u = A Theta_w + q_A = {Aq*ehat + qA} (paper: 2048/3313)')
for sig in STRATS:
    w00 = fixed_point(sig, zero, ehat)
    w10 = fixed_point(sig, [x for x in D1], Ap * qpA + qB)
    w01 = fixed_point(sig, Rbeta, qpB)
    rho = lambda t: sum(F(Ralpha[w], den) * val(sig, t)[pos[w]] for w in block) + (qpA - qA) - Aq * t
    P, Q, R, S = int(w00 < w10), int(w00 < w01), int(w10 < w01), int(rho(w01) > 0)
    assert w00 != w10 and w00 != w01 and w10 != w01
    layers = {(0, 0): (w00, (P, Q)), (1, 0): (w10, (1-P, R)), (0, 1): (w01, (S, 1-Q)), (1, 1): (w01, (1-S, 1-R))}
    inner_idx = sum(sig[i] << i for i in range(3))
    for (la, lb), (t, (oa, ob)) in layers.items():
        s, tied = outmap(t); assert not tied
        v = inner_idx | (la << 3) | (lb << 4)
        out[v] = s[inner_idx] | (oa << 3) | (ob << 4)
        if out[v] != B2[v]: mism += 1
print('assembled outmap:', tuple(out)); print('paper B^2:       ', B2); print('mismatches:', mism)
assert mism == 0
print('ESCAPE LEVEL THEOREM REPRODUCES B^2 FROM THREE DRIVES AND ONE COMPARISON')
