"""The own-successor test with the FREE seed.

def:transport allows Q(G;L,U) for any L <= w* <= U.  Two such bounds cost
nothing: Z_0 = {v : w*(v)=0} and Z_1 = {v : w*(v)=1} are computable by attractor
sweeps in linear time (def:simorder), so U := 0 on Z_0 and L := 1 on Z_1 is a
legitimate polynomial-time seed.  Any stall found without it may be an artefact
of discarding free information.
"""
from fractions import Fraction as F
from mycore import G, wstar, transport_sep, distinguishing, Z01


def seeds(g, w):
    Z0, Z1 = Z01(g, w)
    L = [F(1) if v in Z1 else F(0) for v in range(g.N)]
    U = [F(0) if v in Z0 else F(1) for v in range(g.N)]
    return L[:g.n], U[:g.n], Z0, Z1


def decides_seeded(g, w, v, L, U):
    a, b = g.succ[v]
    if g.kinds[v] == 'max':
        sep = transport_sep(g, [(v, a), (v, b)], L=L, U=U)
        return sep[(v, a)] < 0 or sep[(v, b)] < 0
    sep = transport_sep(g, [(a, v), (b, v)], L=L, U=U)
    return sep[(a, v)] < 0 or sep[(b, v)] < 0


def report(g, w=None):
    if w is None:
        w = wstar(g)
    L, U, Z0, Z1 = seeds(g, w)
    D = distinguishing(g, w)
    und = [v for v in D if not decides_seeded(g, w, v, L, U)]
    return D, und, Z0, Z1
