# Own check of the correctness audit's M6 finding: def:ratio (root16/ratio.py, written from the statement)
# with BOTH clauses of rem:own-successor at v0 on CV(e,s).  Records the first firing round and which clause.
import sys, time
sys.path.insert(0,'.'); sys.path.insert(0,'../root16')
from fractions import Fraction as F
from cv_build import CV
from mycore import G, wstar, Z01
from ratio import ratio_rounds, INF, sound
for e,s in [(int(a),int(b)) for a,b in (x.split(",") for x in sys.argv[1:])] if len(sys.argv)>1 else [(1,3),(2,3),(1,4),(2,4),(3,4)]:
    kinds,succ,names=CV(e,s); g=G(kinds,[list(x) for x in succ]); w=wstar(g)
    Z0,Z1=Z01(g,w); v0=names.index('v0'); H=names.index('H'); d1=names.index('d_1')
    K={1:30,2:50,3:90,4:160,5:320}[e]
    t=time.time(); Rs=ratio_rounds(g,w,K)
    first=None
    for k,R in enumerate(Rs,1):
        assert sound(g,R,w)==0, ('unsound',e,s,k)
        c1=[u for u in g.succ[v0] if R[v0][u] is not INF and R[v0][u]<=1]
        c2=[u for u in g.succ[v0] if R[u][v0] is not INF and R[u][v0]<1] if v0 not in Z0 else []
        if c1 or c2:
            first=(k,'(i)' if c1 else '(ii)',[names[u] for u in c1+c2],
                   {'R(d1,v0)':str(R[d1][v0]),'R(H,v0)':str(R[H][v0]),'R(v0,H)':str(R[v0][H]),'R(v0,d1)':str(R[v0][d1])}); break
    print(f'CV({e},{s}) N={g.N}: def:ratio first fires at v0 at round {first[0] if first else None} via clause {first[1] if first else "-"} {first[2:] if first else ""}   (audit: s=3 -> 10,16 ; s=4 -> 12,22,39)  [{time.time()-t:.0f}s]', flush=True)
