/* ===========================================================================
 * prop43_proof.c
 *
 * The computation constituting the computer-assisted proof of
 * Proposition 4.3 of the review manuscript
 * (dan/latex/gomila-proof-exposition.tex).
 *
 * PROVENANCE AND MODIFICATIONS
 * ----------------------------
 * Derived from src/lemma_sweep_p235711.c in the candidate repository
 * (dbn-lambda-01787854-candidate-audit), which selected between two
 * kernels with a compile switch (-DTRIANGLE_WEIGHT).  This file is that
 * source restricted to its TRIANGLE_WEIGHT configuration, with the code
 * that is dead in this configuration removed:
 *   - the preprocessor branches and the alternative "sharp" kernel
 *     (sweep and naive modes); the triangle kernel is unconditional and
 *     the tag line "WEIGHT TRIANGLE" is always printed;
 *   - the shard-end quantities ge = g(Nend) and ce = (1-ge)/(1+ge),
 *     which fed only the removed kernel, and the corresponding two
 *     parameters of Wcompute;
 *   - four unused variables and two now-pointless (void) casts;
 *   - the program name in the usage string.
 * Additions (this review), pure instrumentation with no effect on
 * computed values:
 *   - if the environment variable PROP43_PROGRESS names a file, a
 *     short progress report (last N, rows done, rate, ETA, running
 *     minimum L12, UNCERT count) is rewritten there at most once per
 *     minute, and stdout is flushed after each per-N line;
 *   - if PROP43_SUMMARY names a file, a human-readable end-of-run
 *     summary is written there on normal completion: the range of N,
 *     the min and max certified L12 (with the N attaining them), a
 *     SUCCESS/FAILURE verdict (success = every N certified, no UNCERT
 *     rows, min L12 > 0), the wall time, and the name of the full
 *     results file as given by PROP43_RESULT.
 * Apart from the listed changes, every statement is line-for-line
 * identical to the original; diff against
 * jude/src/lemma_sweep_p235711.c to audit.
 *
 * PURPOSE
 * -------
 * For each integer N in [Nstart, Nend], compute a certified interval
 * lower bound for the quantity L_N of the manuscript (the mollified
 * lower bound for |f_t| of Lemma 4.2) and print it as a truncated
 * 12-digit decimal.  Proposition 4.3 asserts that these lower bounds,
 * over the four (prime set, N-range) configurations listed there, are
 * all at least T_min = 791366e-12 > 0; running this program over those
 * configurations and inspecting the minimum printed value proves it.
 *
 * CORRESPONDENCE WITH THE MANUSCRIPT
 * ----------------------------------
 * (Lemma 4.1, Lemma 4.2, Proposition 4.3; bt(m) = exp((t/4) log^2 m).)
 *
 *   code       manuscript
 *   ----       ----------
 *   t          one outward-rounded ball containing the exact rational
 *              interval [tlo_num/t_den, thi_num/t_den]  (contains t_0)
 *   y          y_0 = sqrt(y2num/y2den)
 *   xN         x_N = 4 pi N^2 - pi t / 4   (left edge of window W_N)
 *   modgamma   g_N     = exp(0.02 y) (x_N / 4 pi)^(-y/2)
 *   sigma      sigma_N = (1+y)/2 + (t/4) log(x_N/4pi)
 *                        - (t/(2 x_N^2)) (1 - 3y + 4y(1+y)/x_N^2)_+
 *              [the positive part is certified by a sign check; an
 *               uncertain sign aborts the run]
 *   modK       k_N = t y / (2 (x_N - 6))
 *   b(n;N)     B_{N,n} = sum over d dividing D and n, n <= dN, of
 *              lambda_d bt(n/d)
 *   a0(n;N)    A_{N,n} = same sum with the extra factor (n/d)^y
 *   modmoll    M_N = sum over d dividing D of |lambda_d| d^(-sigma_N)
 *   corr       an enclosure of g_N C_N, where
 *              C_N = sum_{m=2}^{N} bt(m)(m^(k_N) - 1) m^(y - sigma_N)
 *   lbound     L_N = (1 - g_N - Ssum)/M_N - corr
 *
 * The mollifier is the Euler product over the auxiliary prime set
 * selected by mtype:
 *
 *   mtype  1    2     3       4         5           6
 *   P      {}   {2}   {2,3}   {2,3,5}   {2,3,5,7}   {2,3,5,7,11}
 *
 * with lambda_d = (-1)^omega(d) prod_{p | d} bt(p) for d dividing
 * D = prod P.  Proposition 4.3 uses mtype 6, 5, 4, 3 on its four
 * N-ranges respectively.
 *
 * THE t-BOX
 * ---------
 * t is a single outward-rounded arb ball containing the exact rational
 * closed interval [tlo_num/t_den, thi_num/t_den].  By inclusion
 * isotonicity of ball arithmetic, every downstream enclosure (g, sigma,
 * bt, b, a0, W, Ssum, corr, lbound) is then valid simultaneously for
 * EVERY real t in that interval, so each logged per-N certificate is
 * uniform in t over the box; in particular it is valid at the exact
 * t_0 = 129/800.  Because the ball has nonzero width, only a one-sided
 * bound is meaningful; the program logs
 *   L12 = floor(10^12 x lower ball endpoint) / 10^12,
 * a certified lower bound for the true L_N.  The legacy flag GT089
 * records arb_gt(lbound, 89/1000); it is not consumed by
 * Proposition 4.3 (only positivity and the global minimum matter).
 *
 * THE SWEEP: FROZEN WEIGHTS
 * -------------------------
 * The sweep evaluates all N in [Nstart, Nend] in one pass.  To make the
 * summand reusable across N it replaces the N-dependent factor g(N) in
 * each term by a FROZEN value fixed at the term's activation step:
 *
 *   dmin      = smallest divisor d of n (in the mollifier support) with
 *               n <= d N     (so n/dmin is the cutoff at which the term
 *               n entered its current activation state)
 *   Nref(n;N) = max(n/dmin, Nstart)
 *   W(n;N)    = |b| + g(Nref) |a0|
 *
 * DOMINATION (why freezing is conservative).  The sweep only evaluates
 * at N >= max(n/dmin, Nstart) = Nref, and g is strictly decreasing in N
 * (x_N increases, y > 0), so
 *   |b| + g(N)|a0|  <=  |b| + g(Nref)|a0|  =  W(n;N).
 * Hence Ssum(N) = sum_n W(n;N) n^(-sigma_N) majorizes the true sum, and
 * the lbound computed from it is a valid lower bound for L_N.
 *
 * AMORTIZED EVALUATION (mode 't')
 * -------------------------------
 * W(n;N) changes only at activation steps of n; between them it is
 * independent of N and nonnegative.  The sweep therefore maintains
 * Taylor moments
 *   MW_k = sum_n W(n) n^(-a0e) exp(-pc log n) (-log n)^k / k!,
 * with a0e = (1+y)/2 and pc a patch center, evaluating
 * Ssum = sum_k MW_k d^k by Horner in d = p - pc (p is the exponent
 * offset sigma_N - a0e), with the Lagrange remainder bound
 *   |R| <= (|d| L)^(K+1) exp(|d| L) / (K+1)!  x  MW_0,   L = log(D N),
 * added to the ball (valid because every moment coefficient is
 * nonnegative).  When |d| exceeds the half-width hw, the patch is
 * rebuilt at a new center.  Activation N-1 -> N adds, per divisor d,
 * the delta W(dN; N) - W(dN; N-1) to the moments; the freezing
 * convention makes this recomputation deterministic in (n, N).  The
 * correction term corr is handled the same way with moments MC and the
 * enclosure of m^(k_N) - 1 in  k_N log m x [1, exp(k_N log N)].
 *
 * MODES, USAGE, OUTPUT
 * --------------------
 *   mode t : amortized sweep as above (the certificate-production mode)
 *   mode n : naive per-point evaluation of the same lbound with the
 *            current g(N) in each summand (no freezing, no
 *            amortization); used as an anchor to spot-check mode t
 *
 *   usage: prop43_proof Nstart Nend tlo_num thi_num t_den
 *          y2num y2den mtype prec K hw mode [stride]
 *
 *   per-N output:  "N <N> L12 0.dddddddddddd GT089 <0|1>"  (or UNCERT)
 *   final line:    "TIMING <wall_s> <points>"
 * =========================================================================== */
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
                     const arb_t c002y, slong prec){
    arb_t b, a0, ga, t1, t2;
    arb_init(b); arb_init(a0); arb_init(ga); arb_init(t1); arb_init(t2);
    ulong dmin = bA0(b, a0, n, Ncut, ms, t, y, prec);
    if(dmin == 0){ arb_zero(W); goto done; }
    ulong Nref = n/dmin; if(Nref < Nstart) Nref = Nstart;
    gamma_at(ga, Nref, t, y, pi, c002y, prec);
    /* Triangle weight:
         |b| + gamma(N) |a0| <= |b| + gamma(Nref) |a0|,
       since gamma decreases with N and Nref <= N.  For a singleton
       Nstart=Nend=N this is the exact Triangle summand. */
    arb_abs(t1, b);
    arb_abs(t2, a0);
    arb_mul(t2, t2, ga, prec);
    arb_add(W, t1, t2, prec);
done:
    arb_clear(b); arb_clear(a0); arb_clear(ga); arb_clear(t1); arb_clear(t2);
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

/* write an fmpz value v (0 <= v < 10^12) as the 12-digit decimal 0.dddddddddddd */
static void write_l12(FILE *f, const fmpz_t v){
    char buf[32]; fmpz_get_str(buf, 10, v);
    int len = (int)strlen(buf);
    fprintf(f, "0.");
    for(int i=len;i<12;i++) fputc('0', f);
    fprintf(f, "%s", buf);
}

int main(int argc, char *argv[]){
    if(argc < 13){ printf("usage: prop43_proof Nstart Nend tlo_num thi_num t_den y2num y2den mtype prec K hw mode [stride]\n"); return 2; }
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
    if(mtype < 1 || mtype > 6){
        printf("mtype 1/2/3/4/5/6 only\n");
        return 2;
    }

    arb_t t, y, a0e, amy, pi, c002y, hw;
    arb_init(t); arb_init(y); arb_init(a0e); arb_init(amy); arb_init(pi); arb_init(c002y); arb_init(hw);
    {   /* t = outward-rounded ball CONTAINING the exact rational closed
           interval [tlonum/tden, thinum/tden] */
        arb_t tlo, thi; arb_init(tlo); arb_init(thi);
        arb_set_ui(tlo, tlonum); arb_div_ui(tlo, tlo, tden, prec);
        arb_set_ui(thi, thinum); arb_div_ui(thi, thi, tden, prec);
        arb_union(t, tlo, thi, prec);
        arb_clear(tlo); arb_clear(thi);
    }
    printf("TBOX %lu/%lu %lu/%lu\n", tlonum, tden, thinum, tden);
    printf("WEIGHT TRIANGLE\n");
    arb_set_ui(y, y2num); arb_div_ui(y, y, y2den, prec); arb_sqrt(y, y, prec);
    arb_add_ui(a0e, y, 1, prec); arb_mul_2exp_si(a0e, a0e, -1);   /* (1+y)/2 */
    arb_sub(amy, a0e, y, prec);
    arb_const_pi(pi, prec);
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
        for(int i=0;i<4;i++) ms.dvec[i] = (mtype==3)? DVEC3[i] : ms.dvec[i];
        arb_clear(b2); arb_clear(b3); arb_clear(b5); arb_clear(b7); arb_clear(b11);
        arb_clear(ln2); arb_clear(ln3); arb_clear(ln5); arb_clear(ln7); arb_clear(ln11);
        arb_clear(tmp);
    }
    ulong D = ms.dvec[ms.nd-1];

    arb_ptr MW = _arb_vec_init(K+1), MC = _arb_vec_init(K+1);
    arb_t pc; arb_init(pc); int have_patch = 0;
    ulong Nactive = 0;

    arb_t N_a, xN, lnx4pi, p, sigma, d_, modK, modgamma, modmoll, lnN;
    arb_init(N_a); arb_init(xN); arb_init(lnx4pi); arb_init(p); arb_init(sigma); arb_init(d_);
    arb_init(modK); arb_init(modgamma); arb_init(modmoll); arb_init(lnN);
    arb_t tmp, tmp2, W, Wold, hW, hC, R, absd, fac, L, Ssum, corr, lbound, thr, btN;
    arb_init(tmp); arb_init(tmp2); arb_init(W); arb_init(Wold); arb_init(hW); arb_init(hC);
    arb_init(R); arb_init(absd); arb_init(fac); arb_init(L); arb_init(Ssum);
    arb_init(corr); arb_init(lbound); arb_init(thr); arb_init(btN);
    arb_set_ui(thr,89); arb_div_ui(thr,thr,1000,prec);
    arf_t flo; arf_init(flo);
    fmpz_t sc, zlo; fmpz_init(sc); fmpz_init(zlo);
    fmpz_set_ui(sc,10); fmpz_pow_ui(sc,sc,12);

    /* progress and summary instrumentation (see header) */
    fmpz_t minlo, maxlo; fmpz_init(minlo); fmpz_init(maxlo);
    int have_min = 0;
    ulong minN = 0, maxN = 0;
    ulong nuncert = 0;
    const char *progress_path = getenv("PROP43_PROGRESS");
    time_t wstart = time(NULL), last_report = 0;
    ulong total_rows = (Nend >= Nstart)? (Nend - Nstart)/stride + 1 : 0;

    clock_t tstart = clock();
    ulong npts = 0;
    int exit_code = 0;

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
            else if(!arb_is_positive(inner)){
                printf("inner sign uncertified\n");
                arb_clear(inner);
                arb_clear(x2);
                exit_code = 3;
                goto cleanup;
            }
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
            /* Naive per-point value, using the selected kernel. */
            arb_zero(Ssum); arb_zero(corr);
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
                arb_abs(m1, b_);
                arb_abs(m2, tmp);
                arb_add(m1, m1, m2, prec);
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
                    Wcompute(W, n, N, Nstart, &ms, t, y, pi, c002y, prec);
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
                        Wcompute(Wold, n, Np-1, Nstart, &ms, t, y, pi, c002y, prec);
                        Wcompute(W,    n, Np,   Nstart, &ms, t, y, pi, c002y, prec);
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
                        Wcompute(W, n, N, Nstart, &ms, t, y, pi, c002y, prec);
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
        arf_get_fmpz(zlo, flo, ARF_RND_FLOOR);
        int gt = arb_gt(lbound, thr);
        /* box width makes two-sided output impossible: log L12 =
           floor of the lower ball endpoint (box-uniform lower bound) */
        if(fmpz_sgn(zlo) >= 0 && fmpz_cmp(zlo, sc) < 0){
            char buf[32]; fmpz_get_str(buf, 10, zlo);
            int len = (int)strlen(buf);
            printf("N %lu L12 0.", N);
            for(int i=len;i<12;i++) putchar('0');
            printf("%s GT089 %d\n", buf, gt);
            if(!have_min || fmpz_cmp(zlo, minlo) < 0){
                fmpz_set(minlo, zlo); minN = N;
            }
            if(!have_min || fmpz_cmp(zlo, maxlo) > 0){
                fmpz_set(maxlo, zlo); maxN = N;
            }
            have_min = 1;
        } else { printf("N %lu UNCERT GT089 %d\n", N, gt); nuncert++; }
        fflush(stdout);
        if(getenv("LEMMA_DEBUG")){
            char *debug_value = arb_get_str(lbound, 25, 0);
            printf("DBG N %lu lbound = %s\n", N, debug_value);
            flint_free(debug_value);
        }
        npts++;
        if(progress_path){
            time_t now = time(NULL);
            if(npts == 1 || difftime(now, last_report) >= 60 || npts == total_rows){
                FILE *pf = fopen(progress_path, "w");
                if(pf){
                    double el = difftime(now, wstart);
                    double rate = (el > 0)? (double)npts / el : 0.0;
                    fprintf(pf, "last_N %lu\nrows_done %lu\nrows_total %lu\n",
                            N, npts, total_rows);
                    fprintf(pf, "elapsed_s %.0f\nrows_per_s %.4f\n", el, rate);
                    if(rate > 0)
                        fprintf(pf, "eta_s %.0f\n",
                                (double)(total_rows - npts) / rate);
                    else
                        fprintf(pf, "eta_s NA\n");
                    if(have_min){
                        char mb[32]; fmpz_get_str(mb, 10, minlo);
                        int ml = (int)strlen(mb);
                        fprintf(pf, "min_L12 0.");
                        for(int i=ml;i<12;i++) fputc('0', pf);
                        fprintf(pf, "%s\n", mb);
                    } else fprintf(pf, "min_L12 NA\n");
                    fprintf(pf, "uncert %lu\n", nuncert);
                    fclose(pf);
                }
                last_report = now;
            }
        }
    }
    printf("TIMING %.3f %lu\n", (double)(clock()-tstart)/CLOCKS_PER_SEC, npts);

    if(getenv("PROP43_SUMMARY")){
        FILE *sf = fopen(getenv("PROP43_SUMMARY"), "w");
        if(sf){
            long es = (long) difftime(time(NULL), wstart);
            const char *resname = getenv("PROP43_RESULT");
            int ok = (npts == total_rows) && (nuncert == 0) &&
                     have_min && (fmpz_sgn(minlo) > 0);
            fprintf(sf, "Proposition 4.3 verification run summary\n");
            fprintf(sf, "========================================\n");
            fprintf(sf, "Range iterated:    N = %lu .. %lu"
                        "  (%lu values, stride %lu)\n",
                    Nstart, Nend, npts, stride);
            fprintf(sf, "Mollifier mtype:   %d\n", mtype);
            fprintf(sf, "Certified rows:    %lu of %lu  (UNCERT rows: %lu)\n",
                    npts - nuncert, total_rows, nuncert);
            if(have_min){
                fprintf(sf, "L12 lower bounds:  min ");
                write_l12(sf, minlo);
                fprintf(sf, "  (at N = %lu)\n", minN);
                fprintf(sf, "                   max ");
                write_l12(sf, maxlo);
                fprintf(sf, "  (at N = %lu)\n", maxN);
            } else {
                fprintf(sf, "L12 lower bounds:  no certified rows\n");
            }
            fprintf(sf, "Success criterion: every N certified"
                        " (no UNCERT rows) and min L12 > 0\n");
            fprintf(sf, "RESULT:            %s\n", ok? "SUCCESS" : "FAILURE");
            if(es >= 3600)
                fprintf(sf, "Wall time:         %ldh %ldm %lds\n",
                        es/3600, (es%3600)/60, es%60);
            else
                fprintf(sf, "Wall time:         %ldm %lds\n", es/60, es%60);
            fprintf(sf, "Full results file: %s\n",
                    resname? resname : "(stdout)");
            fclose(sf);
        }
    }

cleanup:
    fmpz_clear(sc);
    fmpz_clear(zlo);
    fmpz_clear(minlo);
    fmpz_clear(maxlo);
    arf_clear(flo);

    arb_clear(N_a);
    arb_clear(xN);
    arb_clear(lnx4pi);
    arb_clear(p);
    arb_clear(sigma);
    arb_clear(d_);
    arb_clear(modK);
    arb_clear(modgamma);
    arb_clear(modmoll);
    arb_clear(lnN);

    arb_clear(tmp);
    arb_clear(tmp2);
    arb_clear(W);
    arb_clear(Wold);
    arb_clear(hW);
    arb_clear(hC);
    arb_clear(R);
    arb_clear(absd);
    arb_clear(fac);
    arb_clear(L);
    arb_clear(Ssum);
    arb_clear(corr);
    arb_clear(lbound);
    arb_clear(thr);
    arb_clear(btN);

    arb_clear(pc);
    _arb_vec_clear(MW, K + 1);
    _arb_vec_clear(MC, K + 1);

    for(int i=0; i<MAXD; i++){
        arb_clear(ms.moll[i]);
        arb_clear(ms.lnd[i]);
    }

    arb_clear(t);
    arb_clear(y);
    arb_clear(a0e);
    arb_clear(amy);
    arb_clear(pi);
    arb_clear(c002y);
    arb_clear(hw);

    flint_cleanup();
    return exit_code;
}
