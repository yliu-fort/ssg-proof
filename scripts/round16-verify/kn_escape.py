from fractions import Fraction as F
def Kn(n):
    # vertices: per block i: x_i, m_i, c_i, d_i, e_i ; sinks t0,t1
    kinds={}; succ={}
    for i in range(1,n+1):
        x,m,c,d,e=f'x{i}',f'm{i}',f'c{i}',f'd{i}',f'e{i}'
        xn = f'x{i+1}' if i<n else 't1'
        kinds[x]='max'; succ[x]=(c,e)
        kinds[c]='avg'; succ[c]=(m,d)
        kinds[m]='min'; succ[m]=(x,d)
        kinds[d]='avg'; succ[d]=(e,xn)
        kinds[e]='avg'; succ[e]=('t1','t0')
    return kinds,succ
lam=F(19,20)
def cert(n):
    kinds,succ=Kn(n)
    x={}
    for i in range(1,n+1):
        x[f'x{i}']=F(3); x[f'm{i}']=F(60,19); x[f'c{i}']=F(1000,361); x[f'd{i}']=F(40,19); x[f'e{i}']=F(1)
    xh=lambda v: x.get(v,F(0))
    ok=True; worst=F(0)
    for v,k in kinds.items():
        a,b=succ[v]
        sv = max(xh(a),xh(b)) if k in ('max','min') else (xh(a)+xh(b))/2
        if not (x[v]>=1 and sv<=lam*x[v]): ok=False
        worst=max(worst, sv/x[v])
    return ok, worst
for n in (1,2,3,5,8,12,20,40):
    ok,w=cert(n); print(n, ok, 'max ratio Sx/x =', w, float(w))
print('kappa =', F(1000,361)/1)
