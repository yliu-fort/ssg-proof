# Own check of the audit's width law on CV(e,s): M_k := max_{K(Delta_k)} (z(v_1) - 1/2), Delta_k the Z-seeded own-successor
# hybrid matrix (same rounds as ownhyb.hybrid_rounds), K(Delta_k) the tightened transport polytope of mycore.transport_sep.
# Audit: M_0 = M_1 = 1/2 and M_k = lambda^{k-1}/2 for k>=1 (lambda = 1-2^-e); the draft said lambda^k/2.
import sys
sys.path.insert(0,'.'); sys.path.insert(0,'../root16')
from fractions import Fraction as F
from cv_build import CV
from mycore import G, wstar, Z01, slack_step, minplus_close, clamp, ones, check_sound, transport_sep
from zseed import seeds
for e,s,K in [(2,4,6),(3,4,4),(1,3,5)]:
    kinds,succ,names=CV(e,s); g=G(kinds,[list(x) for x in succ]); w=wstar(g); N=g.N
    Z0,Z1=Z01(g,w); L,U,_,_=seeds(g,w); v1=names.index('v1'); lam=1-F(1,2**e)
    pairs=[(p,q) for p in range(N) for q in range(N) if p!=q]
    D=ones(N); row=[]
    def width(D): return transport_sep(g,[(g.T1,v1)],D=D,L=L,U=U)[(g.T1,v1)]+F(1,2)   # max z(v1)-z(t1) + 1/2
    row.append(width(D))
    for k in range(K):
        A=[[clamp(t) for t in r] for r in minplus_close(slack_step(g,D,Z0,Z1),N)]
        M=[[min(D[i][j],A[i][j]) for j in range(N)] for i in range(N)]
        for (p,q),val in transport_sep(g,pairs,D=M,L=L,U=U).items():
            if val is not None: M[q][p]=min(M[q][p],val)
        M=[[clamp(t) for t in r] for r in minplus_close(M,N)]; check_sound(g,M,w,f'r{k+1}'); D=M
        row.append(width(D))
    law=[F(1,2)]+[lam**(k-1)/2 for k in range(1,K+1)]
    print(f'CV({e},{s}): M_k for k=0..{K}: {[str(x) for x in row]}  audit law lambda^(k-1)/2: {[str(x) for x in law]}  match={row==law}', flush=True)
