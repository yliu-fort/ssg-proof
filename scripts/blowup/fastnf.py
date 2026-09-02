"""Floating-point SCREEN for the two-player harmonic normal form.
Used only to drive the search; every candidate is re-verified in exact
rational arithmetic by nf2.NF and then from an explicit SSG."""
import numpy as np

def margins(Ai, bi, m, k, den):
    """Ai : (2n, n) integer array of numerators, bi : (2n,) integer numerators,
    rows indexed 2*v+a.  Returns (mu, z) where mu[sigma, i] = val_sigma(x_i^{other})
    - val_sigma(x_i), and z[sigma] the value vector; None if singular."""
    n = m + k
    NS, NT = 1 << m, 1 << k
    P = Ai / den
    q = bi / den
    Z = np.empty((NS, n))
    for sg in range(NS):
        best = None
        for tt in range(NT):
            rows = [2 * i + ((sg >> i) & 1) for i in range(m)] + \
                   [2 * (m + j) + ((tt >> j) & 1) for j in range(k)]
            M = np.eye(n) - P[rows]
            try:
                z = np.linalg.solve(M, q[rows])
            except np.linalg.LinAlgError:
                return None, None
            best = z if best is None else np.minimum(best, z)
        Z[sg] = best
    mu = np.empty((NS, m))
    for sg in range(NS):
        z = Z[sg]
        for i in range(m):
            a = (sg >> i) & 1
            r = 2 * i + (1 - a)
            mu[sg, i] = P[r] @ z + q[r] - z[i]
    return mu, Z


def fixedpoint_ok(Ai, bi, m, k, den, Z, tol=1e-9):
    """check Z[sg] is a fixed point of T_sigma (float screen)."""
    n = m + k
    P = Ai / den
    q = bi / den
    for sg in range(1 << m):
        z = Z[sg]
        for i in range(m):
            a = (sg >> i) & 1
            r = 2 * i + a
            if abs(P[r] @ z + q[r] - z[i]) > tol:
                return False
        for j in range(k):
            v = m + j
            lo = min(P[2 * v] @ z + q[2 * v], P[2 * v + 1] @ z + q[2 * v + 1])
            if abs(lo - z[v]) > tol:
                return False
    return True
