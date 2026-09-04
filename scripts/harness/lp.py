"""Exact rational two-phase simplex, Bland's rule.  max c.x s.t. A x <= b, x >= 0."""
from fractions import Fraction as F

def _simplex(T, basis, obj, ncols):
    m=len(T)
    while True:
        cx=next((j for j in range(ncols) if obj[j]<0), None)
        if cx is None: return 'ok'
        rs=[(T[i][ncols]/T[i][cx], basis[i], i) for i in range(m) if T[i][cx]>0]
        if not rs: return 'unbounded'
        r=min(rs)[2]
        pv=T[r][cx]; T[r]=[v/pv for v in T[r]]
        for i in range(m):
            if i!=r and T[i][cx]!=0:
                f=T[i][cx]; T[i]=[a-f*bb for a,bb in zip(T[i],T[r])]
        if obj[cx]!=0:
            f=obj[cx]
            for j in range(ncols+1): obj[j]-=f*T[r][j]
        basis[r]=cx

def solve(c,A,b,n):
    m=len(A); c=[F(x) for x in c]
    rows=[[F(x) for x in A[i]]+[F(0)]*m for i in range(m)]
    rhs=[F(b[i]) for i in range(m)]
    for i in range(m): rows[i][n+i]=F(1)
    neg=[i for i in range(m) if rhs[i]<0]
    for i in neg:
        rows[i]=[-v for v in rows[i]]; rhs[i]=-rhs[i]
    na=len(neg); NC=n+m+na
    T=[rows[i]+[F(0)]*na+[rhs[i]] for i in range(m)]
    basis=[n+i for i in range(m)]
    for k,i in enumerate(neg):
        T[i][n+m+k]=F(1); basis[i]=n+m+k
    if na:
        obj1=[F(0)]*NC+[F(0)]
        for k in range(na): obj1[n+m+k]=F(1)
        for i in range(m):
            f=obj1[basis[i]]
            if f!=0:
                for j in range(NC+1): obj1[j]-=f*T[i][j]
        st=_simplex(T,basis,obj1,NC)
        if st=='unbounded' or -obj1[NC]!=0: return ('infeasible',None,None)
        for i in range(m):                      # drive artificials out of the basis
            if basis[i]>=n+m:
                piv=next((j for j in range(n+m) if T[i][j]!=0), None)
                if piv is None: continue
                pv=T[i][piv]; T[i]=[v/pv for v in T[i]]
                for r2 in range(m):
                    if r2!=i and T[r2][piv]!=0:
                        f=T[r2][piv]; T[r2]=[a-f*bb for a,bb in zip(T[r2],T[i])]
                basis[i]=piv
        for i in range(m): del T[i][n+m:n+m+na]
        NC=n+m
    obj=[-x for x in c]+[F(0)]*m+[F(0)]
    for i in range(m):
        f=obj[basis[i]]
        if f!=0:
            for j in range(NC+1): obj[j]-=f*T[i][j]
    st=_simplex(T,basis,obj,NC)
    if st!='ok': return ('unbounded',None,None)
    x=[F(0)]*n
    for i in range(m):
        if basis[i]<n: x[basis[i]]=T[i][NC]
    return ('ok',obj[NC],x)
