"""Exact verification of a huntG candidate: rebuild the normal form in exact
rationals, recompute the Max-cube outmap (Min best-responding), compare with
the target, build the explicit fair-coin SSG and verify it FROM THE GAME."""
import sys, json
sys.path.insert(0, '.')
from fractions import Fraction as F
from nf2 import NF
from build import build_ssg
import verify
from auso import ba_heights, ba_trace
from my_D import is_holt_klee
d = json.load(open(sys.argv[1])); m, k, den = d['m'], d['k'], d['den']; n = m + k
P = [[[F(d['A'][2*v+a][j], den) for j in range(n)] for a in (0, 1)] for v in range(n)]
Q = [[F(d['b'][2*v+a], den) for a in (0, 1)] for v in range(n)]
nf = NF(m, k, P, Q); s, ndeg = nf.outmap()
print('exact outmap matches target:', s == d['target'], 'nondegenerate:', ndeg)
kinds, succ = build_ssg(m, k, P, Q); r = verify.analyse(kinds, succ, cross=3)
h = r['heights']
print('game: N', r['N'], 'kinds', {x: kinds.count(x) for x in ('max', 'min', 'avg')}, 'stopping (trap test) implicit in analyse; nondeg', r['nondegenerate'], 'uso', r['uso'], 'acyclic', r['acyclic'], 'outmap==nf', r['outmap'] == s)
print('BA height', max(h), 'walk from a max start', ba_trace(s, h.index(max(h))))
print('Holt-Klee of the Max cube:', is_holt_klee(s, m)[0])
out = sys.argv[1].replace('.json', '_game.json')
json.dump(dict(kinds=kinds, succ=[list(t) for t in succ], outmap=s, m=m, k=k), open(out, 'w')); print('saved', out)
