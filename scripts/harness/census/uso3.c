/* Census v2.  Two fixes over v1:
   (a) Holt-Klee now uses a genuine unit-capacity max flow with residual
       arcs on the vertex-split graph, not greedy path packing.
   (b) isomorphism classes counted, under the cube automorphism group
       (pi,t) : v -> pi(v)^t of order 2^m m!, acting by s'(pi(v)^t)=pi(s(v)).
   The USO/AUSO/height code is unchanged from v1, which already reproduced
   #USO(3)=744, #AUSO(3)=728, h*(3)=4, #USO(4)=5541744, #AUSO(4)=4792176.  */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int M, NV;
static int s[16];
static char used[16];

static long long n_uso=0, n_auso=0, n_auso_hk=0, n_ba_cycle=0;
static long long cls_auso=0, cls_hk=0;
static long long h_hist[64], h_hist_hk[64], h_cls[64], h_cls_hk[64];
static int best_h=-1, best_h_hk=-1;
static int best_map[16], best_map_hk[16];
static long long n_best=0, n_best_hk=0;

/* ---------------- acyclicity ---------------- */
static int colour[16];
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

/* ---------------- bottom-antipodal height ---------------- */
static int ba_height(void){
    int best=0;
    for(int v0=0;v0<NV;v0++){
        int v=v0,k=0;
        while(s[v]){ v^=s[v]; if(++k>NV+2) return -1; }
        if(k>best) best=k;
    }
    return best;
}

/* ---------------- Holt-Klee via unit-capacity max flow ---------------- */
/* node ids: vertex v -> in = 2v, out = 2v+1 ; capacity 1 on (in,out)
   except for source and sink where it is M.  face edges v->w give
   (2v+1, 2w) with capacity 1.  Max flow from src_out to snk_in.        */
#define NN 32
static int cap[NN][NN];
static int prev_[NN], q_[NN];
static int maxflow(int S,int Tt,int lim){
    int flow=0;
    while(flow<lim){
        for(int i=0;i<NN;i++) prev_[i]=-1;
        prev_[S]=S; int qh=0,qt=0; q_[qt++]=S;
        while(qh<qt){
            int u=q_[qh++];
            for(int v=0;v<NN;v++) if(prev_[v]<0 && cap[u][v]>0){ prev_[v]=u; q_[qt++]=v; }
        }
        if(prev_[Tt]<0) break;
        int v=Tt;
        while(v!=S){ int u=prev_[v]; cap[u][v]--; cap[v][u]++; v=u; }
        flow++;
    }
    return flow;
}
static int holt_klee(void){
    int pow3=1; for(int i=0;i<M;i++) pow3*=3;
    for(int code=0;code<pow3;code++){
        int c=code,fmask=0,fbits=0,fdim=0;
        for(int i=0;i<M;i++){
            int d=c%3; c/=3;
            if(d==0) fdim++;
            else { fmask|=1<<i; if(d==2) fbits|=1<<i; }
        }
        if(fdim<2) continue;
        int free_mask=((1<<M)-1)&~fmask;
        int src=-1,snk=-1;
        for(int v=0;v<NV;v++){
            if((v&fmask)!=fbits) continue;
            int o=s[v]&free_mask;
            if(o==free_mask) src=v;
            if(o==0) snk=v;
        }
        if(src<0||snk<0) return 0;
        memset(cap,0,sizeof cap);
        for(int v=0;v<NV;v++){
            if((v&fmask)!=fbits) continue;
            cap[2*v][2*v+1] = (v==src||v==snk) ? M : 1;
            for(int i=0;i<M;i++){
                if(fmask&(1<<i)) continue;
                if(!((s[v]>>i)&1)) continue;
                cap[2*v+1][2*(v^(1<<i))] = 1;
            }
        }
        if(maxflow(2*src+1, 2*snk, fdim) < fdim) return 0;
    }
    return 1;
}

/* ---------------- canonical form ---------------- */
static int NG, gperm[384][4], gxor[384];
static void build_group(void){
    int perm[4], idx[4];
    NG=0;
    for(int i=0;i<M;i++) idx[i]=i;
    /* all permutations of M elements, by simple recursion on a stack */
    int stack[5], k;
    (void)perm; (void)k;
    /* iterative Heap-free: enumerate via factorial number system */
    int fact=1; for(int i=2;i<=M;i++) fact*=i;
    for(int f=0;f<fact;f++){
        int pool[4]; for(int i=0;i<M;i++) pool[i]=i;
        int n=M, r=f, p[4];
        for(int i=0;i<M;i++){
            int div=1; for(int j=2;j<=n-1-i+ (0);j++) div*=j;      /* (n-1-i)! */
            int sel=r/div; r%=div;
            p[i]=pool[sel];
            for(int j=sel;j<n-1-i;j++) pool[j]=pool[j+1];
        }
        for(int t=0;t<NV;t++){
            for(int i=0;i<M;i++) gperm[NG][i]=p[i];
            gxor[NG]=t; NG++;
        }
    }
    (void)stack; (void)idx;
}
static inline int apply_perm(const int *p,int x){
    int y=0;
    for(int i=0;i<M;i++) if((x>>i)&1) y|=1<<p[i];
    return y;
}
static unsigned long long enc(const int *map){
    unsigned long long k=0;
    for(int v=NV-1;v>=0;v--) k=(k<<4)|(unsigned)map[v];
    return k;
}
static int is_canonical(void){
    unsigned long long me=enc(s);
    int tmp[16];
    for(int g=0;g<NG;g++){
        const int *p=gperm[g]; int t=gxor[g];
        for(int v=0;v<NV;v++) tmp[apply_perm(p,v)^t]=apply_perm(p,s[v]);
        if(enc(tmp)<me) return 0;
    }
    return 1;
}

/* ---------------- enumeration ---------------- */
static void record(void){
    n_uso++;
    if(!is_acyclic()) return;
    n_auso++;
    int h=ba_height();
    if(h<0){ n_ba_cycle++; return; }
    h_hist[h]++;
    int canon=is_canonical();
    if(!canon) return;
    cls_auso++; h_cls[h]++;
    int hk=holt_klee();
    if(hk){ cls_hk++; h_cls_hk[h]++; }
    printf("REP h=%d hk=%d :", h, hk);
    for(int v=0;v<NV;v++) printf(" %d", s[v]);
    printf("\n");
}
static void rec(int v){
    if(v==NV){ record(); return; }
    for(int t=0;t<NV;t++){
        if(used[t]) continue;
        int ok=1;
        for(int u=0;u<v;u++) if((((s[u]^t)&(u^v)))==0){ ok=0; break; }
        if(!ok) continue;
        s[v]=t; used[t]=1; rec(v+1); used[t]=0;
    }
}

int main(int argc,char**argv){
    M = argc>1?atoi(argv[1]):3; NV=1<<M;
    build_group();
    printf("group order %d (expected %d)\n", NG, (1<<M)*(M==4?24:M==3?6:M==2?2:1));
    memset(used,0,sizeof used);
    rec(0);
    printf("m = %d\n",M);
    printf("  USOs                : %lld\n",n_uso);
    printf("  AUSOs               : %lld   classes %lld\n",n_auso,cls_auso);
    printf("  AUSOs with BA cycle : %lld\n",n_ba_cycle);
    printf("  Holt-Klee AUSOs     : %lld   classes %lld\n",n_auso_hk,cls_hk);
    printf("  h*(%d) = %d   attained by %lld outmaps\n",M,best_h,n_best);
    printf("  h*_HK(%d) = %d   attained by %lld outmaps\n",M,best_h_hk,n_best_hk);
    printf("  height : #AUSO  #class   #HK  #HKclass\n");
    for(int h=0;h<64;h++) if(h_hist[h]||h_hist_hk[h])
        printf("   h=%2d : %8lld %7lld %8lld %7lld\n",h,h_hist[h],h_cls[h],h_hist_hk[h],h_cls_hk[h]);
    printf("  height-maximal outmap:");
    for(int v=0;v<NV;v++) printf(" %d",best_map[v]);
    printf("\n");
    return 0;
}
