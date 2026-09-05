#!/usr/bin/env python3
"""Root agent's verification of the round-19 extension-complexity route's ladder theorem (batch I), from the statement.
The ladder L_n of def:ladder is built here (v_i -> (v_{i+1}, w_{i+1}), w_i -> (v_{i+1}, w_{i+1}) average, v_{n+1} = t_0,
w_{n+1} = t_1), every one of its 2^n Max strategies is evaluated exactly, and phi_i(val_sigma) = XOR_{k >= i} sigma_k is
checked for n = 1..10, so that V_C(L_n) is the affine image of the cube under phi^{-1}: a parallelotope with 2n facets.
sigma_i = 1 means v_i -> w_{i+1} (the non-first-listed successor), as in the route's convention a_i = a_{i+1} + sigma_i d_{i+1}."""
import itertools
from fractions import Fraction as F
def say(*a): print(*a, flush=True)
for n in range(1, 11):
    ok = 0
    for sig in itertools.product((0, 1), repeat=n):
        a = [None] * (n + 2); b = [None] * (n + 2); a[n + 1] = F(0); b[n + 1] = F(1)
        for i in range(n, 0, -1):
            b[i] = (a[i + 1] + b[i + 1]) / 2
            a[i] = b[i + 1] if sig[i - 1] == 1 else a[i + 1]
        # the value of a Max strategy: the chosen successor's value (the game is acyclic, values by backward induction)
        phi = [2 ** (n - i) * a[i] - sum(2 ** (n - k) * a[k] for k in range(i + 1, n + 1)) for i in range(1, n + 1)]
        xor = [F(sum(sig[k - 1] for k in range(i, n + 1)) % 2) for i in range(1, n + 1)]
        assert phi == xor, (n, sig, phi, xor); ok += 1
    # the optimal values: w*(v_i) = max over strategies = 1 - 2^-(n-i+1)? just record the maximum
    say(f'[1] ladder L_{n}: phi(val_sigma) = (XOR_{{k>=i}} sigma_k)_i for all {ok} strategies; phi triangular with diagonal 2^(n-i): V_C(L_n) = phi^-1([0,1]^n), a parallelotope with {2*n} facets')
say('EXTENSION-COMPLEXITY ROUTE (ladder theorem): reproduced from the statement')
