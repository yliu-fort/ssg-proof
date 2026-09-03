"""Check gad:xor (i)-(iii) from the printed 100-vertex normal form, and gad:B2-rows' witnesses on the B^2 outmap."""
from fractions import Fraction as F
import itertools
rows={0:[(51,0,121,0,4),(11,165,0,4,2)],1:[(0,84,0,0,21),(7,13,133,102,0)],2:[(94,0,160,0,1),(1,12,70,171,0)],3:[(19,94,8,114,0),(10,38,97,102,2)]}
n=4
def solve(sig):
    A=[[F(int(i==j))-F(rows[i][sig[i]][j],256) for j in range(n)] for i in range(n)]; b=[F(rows[i][sig[i]][4],256) for i in range(n)]
    aug=[A[i]+[b[i]] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if aug[i][c]!=0); aug[c],aug[piv]=aug[piv],aug[c]
        pv=aug[c][c]; aug[c]=[x/pv for x in aug[c]]
        for i in range(n):
            if i!=c and aug[i][c]!=0:
                f=aug[i][c]; aug[i]=[x-f*y for x,y in zip(aug[i],aug[c])]
    return [aug[i][n] for i in range(n)]
def act(v,a,z): return sum(F(rows[v][a][j],256)*z[j] for j in range(n))+F(rows[v][a][4],256)
ok=True; out=[]
for s in range(16):
    sig=[(s>>i)&1 for i in range(n)]; z=solve(sig); L=1 if (sig[2]==1 and sig[3]==1) else 0
    # (i)
    if sig[1]==0: ok&= z[1]==F(21,172)
    # (ii): Delta_1 = act(1,1)-act(1,0) positive iff L=1
    d1=act(1,1,z)-act(1,0,z); ok&= (d1>0)==(L==1)
    if sig[1]==1: ok&= (z[1]>F(21,172))==(L==1) and (z[1]<F(21,172))==(L==0)
    # (iii): sign Delta_0 = + iff sig1 xor L == 0
    d0=act(0,1,z)-act(0,0,z); ok&= (d0>0)==((sig[1]^L)==0)
    o=sum(1<<i for i in range(n) if act(i,1-sig[i],z)>act(i,sig[i],z)); out.append(o)
print('gad:xor (i)-(iii) all hold:', ok)
# threshold bounds
Ts0=[];Ts1=[]
for s in range(16):
    sig=[(s>>i)&1 for i in range(n)]; z=solve(sig); L=1 if (sig[2]==1 and sig[3]==1) else 0
    T=(40*z[0]+121*z[2]-4*z[3]+2)/165; (Ts1 if L else Ts0).append(T)
print('max_{L=0} T =',max(Ts0),'< 21/172 <',min(Ts1),'=min_{L=1} T:', max(Ts0)<F(21,172)<min(Ts1))
print('outmap of the 100-vertex game normal form:', out)
# gad:B2-rows: edges along which g_c passes + -> - and - -> +
B2=[7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
def g(c,u): # + when the c-edge at u points from u_c=0 to u_c=1
    return '+' if ((u>>c)&1)==0 and (B2[u]>>c)&1 or ((u>>c)&1)==1 and not (B2[u]>>c)&1 else '-'
names=['x','a1','b1','a2','b2']
for c in range(5):
    pm=[];mp=[]
    for u in range(32):
        for i in range(5):
            if (B2[u]>>i)&1:
                w=u^(1<<i)
                if g(c,u)=='+' and g(c,w)=='-': pm.append((u,w))
                if g(c,u)=='-' and g(c,w)=='+': mp.append((u,w))
    print(names[c],'+->-',pm[:3],len(pm),' -->+',mp[:3],len(mp))
B1=[0,1,3,6,7,4,5,2]
for c in range(3):
    pm=[];mp=[]
    for u in range(8):
        for i in range(3):
            if (B1[u]>>i)&1:
                w=u^(1<<i)
                gu='+' if (((u>>c)&1)==0)==bool((B1[u]>>c)&1) else '-'
                gw='+' if (((w>>c)&1)==0)==bool((B1[w]>>c)&1) else '-'
                if gu=='+' and gw=='-': pm.append((u,w))
                if gu=='-' and gw=='+': mp.append((u,w))
    print('B1 coord',c,'+->-',len(pm),'-->+',len(mp))
