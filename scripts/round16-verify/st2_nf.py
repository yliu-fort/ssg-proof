# Verify ST(2): compute the harmonic normal form of ST2_GAME.json (first-passage laws onto Vmax u {t1})
# with a sparse exact solver, then run all-switches on the 14-state normal form from every start.
import json, sys, time
from fractions import Fraction as F
sys.path.insert(0,'.')
g=json.load(open('../one-player-howard/ST2_GAME.json')); kinds=g['kinds']; succ=[tuple(s) for s in g['succ']]; n=len(kinds); t0,t1=n,n+1
maxv=[i for i in range(n) if kinds[i]=='max']; assert kinds.count('min')==0
avg=[i for i in range(n) if kinds[i]=='avg']; idx={v:i for i,v in enumerate(avg)}
targets=maxv+[t1]
# for each target T: h_T(v) = prob of first hitting T (among targets) from avg vertex v: h = mean of successors, with target->1, other targets/t0 -> 0
def solve_sparse(rows, rhs):
    # rows: dict var -> dict var->coef (including diagonal), rhs: dict var->F ; returns dict var->value
    remaining=set(rows); col={}
    for v,r in rows.items():
        for u in r: col.setdefault(u,set()).add(v)
    elim=[]
    while remaining:
        piv=min(remaining,key=lambda v:len(rows[v])); r=rows[piv]; pv=piv if r.get(piv,0)!=0 else next(k for k in r if r[k]!=0)
        c=r[pv]; r={k:val/c for k,val in r.items() if val!=0}; rows[piv]=r; rhs[piv]=rhs[piv]/c
        for other in list(col.get(pv,())):
            if other==piv or other not in remaining: continue
            ro=rows[other]; f=ro.get(pv,F(0))
            if f==0: continue
            for k,val in r.items():
                nv=ro.get(k,F(0))-f*val
                if nv==0:
                    if k in ro: del ro[k]; col[k].discard(other)
                else:
                    if k not in ro: col.setdefault(k,set()).add(other)
                    ro[k]=nv
            rhs[other]-=f*rhs[piv]
        remaining.discard(piv); elim.append((piv,pv)); col[pv]=set()
    x={}
    for piv,pv in reversed(elim):
        val=rhs[piv]
        for k,c in rows[piv].items():
            if k!=pv: val-=c*x[k]
        x[pv]=val
    return x
t=time.time()
H={}   # H[T][v] for avg v
for T in targets:
    rows={}; rhs={}
    for v in avg:
        r={v:F(1)}; b=F(0)
        for u in succ[v]:
            if u==T: b+=F(1,2)
            elif u in idx: r[u]=r.get(u,F(0))-F(1,2)
        rows[v]=r; rhs[v]=b
    H[T]=solve_sparse(rows,rhs)
print('first-passage solves done', round(time.time()-t,1),'s', flush=True)
def law(u):   # law of first visit to targets from vertex u (u may be a target itself or a sink)
    if u==t1: return {t1:F(1)}
    if u==t0: return {}
    if u in maxv: return {u:F(1)}
    return {T:H[T][u] for T in targets if H[T][u]!=0}
m=len(maxv); rows_nf={}
for i,v in enumerate(maxv):
    rows_nf[v]=[law(succ[v][a]) for a in (0,1)]
def val_sigma(sigma):
    # solve x_v = sum_w p_w x_w + q on the m states
    M={}; rhs={}
    for i,v in enumerate(maxv):
        L=rows_nf[v][sigma[v]]; r={v:F(1)}
        for w,p in L.items():
            if w in rows_nf: r[w]=r.get(w,F(0))-p
        M[v]=r; rhs[v]=L.get(t1,F(0))
    return solve_sparse(M,rhs)
def readout(v,a,x): L=rows_nf[v][a]; return sum(p*x[w] for w,p in L.items() if w in x)+L.get(t1,F(0))
best=0; ties=0
import itertools
for bits in itertools.product((0,1),repeat=m):
    sigma=dict(zip(maxv,bits)); s=dict(sigma); L=0
    while True:
        x=val_sigma(s); S=[]
        for v in maxv:
            a=s[v]; c=readout(v,a,x); o=readout(v,1-a,x)
            if o==c: ties+=1
            if o>c: S.append(v)
        if not S: break
        for v in S: s[v]=1-s[v]
        L+=1
    if L>best: best=L; bstart=bits
print('ST(2): m',m,'max all-switches run over all starts',best,'at',bstart,'ties',ties, round(time.time()-t,1),'s')
