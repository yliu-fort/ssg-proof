"""My check of lane:rise-bound and lane:peak-source on random TWO-player stopping games:
val_sigma = min over all tau (brute force), first-passage laws of actions onto C u {t1} from the graph.
rise-bound: for sigma_t, sigma_t' on an all-switches run (t<t'), u in Vmax NOT strictly switchable at sigma_t,
b = sigma_t'(u): Delta(u) <= max over W(u,b) of Delta(w). peak-source: max_V Delta = max_{S_t} Delta."""
import random, itertools
from fractions import Fraction as F
random.seed(7)
def solve(kinds,succ,choice):
    n=len(kinds); t0,t1=n,n+1
    M=[[F(0)]*n for _ in range(n)]; q=[F(0)]*n
    for v in range(n):
        tg=[(choice[v],F(1))] if kinds[v] in ('max','min') else [(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        for u,p in tg:
            if u==t1: q[v]+=p
            elif u<n: M[v][u]+=p
    aug=[[(F(1) if i==j else F(0))-M[i][j] for j in range(n)]+[q[i]] for i in range(n)]
    for c in range(n):
        piv=next((i for i in range(c,n) if aug[i][c]!=0),None)
        if piv is None: return None
        aug[c],aug[piv]=aug[piv],aug[c]; pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(n):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return [aug[i][n] for i in range(n)]
def is_stopping(kinds,succ):
    n=len(kinds); U=set(range(n)); ch=True
    while ch:
        ch=False
        for v in list(U):
            inU=[u in U for u in succ[v]]
            if not (all(inU) if kinds[v]=='avg' else any(inU)): U.discard(v); ch=True
    return not U
def val_sigma(kinds,succ,sigma):
    n=len(kinds); MN=[v for v in range(n) if kinds[v]=='min']; best=None
    for tc in itertools.product((0,1),repeat=len(MN)):
        ch=dict(sigma); ch.update({v:succ[v][a] for v,a in zip(MN,tc)})
        x=solve(kinds,succ,ch); best=x if best is None else [min(a,b) for a,b in zip(best,x)]
    return best
def laws(kinds,succ):
    """first-passage law of each action (v,a) onto C u {t1}: dict (v,a) -> {target: prob}"""
    n=len(kinds); t0,t1=n,n+1; C=[v for v in range(n) if kinds[v]!='avg']; AV=[v for v in range(n) if kinds[v]=='avg']
    idx={w:i for i,w in enumerate(AV)}; m=len(AV); targets=C+[t1]
    A=[[F(0)]*m for _ in range(m)]; B=[[F(0)]*len(targets) for _ in range(m)]
    for w in AV:
        for u in succ[w]:
            if u in idx: A[idx[w]][idx[u]]+=F(1,2)
            elif u in targets: B[idx[w]][targets.index(u)]+=F(1,2)
    aug=[[(F(1) if i==j else F(0))-A[i][j] for j in range(m)]+B[i] for i in range(m)]
    for c in range(m):
        piv=next(i for i in range(c,m) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(m):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    H={w:aug[idx[w]][m:] for w in AV}
    def law(u):
        if u in idx: return dict(zip(targets,H[u]))
        if u==t0: return {}
        return {u:F(1)}
    return {(v,a):law(succ[v][a]) for v in C for a in (0,1)}
def val(x,u,n): return F(1) if u==n+1 else (F(0) if u==n else x[u])
viol_rise=viol_peak=0; pairs=0; games=0
while games<250:
    n=random.randint(4,7); kinds=[random.choice(['max','max','min','avg','avg']) for _ in range(n)]
    if 'max' not in kinds: continue
    succ=[tuple(random.choice(range(n+2)) for _ in range(2)) for _ in range(n)]
    if not is_stopping(kinds,succ): continue
    games+=1; MX=[v for v in range(n) if kinds[v]=='max']; L=laws(kinds,succ)
    for start in range(1<<len(MX)):
        sigma={v:succ[v][(start>>i)&1] for i,v in enumerate(MX)}; run=[]
        while True:
            x=val_sigma(kinds,succ,sigma)
            S=[v for v in MX if succ[v][0]!=succ[v][1] and val(x,[u for u in succ[v] if u!=sigma[v]][0],n)>val(x,sigma[v],n)]
            run.append((dict(sigma),x,S))
            if not S: break
            for v in S: sigma[v]=[u for u in succ[v] if u!=sigma[v]][0]
        for t in range(len(run)):
            for t2 in range(t+1,len(run)):
                pairs+=1
                s1,x1,S1=run[t]; s2,x2,_=run[t2]
                D=[b-a for a,b in zip(x1,x2)]
                for u in MX:
                    if u in S1: continue
                    b=succ[u].index(s2[u]); W=[w for w,p in L[(u,b)].items() if w!=u and w<n and p>0]
                    bound=max([D[w] for w in W], default=F(0))
                    if D[u]>bound: viol_rise+=1
                if max(D)>max([D[v] for v in S1],default=F(0)) and max(D)>0: viol_peak+=1
print('games',games,'pairs (t<t\')',pairs,'rise-bound violations',viol_rise,'peak-source violations',viol_peak)

# ---- cor:peak-sharp (auditor's sharpening): the maximum of val_{t'} - val_t is attained at some v in S_t with sigma_{t'}(v) != sigma_t(v)
random.seed(99); viol=0; pairs2=0; games2=0
while games2<250:
    n=random.randint(4,7); kinds=[random.choice(['max','max','min','avg','avg']) for _ in range(n)]
    if 'max' not in kinds: continue
    succ=[tuple(random.choice(range(n+2)) for _ in range(2)) for _ in range(n)]
    if not is_stopping(kinds,succ): continue
    games2+=1; MX=[v for v in range(n) if kinds[v]=='max']
    for start in range(1<<len(MX)):
        sigma={v:succ[v][(start>>i)&1] for i,v in enumerate(MX)}; run=[]
        while True:
            x=val_sigma(kinds,succ,sigma)
            S=[v for v in MX if succ[v][0]!=succ[v][1] and val(x,[u for u in succ[v] if u!=sigma[v]][0],n)>val(x,sigma[v],n)]
            run.append((dict(sigma),x,S))
            if not S: break
            for v in S: sigma[v]=[u for u in succ[v] if u!=sigma[v]][0]
        for t in range(len(run)):
            for t2 in range(t+1,len(run)):
                s1,x1,S1=run[t]; s2,x2,_=run[t2]; D=[b-a for a,b in zip(x1,x2)]; M=max(D)
                if M<=0: continue
                pairs2+=1
                if not any(D[v]==M and s2[v]!=s1[v] for v in S1): viol+=1
print('peak-sharp: games',games2,'pairs',pairs2,'violations',viol)
