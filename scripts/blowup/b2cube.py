import sys, json, itertools; sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights
from my_D import is_holt_klee
from blowz import D_general

def automorphs(m):
    for perm in itertools.permutations(range(m)):
        for t in range(1<<m):
            yield perm, t
def apply(s, m, perm, t):
    n=1<<m
    def pi(v): 
        w=0
        for i in range(m):
            if v>>i&1: w|=1<<perm[i]
        return w
    out=[0]*n
    for v in range(n):
        w = pi(v)^t
        out[w] = pi(s[v])
    return out
def canon_key(s,m):
    return min(tuple(apply(s,m,p,t)) for p,t in automorphs(m))

surv = json.load(open('survey_h6HK_k0.json'))
keys = {}
for e in surv:
    keys[canon_key(e['outmap'],4)] = e
print('survey HK h6 classes:', len(keys), 'realised:', sum(1 for e in surv if e['ok']))

# all AUSOs of the 2-cube
twos=[]
for s in itertools.product(range(4), repeat=4):
    s=list(s)
    if is_uso(s,2) and is_acyclic(s,2): twos.append(s)
print('2-cube AUSOs:', len(twos))
seen=set()
for s in twos:
    h=max(ba_heights(s,2))
    B=D_general(s,2,'sinkstart')
    ok = is_uso(B,4) and is_acyclic(B,4)
    hB = max(ba_heights(B,4)) if ok else None
    hk = is_holt_klee(B,4) if ok else None
    ck = canon_key(B,4)
    tag = ck in keys
    e = keys.get(ck)
    print('seed',s,'h',h,'-> B: AUSO',ok,'height',hB,'HK',hk,'in survey',tag, 'realised' if e and e['ok'] else '', 'canon', ck[:16] if ck in seen else '')
    seen.add(ck)

# B^2 from the 1-cube
s1=D_general([1,0],1,'sinkstart'); print('B^1 =', s1, 'h', max(ba_heights(s1,3)), 'HK', is_holt_klee(s1,3))
s2=D_general(s1,3,'sinkstart'); print('B^2 AUSO', is_uso(s2,5) and is_acyclic(s2,5), 'h', max(ba_heights(s2,5)), 'HK', is_holt_klee(s2,5))
h=ba_heights(s1,3); sink=[v for v in range(8) if s1[v]==0][0]; start=max(range(8), key=lambda v:h[v]); z=sink^start
print('level-2 z =', z, '(bits)', [i for i in range(3) if z>>i&1], 'sink',sink,'start',start)
diff=[]
for v in range(8):
    d = s1[v^z]^s1[v]
    for i in range(3):
        if d>>i&1: diff.append((v,i))
print('layer-00 incidences that differ from s1:', len(diff), 'of 24;', diff)
print('  with i == translated coord:', [(v,i) for v,i in diff if z>>i&1], ' i != j:', [(v,i) for v,i in diff if not z>>i&1])
print('B^2 outmap:', s2)
