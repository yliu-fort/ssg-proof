import sys, random; sys.path.insert(0, '.')
from fractions import Fraction as F
import mycore as M, bsi as B, gen
import myinst, gstar, cc, wd

def corners(g):
    return [(B.corner(g, 'max', a), B.corner(g, 'min', b), f"s{a}t{b}") for a in (0, 1) for b in (0, 1)]

def table(name, g, w=None):
    if w is None: w = B.wstar_hk(g)
    print(f"== {name}: N={g.N} |Vmax|={len(g.of('max'))} |Vmin|={len(g.of('min'))} a={len(g.of('avg'))} stopping={B.is_stopping(g)}", flush=True)
    for sig, tau, lab in corners(g):
        r0, *_ = B.all_switches(g, sig)
        r1, s1, t1, L1, U1, h1 = B.bsi(g, sig, tau)
        r2, s2, t2, L2, U2, h2 = B.bsi(g, sig, tau, strict=True)
        ok1 = (L1 == U1 == w); ok2 = (L2 == U2 == w)
        print(f"   start {lab}: all-switches {r0:3d}   BSI {r1:3d} (opt {ok1})   strict {r2:3d} (opt {ok2})", flush=True)

# cross-check wstar_hk against brute force on small random stopping games
rng = random.Random(7)
n_ok = 0
for i in range(300):
    g = gen.rand_game(rng.choice([6, 7, 8]), rng, sink_bias=0.3)
    if not M.is_stopping(g): continue
    assert B.wstar_hk(g) == M.wstar(g); n_ok += 1
print("wstar_hk == brute on", n_ok, "stopping games", flush=True)

# ONE-PLAYER claim: BSI halts within |Vmax| rounds (U = w* exactly, so the veto
# admits only greedy switches; lem:max-deficit gives one non-greedy switch per round)
worst = 0; cnt = 0
for i in range(2000):
    g = gen.rand_game(rng.choice([8, 10, 12]), rng, p_avg=0.5, sink_bias=0.3)
    if not M.is_stopping(g) or g.of('min') or len(g.of('max')) < 2: continue
    w = B.wstar_hk(g)
    for a in (0, 1):
        r, s, t, L, U, h = B.bsi(g, B.corner(g, 'max', a), {}, brute=False)
        assert L == U == w
        worst = max(worst, r - len(g.of('max'))); cnt += 1
    if cnt >= 400: break
print("one-player: runs", cnt, "max(rounds - |Vmax|) =", worst, flush=True)
for n in range(1, 13):
    g = B.ladder(n); r, *_ = B.bsi(g, B.corner(g, 'max', 0), {})
    print("  L_%d one-player BSI rounds %d" % (n, r), flush=True)

for n in range(1, 11):
    g = B.ladder(n)
    table(f"L_{n} (+) dual", B.union(g, B.dual(g)))
for m in (3, 4, 5):
    table(f"H_{m}", myinst.H_m(m))
table("G* (gstar)", gstar.Gstar())
table("CC(1,2)", cc.CC(1, 2)); table("CC(2,3)", cc.CC(2, 3))
table("WD(4,2,6)", wd.WD(4, 2, 6))
kinds = ['min','min','avg','avg','max','avg','min','min']; T0, T1 = 8, 9
R = M.G(kinds, [(2,5),(5,3),(5,2),(0,T1),(0,T0),(T1,T0),(0,T0),(5,2)])
table("R (prop:own-stall)", R)
table("R (+) dual R", B.union(R, B.dual(R)))
