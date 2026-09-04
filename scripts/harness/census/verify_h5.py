"""Independent check of the h*(5)=12 witness, from the outmap alone."""
S = [15,0,1,2,27,30,12,29,19,26,8,25,22,21,20,23,31,18,28,17,3,6,24,5,7,14,16,13,10,9,4,11]
M, NV = 5, 32
assert len(S) == NV
# bijection?
print('bijection            :', sorted(S) == list(range(NV)))
# USO condition
uso = all(((S[u]^S[v]) & (u^v)) != 0 for u in range(NV) for v in range(u+1, NV))
print('unique sink condition:', uso)
# acyclic?
colour = [0]*NV
def dfs(v):
    colour[v] = 1
    for i in range(M):
        if (S[v] >> i) & 1:
            w = v ^ (1 << i)
            if colour[w] == 1: return True
            if colour[w] == 0 and dfs(w): return True
    colour[v] = 2
    return False
acyc = not any(colour[v] == 0 and dfs(v) for v in range(NV))
print('acyclic              :', acyc)
# every face has a unique sink and a unique source (a direct check, not via the condition)
from itertools import product
ok_faces = True
for fixed in product([0,1,2], repeat=M):
    free = [i for i in range(M) if fixed[i] == 2]
    if not free: continue
    base = sum((fixed[i] & 1) << i for i in range(M) if fixed[i] != 2)
    fm = sum(1 << i for i in free)
    verts = [base | sum(((b >> t) & 1) << free[t] for t in range(len(free))) for b in range(1 << len(free))]
    sinks = [v for v in verts if (S[v] & fm) == 0]
    srcs  = [v for v in verts if (S[v] & fm) == fm]
    if len(sinks) != 1 or len(srcs) != 1: ok_faces = False
print('every face has exactly one sink and one source:', ok_faces)
# bottom-antipodal heights
h = []
for v0 in range(NV):
    v, k = v0, 0
    while S[v]:
        v ^= S[v]; k += 1
        assert k <= NV
    h.append(k)
print('bottom-antipodal height =', max(h), ' attained from', h.index(max(h)))
trace = []
v = h.index(max(h))
while True:
    trace.append(v)
    if S[v] == 0: break
    v ^= S[v]
print('trace                   =', trace, 'length', len(trace)-1)
# the two laws, checked directly on this trace
sig = trace; L = len(sig)-1
Sk = [sig[t] ^ sig[t+1] for t in range(L)]
law_i  = all((sig[t]^sig[tp]) & Sk[t] for t in range(L+1) for tp in range(t+1, L+1) if t < L)
law_ii = all(((sig[t]^sig[tp]) & ~Sk[tp]) & 31 for tp in range(L) for t in range(tp))
print('trace obeys cor:no-return and cor:law-b:', law_i and law_ii)
