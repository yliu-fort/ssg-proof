"""The full |C|-cube orientation of G# (4 Max + 2 Min), from its printed
harmonic normal form: at profile (sigma,tau) a controlled vertex is 'out' in
its coordinate iff its owner strictly prefers the other action under the
profile's value vector.  Check USO / acyclic / Holt-Klee, and that the sink
projection (Min face sinks) reproduces G#'s Max-cube outmap."""
import sys; sys.path.insert(0, '.')
from fractions import Fraction as F
from nf2 import NF
from auso import is_uso, is_acyclic, ba_heights
from my_D import is_holt_klee
rows = {
 0: [(6,3,88,1,0,0,4), (1,0,0,0,126,0,0)],
 1: [(0,0,14,113,0,0,0), (0,6,0,0,0,0,53)],
 2: [(0,0,0,127,0,0,0), (120,0,0,0,0,0,7)],
 3: [(0,0,0,0,0,120,7), (2,74,46,0,0,0,0)],
 4: [(0,0,0,0,13,0,64), (0,0,125,0,0,1,1)],
 5: [(0,127,0,0,0,0,0), (0,0,121,0,0,1,4)],
}
m, k = 4, 2; n = 6
P = [[[F(rows[v][a][j], 128) for j in range(n)] for a in (0, 1)] for v in range(n)]
Q = [[F(rows[v][a][6], 128) for a in (0, 1)] for v in range(n)]
nf = NF(m, k, P, Q)
s4, ndeg = nf.outmap()
print('Max-cube outmap from the rows:', s4, 'nondegenerate', ndeg)
print('matches the paper:', s4 == [0,1,3,6,7,4,13,10,14,15,9,12,11,8,5,2])
# big cube: vertex index = sigma | (tau << m)
big = [0] * (1 << n); ties = 0
for sigma in range(1 << m):
    for tau in range(1 << k):
        z = nf.pair_value(sigma, tau)
        o = 0
        for i in range(m):
            a = (sigma >> i) & 1
            alt = nf.apply_row(i, 1 - a, z)
            if alt > z[i]: o |= 1 << i
            elif alt == z[i]: ties += 1
        for j in range(k):
            v = m + j; a = (tau >> j) & 1
            alt = nf.apply_row(v, 1 - a, z)
            if alt < z[v]: o |= 1 << (m + j)
            elif alt == z[v]: ties += 1
        big[sigma | (tau << m)] = o
print('6-cube: ties', ties, 'USO', is_uso(big, n), 'acyclic', is_acyclic(big, n))
h = ba_heights(big, n); print('6-cube BA heights: max', max(h) if h else None)
hk, wit = is_holt_klee(big, n); print('6-cube Holt-Klee:', hk, wit)
# sink projection: for each sigma the tau with no Min coordinate out; Max part there
proj = []
for sigma in range(1 << m):
    sinks = [tau for tau in range(1 << k) if (big[sigma | (tau << m)] >> m) == 0]
    assert len(sinks) == 1, (sigma, sinks)
    proj.append(big[sigma | (sinks[0] << m)] & ((1 << m) - 1))
print('sink projection equals the Max-cube outmap:', proj == s4)
