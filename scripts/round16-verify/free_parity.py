import sys, random, json
sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace
random.seed(3)
def Bpz(sA, m, p, z):
    n=1<<m; A,Bb=1<<m,1<<(m+1); s=[0]*(n<<2)
    for layer in range(4):
        a,b=layer&1,layer>>1
        for v in range(n):
            lo = sA[v^z] if layer==0 else sA[v]
            even = (p[v]==0)
            if (a,b)==(0,0): hi=0
            elif (a,b)==(1,0): hi=(A|Bb) if even else A
            elif (a,b)==(0,1): hi=Bb if even else (A|Bb)
            else: hi=A if even else Bb
            s[v|(a*A)|(b*Bb)]=lo|hi
    return s
paper_B2=[7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18]
B1=[0,1,3,6,7,4,5,2]
seeds=[(B1,3),(paper_B2,5),([0,1,3,2],2),([1,0],1)]
bad=0; tests=0; walkbad=0
for sA,m in seeds:
    n=1<<m; h=ba_heights(sA,m); o=[v for v in range(n) if sA[v]==0][0]
    for trial in range(60):
        p=[random.randint(0,1) for _ in range(n)]; z=random.randrange(n)
        s=Bpz(sA,m,p,z); tests+=1
        if not (is_uso(s,m+2) and is_acyclic(s,m+2)): bad+=1; print('NOT AUSO',m,p,z)
        # sink check
        sink=[v for v in range(n<<2) if s[v]==0]
        if sink!=[o^z]: bad+=1; print('sink wrong',m,sink,o^z)
    # walk-length claim: p agrees with parity along the walk of s from u (max height), then walk from (1,0,u) or (0,1,u) has length h(u)+2+h(o xor z)
    for u in [v for v in range(n) if h[v]==max(h)]:
        walk=ba_trace(sA,u)
        for trial in range(20):
            p=[random.randint(0,1) for _ in range(n)]
            for v in walk: p[v]=h[v]%2
            z=random.randrange(n); s=Bpz(sA,m,p,z)
            start = u | ((1<<m) if h[u]%2==0 else (1<<(m+1)))
            L=len(ba_trace(s,start))-1
            exp=h[u]+2+ba_heights(sA,m)[o^z]
            if L!=exp: walkbad+=1; print('walk length',m,u,z,L,exp)
print('AUSO tests',tests,'failures',bad,'| walk-length failures',walkbad)
