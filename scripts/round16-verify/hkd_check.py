import sys, re, glob
sys.path.insert(0,'.')
from auso import is_uso, is_acyclic, ba_heights, ba_trace
from my_D import is_holt_klee
s6=[5,10,15,4,9,14,11,8,13,6,7,12,1,0,2,3,48,17,51,50,54,61,60,55,30,25,24,59,26,53,52,63,32,49,35,34,38,45,44,39,62,57,56,43,58,37,36,47,16,33,19,18,22,29,28,23,46,41,40,27,42,21,20,31]
s7=[7,4,21,6,10,11,17,24,29,12,31,14,3,0,25,2,23,18,5,20,19,22,8,9,15,28,13,30,27,26,1,16,56,113,43,42,102,117,100,103,98,121,32,99,46,127,44,125,41,40,54,51,116,101,50,119,48,97,58,59,62,109,60,111,120,81,107,106,70,85,68,71,66,89,96,67,110,95,108,93,105,104,118,115,84,69,114,87,112,65,122,123,126,77,124,79,88,49,75,74,38,53,36,39,34,57,64,35,78,63,76,61,73,72,86,83,52,37,82,55,80,33,90,91,94,45,92,47]
for s,m,name in ((s6,6,'s_6'),(s7,7,'s_7')):
    u=is_uso(s,m); a=is_acyclic(s,m); h=ba_heights(s,m); hk,w=is_holt_klee(s,m)
    top=[v for v in range(1<<m) if h[v]==max(h)]
    print(f'{name}: USO {u} acyclic {a} height {max(h)} at {top} HK {hk} walk from {top[0]}: {ba_trace(s,top[0])}', flush=True)
# hkd:plus-one: L(s)(v,b) = s(v) u {m : phi(v) != b}, phi = 1_o
def lift(s,m):
    n=1<<m; o=[v for v in range(n) if s[v]==0][0]; L=[0]*(2*n)
    for b in (0,1):
        for v in range(n):
            phi = 1 if v==o else 0
            L[v|(b<<m)] = s[v] | ((1<<m) if phi!=b else 0)
    return L
B1=[0,1,3,6,7,4,5,2]; gsharp=[0,1,3,6,7,4,13,10,14,15,9,12,11,8,5,2]
txt=open('/data/ssg-proof/frontier.tex').read(); i=txt.find('label{prop:hkfive}'); seg=txt[i:i+3000]
hk11=[int(x) for x in re.search(r'\(((?:\d+,\s*){31}\d+)\)',seg).group(1).replace(' ','').split(',')]
for s,m,name in ((B1,3,'B^1'),(gsharp,4,'G#'),(hk11,5,'HK11'),(s6,6,'s_6')):
    L=lift(s,m); h0=max(ba_heights(s,m)); u=is_uso(L,m+1); a=is_acyclic(L,m+1); h=max(ba_heights(L,m+1)) if (u and a) else None
    hk0=is_holt_klee(s,m)[0]; hk1=is_holt_klee(L,m+1)[0] if (u and a) else None
    print(f'lift of {name}: USO {u} acyclic {a} height {h0} -> {h} HK {hk0} -> {hk1}', flush=True)
