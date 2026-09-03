"""Anchor table for the realised blow-up of the 2-cube (AP_m4_k0_den256_s200):
isomorphism to B(seed), normal-form rows, and per-strategy values and inner option values."""
import sys, json, itertools; sys.path.insert(0,'.')
from fractions import Fraction as F
from blowz import D_general
d=json.load(open('AP_m4_k0_den256_s200.json')); m,k,den=int(d['m']),int(d['k']),int(d['den']); n=m+k
A=d['A']; b=d['b']; target=[int(x) for x in d['target']]
def apply(s,m,perm,t):
    def pi(v):
        w=0
        for i in range(m):
            if v>>i&1: w|=1<<perm[i]
        return w
    out=[0]*(1<<m)
    for v in range(1<<m): out[pi(v)^t]=pi(s[v])
    return out
found=None
for seed in ([0,1,3,2],[0,3,2,1],[3,0,1,2],[3,2,0,1]):
    B=D_general(seed,2,'sinkstart')
    for p in itertools.permutations(range(4)):
        for t in range(16):
            if apply(B,4,p,t)==target: found=(seed,p,t); break
        if found: break
    if found: break
seed,perm,t=found
print('seed',seed,'perm',perm,'t',t,'| game inner coords',perm[0],perm[1],'| outer (alpha,beta)',perm[2],perm[3],"| B's layer 00 = game bits alpha,beta =",t>>perm[2]&1,t>>perm[3]&1)
P=[[[F(A[2*v+a][j],den) for j in range(n)] for a in (0,1)] for v in range(n)]
Q=[[F(b[2*v+a],den) for a in (0,1)] for v in range(n)]
def solve(sigma):
    M=[[(F(1) if v==j else F(0))-P[v][sigma>>v&1][j] for j in range(n)] for v in range(n)]
    r=[Q[v][sigma>>v&1] for v in range(n)]
    aug=[M[i]+[r[i]] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(n):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return [aug[i][n] for i in range(n)]
for v in range(n):
    for a in (0,1): print('row',v,a,':',[A[2*v+a][j] for j in range(n)],'+',b[2*v+a],'/',den)
al,be=perm[2],perm[3]
for sigma in range(16):
    x=solve(sigma)
    opts={v:[sum(P[v][a][j]*x[j] for j in range(n))+Q[v][a] for a in (0,1)] for v in range(n)}
    print(f'{sigma:04b} L=({sigma>>al&1},{sigma>>be&1}) x={[str(v) for v in x]} opts={ {v:[str(o) for o in opts[v]] for v in range(n)} } out={target[sigma]:04b}')
