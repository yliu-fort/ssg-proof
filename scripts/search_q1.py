"""Random search for a Q_1 stall: a STOPPING SSG with a value-distinguishing
controlled vertex on which the level-1 Balas separator decides no controlled
vertex at all."""
import random, sys, time
from fractions import Fraction as F
from lp_exact import Game
from transport import sep, level_subsets, sanity, lift_point, build_lift
from lp_exact import check_feasible


def random_game(nmax, nmin, navg, rng):
    n = nmax + nmin + navg
    kinds = ['max'] * nmax + ['min'] * nmin + ['avg'] * navg
    rng.shuffle(kinds)
    succ = [(rng.randrange(n + 2), rng.randrange(n + 2)) for _ in range(n)]
    return Game(kinds, succ)


def q_stall(g, level=1, verbose=False):
    """Returns None if not a stall; otherwise a dict of data."""
    if not g.is_stopping():
        return None
    w = g.value()
    dist = [v for v in g.ctrl if w[g.succ[v][0]] != w[g.succ[v][1]]]
    if not dist:
        return None
    subs = level_subsets(g, level)
    # rule 6-ii: w* must be feasible for the lift before anything is interpreted
    rows = build_lift(g, subs)[1]
    check_feasible(rows, lift_point(g, w, subs), "lift")
    data = {}
    for v in g.ctrl:
        a, b = g.succ[v]
        s0 = sep(g, a, b, subsets=subs)[0]
        s1 = sep(g, b, a, subsets=subs)[0]
        data[v] = (s0, s1)
        if s0 <= 0 or s1 <= 0:
            return None                      # decided
    return {'w': w, 'dist': dist, 'sep': data}


if __name__ == '__main__':
    nmax, nmin, navg, trials, seed = (int(x) for x in sys.argv[1:6])
    lvl = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    rng = random.Random(seed)
    t0 = time.time()
    stop_ct = 0
    for it in range(trials):
        g = random_game(nmax, nmin, navg, rng)
        try:
            r = q_stall(g, lvl)
        except Exception as e:
            print("ERR", g.kinds, g.succ, e)
            raise
        if g.is_stopping():
            stop_ct += 1
        if r:
            print("STALL", g.kinds, g.succ)
            print("  w*=", r['w'])
            print("  dist=", r['dist'], " sep=", r['sep'])
            sys.stdout.flush()
    print(f"# done {trials} trials, {stop_ct} stopping, {time.time()-t0:.1f}s")
