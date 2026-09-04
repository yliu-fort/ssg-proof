#!/usr/bin/env python3
"""The order-lattice correctness auditor's G_c: a NON-separated stopping game with one Max and one Min
vertex on which the decode-and-re-sort iteration of rem:order-unique has a 2-cycle while the antipodal
walk of the profile cube converges (so rem:cyclic-antipodal's no-cycle statement needs separatedness).
Run from scripts/round17-verify with ol_verify.py alongside."""
import sys, itertools; sys.argv = ['x']
exec(open('ol_verify.py').read().split("def preorders(A):")[0])
kinds = ['max','min','avg','avg','avg','avg','avg','avg']; succ = [(1,4),(2,7),(8,5),(5,4),(0,6),(9,8),(0,8),(3,0)]
g = Game(kinds, succ); w = g.wstar()
print('G_c: stopping', g.is_stopping(), 'w* =', [str(x) for x in w[:8]], 'separated:', all(s >= 2 for v in g.C for s in g.succ[v]))
ys = {pi: g.value(dict(zip(g.C, pi))) for pi in itertools.product((0, 1), repeat=2)}
orbit = []; rk = g.induced(ys[(0, 1)])
for step in range(6):
    decs = g.decode_all(rk); assert len(decs) == 1
    ch, x = decs[0]; orbit.append(tuple(ch[v] for v in g.C)); rk = g.induced(x)
print('decode-and-re-sort from ord(y_(0,1)):', orbit)
def step(pi):
    ch = dict(zip(g.C, pi)); x = ys[pi]; s = set()
    for v in g.C:
        cur = x[v]; other = x[g.succ[v][1 - ch[v]]]
        if (g.kinds[v] == 'max' and other > cur) or (g.kinds[v] == 'min' and other < cur): s.add(v)
    return tuple(pi[i] ^ (1 if g.C[i] in s else 0) for i in range(2))
print('antipodal walk:', {pi: step(pi) for pi in ys})
