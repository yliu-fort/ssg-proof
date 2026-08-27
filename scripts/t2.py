from fractions import Fraction as F
from lp_exact import Game
from transport import *

def Sr(r):
    n = r+4; t0=n; t1=n+1
    kinds = ['max','avg'] + ['avg']*(r+2)
    succ = [(1,2),(t1,t0)]
    for i in range(0,r):      # b_i index 2+i
        succ.append((0, 3+i))
    succ.append((3+r, t0))    # b_r
    succ.append((t1, t0))     # b_{r+1}
    return Game(kinds, succ)

for r in range(2,8):
    G = Sr(r)
    w = G.value()
    subs = level_subsets(G,1)
    sanity(G, subs, name=f"S_{r}")
    s0 = sep(G,1,2)[0]; s1 = sep(G,2,1)[0]
    q0 = sep(G,1,2,subsets=subs)[0]; q1 = sep(G,2,1,subsets=subs)[0]
    print(f"r={r} N={G.N} stopping={G.is_stopping()} w*(v)={w[0]} w*(a)={w[1]} w*(b0)={w[2]}")
    print(f"      Q : Sep(a,b0)={s0}  Sep(b0,a)={s1}")
    print(f"      Q1: Sep(a,b0)={q0}  Sep(b0,a)={q1}")
