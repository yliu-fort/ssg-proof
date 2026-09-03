"""Generic verifier: a game json {kinds, succ} -> stopping, ties, improvement outmap (val_sigma = min over tau), USO, acyclic, height, HK."""
import sys, json, itertools, glob, os; sys.path.insert(0,'../solo')
from fractions import Fraction as F
from auso import is_uso, is_acyclic, ba_heights
from my_D import is_holt_klee
def analyse(path):
    d=json.load(open(path)); kinds=d['kinds']; succ=[tuple(s) for s in d['succ']]; n=len(kinds); t0,t1=n,n+1
    MX=[v for v in range(n) if kinds[v]=='max']; MN=[v for v in range(n) if kinds[v]=='min']; m=len(MX)
    U=set(range(n)); ch=True
    while ch:
        ch=False
        for v in list(U):
            inU=[u in U for u in succ[v]]
            if not (all(inU) if kinds[v]=='avg' else any(inU)): U.discard(v); ch=True
    stopping=not U
    def solve(choice):
        M=[[F(0)]*n for _ in range(n)]; q=[F(0)]*n
        for v in range(n):
            tg=[(choice[v],F(1))] if kinds[v] in ('max','min') else [(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
            for u,p in tg:
                if u==t1: q[v]+=p
                elif u<n: M[v][u]+=p
        aug=[[(F(1) if i==j else F(0))-M[i][j] for j in range(n)]+[q[i]] for i in range(n)]
        for c in range(n):
            piv=next(i for i in range(c,n) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
            pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
            for i in range(n):
                if i!=c and aug[i][c]!=0:
                    f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
        return [aug[i][n] for i in range(n)]
    def val(x,u): return F(1) if u==t1 else (F(0) if u==t0 else x[u])
    out=[]; ties=0
    for s in range(1<<m):
        best=None
        for tc in itertools.product((0,1),repeat=len(MN)):
            chc={v:succ[v][(s>>i)&1] for i,v in enumerate(MX)}; chc.update({v:succ[v][a] for v,a in zip(MN,tc)})
            x=solve(chc); best=x if best is None else [min(a,b) for a,b in zip(best,x)]
        o=0
        for i,v in enumerate(MX):
            a=(s>>i)&1; cur=val(best,succ[v][a]); alt=val(best,succ[v][1-a])
            if alt>cur: o|=1<<i
            elif alt==cur: ties+=1
        out.append(o)
    return dict(N=n+2, m=m, k=len(MN), stopping=stopping, ties=ties, outmap=out, uso=is_uso(out,m), acyclic=is_acyclic(out,m), height=max(ba_heights(out,m)) if is_acyclic(out,m) else None, hk=is_holt_klee(out,m)[0] if is_uso(out,m) else None)
if __name__=='__main__':
    for path in sys.argv[1:]:
        r=analyse(path); print(os.path.basename(path), r)
