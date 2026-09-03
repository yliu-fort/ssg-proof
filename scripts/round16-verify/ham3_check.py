from fractions import Fraction as F
import itertools
# HAM_3 normal form (one player): f_{v,a}(y) = q + p.y ; beta = (1,0,0); d = 1
f = { 0: [(F(1,8), (F(5,8),F(1,8),F(0))), (F(0), (F(1,16),F(0),F(11,16)))],
      1: [(F(0), (F(5,8),F(5,16),F(0))), (F(1,8), (F(1,16),F(0),F(7,16)))],
      2: [(F(1,4), (F(0),F(0),F(7,16))), (F(1,16), (F(0),F(0),F(15,16)))] }
beta=(1,0,0)
def value(pi, lam):
    # solve y_v = q_{v,pi(v)} + p.y - lam*[pi(v)!=beta(v)]
    n=3; M=[[F(0)]*(n+1) for _ in range(n)]
    for v in range(n):
        q,p=f[v][pi[v]]; M[v][v]+=1
        for j in range(n): M[v][j]-=p[j]
        M[v][n]=q-(lam if pi[v]!=beta[v] else 0)
    for c in range(n):
        r=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[r]=M[r],M[c]; pv=M[c][c]; M[c]=[x/pv for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                g=M[r][c]; M[r]=[x-g*z for x,z in zip(M[r],M[c])]
    return [M[i][n] for i in range(n)]
def optimal(lam):
    # lambda-optimal profiles: those whose value y satisfies T_lambda y = y (max over actions of biased readouts)
    opt=[]
    for pi in itertools.product((0,1),repeat=3):
        y=value(pi,lam); ok=True
        for v in range(3):
            best=max(f[v][a][0]+sum(f[v][a][1][j]*y[j] for j in range(3))-(lam if a!=beta[v] else 0) for a in (0,1))
            if y[v]!=best: ok=False
        if ok: opt.append(pi)
    return opt
bps=[F(47,1080),F(391,9720),F(283,7416),F(5,144),F(29,876),F(71,2216),F(7,232)]
path=[(1,0,0),(1,1,0),(0,1,0),(0,0,0),(0,0,1),(0,1,1),(1,1,1),(1,0,1)]
print('breakpoints decreasing:', all(bps[i]>bps[i+1] for i in range(6)))
pts=[bps[0]*2]+[(bps[i]+bps[i+1])/2 for i in range(6)]+[bps[6]/2]
ok=True
for i,lam in enumerate(pts):
    o=optimal(lam)
    if o!=[path[i]]: ok=False; print('at lambda',lam,'optimal',o,'expected',path[i])
for i,b in enumerate(bps):
    o=optimal(b)
    if set(o)!={path[i],path[i+1]}: ok=False; print('breakpoint',b,'optimal',o)
print('HAM_3 path verified:',ok,'| val at lambda=0:',value(path[-1],F(0)))
