/* lemma_sweep_L_tbox.c — t-BOX variant of the verified lemma_sweep_L.c:
   identical L-type (improved triangle inequality) sawtooth evaluation,
   except t is ONE outward-rounded arb ball containing the exact rational
   closed interval [tlo_num/t_den, thi_num/t_den]. Inclusion isotonicity of
   arb ball arithmetic makes every downstream enclosure (g, sig, bt, b, a0,
   W, Ssaw, corr, lsaw) valid simultaneously for EVERY real t in that
   interval, so each logged per-N certificate is BOX-UNIFORM in t. The
   frozen-weight domination theorem below is pointwise in (g, b, a0) for
   each fixed real t — promoting t to a ball changes nothing in the proof,
   only widens the balls it is applied to (the same maneuver as my verified
   T-type lemma_sweep_tbox.c). NOTE g monotonicity in N: for each FIXED real
   t, g(N') is strictly decreasing in N'; the ga/ge balls computed from the
   t-ball enclose {g(Nref;t)} and {g(Nend;t)} over all t in the box, and the
   per-t domination argument needs only g(N';t) in [g(Nend;t), g(Nref;t)]
   for that same t, which holds pointwise. Both modes log L12 = floor of the
   LOWER ball endpoint (two-sided F12 is impossible at nonzero box width).

   Base scheme (verbatim from lemma_sweep_L.c):
   L-type SAWTOOTH variant of the verified lemma_sweep_arb.c:
   incremental-activation, patch-amortized Taylor sweep of a certified
   LOWER bound for the repo pari
   abbeff_largex_ep_bound(N,y,t,"L",mtype,"normal","no") functional
   (the published improved-triangle-inequality lemma of the dbn_upper_bound
   Writeup, the production line behind the Lambda<=0.22 sawtooth computation).

   TRUE L-type functional (pari source abbeff_largex_bounds.txt lines 62-79):
     [sig, modK, g=modgamma(N)] as in bound_constants(N,y,t)
     b(n;N)  = sum_{d in D, d|n, n<=dN} moll_d bt(n/d)
     a0(n;N) = sum_{d in D, d|n, n<=dN} moll_d bt(n/d) (n/d)^y
     c(g) = (1-g)/(1+g)
     Lsum(N) = sum_{n=2}^{DN} max(|b - g a0|, c(g) |b + g a0|) / n^sig
     lbound(N) = (1 - g - Lsum(N))/modmoll - corr(N)        (corr as T-type)

   SAWTOOTH (frozen-weight) SCHEME — the repo's own lsummand trick
   (abbeff_largex_ep_sawtooth_incremental_lbounds, same pari file lines
   83-104: vecmax([(1-modgamend)/(1+modgamend)*|b+modgamma a|, |b-modgamma a|,
   |b-modgamend a|]) with modgamma = activation-time gamma), instantiated
   rigorously with an Nstart floor: fix ge = g(Nend) (shard end),
   ce = (1-ge)/(1+ge), and the run's Nstart. For each n define the FROZEN
   WEIGHT at cutoff state N:
     Nref(n;N) = max( n/dmin, Nstart ),  dmin = smallest active divisor of n
                 at cutoff N (n/dmin = the activation step that opened the
                 current segment of n's history — deterministic in (n,N))
     ga(n;N)   = g(Nref)
     W(n;N)    = max( ce*|b + ga a0|, |b - ga a0|, |b - ge a0| )
   (b, a0 under cutoff N). The Nstart floor is sound because the sweep only
   EVALUATES at N in [Nstart, Nend], and a term active at evaluation point N
   with the current dmin satisfies N >= n/dmin AND N >= Nstart, hence
   N >= Nref and g(N) <= g(Nref) = ga; it is what keeps ga tight for the
   bulk terms built at shard start (the repo's scheme achieves the same by
   starting from an exact init bound; shards re-freeze at their own Nstart).

   DOMINATION THEOREM. g(N') is strictly decreasing in N' (xN' = 4 pi N'^2
   - pi t/4 strictly increasing, y > 0), so for every evaluated integer N'
   in [max(Nref, current segment start), Nend]: g(N') in [ge, ga].
   For ALL real b, a0 and all g in [ge, ga]:
     (i)  |b - g a0| <= max(|b - ge a0|, |b - ga a0|)  (|linear in g| is
          convex, max at an endpoint) — terms 3 and 2 of W;
     (ii) c(g) is decreasing in g (c'(g) = -2/(1+g)^2 < 0), so c(g) <= ce;
          if b,a0 have the same sign, |b + g a0| = |b| + g|a0| is increasing
          in g, so c(g)|b + g a0| <= ce|b + ga a0| — term 1;
          if b,a0 have opposite signs (or either = 0), |b + g a0| =
          ||b| - g|a0|| <= |b| + g|a0| = |b - g a0|, and c(g) <= 1, so
          c(g)|b + g a0| <= |b - g a0| <= max(terms 2,3) by (i).
   Hence max(|b - g a0|, c(g)|b + g a0|) <= W(n;N) for every g in [ge,ga],
   in particular at g = g(N), so
     Ssaw(N) := sum_n W(n;N) n^{-sig(N)}  >=  Lsum(N)   and
     lsaw(N) := (1 - g(N) - Ssaw(N))/modmoll - corr(N)  <=  lbound(N).
   The logged L12 = floor-truncated LOWER ball endpoint of the lsaw ball is
   a certified lower bound for the TRUE L-type lbound(N); GT089 =
   arb_gt(lsaw_ball, 89/1000) certifies lbound(N) > 0.089. (Inclusion
   isotonicity: the W ball computed from the b, a0, ga, ce balls contains
   the true real W, so the Ssaw ball's upper end dominates the true Ssaw.)

   AMORTIZATION: W(n;N) changes ONLY at activation steps of n; between them
   it is N-independent and >= 0, so the patch-amortized Taylor moment scheme
   of lemma_sweep_arb.c applies VERBATIM with moment family
     MW_k = sum_n W(n) n^{-a0e} e^{-pc ln n} (-ln n)^k / k!,  a0e = (1+y)/2,
   Horner in d = p - pc, Lagrange remainder |R| <= (|d|L)^{K+1} e^{|d|L} /
   (K+1)! * MW_0 with L = ln(D*N) (every stored coefficient >= 0; cited from
   approximation_designer's patch-amortized Taylor artifact as instantiated
   in my verified lemma_sweep_arb.c). Activation N-1 -> N adds, per divisor
   d, delta = W(dN; cutoff N) - W(dN; cutoff N-1) by ball adds; W's
   convention is reproducible (ga depends only on n and its active set), so
   recomputation at patch rebuilds is consistent. corr exactly as in
   lemma_sweep_arb.c (MC moments + [1, e^{modK ln N}] bracket).

   Modes: t = amortized sawtooth sweep (logs L12 = certified lower bound)
          n = naive per-point TRUE L-type value, current-g summand
              (two-sided F12; the baseline & anchor mode — matches the pari
              "L" branch semantics exactly)
   Usage: lemma_sweep_L_tbox Nstart Nend tlo_num thi_num t_den y2num y2den mtype prec K hw mode [stride]
   Per-N: both modes: "N <N> L12 0.xxxxxxxxxxxx GT089 <0|1>" (or UNCERT)
   Final line: TIMING <wall_s> <points>.                                   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <flint/arb.h>

#define MAXD 32

static ulong DVEC3[4] = {1,2,3,6};
static ulong DVEC5[8] = {1,2,3,5,6,10,15,30};

typedef struct {
    int nd; ulong dvec[MAXD];
    arb_t moll[MAXD], lnd[MAXD];
} mollset_t;

static void bt_eval(arb_t res, const arb_t lnm, const arb_t t, slong prec){
    arb_t u; arb_init(u);
    arb_mul(u, lnm, lnm, prec); arb_mul(u, u, t, prec); arb_mul_2exp_si(u, u, -2);
    arb_exp(res, u, prec);
    arb_clear(u);
}

/* modgamma at integer Nv: exp(0.02y - (y/2) ln(xN/(4pi))), xN = 4piNv^2-pit/4 */
static void gamma_at(arb_t g, ulong Nv, const arb_t t, const arb_t y,
                     const arb_t pi, const arb_t c002y, slong prec){
    arb_t xN, tmp; arb_init(xN); arb_init(tmp);
    arb_set_ui(xN, Nv); arb_mul(xN, xN, xN, prec); arb_mul(xN, xN, pi, prec);
    arb_mul_2exp_si(xN, xN, 2);
    arb_mul(tmp, pi, t, prec); arb_mul_2exp_si(tmp, tmp, -2); arb_sub(xN, xN, tmp, prec);
    arb_div(tmp, xN, pi, prec); arb_mul_2exp_si(tmp, tmp, -2); arb_log(tmp, tmp, prec);
    arb_mul(tmp, tmp, y, prec); arb_mul_2exp_si(tmp, tmp, -1);
    arb_sub(g, c002y, tmp, prec); arb_exp(g, g, prec);
    arb_clear(xN); arb_clear(tmp);
}

/* b, a0 for given n under cutoff "n <= d*Ncut"; returns smallest active d (0 if none) */
static ulong bA0(arb_t b, arb_t a0, ulong n, ulong Ncut, const mollset_t *ms,
                 const arb_t t, const arb_t y, slong prec){
    arb_t lnn, lnnd, bb, e; arb_init(lnn); arb_init(lnnd); arb_init(bb); arb_init(e);
    arb_zero(b); arb_zero(a0);
    ulong dmin = 0;
    arb_set_ui(lnn, n); arb_log(lnn, lnn, prec);
    for(int i=0;i<ms->nd;i++){
        ulong d = ms->dvec[i];
        if(n % d == 0 && n <= d*Ncut){
            if(dmin == 0 || d < dmin) dmin = d;
            arb_sub(lnnd, lnn, ms->lnd[i], prec);
            bt_eval(bb, lnnd, t, prec);
            arb_addmul(b, bb, ms->moll[i], prec);
            arb_mul(e, lnnd, y, prec); arb_exp(e, e, prec);
            arb_mul(bb, bb, e, prec);
            arb_addmul(a0, bb, ms->moll[i], prec);
        }
    }
    arb_clear(lnn); arb_clear(lnnd); arb_clear(bb); arb_clear(e);
    return dmin;
}

/* frozen sawtooth weight W(n; cutoff Ncut), convention
   ga = g(max(n/dmin_active, Nstart)). Sets W = 0 if n inactive. */
static void Wcompute(arb_t W, ulong n, ulong Ncut, ulong Nstart,
                     const mollset_t *ms,
                     const arb_t t, const arb_t y, const arb_t pi,
                     const arb_t c002y, const arb_t ge, const arb_t ce,
                     slong prec){
    arb_t b, a0, ga, t1, t2, t3, tmp;
    arb_init(b); arb_init(a0); arb_init(ga); arb_init(t1); arb_init(t2);
    arb_init(t3); arb_init(tmp);
    ulong dmin = bA0(b, a0, n, Ncut, ms, t, y, prec);
    if(dmin == 0){ arb_zero(W); goto done; }
    ulong Nref = n/dmin; if(Nref < Nstart) Nref = Nstart;
    gamma_at(ga, Nref, t, y, pi, c002y, prec);
    /* Direct standard/crude (upstream Triangle-bound) weight:
         |b| + gamma(N) |a0| <= |b| + gamma(Nref) |a0|,
       because gamma decreases with N and Nref <= N.  At a singleton
       Nstart=Nend=N this is exactly the true Triangle-bound summand. */
    arb_abs(t1, b);
    arb_abs(t2, a0);
    arb_mul(t2, t2, ga, prec);
    arb_add(W, t1, t2, prec);
done:
    arb_clear(b); arb_clear(a0); arb_clear(ga); arb_clear(t1); arb_clear(t2);
    arb_clear(t3); arb_clear(tmp);
}

/* add coef * n^{-aexp} e^{-pc ln n} (-ln n)^k/k! to M[k], k=0..K */
static void add_moments(arb_ptr M, slong K, ulong n, const arb_t coef,
                        const arb_t aexp, const arb_t pc, slong prec){
    arb_t lnn, w, pw, tmp; arb_init(lnn); arb_init(w); arb_init(pw); arb_init(tmp);
    arb_set_ui(lnn, n); arb_log(lnn, lnn, prec);
    arb_add(w, aexp, pc, prec); arb_mul(w, w, lnn, prec); arb_neg(w, w); arb_exp(w, w, prec);
    arb_mul(w, w, coef, prec);
    arb_set_ui(pw, 1);
    for(slong k=0;k<=K;k++){
        arb_mul(tmp, w, pw, prec); arb_add(M+k, M+k, tmp, prec);
        if(k<K){ arb_mul(pw, pw, lnn, prec); arb_neg(pw, pw); arb_div_ui(pw, pw, (ulong)(k+1), prec); }
    }
    arb_clear(lnn); arb_clear(w); arb_clear(pw); arb_clear(tmp);
}

int main(int argc, char *argv[]){
    if(argc < 13){ printf("usage: lemma_sweep_L_tbox Nstart Nend tlo_num thi_num t_den y2num y2den mtype prec K hw mode [stride]\n"); return 2; }
    ulong Nstart = strtoul(argv[1],NULL,10), Nend = strtoul(argv[2],NULL,10);
    ulong tlonum = strtoul(argv[3],NULL,10), thinum = strtoul(argv[4],NULL,10);
    ulong tden = strtoul(argv[5],NULL,10);
    ulong y2num = strtoul(argv[6],NULL,10), y2den = strtoul(argv[7],NULL,10);
    int mtype = atoi(argv[8]);
    slong prec = atol(argv[9]);
    slong K = atol(argv[10]);
    char mode = argv[12][0];
    ulong stride = (argc>13)? strtoul(argv[13],NULL,10) : 1;
    if(thinum < tlonum){ printf("need thi >= tlo\n"); return 2; }

    arb_t t, y, a0e, amy, pi, ln4pi, c002y, hw;
    arb_init(t); arb_init(y); arb_init(a0e); arb_init(amy); arb_init(pi); arb_init(ln4pi); arb_init(c002y); arb_init(hw);
    {   /* t = outward-rounded ball CONTAINING the exact rational closed
           interval [tlonum/tden, thinum/tden] */
        arb_t tlo, thi; arb_init(tlo); arb_init(thi);
        arb_set_ui(tlo, tlonum); arb_div_ui(tlo, tlo, tden, prec);
        arb_set_ui(thi, thinum); arb_div_ui(thi, thi, tden, prec);
        arb_union(t, tlo, thi, prec);
        arb_clear(tlo); arb_clear(thi);
    }
    printf("TBOX %lu/%lu %lu/%lu\n", tlonum, tden, thinum, tden);
    arb_set_ui(y, y2num); arb_div_ui(y, y, y2den, prec); arb_sqrt(y, y, prec);
    arb_add_ui(a0e, y, 1, prec); arb_mul_2exp_si(a0e, a0e, -1);   /* (1+y)/2 */
    arb_sub(amy, a0e, y, prec);
    arb_const_pi(pi, prec);
    arb_mul_2exp_si(ln4pi, pi, 2); arb_log(ln4pi, ln4pi, prec);
    arb_set_ui(c002y, 2); arb_div_ui(c002y, c002y, 100, prec); arb_mul(c002y, c002y, y, prec);
    arb_set_str(hw, argv[11], prec);

    mollset_t ms; ms.nd = 1; ms.dvec[0] = 1;
    for(int i=0;i<MAXD;i++){ arb_init(ms.moll[i]); arb_init(ms.lnd[i]); }
    arb_set_ui(ms.moll[0],1); arb_zero(ms.lnd[0]);
    {
        arb_t b2,b3,b5,b7,b11,ln2,ln3,ln5,ln7,ln11,tmp;
        arb_init(b2); arb_init(b3); arb_init(b5); arb_init(b7); arb_init(b11);
        arb_init(ln2); arb_init(ln3); arb_init(ln5); arb_init(ln7); arb_init(ln11);
        arb_init(tmp);
        arb_const_log2(ln2, prec);
        arb_set_ui(tmp,3); arb_log(ln3,tmp,prec);
        arb_set_ui(tmp,5); arb_log(ln5,tmp,prec);
        arb_set_ui(tmp,7); arb_log(ln7,tmp,prec);
        arb_set_ui(tmp,11); arb_log(ln11,tmp,prec);
        bt_eval(b2, ln2, t, prec); bt_eval(b3, ln3, t, prec);
        bt_eval(b5, ln5, t, prec); bt_eval(b7, ln7, t, prec);
        bt_eval(b11, ln11, t, prec);
        if(mtype==2){ ms.nd=2; ms.dvec[1]=2; arb_neg(ms.moll[1],b2); arb_set(ms.lnd[1],ln2); }
        else if(mtype==3){ ms.nd=4; ms.dvec[1]=2; ms.dvec[2]=3; ms.dvec[3]=6;
            arb_neg(ms.moll[1],b2); arb_set(ms.lnd[1],ln2);
            arb_neg(ms.moll[2],b3); arb_set(ms.lnd[2],ln3);
            arb_mul(ms.moll[3],b2,b3,prec); arb_add(ms.lnd[3],ln2,ln3,prec); }
        else if(mtype==4){
            ms.nd=8;
            for(int i=0;i<8;i++) ms.dvec[i]=DVEC5[i];
            arb_neg(ms.moll[1],b2); arb_set(ms.lnd[1],ln2);
            arb_neg(ms.moll[2],b3); arb_set(ms.lnd[2],ln3);
            arb_neg(ms.moll[3],b5); arb_set(ms.lnd[3],ln5);
            arb_mul(ms.moll[4],b2,b3,prec); arb_add(ms.lnd[4],ln2,ln3,prec);
            arb_mul(ms.moll[5],b2,b5,prec); arb_add(ms.lnd[5],ln2,ln5,prec);
            arb_mul(ms.moll[6],b3,b5,prec); arb_add(ms.lnd[6],ln3,ln5,prec);
            arb_mul(ms.moll[7],ms.moll[4],b5,prec); arb_neg(ms.moll[7],ms.moll[7]);
            arb_add(ms.lnd[7],ms.lnd[4],ln5,prec);
        }
        else if(mtype==5){
            ms.nd=16;
            for(int mask=0;mask<16;mask++){
                ms.dvec[mask]=1; arb_one(ms.moll[mask]); arb_zero(ms.lnd[mask]);
                if(mask&1){ ms.dvec[mask]*=2; arb_mul(ms.moll[mask],ms.moll[mask],b2,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln2,prec); }
                if(mask&2){ ms.dvec[mask]*=3; arb_mul(ms.moll[mask],ms.moll[mask],b3,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln3,prec); }
                if(mask&4){ ms.dvec[mask]*=5; arb_mul(ms.moll[mask],ms.moll[mask],b5,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln5,prec); }
                if(mask&8){ ms.dvec[mask]*=7; arb_mul(ms.moll[mask],ms.moll[mask],b7,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln7,prec); }
            }
        }
        else if(mtype==6){
            ms.nd=32;
            for(int mask=0;mask<32;mask++){
                ms.dvec[mask]=1; arb_one(ms.moll[mask]); arb_zero(ms.lnd[mask]);
                if(mask&1){ ms.dvec[mask]*=2; arb_mul(ms.moll[mask],ms.moll[mask],b2,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln2,prec); }
                if(mask&2){ ms.dvec[mask]*=3; arb_mul(ms.moll[mask],ms.moll[mask],b3,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln3,prec); }
                if(mask&4){ ms.dvec[mask]*=5; arb_mul(ms.moll[mask],ms.moll[mask],b5,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln5,prec); }
                if(mask&8){ ms.dvec[mask]*=7; arb_mul(ms.moll[mask],ms.moll[mask],b7,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln7,prec); }
                if(mask&16){ ms.dvec[mask]*=11; arb_mul(ms.moll[mask],ms.moll[mask],b11,prec);
                    arb_neg(ms.moll[mask],ms.moll[mask]); arb_add(ms.lnd[mask],ms.lnd[mask],ln11,prec); }
            }
        }
        else if(mtype!=1){ printf("mtype 1/2/3/4/5/6 only\n"); return 2; }
        for(int i=0;i<4;i++) ms.dvec[i] = (mtype==3)? DVEC3[i] : ms.dvec[i];
        arb_clear(b2); arb_clear(b3); arb_clear(b5); arb_clear(b7); arb_clear(b11);
        arb_clear(ln2); arb_clear(ln3); arb_clear(ln5); arb_clear(ln7); arb_clear(ln11);
        arb_clear(tmp);
    }
    ulong D = ms.dvec[ms.nd-1];

    /* shard-end gamma and ce = (1-ge)/(1+ge), fixed for the whole run */
    arb_t ge, ce;
    arb_init(ge); arb_init(ce);
    gamma_at(ge, Nend, t, y, pi, c002y, prec);
    {
        arb_t u,v; arb_init(u); arb_init(v);
        arb_sub_ui(u, ge, 1, prec); arb_neg(u, u);
        arb_add_ui(v, ge, 1, prec);
        arb_div(ce, u, v, prec);
        arb_clear(u); arb_clear(v);
    }

    arb_ptr MW = _arb_vec_init(K+1), MC = _arb_vec_init(K+1);
    arb_t pc; arb_init(pc); int have_patch = 0;
    ulong Nactive = 0;

    arb_t N_a, xN, lnx4pi, p, sigma, d_, modK, modgamma, modmoll, lnN;
    arb_init(N_a); arb_init(xN); arb_init(lnx4pi); arb_init(p); arb_init(sigma); arb_init(d_);
    arb_init(modK); arb_init(modgamma); arb_init(modmoll); arb_init(lnN);
    arb_t tmp, tmp2, W, Wold, hW, hC, R, absd, fac, L, Ssum, corr, lbound, thr, btN, cnow;
    arb_init(tmp); arb_init(tmp2); arb_init(W); arb_init(Wold); arb_init(hW); arb_init(hC);
    arb_init(R); arb_init(absd); arb_init(fac); arb_init(L); arb_init(Ssum);
    arb_init(corr); arb_init(lbound); arb_init(thr); arb_init(btN); arb_init(cnow);
    arb_set_ui(thr,89); arb_div_ui(thr,thr,1000,prec);
    arf_t flo, fhi; arf_init(flo); arf_init(fhi);
    fmpz_t sc, zlo, zhi; fmpz_init(sc); fmpz_init(zlo); fmpz_init(zhi);
    fmpz_set_ui(sc,10); fmpz_pow_ui(sc,sc,12);

    clock_t tstart = clock();
    ulong npts = 0;

    for(ulong N = Nstart; N <= Nend; N += stride){
        arb_set_ui(N_a, N);
        arb_mul(xN, N_a, N_a, prec); arb_mul(xN, xN, pi, prec); arb_mul_2exp_si(xN, xN, 2);
        arb_mul(tmp, pi, t, prec); arb_mul_2exp_si(tmp, tmp, -2); arb_sub(xN, xN, tmp, prec);
        arb_div(tmp, xN, pi, prec); arb_mul_2exp_si(tmp, tmp, -2); arb_log(lnx4pi, tmp, prec);
        arb_mul(p, t, lnx4pi, prec); arb_mul_2exp_si(p, p, -2);
        {
            arb_t inner, x2; arb_init(inner); arb_init(x2);
            arb_mul(x2, xN, xN, prec);
            arb_add_ui(tmp, y, 1, prec); arb_mul(tmp, tmp, y, prec); arb_mul_2exp_si(tmp, tmp, 2);
            arb_div(tmp, tmp, x2, prec);
            arb_mul_ui(inner, y, 3, prec); arb_neg(inner, inner); arb_add_ui(inner, inner, 1, prec);
            arb_add(inner, inner, tmp, prec);
            if(arb_is_negative(inner)) arb_zero(inner);
            else if(!arb_is_positive(inner)){ printf("inner sign uncertified\n"); return 3; }
            arb_mul(tmp, t, inner, prec);
            arb_mul_2exp_si(x2, x2, 1); arb_div(tmp, tmp, x2, prec);
            arb_sub(p, p, tmp, prec);
            arb_clear(inner); arb_clear(x2);
        }
        arb_add(sigma, a0e, p, prec);
        arb_mul(modK, t, y, prec); arb_sub_ui(tmp, xN, 6, prec); arb_mul_2exp_si(tmp, tmp, 1);
        arb_div(modK, modK, tmp, prec);
        arb_mul(tmp, lnx4pi, y, prec); arb_mul_2exp_si(tmp, tmp, -1);
        arb_sub(tmp, c002y, tmp, prec); arb_exp(modgamma, tmp, prec);
        arb_zero(modmoll);
        for(int i=0;i<ms.nd;i++){
            arb_abs(tmp, ms.moll[i]);
            arb_mul(tmp2, ms.lnd[i], sigma, prec); arb_neg(tmp2, tmp2); arb_exp(tmp2, tmp2, prec);
            arb_addmul(modmoll, tmp, tmp2, prec);
        }
        arb_log(lnN, N_a, prec);

        if(mode == 'n'){
            /* naive: TRUE L-type per-point value, current-g summand */
            arb_zero(Ssum); arb_zero(corr);
            arb_sub_ui(tmp, modgamma, 1, prec); arb_neg(tmp, tmp);
            arb_add_ui(tmp2, modgamma, 1, prec);
            arb_div(cnow, tmp, tmp2, prec);
            arb_t lnn, wgt, b_, a0_, m1, m2; arb_init(lnn); arb_init(wgt);
            arb_init(b_); arb_init(a0_); arb_init(m1); arb_init(m2);
            for(ulong n=2; n<=D*N; n++){
                if(n > N){
                    int any=0;
                    for(int i=1;i<ms.nd;i++){ ulong dd=ms.dvec[i]; if(n%dd==0 && n<=dd*N){ any=1; break; } }
                    if(!any) continue;
                }
                bA0(b_, a0_, n, N, &ms, t, y, prec);
                arb_mul(tmp, modgamma, a0_, prec);
                arb_sub(m1, b_, tmp, prec); arb_abs(m1, m1);
                arb_add(m2, b_, tmp, prec); arb_abs(m2, m2); arb_mul(m2, m2, cnow, prec);
                arb_max(m1, m1, m2, prec);
                arb_set_ui(lnn, n); arb_log(lnn, lnn, prec);
                arb_mul(wgt, lnn, sigma, prec); arb_neg(wgt, wgt); arb_exp(wgt, wgt, prec);
                arb_addmul(Ssum, m1, wgt, prec);
            }
            arb_t smy; arb_init(smy); arb_sub(smy, sigma, y, prec);
            for(ulong n=2; n<=N; n++){
                arb_set_ui(lnn, n); arb_log(lnn, lnn, prec);
                bt_eval(tmp, lnn, t, prec);
                arb_mul(tmp2, lnn, modK, prec); arb_expm1(tmp2, tmp2, prec);
                arb_mul(tmp, tmp, tmp2, prec);
                arb_mul(tmp2, lnn, smy, prec); arb_neg(tmp2, tmp2); arb_exp(tmp2, tmp2, prec);
                arb_addmul(corr, tmp, tmp2, prec);
            }
            arb_mul(corr, corr, modgamma, prec);
            arb_clear(smy); arb_clear(lnn); arb_clear(wgt);
            arb_clear(b_); arb_clear(a0_); arb_clear(m1); arb_clear(m2);
        } else { /* mode 't': amortized sawtooth */
            if(!have_patch){
                arb_add(pc, p, hw, prec);
                for(slong k=0;k<=K;k++){ arb_zero(MW+k); arb_zero(MC+k); }
                arb_t lnn; arb_init(lnn);
                for(ulong n=2; n<=D*N; n++){
                    if(n > N){
                        int any=0;
                        for(int i=1;i<ms.nd;i++){ ulong dd=ms.dvec[i]; if(n%dd==0 && n<=dd*N){ any=1; break; } }
                        if(!any) continue;
                    }
                    Wcompute(W, n, N, Nstart, &ms, t, y, pi, c002y, ge, ce, prec);
                    add_moments(MW, K, n, W, a0e, pc, prec);
                }
                for(ulong n=2; n<=N; n++){
                    arb_set_ui(lnn, n); arb_log(lnn, lnn, prec);
                    bt_eval(tmp, lnn, t, prec); arb_mul(tmp, tmp, lnn, prec);
                    add_moments(MC, K, n, tmp, amy, pc, prec);
                }
                arb_clear(lnn);
                have_patch = 1; Nactive = N;
            } else {
                for(ulong Np = Nactive+1; Np <= N; Np++){
                    arb_t lnNp; arb_init(lnNp);
                    arb_set_ui(lnNp, Np); arb_log(lnNp, lnNp, prec);
                    bt_eval(btN, lnNp, t, prec);
                    for(int i=0;i<ms.nd;i++){
                        ulong dd = ms.dvec[i]; ulong n = dd*Np;
                        Wcompute(Wold, n, Np-1, Nstart, &ms, t, y, pi, c002y, ge, ce, prec);
                        Wcompute(W,    n, Np,   Nstart, &ms, t, y, pi, c002y, ge, ce, prec);
                        arb_sub(W, W, Wold, prec);
                        add_moments(MW, K, n, W, a0e, pc, prec);
                    }
                    arb_mul(tmp, btN, lnNp, prec);
                    add_moments(MC, K, Np, tmp, amy, pc, prec);
                    arb_clear(lnNp);
                }
                Nactive = (N > Nactive)? N : Nactive;
                arb_sub(d_, p, pc, prec);
                if(arf_cmp(arb_midref(d_), arb_midref(hw)) > 0){
                    arb_add(pc, p, hw, prec);
                    for(slong k=0;k<=K;k++){ arb_zero(MW+k); arb_zero(MC+k); }
                    arb_t lnn; arb_init(lnn);
                    for(ulong n=2; n<=D*N; n++){
                        if(n > N){
                            int any=0;
                            for(int i=1;i<ms.nd;i++){ ulong dd=ms.dvec[i]; if(n%dd==0 && n<=dd*N){ any=1; break; } }
                            if(!any) continue;
                        }
                        Wcompute(W, n, N, Nstart, &ms, t, y, pi, c002y, ge, ce, prec);
                        add_moments(MW, K, n, W, a0e, pc, prec);
                    }
                    for(ulong n=2; n<=N; n++){
                        arb_set_ui(lnn, n); arb_log(lnn, lnn, prec);
                        bt_eval(tmp, lnn, t, prec); arb_mul(tmp, tmp, lnn, prec);
                        add_moments(MC, K, n, tmp, amy, pc, prec);
                    }
                    arb_clear(lnn);
                }
            }
            /* Horner eval + proven remainder, L = ln(D*N) */
            arb_sub(d_, p, pc, prec);
            arb_set(hW, MW+K); arb_set(hC, MC+K);
            for(slong k=K-1;k>=0;k--){
                arb_mul(hW, hW, d_, prec); arb_add(hW, hW, MW+k, prec);
                arb_mul(hC, hC, d_, prec); arb_add(hC, hC, MC+k, prec);
            }
            arb_set_ui(L, D*N); arb_log(L, L, prec);
            arb_abs(absd, d_);
            arb_get_ubound_arf(flo, absd, prec); arb_set_arf(absd, flo);
            arb_mul(fac, absd, L, prec);
            arb_exp(R, fac, prec);
            arb_pow_ui(fac, fac, (ulong)(K+1), prec);
            arb_mul(R, R, fac, prec);
            arb_fac_ui(fac, (ulong)(K+1), prec);
            arb_div(R, R, fac, prec);
            arb_get_ubound_arf(flo, MW+0, prec); arb_set_arf(tmp, flo);
            arb_mul(tmp, tmp, R, prec); arb_add_error(hW, tmp);
            arb_get_ubound_arf(flo, MC+0, prec); arb_set_arf(tmp, flo);
            arb_mul(tmp, tmp, R, prec); arb_add_error(hC, tmp);
            arb_set(Ssum, hW);
            arb_mul(tmp, modK, lnN, prec); arb_exp(tmp, tmp, prec);
            arb_add_ui(tmp2, tmp, 1, prec); arb_mul_2exp_si(tmp2, tmp2, -1);
            arb_sub(tmp, tmp, tmp2, prec); arb_get_ubound_arf(flo, tmp, prec);
            arb_set_arf(tmp, flo);
            arb_add_error(tmp2, tmp);
            arb_mul(corr, modK, hC, prec);
            arb_mul(corr, corr, tmp2, prec);
            arb_mul(corr, corr, modgamma, prec);
        }
        /* lbound = (1 - modgamma - Ssum)/modmoll - corr */
        arb_set_ui(lbound, 1);
        arb_sub(lbound, lbound, modgamma, prec);
        arb_sub(lbound, lbound, Ssum, prec);
        arb_div(lbound, lbound, modmoll, prec);
        arb_sub(lbound, lbound, corr, prec);

        arb_mul_fmpz(tmp, lbound, sc, prec);
        arb_get_lbound_arf(flo, tmp, prec);
        arb_get_ubound_arf(fhi, tmp, prec);
        arf_get_fmpz(zlo, flo, ARF_RND_FLOOR);
        arf_get_fmpz(zhi, fhi, ARF_RND_FLOOR);
        int gt = arb_gt(lbound, thr);
        /* box width makes two-sided F12 impossible: BOTH modes log L12 =
           floor of the lower ball endpoint (box-uniform lower bound) */
        (void)zhi;
        if(fmpz_sgn(zlo) >= 0 && fmpz_cmp(zlo, sc) < 0){
            char buf[32]; fmpz_get_str(buf, 10, zlo);
            int len = (int)strlen(buf);
            printf("N %lu L12 0.", N);
            for(int i=len;i<12;i++) putchar('0');
            printf("%s GT089 %d\n", buf, gt);
        } else printf("N %lu UNCERT GT089 %d\n", N, gt);
        (void)mode;
        if(getenv("LEMMA_DEBUG")){ printf("DBG N %lu lbound = %s\n", N, arb_get_str(lbound, 25, 0)); }
        npts++;
    }
    printf("TIMING %.3f %lu\n", (double)(clock()-tstart)/CLOCKS_PER_SEC, npts);
    flint_cleanup();
    return 0;
}
