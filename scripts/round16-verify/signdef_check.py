# thm:signdef: on a sign-definite stopping SSG every Max vertex switches at most twice along any improving run.
import random, itertools
from fractions import Fraction as F
random.seed(7)
exec(open('fs16_check.py').read().split('# ---- fs16:gate ----')[0])   # solve, is_stopping, value, rand_game
def firstpass(kinds,succ,names):
    # law of first visit to C u {t0,t1} from each vertex, C = controlled
    C=[v for v in names if kinds[v] in ('max','min')]; targets=C+['t1']
    avg=[v for v in names if kinds[v]=='avg']
    H={}
    for T in targets:
        # h(v) for avg v: mean over successors; target T ->1; other targets/t0 -> 0; avg -> variable
        n=len(avg); idx={v:i for i,v in enumerate(avg)}
        M=[[F(0)]*(n+1) for _ in range(n)]
        for v in avg:
            i=idx[v]; M[i][i]+=1
            for u in succ[v]:
                if u==T: M[i][n]+=F(1,2)
                elif u in idx: M[i][idx[u]]-=F(1,2)
        for c in range(n):
            p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]; pv=M[c][c]; M[c]=[a/pv for a in M[c]]
            for r in range(n):
                if r!=c and M[r][c]!=0:
                    f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
        H[T]={v:M[idx[v]][n] for v in avg}
    def law(u):
        if u=='t1': return {'t1':F(1)}
        if u=='t0': return {}
        if u in C: return {u:F(1)}
        return {T:H[T][u] for T in targets}
    return C,law
checked=0; signdef=0; viol=0; maxsw=0
for trial in range(400):
    kinds,succ,names=rand_game(random.randint(4,8),'g')
    C,law=firstpass(kinds,succ,names)
    maxs=[v for v in names if kinds[v]=='max']
    if not maxs: continue
    sd=True
    for v in maxs:
        d={c: law(succ[v][1]).get(c,F(0))-law(succ[v][0]).get(c,F(0)) for c in C}
        if any(x>0 for x in d.values()) and any(x<0 for x in d.values()): sd=False
    checked+=1
    if not sd: continue
    signdef+=1
    mins=[v for v in names if kinds[v]=='min']
    def valsig(sigma):
        worst=None
        for tb in itertools.product((0,1),repeat=len(mins)):
            ch=dict(sigma); ch.update(zip(mins,tb)); val=solve(kinds,succ,ch)
            worst=val if worst is None else {u:min(worst[u],val[u]) for u in val}
        return worst
    for bits in itertools.product((0,1),repeat=len(maxs)):
        s=dict(zip(maxs,bits)); count={v:0 for v in maxs}
        while True:
            x=valsig(s); w=lambda u: x[u] if u in x else (F(1) if u=='t1' else F(0))
            S=[v for v in maxs if w(succ[v][1-s[v]])>w(succ[v][s[v]])]
            if not S: break
            for v in S: s[v]=1-s[v]; count[v]+=1
        mx=max(count.values()); maxsw=max(maxsw,mx)
        if mx>2: viol+=1; print('VIOLATION',kinds,succ,bits)
print('games',checked,'sign-definite',signdef,'violations of n_v<=2:',viol,'max switches per vertex',maxsw)
