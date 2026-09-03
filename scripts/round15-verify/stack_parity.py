"""Verify lem:hcube-stack (a),(b) and cor:hcube-parity's census claims with my own predicates."""
import sys, itertools; sys.path.insert(0,'../solo')
from auso import is_uso, is_acyclic, ba_heights
from my_D import is_holt_klee
two=[list(s) for s in itertools.product(range(4),repeat=4) if is_uso(list(s),2)]
print('2-cube USOs', len(two), 'acyclic', sum(is_acyclic(s,2) for s in two))
def stack(G,F,phi):  # bottom copy (x3=0) carries G, top carries F; vertical edge at v points up iff phi(v)=1
    s=[0]*8
    for v in range(4):
        s[v]=G[v] | (4 if phi[v] else 0)        # bottom: up-edge out iff phi=1
        s[v|4]=F[v] | (0 if phi[v] else 4)      # top: down-edge out iff phi=0
    return s
def src(F):
    return [v for v in range(4) if F[v]==3][0]
def snk(F): return [v for v in range(4) if F[v]==0][0]
# (a) G=F, all phi
tot=0; good=0; rule=0
for F in two:
    for bits in range(16):
        phi=[(bits>>v)&1 for v in range(4)]
        s=stack(F,F,phi); tot+=1
        ok=is_uso(s,3) and is_acyclic(s,3) and is_holt_klee(s,3)[0]
        balanced = sum(phi)==2
        pred = not (balanced and phi[src(F)]==phi[snk(F)])
        good+=ok; rule+= (ok==pred)
        assert is_uso(s,3)
print('(a) pairs',tot,'acyclic+HK',good,'rule agrees',rule)
# (b) phi=0, all F,G
tot=0; fail=0; rule=0
def adj(a,b): return bin(a^b).count('1')==1
for F in two:
    for G in two:
        s=stack(G,F,[0,0,0,0]); tot+=1
        assert is_uso(s,3) and is_acyclic(s,3)
        hk=is_holt_klee(s,3)[0]
        pred_fail = adj(src(F),snk(F)) and adj(src(G),snk(G)) and (src(F)^snk(F))==(src(G)^snk(G)) and ((src(F)&~(src(F)^snk(F)))!=(src(G)&~(src(G)^snk(G))))
        # opposite edges of the square: same direction, different fixed coordinate
        fail+= (not hk); rule+= ((not hk)==pred_fail)
print('(b) pairs',tot,'not HK',fail,'rule agrees',rule)
# parity-good census at m=4
def parity_good(s,m):
    h=ba_heights(s,m)
    for i in range(m):
        for j in range(i+1,m):
            mask=(1<<i)|(1<<j)
            for base in range(1<<m):
                if base&mask: continue
                verts=[base|sub for sub in (0,1<<i,1<<j,mask)]
                # face orientation: restrict s to {i,j}
                F={v:((s[v]>>i)&1)|(((s[v]>>j)&1)<<1) for v in verts}
                srcv=[v for v in verts if F[v]==3][0]; snkv=[v for v in verts if F[v]==0][0]
                par=[h[v]%2 for v in verts]
                if sum(par)==2 and h[srcv]%2==h[snkv]%2: return False
    return True
reps=[]
for line in open('../solo/census/classes4.txt'):
    if not line.startswith('REP'): continue
    parts=line.split(); hh=int(parts[1][2:]); hk=int(parts[2][3:]); s=[int(x) for x in parts[4:]]
    reps.append((hh,hk,s))
h7=[s for hh,hk,s in reps if hh==7]; h6hk=[s for hh,hk,s in reps if hh==6 and hk==1]
print('m=4: height-7 class parity-good:', [parity_good(s,4) for s in h7], '| HK height-6 classes parity-good:', sum(parity_good(s,4) for s in h6hk), 'of', len(h6hk))
# m=3 classes: enumerate all AUSOs of the 3-cube and find max height among parity-good
three=[list(s) for s in itertools.product(range(8),repeat=8) if is_uso(list(s),3) and is_acyclic(list(s),3)]
pg=[max(ba_heights(s,3)) for s in three if parity_good(s,3)]
print('m=3 AUSOs',len(three),'parity-good',len(pg),'max height among parity-good',max(pg), 'height-4 parity-good count', sum(1 for x in pg if x==4))
