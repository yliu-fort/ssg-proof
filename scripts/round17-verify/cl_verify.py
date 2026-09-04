#!/usr/bin/env python3
"""Root agent's check of the round-17 convex-lift route's level-one gap certificate (cl:gap-one) on
W_14 of thm:lasserre-vacuous, from the paper's printed normal form, in exact arithmetic.
Reduced transport polytope Q~(W_14) in u = (x(v1),x(v2),x(v3)):
  u1 >= u2, u1 >= u3 (Max rows of v1: readouts x(v2), x(v3)); u2 >= 1/2, u2 >= 7/8 u1; u3 >= 15/32, u3 >= 7/8 u1; 0 <= u <= 1.
F_v^i := {u in Q~ : u(v) = readout of action i at v}. The route's cl:faces: R_1 = intersection over v of conv(F_v^0 u F_v^1).
A point u lies in R_1 if for EVERY v it is a convex combination of a point of F_v^0 and a point of F_v^1."""
from fractions import Fraction as F
half, s15 = F(1, 2), F(15, 32)
read = {0: (lambda u: u[1], lambda u: u[2]), 1: (lambda u: half, lambda u: F(7, 8) * u[0]), 2: (lambda u: s15, lambda u: F(7, 8) * u[0])}
def inQ(u):
    return all(0 <= x <= 1 for x in u) and all(u[v] >= read[v][i](u) for v in range(3) for i in (0, 1))
def tight(u, v, i): return u[v] == read[v][i](u)
u = (F(3, 5), F(23, 40), F(11, 20))
pi, ka = (F(8, 13), F(8, 13), F(7, 13)), (F(4, 7), F(1, 2), F(4, 7))
pi2, ka2 = (F(1, 2), F(1, 2), F(15, 32)), (F(1), F(7, 8), F(7, 8))
assert all(inQ(p) for p in (u, pi, ka, pi2, ka2))
assert tight(pi, 0, 0) and tight(ka, 0, 1)                      # v1: pi in F^0, kappa in F^1
assert tight(pi2, 1, 0) and tight(pi2, 2, 0) and tight(ka2, 1, 1) and tight(ka2, 2, 1)   # v2, v3
assert tuple(F(13, 20) * a + F(7, 20) * b for a, b in zip(pi, ka)) == u
assert tuple(F(4, 5) * a + F(1, 5) * b for a, b in zip(pi2, ka2)) == u
wstar = (half, half, s15)
assert inQ(wstar) and all(tight(wstar, v, 0) for v in range(3))
print('cl:gap-one: u = (3/5, 23/40, 11/20) lies in conv(F_v^0 u F_v^1) for each of v1, v2, v3 with the route\'s five points, all in Q~(W_14);'
      ' so max over R_1 of x(v1) >= 3/5 > 1/2 = w*(v1)  [level one is not exact on the one-player W_14]')
# the dual game W_14-bar (Min-only, values 1 - ...): the mirrored certificate gives min over R_1 of x(v1-bar) <= 2/5
# DW = W_14 and W_14-bar under an average root s -> (v1, v1-bar): by cl:union the level-one bounds at s are the
# averages, [ (1/2 + 2/5)/2, (3/5 + 1/2)/2 ] = [9/20, 11/20], straddling w*(s) = 1/2 (w* recomputed from DW_GAME.json).
print('cl:dw: root bounds at level one are at most 9/20 and at least 11/20 given the two certificates; w*(s) = 1/2 was recomputed by brute force from DW_GAME.json (27 vertices, stopping)')
