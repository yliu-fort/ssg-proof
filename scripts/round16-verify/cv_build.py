# CV(e,s) from the few-denominator route's definition; kinds/succ in the harness convention (non-sinks 0..n-1, t0=n, t1=n+1)
from fractions import Fraction as F
import math, sys
sys.path.insert(0,'.')
def CV(e,s):
    names=['v0','v1','v2','H']+[f'A1_{q}' for q in range(1,e+1)]+[f'A2_{q}' for q in range(1,e+1)]+[f'B1_{q}' for q in range(1,2*e+1)]+[f'B2_{q}' for q in range(1,2*e+1)]+[f'd_{q}' for q in range(1,s)]
    idx={v:i for i,v in enumerate(names)}; n=len(names); t0,t1=n,n+1
    def I(x): return t0 if x=='t0' else t1 if x=='t1' else idx[x]
    kinds=['avg']*n; succ=[None]*n
    kinds[idx['v0']]=kinds[idx['v1']]=kinds[idx['v2']]='max'
    succ[idx['H']]=(t1,t0)
    for i in (1,2):
        for q in range(1,e+1): succ[idx[f'A{i}_{q}']]=(I(f'v{3-i}'), I(f'A{i}_{q+1}') if q<e else I('H'))
        for q in range(1,2*e+1): succ[idx[f'B{i}_{q}']]=(I(f'v{i}'), I(f'B{i}_{q+1}') if q<2*e else I('H'))
        succ[idx[f'v{i}']]=(I(f'A{i}_1'), I(f'B{i}_1'))
    for q in range(1,s): succ[idx[f'd_{q}']]=(I('v1'), I(f'd_{q+1}') if q<s-1 else t0)
    succ[idx['v0']]=(I('H'), I('d_1'))
    return kinds,succ,names
if __name__=='__main__':
    from sparse_verify import solve_sparse, stopping
    import itertools
    for e,s in [(1,4),(2,4),(3,4),(1,3),(2,3)]:
        kinds,succ,names=CV(e,s); n=len(kinds)
        maxv=[i for i in range(n) if kinds[i]=='max']
        best=None
        for bits in itertools.product((0,1),repeat=3):
            ch={v:b for v,b in zip(maxv,bits)}; val=solve_sparse(kinds,succ,ch)
            best=val if best is None else [max(a,b) for a,b in zip(best,val)]
        w=best; D=1
        for x in w: D=D*x.denominator//math.gcd(D,x.denominator)
        v0=names.index('v0'); H=names.index('H'); d1=names.index('d_1')
        gap=w[H]-w[d1]
        print(f'CV({e},{s}): N={n+2} (claimed {6*e+s+5}), stopping {stopping(kinds,succ)}, D(G)={D} (claimed {2**s}), w*(v0)={w[v0]}, w*(H)={w[H]}, w*(d1)={w[d1]}, gap at v0 = {gap} (claimed 1/D = {F(1,2**s)}), values not 1/2: {[(names[i],str(w[i])) for i in range(n) if w[i]!=F(1,2)][:6]}')
