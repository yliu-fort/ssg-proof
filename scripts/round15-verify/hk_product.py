"""lem:hstar-super product with the h*_HK(5)=11 witness as FIRST block and the 1-cube as second, z=1: HK? height?  Then once more to dim 7."""
import itertools, collections
W5=[0,7,28,23,30,11,29,9,25,27,26,18]  # walk in the paper (for reference)
# witness outmap from the paper (prop:hkfive): read from frontier.tex
import re
src=open('/data/ssg-proof/frontier.tex').read()
i=src.index('\\label{prop:hkfive}'); seg=src[i:i+3000]
m=re.search(r'\(((?:\d+,\s*){31}\d+)\)', seg); s5=[int(x) for x in m.group(1).replace(' ','').split(',')]
assert len(s5)==32, s5
def is_uso(s,n):
    for u in range(2**n):
        for v in range(u+1,2**n):
            if (s[u]^s[v])&(u^v)==0: return False
    return True
def acyclic(s,n):
    # edges u -> u^e for e in s[u]
    N=2**n; indeg=[0]*N; adj=[[] for _ in range(N)]
    for u in range(N):
        for i in range(n):
            if s[u]>>i&1: adj[u].append(u^(1<<i)); indeg[u^(1<<i)]+=1
    q=[u for u in range(N) if indeg[u]==0]; seen=0
    while q:
        u=q.pop(); seen+=1
        for w in adj[u]:
            indeg[w]-=1
            if indeg[w]==0: q.append(w)
    return seen==N
def ba_height(s,n,start):
    h=0; u=start
    while s[u]: u^=s[u]; h+=1
    return h
def max_height(s,n): return max(ba_height(s,n,u) for u in range(2**n))
def hk_face(s,n,free,base):
    """face: coordinates 'free' (list), base bits for the others. HK: dim vertex-disjoint paths source->sink within the face."""
    d=len(free)
    if d<2: return True
    verts=[]; 
    for bits in range(2**d):
        u=base
        for j,c in enumerate(free):
            if bits>>j&1: u|=1<<c
        verts.append(u)
    mask=sum(1<<c for c in free)
    out={u:(s[u]&mask) for u in verts}
    sink=[u for u in verts if out[u]==0]; source=[u for u in verts if out[u]==mask]
    assert len(sink)==1 and len(source)==1, (free,base)
    src,snk=source[0],sink[0]
    # unit vertex capacity max flow via node splitting, simple augmenting paths (BFS)
    # nodes: (u,'in'),(u,'out'); edge in->out cap1 (inf for src/snk); u_out -> w_in cap 1 for arcs u->w
    cap=collections.defaultdict(int)
    def add(a,b,c): cap[(a,b)]+=c; cap[(b,a)]+=0
    for u in verts:
        add((u,0),(u,1), 10**6 if u in (src,snk) else 1)
        for c in free:
            if s[u]>>c&1: add((u,1),((u^(1<<c)),0),1)
    flow=0; S=(src,0); T=(snk,1)
    while True:
        par={S:None}; q=[S]
        while q and T not in par:
            a=q.pop(0)
            for (x,y),c in list(cap.items()):
                if x==a and c>0 and y not in par: par[y]=a; q.append(y)
        if T not in par: break
        b=T
        while par[b] is not None:
            a=par[b]; cap[(a,b)]-=1; cap[(b,a)]+=1; b=a
        flow+=1
        if flow>=d: break
    return flow>=d
def is_hk(s,n):
    for d in range(2,n+1):
        for free in itertools.combinations(range(n),d):
            others=[c for c in range(n) if c not in free]
            for bits in range(2**len(others)):
                base=0
                for j,c in enumerate(others):
                    if bits>>j&1: base|=1<<c
                if not hk_face(s,n,list(free),base): return False
    return True
def product(s1,k,s2,l,z):
    """lem:hstar-super: s1 translated so sink is 0 (assumed), s(v1,v2)=(s1(v1), s2(v2 xor c(v1))) with c=z if v1!=0 else 0; first block = low k bits."""
    N=2**(k+l); s=[0]*N
    for v in range(N):
        v1=v&((1<<k)-1); v2=v>>k; c=z if v1!=0 else 0
        s[v]=s1[v1] | (s2[v2^c]<<k)
    return s
# translate s5 so its sink is 0
sink=[u for u in range(32) if s5[u]==0][0]
s5t=[s5[u^sink] for u in range(32)]  # translated: s'(u)=s(u xor sink)
assert s5t[0]==0 and is_uso(s5t,5) and acyclic(s5t,5)
print('witness: uso, acyclic, height', max_height(s5t,5), 'HK', is_hk(s5t,5))
s2=[1,0]  # 1-cube: vertex 0 points up (out={0}), vertex 1 sink
s6=product(s5t,5,s2,1,1)
print('6-cube: uso',is_uso(s6,6),'acyclic',acyclic(s6,6),'height',max_height(s6,6),'HK',is_hk(s6,6))
# also the other order: 1-cube first, witness second (auditor says this one fails HK / height <=11)
s6b=product([1,0],1,s5t,5,1)
print('6-cube (1-cube first): uso',is_uso(s6b,6),'acyclic',acyclic(s6b,6),'height',max_height(s6b,6),'HK',is_hk(s6b,6))
sink6=[u for u in range(64) if s6[u]==0][0]; s6t=[s6[u^sink6] for u in range(64)]
s7=product(s6t,6,s2,1,1)
print('7-cube: uso',is_uso(s7,7),'acyclic',acyclic(s7,7),'height',max_height(s7,7),'HK',is_hk(s7,7))
print('s6 outmap', s6)
