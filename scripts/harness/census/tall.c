/* Lower bounds on h*(m), the greatest bottom-antipodal height of an AUSO of
   the m-cube, by randomised DFS generation plus suffix re-randomisation.
   The USO test is the Szabo-Welzl condition (s(u)^s(v)) & (u^v) != 0.        */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int M, NV;
static int s[32], used[32];
static unsigned long long rng_state;
static unsigned long long rnd(void){
    rng_state ^= rng_state<<13; rng_state ^= rng_state>>7; rng_state ^= rng_state<<17;
    return rng_state;
}
static int colour[32];
static int dfs_cyc(int v){
    colour[v]=1;
    for(int i=0;i<M;i++) if((s[v]>>i)&1){
        int w=v^(1<<i);
        if(colour[w]==1) return 1;
        if(colour[w]==0 && dfs_cyc(w)) return 1;
    }
    colour[v]=2; return 0;
}
static int is_acyclic(void){
    memset(colour,0,sizeof colour);
    for(int v=0;v<NV;v++) if(!colour[v] && dfs_cyc(v)) return 0;
    return 1;
}
static int ba_height(void){
    int best=0;
    for(int v0=0;v0<NV;v0++){
        int v=v0,k=0;
        while(s[v]){ v^=s[v]; if(++k>NV+2) return -1; }
        if(k>best) best=k;
    }
    return best;
}
/* randomised completion of s from position p onward; returns 1 on success */
static int complete(int p){
    if(p==NV) return 1;
    int cand[32], nc=0;
    for(int t=0;t<NV;t++){
        if(used[t]) continue;
        int ok=1;
        for(int u=0;u<p;u++) if((((s[u]^t)&(u^p)))==0){ ok=0; break; }
        if(ok) cand[nc++]=t;
    }
    /* shuffle */
    for(int i=nc-1;i>0;i--){ int j=rnd()%(i+1); int tmp=cand[i]; cand[i]=cand[j]; cand[j]=tmp; }
    for(int i=0;i<nc;i++){
        s[p]=cand[i]; used[cand[i]]=1;
        if(complete(p+1)) return 1;
        used[cand[i]]=0;
    }
    return 0;
}
int main(int argc,char**argv){
    M = argc>1?atoi(argv[1]):5;
    long long iters = argc>2?atoll(argv[2]):200000;
    rng_state = argc>3?atoll(argv[3]):88172645463325252ULL;
    NV=1<<M;
    int best=-1, best_s[32]; long long hist[80]; memset(hist,0,sizeof hist);
    long long n_acyc=0, n_gen=0;
    /* phase 1: random restarts */
    for(long long it=0; it<iters; it++){
        memset(used,0,sizeof used);
        if(!complete(0)) continue;
        n_gen++;
        if(!is_acyclic()) continue;
        n_acyc++;
        int h=ba_height();
        if(h>=0 && h<80) hist[h]++;
        if(h>best){ best=h; memcpy(best_s,s,sizeof s);
            printf("[gen %lld] new best BA height %d\n",it,h); fflush(stdout); }
    }
    /* phase 2: suffix re-randomisation around the best */
    for(long long it=0; it<iters*4; it++){
        int cut = 1 + rnd()%(NV-1);
        memcpy(s,best_s,sizeof s);
        memset(used,0,sizeof used);
        for(int v=0;v<cut;v++) used[s[v]]=1;
        if(!complete(cut)) continue;
        if(!is_acyclic()) continue;
        int h=ba_height();
        if(h>=0 && h<80) hist[h]++;
        if(h>best){ best=h; memcpy(best_s,s,sizeof s);
            printf("[suffix %lld cut %d] new best BA height %d\n",it,cut,h); fflush(stdout); }
    }
    printf("m=%d  generated %lld, acyclic %lld,  best BA height found = %d\n",M,n_gen,n_acyc,best);
    printf("height histogram over sampled AUSOs:\n");
    for(int h=0;h<80;h++) if(hist[h]) printf("  h=%2d : %lld\n",h,hist[h]);
    printf("best outmap:");
    for(int v=0;v<NV;v++) printf(" %d",best_s[v]);
    printf("\n");
    return 0;
}
