#!/usr/bin/env python3
"""Root-agent verification of the round-18 drive-line route's combinatorial claims, from the statements:
dl:flippable (a): reversing one edge {sigma, sigma^e_v} of a unique sink orientation s leaves a USO iff the endpoints
have the same bottom-antipodal successor (sigma ^ s(sigma) == sigma' ^ s(sigma')); the flip then transposes the outmap
values; (b) acyclicity of the flipped orientation iff no other directed path sigma -> sigma'; (c) parity: over all pairs of
USOs of the m-cube, d(s,s') = [sgn s != sgn s'] mod 2; dl:b2-distance: d(B^2, B^2(.^z)) = 42,52,32,44 for z = 8,10,24,26,
17 combed edges in B^2, sgn(B^2) = +1. Outmaps as bitmasks of outgoing directions; exhaustive at m = 2,3."""
import itertools, sys

def faces(m):
    out = []
    for J in range(1, 1 << m):
        fixed = [v for v in range(m) if not (J >> v) & 1]
        for bits in itertools.product((0, 1), repeat=len(fixed)):
            base = sum(b << v for b, v in zip(bits, fixed))
            verts = [base | sub for sub in range(1 << m) if sub & ~J == 0]
            out.append((J, verts))
    return out

def is_uso(s, m, FACES):
    for J, verts in FACES:
        if sum(1 for v in verts if s[v] & J == 0) != 1: return False
    return True

def all_usos(m):
    FACES = faces(m); n = 1 << m; edges = [(v, v | (1 << k)) for v in range(n) for k in range(m) if not (v >> k) & 1]
    res = []
    for bits in range(1 << len(edges)):
        s = [0] * n
        for i, (a, b) in enumerate(edges):
            k = (a ^ b)
            if (bits >> i) & 1: s[a] |= k      # oriented a -> b: k outgoing at a
            else: s[b] |= k
        if is_uso(s, m, FACES): res.append(tuple(s))
    return res, FACES

def acyclic(s, m):
    n = 1 << m; adj = {v: [v ^ (1 << k) for k in range(m) if (s[v] >> k) & 1] for v in range(n)}
    state = [0]*n
    def dfs(u):
        state[u] = 1
        for w in adj[u]:
            if state[w] == 1: return False
            if state[w] == 0 and not dfs(w): return False
        state[u] = 2; return True
    return all(state[v] or dfs(v) for v in range(n))

def has_path_avoiding(s, m, a, b):
    """directed path a -> b in s not using the edge (a,b)."""
    n = 1 << m; seen = {a}; stack = [a]
    while stack:
        u = stack.pop()
        for k in range(m):
            if (s[u] >> k) & 1:
                w = u ^ (1 << k)
                if u == a and w == b: continue
                if w == b: return True
                if w not in seen: seen.add(w); stack.append(w)
    return False

def sign(perm):
    seen = [False]*len(perm); sgn = 1
    for i in range(len(perm)):
        if not seen[i]:
            j = i; L = 0
            while not seen[j]: seen[j] = True; j = perm[j]; L += 1
            if L % 2 == 0: sgn = -sgn
    return sgn

def dist(s, t, m):
    n = 1 << m
    return sum(1 for v in range(n) for k in range(m) if not (v >> k) & 1 and ((s[v] >> k) & 1) != ((t[v] >> k) & 1))

for m in (2, 3):
    U, FACES = all_usos(m); n = 1 << m; Uset = set(U)
    viol = 0; flips = 0; acy_viol = 0
    for s in U:
        for v in range(n):
            for k in range(m):
                if (v >> k) & 1: continue
                w = v | (1 << k); flips += 1
                t = list(s); t[v] ^= 1 << k; t[w] ^= 1 << k; t = tuple(t)
                combed = (v ^ s[v]) == (w ^ s[w])
                if (t in Uset) != combed: viol += 1
                if combed:
                    # the flip transposes the outmap values of the endpoints
                    assert t[v] == s[w] and t[w] == s[v]
                    if acyclic(s, m):
                        a, b = (v, w) if (s[v] >> k) & 1 else (w, v)
                        if acyclic(t, m) != (not has_path_avoiding(s, m, a, b)): acy_viol += 1
    # parity claim over all pairs
    perms = [tuple(s) for s in U]; sg = [sign(p) for p in perms]   # the outmap itself is the bijection
    par_viol = sum(1 for i in range(len(U)) for j in range(i+1, len(U)) if dist(U[i], U[j], m) % 2 != (sg[i] != sg[j]))
    print(f'm={m}: {len(U)} USOs, {flips} single-edge flips: combed criterion violations {viol}; acyclicity law violations {acy_viol}; parity law violations over all pairs {par_viol}')
    assert viol == 0 and acy_viol == 0 and par_viol == 0

# B^2 (coordinates seed, alpha1, beta1, alpha2, beta2), the paper's outmap
B2 = (7,4,5,2,0,1,3,6,24,9,27,14,31,28,29,10,16,25,19,30,23,20,21,26,8,17,11,22,15,12,13,18)
m = 5; n = 32; FACES5 = faces(5)
assert is_uso(B2, 5, FACES5) and acyclic(B2, 5)
combed = sum(1 for v in range(n) for k in range(m) if not (v >> k) & 1 and (v ^ B2[v]) == ((v | 1 << k) ^ B2[v | 1 << k]))
sg = sign(tuple(B2))
print(f'B^2: USO, acyclic, combed edges {combed} of 80, sgn {sg}')
for z in (8, 10, 24, 26):
    t = tuple(B2[v ^ z] for v in range(n))
    print(f'  d(B^2, B^2(.^{z})) = {dist(B2, t, m)}, translate is USO: {is_uso(t, 5, FACES5)}, acyclic: {acyclic(t, 5)}')
assert combed == 17 and sg == 1 and [dist(B2, tuple(B2[v ^ z] for v in range(n)), m) for z in (8, 10, 24, 26)] == [42, 52, 32, 44]
print('ALL DL COMBINATORIAL CHECKS PASSED')
