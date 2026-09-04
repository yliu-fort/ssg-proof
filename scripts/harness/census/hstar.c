/* Decide h*(m) exactly for m = 5 (and re-derive f(m)) by combining the two
   halves of lem:auso-laws.

   f(m) = greatest L with a sequence sigma_0..sigma_L, S_t = sigma_t ^ sigma_{t+1}
          nonempty for t<L, obeying
            (i)  (sigma_t ^ sigma_t') & S_t != 0        for 0<=t<t'<=L
            (ii) (sigma_t ^ sigma_t') not subset of S_t' for 0<=t<t'<=L-1.
   h*(m) = greatest L such that some such sequence is the bottom-antipodal trace
          of an AUSO, i.e. s(sigma_t)=S_t (t<L), s(sigma_L)=0, and s extends to
          an acyclic unique sink orientation of the whole cube.
   By lem:auso-laws h* <= f; this program computes both.                     */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int M, NV, FULL;
static int sig[40], S[40];
static int s[32]; static char used[32];
static long long n_seq_at_L = 0, n_completion_tries = 0;
static int TARGET;              /* sequence length we are testing            */
static int MODE;                /* 0 = just find f(m); 1 = also realise      */
static int found = 0, best_seq_len = 0;
static int found_s[32], found_sig[40];

/* ---- acyclicity ---- */
static int colour[32];
static int dfs_cyc(int v){
    colour[v]=1;
    for(int i=0;i<M;i++) if((s[v]>>i)&1){ int w=v^(1<<i);
        if(colour[w]==1) return 1;
        if(colour[w]==0 && dfs_cyc(w)) return 1; }
    colour[v]=2; return 0;
}
static int is_acyclic(void){
    memset(colour,0,sizeof colour);
    for(int v=0;v<NV;v++) if(!colour[v] && dfs_cyc(v)) return 0;
    return 1;
}
/* ---- complete the outmap over the vertices not on the trace ---- */
static int rest[32], nrest;
static int complete(int p){
    if(p==nrest) return is_acyclic();
    int v=rest[p];
    for(int t=0;t<NV;t++){
        if(used[t]) continue;
        int ok=1;
        for(int u=0;u<NV;u++){
            if(u==v) continue;
            if(s[u]<0) continue;
            if((((s[u]^t)&(u^v)))==0){ ok=0; break; }
        }
        if(!ok) continue;
        s[v]=t; used[t]=1;
        if(complete(p+1)) return 1;
        used[t]=0; s[v]=-1;
    }
    return 0;
}
static int realise(int L){
    n_completion_tries++;
    for(int v=0;v<NV;v++){ s[v]=-1; }
    memset(used,0,sizeof used);
    for(int t=0;t<=L;t++){
        int v=sig[t], val=(t<L)?S[t]:0;
        if(s[v]>=0) return 0;             /* cannot happen: sigmas distinct */
        if(used[val]) return 0;           /* outmap must be a bijection     */
        s[v]=val; used[val]=1;
    }
    /* the trace values must already be pairwise USO-compatible */
    for(int a=0;a<NV;a++) if(s[a]>=0) for(int b=a+1;b<NV;b++) if(s[b]>=0)
        if((((s[a]^s[b])&(a^b)))==0) return 0;
    nrest=0;
    for(int v=0;v<NV;v++) if(s[v]<0) rest[nrest++]=v;
    return complete(0);
}

static void rec(int t){
    if(found) return;
    if(t==TARGET){
        n_seq_at_L++;
        if(MODE && realise(TARGET)){
            found=1; memcpy(found_s,s,sizeof s); memcpy(found_sig,sig,sizeof sig);
        }
        return;
    }
    for(int Sm=1; Sm<=FULL; Sm++){
        /* law (ii): for all u < t, (sigma_u ^ sigma_t) not subset of S_t */
        int ok=1;
        for(int u=0;u<t;u++) if((((sig[u]^sig[t]) & ~Sm) & FULL)==0){ ok=0; break; }
        if(!ok) continue;
        int nxt = sig[t]^Sm;
        /* law (i): for all u <= t, (sigma_u ^ nxt) & S_u != 0 */
        for(int u=0;u<=t;u++){
            int Su = (u==t)?Sm:S[u];
            if((((sig[u]^nxt)&Su))==0){ ok=0; break; }
        }
        if(!ok) continue;
        S[t]=Sm; sig[t+1]=nxt;
        rec(t+1);
        if(found) return;
    }
}

int main(int argc,char**argv){
    M = argc>1?atoi(argv[1]):5;
    NV=1<<M; FULL=NV-1;
    /* by translation invariance we may take sigma_0 = 0 */
    sig[0]=0;
    printf("m = %d\n", M);
    /* pass 1: f(m) -- longest law-abiding sequence */
    MODE=0;
    int L;
    for(L=1; L<=NV; L++){
        TARGET=L; n_seq_at_L=0; found=0;
        rec(0);
        if(n_seq_at_L==0){ printf("  f(%d) = %d\n", M, L-1); break; }
        printf("    law-abiding sequences of length %2d from sigma_0=0 : %lld\n", L, n_seq_at_L);
    }
    int fm = L-1;
    /* pass 2: h*(m) -- longest realisable one */
    MODE=1;
    for(L=fm; L>=1; L--){
        TARGET=L; n_seq_at_L=0; found=0; n_completion_tries=0;
        rec(0);
        printf("    L=%2d : %lld sequences, %lld completion attempts, realisable = %s\n",
               L, n_seq_at_L, n_completion_tries, found?"YES":"no");
        fflush(stdout);
        if(found){
            printf("  h*(%d) = %d\n", M, L);
            printf("  trace:"); for(int t=0;t<=L;t++) printf(" %d",found_sig[t]);
            printf("\n  outmap:"); for(int v=0;v<NV;v++) printf(" %d",found_s[v]);
            printf("\n");
            break;
        }
    }
    return 0;
}
