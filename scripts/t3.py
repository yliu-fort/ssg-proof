from fractions import Fraction as F
from lp_exact import Game, check_feasible
from transport import sep, level_subsets, build_lift, lift_point
from reduced import sep_c, levels, build_lift_c, lift_point_c, phi
import random

def Sr(r):
    n=r+4; t0=n; t1=n+1
    kinds=['max','avg']+['avg']*(r+2)
    succ=[(1,2),(t1,t0)]
    for i in range(r): succ.append((0,3+i))
    succ.append((3+r,t0)); succ.append((t1,t0))
    return Game(kinds,succ)

S=Game(['max','avg','avg','avg','avg'],[(1,2),(6,5),(0,3),(4,5),(6,5)])
for G,name,p,q in [(S,'S',1,2)]+[(Sr(r),f'S_{r}',1,2) for r in range(2,6)]:
    subs=level_subsets(G,1)
    full0=sep(G,p,q)[0]; red0=sep_c(G,p,q)[0]
    full1=sep(G,p,q,subsets=subs)[0]; red1=sep_c(G,p,q,levels(G,1))[0]
    print(name,"Q:",full0,red0,full0==red0," Q1:",full1,red1,full1==red1)

# cross-check on random games with 2-3 controlled vertices
rng=random.Random(5); ok=0; tested=0
while tested<40:
    n=7
    kinds=['max','min','max']+['avg']*(n-3); rng.shuffle(kinds)
    succ=[(rng.randrange(n+2),rng.randrange(n+2)) for _ in range(n)]
    g=Game(kinds,succ)
    if not g.is_stopping(): continue
    tested+=1
    subs=level_subsets(g,1)
    for (p,q) in [(g.succ[v][0],g.succ[v][1]) for v in g.ctrl]:
        a=sep(g,p,q,subsets=subs)[0]; b=sep_c(g,p,q,levels(g,1))[0]
        assert a==b,(g.kinds,g.succ,p,q,a,b)
        c=sep(g,p,q)[0]; d=sep_c(g,p,q)[0]
        assert c==d,(g.kinds,g.succ,p,q,c,d)
    ok+=1
print("cross-check on",ok,"random stopping games: identical")
