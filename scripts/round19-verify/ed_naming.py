#!/usr/bin/env python3
"""On the adversary certificates of prop:eval-decide-lower: at every node, are the optimal strategies of the NO world
and of the YES witness disjoint? If so, no output strategy is optimal in both consistent worlds after m queries, and
NAMING an optimal strategy also needs m + 1 evaluations at m in {2, 3} -- with the star (ed_star.py) the naming and
the decision complexity are then both exactly |C| + 1 there. Also: of the 149 depth-3 nodes whose fourth query
sigma_1 xor sigma_2 xor sigma_3 is forced (ed_depth4.py), how many are face completions and how many
codimension-one coincidences of the designed worlds."""
import sys, os, json, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
R18 = os.path.join(HERE, '..', 'round18-verify')
from ed_star import Sys, alpha_system, rank

for m, fn in ((2, 'cert_m2_d2.json'), (3, 'cert_m3_d3.json')):
    cert = json.load(open(os.path.join(R18, fn))); strategies = list(itertools.product((0, 1), repeat=m))
    disjoint = 0; overlap = []; bydepth = {}
    for c in cert:
        W = Sys(m, {tuple(map(int, k.split(','))): tuple(F(x) for x in v) for k, v in c['no_rows'].items()})
        Y = Sys(m, {tuple(map(int, k.split(','))): tuple(F(x) for x in v) for k, v in c['yes_rows'].items()})
        def optimal(S):
            vals = {s: S.value(s) for s in strategies}; star = [max(vals[s][i] for s in strategies) for i in range(m)]
            return {s for s in strategies if vals[s] == star}
        oW, oY = optimal(W), optimal(Y)
        assert len(oW) == 1 and len(oY) == 1     # nondegenerate one-player: a unique optimum
        dep = len(c['queries']); bydepth.setdefault(dep, [0, 0]); bydepth[dep][1] += 1
        if oW & oY: overlap.append((c['queries'], oW, oY)); bydepth[dep][0] += 1
        else: disjoint += 1
    print(f'm={m}: {len(cert)} nodes; optimal strategies of NO world and YES witness disjoint at {disjoint}, overlapping at {len(overlap)}; by depth (overlapping/total): ' + ', '.join(f'depth {d}: {o}/{n}' for d, (o, n) in sorted(bydepth.items())))
    if overlap: print('   overlaps:', overlap[:5])
    if m == 3:
        faces = coinc = 0
        for c in cert:
            if len(c['queries']) != 3: continue
            triple = tuple(tuple(q) for q in c['queries']); W = Sys(3, {tuple(map(int, k.split(','))): tuple(F(x) for x in v) for k, v in c['no_rows'].items()})
            xs = [W.value(s) for s in triple]; assert rank([[F(1)] + list(x) for x in xs]) == 3
            xor = tuple(a ^ b ^ c for a, b, c in zip(*triple))
            on_face = any(all(s[v] == triple[0][v] for s in triple) for v in range(3))
            forced = alpha_system(W, triple, xs, xor) is not None
            for sig in strategies:
                if sig not in triple and sig != xor: assert alpha_system(W, triple, xs, sig) is None
            if forced and on_face: faces += 1
            elif forced: coinc += 1
            else: assert not on_face
        print(f'   depth-3 nodes with a forced fourth query: {faces} face completions (of 144 ordered face triples) + {coinc} coincidences = {faces + coinc}')
