#!/usr/bin/env python3
"""Does thm:fold's P_D, read as a DISCOUNT game (u -> (t0,t1) unfrozen, every step surviving with
probability beta), have any breakpoint of its optimal pair in beta? The parametric-path route and its
novelty auditor say no (the naive transplant of the fold dies); checked here from thm:fold's statement."""
from fractions import Fraction as F
import sys
sys.argv = ['x']
exec(open('bp_verify.py').read().split('for D in range(1, 9):')[0])   # values(kinds, succ, beta), tent
def build_PD(D):
    kinds = {}; succ = {}
    def add(n, k, a, b): kinds[n] = k; succ[n] = (a, b)
    add('u', 'avg', 't0', 't1')
    for j in range(1, 2 * D):
        add(f'k{j}', 'avg', 't0', f'k{j+1}' if j < 2 * D - 1 else 't1')
    Fv = {0: 'u'}; G = {0: 't0'}
    for d in range(1, D + 1):
        add(f'X{d}', 'avg', 't0', Fv[d-1]); add(f'Y{d}', 'avg', f'k{2*D-2*d+1}', G[d-1])
        add(f'F{d}', 'max', f'X{d}', f'Y{d}'); add(f'G{d}', 'min', f'X{d}', f'Y{d}')
        Fv[d] = f'F{d}'; G[d] = f'G{d}'
    return kinds, succ
for D in range(1, 8):
    kinds, succ = build_PD(D); assert len(kinds) + 2 == 6 * D + 2
    pairs = set(); ties = 0
    for j in range(1, 400):
        beta = F(j, 400)
        w, tied, ch = values(kinds, succ, beta)
        if tied: ties += 1; continue
        pairs.add(tuple(sorted(ch.items())))
    # the frozen-payoff sweep of thm:fold at beta = 1, for contrast: pieces of val(F_D) as a function of theta
    print(f'P_{D} as a discount game: N = {6*D+2}, {len(pairs)} distinct optimal pair(s) over 399 rationals beta = j/400, {ties} tied samples', flush=True)

# --- the parametric-path correctness auditor's repair: P_D with the seed u replaced by the two-vertex
# chain u -> (u2,u2), u2 -> (t1,t1) (val rho^2), on 6D+3 vertices; claim: breakpoints exactly {k/2^D}
def build_PD_chain(D):
    kinds, succ = build_PD(D)
    succ['u'] = ('u2', 'u2'); kinds['u2'] = 'avg'; succ['u2'] = ('t1', 't1')
    return kinds, succ
for D in range(1, 9):
    kinds, succ = build_PD_chain(D); N = len(kinds) + 2; assert N == 6 * D + 3
    for beta in [F(j, 97) for j in range(1, 97, 7)]:
        w, tied, ch = values(kinds, succ, beta); assert not tied
        for d in range(1, D + 1):
            e_d = beta * (beta ** 2 / 4) ** d; phi = w[f'F{d}'] - w[f'G{d}']; z = beta
            for _ in range(d): z = tent(z)
            assert phi == z * e_d, (D, d, beta)
    for k in range(1, 2 ** D):
        w, tied, ch = values(kinds, succ, F(k, 2 ** D)); v2 = 0; kk = k
        while kk % 2 == 0: kk //= 2; v2 += 1
        assert tied == {f'F{D-v2}', f'G{D-v2}'}, (D, k, tied)
    pairs = []
    for k in range(2 ** D):
        ps = set()
        for off in (F(1, 5), F(1, 2), F(4, 5)):
            w, tied, ch = values(kinds, succ, (k + off) / 2 ** D); assert not tied
            ps.add(tuple(sorted(ch.items())))
        assert len(ps) == 1; pairs.append(ps.pop())
    assert len(set(pairs)) == 2 ** D and all(pairs[i] != pairs[i + 1] for i in range(2 ** D - 1))
    print(f"P'_{D} (P_D with the two-vertex chain seed): N = {N}, phi_d = T^d(rho) e_d with e_d = rho (rho^2/4)^d at 14 rationals, breakpoints exactly {{k/2^{D}}} ({2**D-1}) with F_d,G_d tied, {2**D} distinct pairs constant inside each interval", flush=True)
