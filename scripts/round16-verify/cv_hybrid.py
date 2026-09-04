import sys, time
sys.path.insert(0,'.'); sys.path.insert(0,'../root16')
from cv_build import CV
from mycore import G, wstar
from ownhyb import hybrid_rounds
for e,s in [(1,4),(2,4),(1,3),(2,3),(3,3)]:
    kinds,succ,names=CV(e,s)
    g=G(kinds,[list(x) for x in succ]); w=wstar(g)
    t=time.time(); first,dist=hybrid_rounds(g,w,K=40,seeded=True)
    v0=names.index('v0')
    print(f'CV({e},{s}) N={len(kinds)+2}: distinguishing vertices {[names[v] for v in dist]}, first firing at v0 = {first.get(v0)} (route: hybrid 4,8 at s=4 e=1,2; 3,5,10 at s=3 e=1,2,3)  [{time.time()-t:.0f}s]', flush=True)
