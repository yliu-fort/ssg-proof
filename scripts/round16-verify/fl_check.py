from fractions import Fraction as F
import itertools
def FL(D, theta):
    kinds={}; succ={}
    # u is a terminal of payoff theta: model as vertex 'u' avg over a dyadic chain? use payoff game directly: treat 'u' as terminal with payoff theta in the solver
    for d in range(1,D+1):
        Fp = 'u' if d==1 else f'F{d-1}'; Gp = 't0' if d==1 else f'G{d-1}'
        kinds[f'X{d}']='avg'; succ[f'X{d}']=('t0',Fp)
        kinds[f'Y{d}']='avg'; succ[f'Y{d}']=(f'C{d}_1',Gp)
        kinds[f'F{d}']='max'; succ[f'F{d}']=(f'X{d}',f'Y{d}')
        kinds[f'G{d}']='min'; succ[f'G{d}']=(f'X{d}',f'Y{d}')
        for j in range(1,2*d):
            kinds[f'C{d}_{j}']='avg'; succ[f'C{d}_{j}']=('t0', f'C{d}_{j+1}' if j<2*d-1 else 't1')
    return kinds,succ
def solve(kinds,succ,choice,term):
    V=list(kinds); idx={v:i for i,v in enumerate(V)}; n=len(V)
    M=[[F(0)]*(n+1) for _ in range(n)]
    for v in V:
        i=idx[v]; M[i][i]+=1
        tg=[(succ[v][0],F(1,2)),(succ[v][1],F(1,2))] if kinds[v]=='avg' else [(succ[v][choice[v]],F(1))]
        for u,c in tg:
            if u in term: M[i][n]+=c*term[u]
            else: M[i][idx[u]]-=c
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[a/pv for a in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return {v:M[idx[v]][n] for v in V}
def value(kinds,succ,term):
    maxs=[v for v in kinds if kinds[v]=='max']; mins=[v for v in kinds if kinds[v]=='min']
    best=None
    for sb in itertools.product((0,1),repeat=len(maxs)):
        sigma=dict(zip(maxs,sb)); worst=None
        for tb in itertools.product((0,1),repeat=len(mins)):
            ch=dict(sigma); ch.update(zip(mins,tb)); val=solve(kinds,succ,ch,term)
            worst=val if worst is None else {v:min(worst[v],val[v]) for v in val}
        best=worst if best is None else {v:max(best[v],worst[v]) for v in worst}
    return best
def tent(x): return 2*x if x<=F(1,2) else 2-2*x
for D in (1,2,3,4):
    kinds,succ=FL(D,None)
    bad=0; pieces=set()
    thetas=[F(i,2**(D+2)) for i in range(2**(D+2)+1)]
    prev=None; slopes=[]
    for th in thetas:
        val=value(kinds,succ,{'t0':F(0),'t1':F(1),'u':th})[f'F{D}']
        T=th
        for _ in range(D): T=tent(T)
        formula=F(1,2**(D+1))*(th + 1 - F(1,2**D) + F(1,2**D)*T)
        if val!=formula: bad+=1
        if prev is not None: slopes.append((val-prev)/(th-prev_th))
        prev, prev_th = val, th
    # count maximal runs of constant slope
    runs=1+sum(1 for i in range(1,len(slopes)) if slopes[i]!=slopes[i-1])
    print(f'D={D}: |V|={len(kinds)+2} (claimed {D*D+4*D+3}), formula mismatches {bad}/{len(thetas)}, slope runs on the sampled grid {runs} (claimed 2^D = {2**D}), slopes seen {sorted(set(slopes))}')
