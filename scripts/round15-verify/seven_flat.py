"""Independent check of degen:lem-seven-flat's finite part on the height-7 representative:
(F1)-subcubes (blocks on which s(x) xor s(y) = x xor y), which of them meet a length-7 walk,
and (F2) at walk vertices."""
import itertools
s=[0,1,3,6,7,4,13,10,14,15,9,12,11,8,5,2]; m=4
def walk(v):
    w=[v]
    while s[v]: v^=s[v]; w.append(v)
    return w
starts=[v for v in range(16) if len(walk(v))-1==7]
print('starts of walk length 7:', starts, [walk(v) for v in starts])
# all subcubes: (base with zeros on directions D, D nonempty)
blocks=[]
for r in range(1,m+1):
    for D in itertools.combinations(range(m),r):
        mask=sum(1<<i for i in D)
        for base in range(16):
            if base & mask: continue
            verts=[base|sub for sub in range(16) if sub & ~mask==0]
            ok=all((s[x]^s[y])==(x^y) for x,y in itertools.combinations(verts,2))
            if ok: blocks.append((D,verts))
print('(F1)-subcubes of dim>=1:', blocks)
for st in starts:
    w=walk(st)
    for D,verts in blocks:
        meet=[(t,v) for t,v in enumerate(w) if v in verts]
        if not meet: continue
        mask=sum(1<<i for i in D)
        f2=all(s[v]&mask==0 for t,v in meet)
        print(f'start {st}: block {verts} (dirs {D}) meets walk at {meet}; (F2) s(sigma_t) avoids block dirs: {f2}; both ends on walk: {len(meet)>1}')
