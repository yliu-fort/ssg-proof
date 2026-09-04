/* Independent census of unique sink orientations of the m-cube.
   Written from the Szabo-Welzl definition, not from any existing code here.

   Outmap s : {0,1}^m -> {0,1}^m ; bit i of s(v) = 1 iff the edge
   {v, v^e_i} is directed OUT of v.  s is the outmap of a USO iff for all
   u != v,   (s(u) ^ s(v)) & (u ^ v)  !=  0.
   Bottom-antipodal walk: v -> v ^ s(v).  Height = max over starts of the
   number of steps to the global sink (s(v)=0).
   Holt-Klee: every face of dimension d carries d internally vertex-disjoint
   directed paths from its source to its sink.                            */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int M, NV;
static int s[16];
static char used[16];

static long long n_uso = 0, n_auso = 0, n_auso_hk = 0;
static long long h_hist[64];          /* BA height histogram over AUSOs   */
static long long h_hist_hk[64];       /* ... restricted to Holt-Klee      */
static long long n_ba_cycle = 0;
static int best_h = -1;
static int best_map[16];
static int best_h_hk = -1;
static int best_map_hk[16];

/* ---------- acyclicity of the induced digraph ---------- */
static int colour[16];
static int dfs_cyc(int v)
{
    colour[v] = 1;
    for (int i = 0; i < M; i++)
        if ((s[v] >> i) & 1) {
            int w = v ^ (1 << i);
            if (colour[w] == 1) return 1;
            if (colour[w] == 0 && dfs_cyc(w)) return 1;
        }
    colour[v] = 2;
    return 0;
}
static int is_acyclic(void)
{
    memset(colour, 0, sizeof colour);
    for (int v = 0; v < NV; v++)
        if (colour[v] == 0 && dfs_cyc(v)) return 0;
    return 1;
}

/* ---------- bottom-antipodal height ---------- */
static int ba_height(void)          /* -1 if some walk cycles */
{
    int best = 0;
    for (int v0 = 0; v0 < NV; v0++) {
        int v = v0, k = 0;
        while (s[v] != 0) {
            v ^= s[v];
            if (++k > NV + 2) return -1;
        }
        if (k > best) best = k;
    }
    return best;
}

/* ---------- Holt-Klee ---------- */
/* face = (fixed mask, fixed bits).  free coords = ~fixed.
   max number of internally vertex-disjoint source->sink directed paths,
   by unit-capacity vertex-split max flow (Ford-Fulkerson, tiny graphs).  */
static int fmask, fbits, fdim;
static int in_face(int v) { return (v & fmask) == fbits; }

static char blocked[16];   /* interior vertex already used by a path */
static char seen[16];
static int src, snk;
static int aug(int v)
{
    if (v == snk) return 1;
    for (int i = 0; i < M; i++) {
        if (fmask & (1 << i)) continue;
        if (!((s[v] >> i) & 1)) continue;
        int w = v ^ (1 << i);
        if (seen[w] || (w != snk && blocked[w])) continue;
        seen[w] = 1;
        if (aug(w)) { if (w != snk) blocked[w] = 1; return 1; }
    }
    return 0;
}
static int disjoint_paths(void)
{
    int cnt = 0;
    memset(blocked, 0, sizeof blocked);
    for (;;) {
        memset(seen, 0, sizeof seen);
        seen[src] = 1;
        if (!aug(src)) break;
        cnt++;
        if (cnt >= fdim) break;
    }
    return cnt;
}
static int holt_klee(void)
{
    /* iterate over all faces: each coordinate fixed to 0, 1, or free */
    int pow3 = 1;
    for (int i = 0; i < M; i++) pow3 *= 3;
    for (int code = 0; code < pow3; code++) {
        int c = code;
        fmask = 0; fbits = 0; fdim = 0;
        for (int i = 0; i < M; i++) {
            int d = c % 3; c /= 3;
            if (d == 0) fdim++;
            else { fmask |= 1 << i; if (d == 2) fbits |= 1 << i; }
        }
        if (fdim < 2) continue;              /* dim 0,1 are automatic */
        /* source: s(v) covers all free coords ; sink: none */
        int free_mask = ((1 << M) - 1) & ~fmask;
        src = -1; snk = -1;
        for (int v = 0; v < NV; v++) {
            if (!in_face(v)) continue;
            int o = s[v] & free_mask;
            if (o == free_mask) src = v;
            if (o == 0) snk = v;
        }
        if (src < 0 || snk < 0) return 0;    /* not a USO face; cannot happen */
        if (disjoint_paths() < fdim) return 0;
    }
    return 1;
}

/* ---------- enumeration ---------- */
static void record(void)
{
    n_uso++;
    if (!is_acyclic()) return;
    n_auso++;
    int h = ba_height();
    if (h < 0) { n_ba_cycle++; return; }
    if (h < 64) h_hist[h]++;
    if (h > best_h) { best_h = h; memcpy(best_map, s, sizeof s); }
    if (holt_klee()) {
        n_auso_hk++;
        if (h < 64) h_hist_hk[h]++;
        if (h > best_h_hk) { best_h_hk = h; memcpy(best_map_hk, s, sizeof s); }
    }
}

static void rec(int v)
{
    if (v == NV) { record(); return; }
    for (int t = 0; t < NV; t++) {
        if (used[t]) continue;               /* the outmap is a bijection */
        int ok = 1;
        for (int u = 0; u < v; u++)
            if (((s[u] ^ t) & (u ^ v)) == 0) { ok = 0; break; }
        if (!ok) continue;
        s[v] = t; used[t] = 1;
        rec(v + 1);
        used[t] = 0;
    }
}

int main(int argc, char **argv)
{
    M = argc > 1 ? atoi(argv[1]) : 3;
    NV = 1 << M;
    memset(used, 0, sizeof used);
    rec(0);
    printf("m = %d\n", M);
    printf("  USOs                 : %lld\n", n_uso);
    printf("  acyclic USOs (AUSO)  : %lld\n", n_auso);
    printf("  AUSOs with BA cycle  : %lld\n", n_ba_cycle);
    printf("  Holt-Klee AUSOs      : %lld\n", n_auso_hk);
    printf("  h*(%d)               : %d\n", M, best_h);
    printf("  h*_HK(%d)            : %d\n", M, best_h_hk);
    printf("  BA height histogram (all AUSOs):\n");
    for (int h = 0; h < 64; h++) if (h_hist[h]) printf("    h=%2d : %lld\n", h, h_hist[h]);
    printf("  BA height histogram (Holt-Klee AUSOs):\n");
    for (int h = 0; h < 64; h++) if (h_hist_hk[h]) printf("    h=%2d : %lld\n", h, h_hist_hk[h]);
    printf("  a height-maximal outmap:");
    for (int v = 0; v < NV; v++) printf(" %d", best_map[v]);
    printf("\n  a height-maximal Holt-Klee outmap:");
    for (int v = 0; v < NV; v++) printf(" %d", best_map_hk[v]);
    printf("\n");
    return 0;
}
