from fractions import Fraction as F
import itertools, sys
def Mn(n):
    kinds={}; succ={}
    def x(i): return 'h' if i==n+1 else f'x{i}'
    kinds['h']='max'; succ['h']=('x1', f'c{2*n}')
    for i in range(1,n+1):
        kinds[f'x{i}']='max'; succ[f'x{i}']=(f'b{i}', f'c{n+i}')
        kinds[f'b{i}']='avg'; succ[f'b{i}']=(f'y{i}','c1')
        kinds[f'y{i}']='min'; succ[f'y{i}']=(x(i+1), f'b{i}')
    for j in range(1,2*n):
        o = 'c1' if j<n else ('t1' if j==n else 't0')
        kinds[f'c{j}']='avg'; succ[f'c{j}']=(o, f'c{j+1}')
    kinds[f'c{2*n}']='avg'; succ[f'c{2*n}']=('t0','t1')
    return kinds,succ
def solve(kinds,succ,choice):
    V=list(kinds); idx={v:i for i,v in enumerate(V)}; n=len(V)
    M=[[F(0)]*(n+1) for _ in range(n)]
    for v in V:
        i=idx[v]; M[i][i]+=1
        if kinds[v]=='avg': tg=[(succ[v][0],F(1,2)),(succ[v][1],F(1,2))]
        else: tg=[(succ[v][choice[v]],F(1))]
        for u,c in tg:
            if u=='t1': M[i][n]+=c
            elif u=='t0': pass
            else: M[i][idx[u]]-=c
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]
        pv=M[c][c]; M[c]=[a/pv for a in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    return {v:M[idx[v]][n] for v in V}
def val_sigma(kinds,succ,sigma):
    mins=[v for v in kinds if kinds[v]=='min']
    best=None
    for bits in itertools.product((0,1),repeat=len(mins)):
        ch=dict(sigma); ch.update(zip(mins,bits))
        val=solve(kinds,succ,ch)
        if best is None: best=val
        else: best={v:min(best[v],val[v]) for v in val}   # componentwise min over tau (stopping game: min over positional tau is attained by one tau, but the componentwise min is safe as a lower bound; check equality below)
    return best
def escape_exponent(kinds,succ,sigma):
    # levels C_j per lem:descent with sigma
    level={'t1':0}
    changed=True; j=0
    while changed:
        changed=False; j+=1
        for v in kinds:
            if v in level: continue
            s=succ[v]; k=kinds[v]
            inC=[u in level for u in s]
            if (k=='avg' and any(inC)) or (k=='max' and s[sigma[v]] in level) or (k=='min' and all(inC)):
                level[v]=j; changed=True
    # descent paths: l strictly decreasing, follow sigma at max
    memo={}
    def A(v):
        if v=='t1': return 0
        if v in memo: return memo[v]
        s=succ[v]; k=kinds[v]
        nxt = [s[sigma[v]]] if k=='max' else list(s)
        nxt=[u for u in nxt if u in level and level[u]<level[v]]
        w = 1 if (k=='avg' and len(nxt)==1) else 0
        memo[v]= w + max(A(u) for u in nxt)
        return memo[v]
    return max(A(v) for v in level if v!='t1'), level
for n in (3,4,5):
    kinds,succ=Mn(n)
    maxs=[v for v in kinds if kinds[v]=='max']
    best=None; vals={}
    for bits in itertools.product((0,1),repeat=len(maxs)):
        sigma=dict(zip(maxs,bits)); vals[bits]=val_sigma(kinds,succ,sigma)
    wstar={v:max(vals[b][v] for b in vals) for v in kinds}
    opt=[b for b in vals if all(vals[b][v]==wstar[v] for v in kinds)]
    ds=[]
    for b in opt:
        d,lev=escape_exponent(kinds,succ,dict(zip(maxs,b))); ds.append(d)
    import math
    D=1
    for v in wstar: D=D*wstar[v].denominator//math.gcd(D,wstar[v].denominator)
    print(f'n={n}: N={len(kinds)+2}, val(h)={wstar["h"]}, optimal sigma count={len(opt)}, d(M_n)=min over optimal={min(ds)} (all: {sorted(set(ds))}), D(M_n)={D}, |Vmax|={len(maxs)}')
