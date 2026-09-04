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
