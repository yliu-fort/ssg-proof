"""fs15:top reduction: on random stopping games with all non-sink values in (0,1), adjoin the reference chain
e_1..e_r and boost chains c_p^(1..m), c_q^(1..m); check argmax over Vavg is c_p^(m) iff val(p) >= val(q)."""
import random, itertools, sys; sys.path.insert(0,'.')
from fractions import Fraction as F
from rise_bound import solve, is_stopping, val_sigma
random.seed(11)
def wstar(kinds,succ):
    n=len(kinds); MX=[v for v in range(n) if kinds[v]=='max']; best=None
    for sc in itertools.product((0,1),repeat=len(MX)):
        sigma={v:succ[v][a] for v,a in zip(MX,sc)}; x=val_sigma(kinds,succ,sigma)
        best=x if best is None else [max(a,b) for a,b in zip(best,x)]
    return best
tested=0; wrong=0
while tested<150:
    n=random.randint(3,6); kinds=[random.choice(['max','min','avg','avg']) for _ in range(n)]
    succ=[tuple(random.choice(range(n+2)) for _ in range(2)) for _ in range(n)]
    if not is_stopping(kinds,succ): continue
    w=wstar(kinds,succ)
    if any(w[v] in (0,1) for v in range(n)): continue   # the reduction first collapses these; skip such games
    a=kinds.count('avg')
    if a==0: continue
    p,q=random.sample(range(n),2)
    r=2*a+2; m=r+2
    T0,T1='t0','t1'; K=list(kinds); S=[[(T0 if u==n else (T1 if u==n+1 else u)) for u in s] for s in succ]
    def add(kind,s0,s1):
        K.append(kind); S.append([s0,s1]); return len(K)-1
    # reference chain e_1 -> (t1,t0), e_{j+1} -> (t1, e_j)
    e=add('avg',T1,T0)
    for j in range(2,r+1): e=add('avg',T1,e)
    er=e
    cp=add('avg',T1,p)
    for j in range(2,m+1): cp=add('avg',T1,cp)
    cq=add('avg',er,q)
    for j in range(2,m+1): cq=add('avg',T1,cq)
    N=len(K); succ2=[tuple((N if u==T0 else (N+1 if u==T1 else u)) for u in s) for s in S]
    assert is_stopping(K,succ2)
    w2=wstar(K,succ2)
    assert all(w2[v]==w[v] for v in range(n))
    avg=[v for v in range(N) if K[v]=='avg']; top=max(avg,key=lambda v:w2[v]); tops=[v for v in avg if w2[v]==w2[top]]
    ok = (len(tops)==1) and ((tops[0]==cp) == (w[p]>=w[q])) and (tops[0] in (cp,cq))
    tested+=1; wrong+= (not ok)
print('tested',tested,'wrong',wrong)
