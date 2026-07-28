/*
 * Independent FLINT/Arb verification of the P1113 tail interface for
 *
 *   t in [129/800, 161250001/10^9],
 *   y0^2 = 87677/2500000,
 *   N >= N1 = 3840000,
 *   M = 153814.
 *
 * This is a new implementation of the endpoint-cap / exact-convolution
 * calculation.  It shares the mathematical statement and exact rational
 * inputs with the Python verifier, but no Python, mpmath code, cached
 * decimal, or serialized coefficient is read.
 *
 * The program refuses precision below 256 bits.  Every decisive comparison
 * is an Arb strict comparison and therefore fails closed when balls overlap.
 */

#include <flint/arb.h>
#include <flint/flint.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MHEAD 153814
#define MERR 3000
#define N1 3840000UL
#define NLAMBDA 11

static slong wp = 320;
static int checks = 0;
static int failures = 0;

static const ulong divisors[NLAMBDA] =
    {1, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14};
static const slong lambda_num[NLAMBDA] =
    {1, -1021, -1054, -9, -1119, 1001, -1043, 128, -161, -447, 456373};
static const ulong lambda_den[NLAMBDA] =
    {1, 1000, 1000, 200, 1000, 1000, 1000, 125, 200, 500, 500000};

static void
report(const char *name, int ok)
{
    checks++;
    if (!ok)
        failures++;
    printf("[%s] %s\n", ok ? "PASS" : "FAIL", name);
}

static void
set_q(arb_t out, slong numerator, ulong denominator)
{
    arb_set_si(out, numerator);
    arb_div_ui(out, out, denominator, wp);
}

static void
set_range_q(arb_t out,
            slong lower_num, ulong lower_den,
            slong upper_num, ulong upper_den)
{
    arb_t lo, hi;
    arb_init(lo);
    arb_init(hi);
    set_q(lo, lower_num, lower_den);
    set_q(hi, upper_num, upper_den);
    arb_union(out, lo, hi, wp);
    arb_clear(lo);
    arb_clear(hi);
}

/* Exact point equal to a directed endpoint of an Arb ball. */
static void
upper_point(arb_t out, const arb_t in)
{
    arf_t u;
    arf_init(u);
    arb_get_ubound_arf(u, in, wp);
    arb_set_arf(out, u);
    arf_clear(u);
}

static void
lower_point(arb_t out, const arb_t in)
{
    arf_t l;
    arf_init(l);
    arb_get_lbound_arf(l, in, wp);
    arb_set_arf(out, l);
    arf_clear(l);
}

static void
max_upper_point(arb_t out, const arb_t a, const arb_t b)
{
    arf_t au, bu;
    arf_init(au);
    arf_init(bu);
    arb_get_ubound_arf(au, a, wp);
    arb_get_ubound_arf(bu, b, wp);
    if (arf_cmp(au, bu) >= 0)
        arb_set_arf(out, au);
    else
        arb_set_arf(out, bu);
    arf_clear(au);
    arf_clear(bu);
}

static int
gt_q(const arb_t x, slong numerator, ulong denominator)
{
    arb_t q;
    int ok;
    arb_init(q);
    set_q(q, numerator, denominator);
    ok = arb_gt(x, q);
    arb_clear(q);
    return ok;
}

static int
lt_q(const arb_t x, slong numerator, ulong denominator)
{
    arb_t q;
    int ok;
    arb_init(q);
    set_q(q, numerator, denominator);
    ok = arb_lt(x, q);
    arb_clear(q);
    return ok;
}

static void
print_ball(const char *label, const arb_t x)
{
    printf("%s = ", label);
    arb_printn(x, 30, ARB_STR_MORE);
    putchar('\n');
}

/* exp((1-sigma) log(u) + (t/4) log(u)^2). */
static void
endpoint_weight(arb_t out, const arb_t logu,
                const arb_t sigma_lower, const arb_t t)
{
    arb_t a, b, c;
    arb_init(a);
    arb_init(b);
    arb_init(c);

    arb_one(a);
    arb_sub(a, a, sigma_lower, wp);
    arb_mul(a, a, logu, wp);

    arb_mul(b, logu, logu, wp);
    arb_mul(b, b, t, wp);
    arb_div_ui(b, b, 4, wp);

    arb_add(c, a, b, wp);
    arb_exp(out, c, wp);

    arb_clear(a);
    arb_clear(b);
    arb_clear(c);
}

/*
 * Endpoint-cap upper bound:
 * max(E(a), E(c)) (log(c)-log(a)).
 * sigma_lower is a point lower bound for sigma.
 */
static void
cap_upper(arb_t out, const arb_t loga, const arb_t logc,
          const arb_t sigma_lower, const arb_t t)
{
    arb_t ea, ec, maximum, width, width_upper, product;
    arb_init(ea);
    arb_init(ec);
    arb_init(maximum);
    arb_init(width);
    arb_init(width_upper);
    arb_init(product);

    endpoint_weight(ea, loga, sigma_lower, t);
    endpoint_weight(ec, logc, sigma_lower, t);
    max_upper_point(maximum, ea, ec);
    arb_sub(width, logc, loga, wp);
    upper_point(width_upper, width);
    arb_mul(product, maximum, width_upper, wp);
    upper_point(out, product);

    arb_clear(ea);
    arb_clear(ec);
    arb_clear(maximum);
    arb_clear(width);
    arb_clear(width_upper);
    arb_clear(product);
}

static void
exp_minus_sigma_log(arb_t out, const arb_t sigma_lower, const arb_t logu)
{
    arb_t z;
    arb_init(z);
    arb_mul(z, sigma_lower, logu, wp);
    arb_neg(z, z);
    arb_exp(out, z, wp);
    arb_clear(z);
}

static arb_ptr
new_vec(slong n)
{
    slong i;
    arb_ptr v = flint_malloc((size_t) n * sizeof(arb_struct));
    if (v == NULL)
    {
        fprintf(stderr, "allocation failure\n");
        exit(2);
    }
    for (i = 0; i < n; i++)
        arb_init(v + i);
    return v;
}

static void
clear_vec(arb_ptr v, slong n)
{
    slong i;
    for (i = 0; i < n; i++)
        arb_clear(v + i);
    flint_free(v);
}

static int
exact_hull_checks(void)
{
    /*
     * These comparisons are exact integer arithmetic.  Each product is
     * below UINT64_MAX (the largest is < 8.77e18).
     */
    uint64_t ylo2_scaled =
        UINT64_C(1872719) * UINT64_C(1872719) * UINT64_C(2500000);
    uint64_t y0_scaled_lo =
        UINT64_C(87677) * UINT64_C(10000000) * UINT64_C(10000000);
    uint64_t y0_scaled_hi =
        UINT64_C(87677) * UINT64_C(125000) * UINT64_C(125000);
    uint64_t yhi2_scaled =
        UINT64_C(23409) * UINT64_C(23409) * UINT64_C(2500000);
    uint64_t ytop2_scaled =
        UINT64_C(8231039) * UINT64_C(8231039) * UINT64_C(400);
    uint64_t top_target_scaled =
        UINT64_C(271) * UINT64_C(10000000) * UINT64_C(10000000);
    uint64_t yprev2_scaled =
        UINT64_C(4115519) * UINT64_C(4115519) * UINT64_C(400);
    uint64_t prev_target_scaled =
        UINT64_C(271) * UINT64_C(5000000) * UINT64_C(5000000);
    uint64_t yhi_tupper_left =
        UINT64_C(23409) * UINT64_C(23409) * UINT64_C(1000000000);
    uint64_t yhi_tupper_right =
        (UINT64_C(1000000000) - 2 * UINT64_C(161250001))
        * UINT64_C(125000) * UINT64_C(125000);

    return ylo2_scaled < y0_scaled_lo
        && y0_scaled_hi < yhi2_scaled
        && ytop2_scaled >= top_target_scaled
        && yprev2_scaled < prev_target_scaled
        && yhi_tupper_left <= yhi_tupper_right;
}

int
main(int argc, char **argv)
{
    slong i, n;
    ulong lambda_abs_scaled = 0;
    arb_ptr logs, bt, coefficient;

    arb_t zero, one, two, pi;
    arb_t t, tlo, thi, ybox, yext;
    arb_t lnN, nball, n2, x1, l1, z16, delta, kappa;
    arb_t base1, base2, s1box, s2box, s1ext, s2ext;
    arb_t s1box_lo, s2box_lo, s1ext_lo, s2ext_lo;
    arb_t tmp, tmp2, tmp3, tmp4, term, sum, lambda, abs_lambda;
    arb_t P_raw, P, P_lower, P_width;
    arb_t TR, OV, Mmax, Gbox, PA, capB, AB;
    arb_t D, flow;
    arb_t ygate1, ygate2, threshold;
    arb_t delerr, SB, PAerr, Gerr, ABerr, eAB, eC0, err;
    arb_t log3, abslog, exponent, powers3;
    arb_t one_minus_D, margin;
    arb_t loga, width, gate_a, gate_b;
    int routed_gates = 1;
    int overshoot_gates = 1;
    int main_cap_gates = 1;
    int error_cap_gates = 1;

    if (argc > 2)
    {
        fprintf(stderr, "usage: %s [precision_bits]\n", argv[0]);
        return 2;
    }
    if (argc == 2)
        wp = (slong) strtol(argv[1], NULL, 10);
    if (wp < 256)
    {
        fprintf(stderr, "refusing precision below 256 bits\n");
        return 2;
    }

    printf("P1113 Arb verifier: precision=%ld, N1=%lu, M=%d\n",
           (long) wp, N1, MHEAD);

    arb_init(zero); arb_init(one); arb_init(two); arb_init(pi);
    arb_init(t); arb_init(tlo); arb_init(thi); arb_init(ybox); arb_init(yext);
    arb_init(lnN); arb_init(nball); arb_init(n2); arb_init(x1); arb_init(l1);
    arb_init(z16); arb_init(delta); arb_init(kappa);
    arb_init(base1); arb_init(base2); arb_init(s1box); arb_init(s2box);
    arb_init(s1ext); arb_init(s2ext);
    arb_init(s1box_lo); arb_init(s2box_lo);
    arb_init(s1ext_lo); arb_init(s2ext_lo);
    arb_init(tmp); arb_init(tmp2); arb_init(tmp3); arb_init(tmp4);
    arb_init(term); arb_init(sum); arb_init(lambda); arb_init(abs_lambda);
    arb_init(P_raw); arb_init(P); arb_init(P_lower); arb_init(P_width);
    arb_init(TR); arb_init(OV); arb_init(Mmax); arb_init(Gbox);
    arb_init(PA); arb_init(capB); arb_init(AB);
    arb_init(D); arb_init(flow);
    arb_init(ygate1); arb_init(ygate2); arb_init(threshold);
    arb_init(delerr); arb_init(SB); arb_init(PAerr); arb_init(Gerr);
    arb_init(ABerr); arb_init(eAB); arb_init(eC0); arb_init(err);
    arb_init(log3); arb_init(abslog); arb_init(exponent); arb_init(powers3);
    arb_init(one_minus_D); arb_init(margin);
    arb_init(loga); arb_init(width); arb_init(gate_a); arb_init(gate_b);

    arb_zero(zero);
    arb_one(one);
    arb_set_ui(two, 2);
    arb_const_pi(pi, wp);

    set_q(tlo, 129, 800);
    set_q(thi, 161250001, 1000000000UL);
    arb_union(t, tlo, thi, wp);
    set_range_q(ybox, 1872719, 10000000UL, 23409, 125000UL);
    set_range_q(yext, 1872719, 10000000UL, 8231039, 10000000UL);

    report("exact rational target and y-hull containments", exact_hull_checks());
    report("exact target identity t0+y0^2/2 = 893927/5000000",
           129UL * 6250UL + 87677UL == 893927UL);
    report("domain: 0 < t <= 1/2", arb_gt(t, zero) && lt_q(t, 1, 2));
    report("domain: 0 < ybox <= yext <= 1",
           arb_gt(ybox, zero) && arb_gt(yext, zero)
           && lt_q(ybox, 1, 1) && lt_q(yext, 1, 1));
    report("domain: N1 > MHEAD > MERR > 1",
           N1 > MHEAD && MHEAD > MERR && MERR > 1);
    report("P1113 has lambda_1 = 1",
           divisors[0] == 1 && lambda_num[0] == 1 && lambda_den[0] == 1);
    for (i = 0; i < NLAMBDA; i++)
    {
        ulong a = (ulong) (lambda_num[i] < 0 ? -lambda_num[i] : lambda_num[i]);
        if (1000000UL % lambda_den[i] != 0)
            lambda_abs_scaled = 0;
        else
            lambda_abs_scaled += a * (1000000UL / lambda_den[i]);
    }
    report("exact P1113 vector normalization sum|lambda|=9918746/1000000",
           lambda_abs_scaled == 9918746UL);

    logs = new_vec(MHEAD + 1);
    bt = new_vec(MHEAD + 1);
    coefficient = new_vec(MHEAD + 1);
    arb_zero(logs + 0);
    arb_zero(logs + 1);
    arb_one(bt + 0);
    arb_one(bt + 1);

    for (n = 2; n <= MHEAD; n++)
    {
        arb_set_ui(tmp, (ulong) n);
        arb_log(logs + n, tmp, wp);
    }

    arb_set_ui(nball, N1);
    arb_log(lnN, nball, wp);
    arb_mul(n2, nball, nball, wp);
    arb_div_ui(tmp, t, 16, wp);
    arb_sub(tmp2, n2, tmp, wp);                  /* N^2 - t/16 */
    arb_log(l1, tmp2, wp);
    arb_mul(x1, pi, tmp2, wp);
    arb_mul_ui(x1, x1, 4, wp);

    report("domain: X_N(t) > 200 and all error denominators positive",
           gt_q(x1, 200, 1) && gt_q(x1, 12, 1));
    report("domain: log(N^2-t/16) > 2", gt_q(l1, 2, 1));

    /* z = t/(16N^2). */
    arb_mul_ui(tmp, n2, 16, wp);
    arb_div(z16, t, tmp, wp);
    report("domain: 0 < t/(16N^2) < 1", arb_gt(z16, zero) && arb_lt(z16, one));

    /*
     * delta_hat =
     * t/4[-log(1-z)] + t/(2 X_N^2), at the whole t interval.
     */
    arb_sub(tmp, one, z16, wp);
    arb_log(tmp, tmp, wp);
    arb_neg(tmp, tmp);
    arb_mul(tmp, tmp, t, wp);
    arb_div_ui(tmp, tmp, 4, wp);
    arb_mul(tmp2, x1, x1, wp);
    arb_mul_ui(tmp2, tmp2, 2, wp);
    arb_div(tmp2, t, tmp2, wp);
    arb_add(tmp, tmp, tmp2, wp);
    upper_point(delta, tmp);

    /* kappa_hat = t/[2(X_N-6)], using y <= 1. */
    arb_sub_ui(tmp, x1, 6, wp);
    arb_mul_ui(tmp, tmp, 2, wp);
    arb_div(tmp, t, tmp, wp);
    upper_point(kappa, tmp);

    /*
     * sigma1 = 1/2 + (t/2) log N - delta_hat + y/2
     * sigma2 = 1/2 + (t/2) log N - delta_hat-kappa_hat - y/2.
     */
    arb_mul(tmp, t, lnN, wp);
    arb_div_ui(tmp, tmp, 2, wp);
    set_q(base1, 1, 2);
    arb_add(base1, base1, tmp, wp);
    arb_sub(base1, base1, delta, wp);
    arb_sub(base2, base1, kappa, wp);

    arb_div_ui(tmp, ybox, 2, wp);
    arb_add(s1box, base1, tmp, wp);
    arb_sub(s2box, base2, tmp, wp);
    arb_div_ui(tmp, yext, 2, wp);
    arb_add(s1ext, base1, tmp, wp);
    arb_sub(s2ext, base2, tmp, wp);
    lower_point(s1box_lo, s1box);
    lower_point(s2box_lo, s2box);
    lower_point(s1ext_lo, s1ext);
    lower_point(s2ext_lo, s2ext);

    /* Cap validity: sigma_j > (t/2) log N, on both hulls. */
    arb_mul(tmp, thi, lnN, wp);
    arb_div_ui(tmp, tmp, 2, wp);
    upper_point(threshold, tmp);
    report("SC1: sigma1 > (t/2) log N on box and extended hull",
           arb_gt(s1box_lo, threshold) && arb_gt(s1ext_lo, threshold));
    report("SC2: sigma2 > (t/2) log N on box and extended hull",
           arb_gt(s2box_lo, threshold) && arb_gt(s2ext_lo, threshold));
    report("SC3: sigma1,sigma2 > 1 on extended hull",
           arb_gt(s1ext_lo, one) && arb_gt(s2ext_lo, one));

    /* Structural window-freeze/domain gates. */
    arb_mul(tmp, nball, one, wp);
    arb_sub(tmp2, one, z16, wp);
    arb_mul(tmp, tmp, tmp2, wp);
    report("window log gate: N(1-t/(16N^2)) > 1", arb_gt(tmp, one));
    report("delta and kappa cutoff monotonicity premises: t>=0, X_N>12",
           arb_gt(t, zero) && gt_q(x1, 12, 1));
    report("sigma N-slope t/2 is positive", arb_gt(t, zero));
    report("G N-monotonicity premises: y>0 and N^2-t/16>0",
           arb_gt(yext, zero) && arb_gt(tmp2, zero));

    /* b_t(n). */
    for (n = 2; n <= MHEAD; n++)
    {
        arb_mul(tmp, logs + n, logs + n, wp);
        arb_mul(tmp, tmp, t, wp);
        arb_div_ui(tmp, tmp, 4, wp);
        arb_exp(bt + n, tmp, wp);
    }

    /* Independent exact Dirichlet convolution c_m. */
    for (i = 0; i < NLAMBDA; i++)
    {
        ulong d = divisors[i];
        ulong kmax = MHEAD / d;
        set_q(lambda, lambda_num[i], lambda_den[i]);
        for (ulong k = 1; k <= kmax; k++)
        {
            ulong m = d * k;
            if (m < 2)
                continue;
            if (k == 1)
                arb_set(term, lambda);
            else
                arb_mul(term, lambda, bt + k, wp);
            arb_add(coefficient + m, coefficient + m, term, wp);
        }
    }

    /* P = sum_{m=2}^M |c_m| m^{-sigma1}. */
    arb_zero(P_raw);
    for (n = 2; n <= MHEAD; n++)
    {
        arb_abs(tmp, coefficient + n);
        exp_minus_sigma_log(tmp2, s1box_lo, logs + n);
        arb_mul(term, tmp, tmp2, wp);
        arb_add(P_raw, P_raw, term, wp);
    }
    lower_point(P_lower, P_raw);
    upper_point(P, P_raw);
    arb_sub(P_width, P, P_lower, wp);

    /* TR: complete routed remainder after the exact convolution head. */
    arb_zero(TR);
    for (i = 0; i < NLAMBDA; i++)
    {
        ulong d = divisors[i];
        ulong a = MHEAD / d;
        arb_set(loga, logs + a);
        cap_upper(tmp, loga, lnN, s1box_lo, t);

        set_q(abs_lambda,
              lambda_num[i] < 0 ? -lambda_num[i] : lambda_num[i],
              lambda_den[i]);
        if (d == 1)
            arb_one(tmp2);
        else
            exp_minus_sigma_log(tmp2, s1box_lo, logs + d);
        arb_mul(tmp3, abs_lambda, tmp2, wp);
        arb_mul(term, tmp3, tmp, wp);
        arb_add(TR, TR, term, wp);

        arb_sub(width, lnN, loga, wp);
        arb_mul(gate_a, tlo, loga, wp);
        arb_mul(gate_a, gate_a, width, wp);
        arb_div_ui(gate_a, gate_a, 2, wp);
        arb_sub(gate_b, s1ext_lo, one, wp);
        arb_mul(gate_b, gate_b, width, wp);
        if (!(arb_gt(gate_a, one) && arb_gt(gate_b, one)
              && a >= 1 && a < N1))
            routed_gates = 0;
    }
    upper_point(TR, TR);
    report("GN-TR: every fixed-left routed cap decreases for all N>=N1",
           routed_gates);

    /*
     * OV is redundant nonnegative padding.  We reproduce it and also check
     * the advertised floor containment.
     */
    arb_zero(OV);
    for (i = 0; i < NLAMBDA; i++)
    {
        ulong d = divisors[i];
        if (d == 1)
            continue;
        arb_set_ui(tmp, d + 1);
        arb_log(tmp, tmp, wp);
        arb_sub(loga, lnN, tmp, wp);
        cap_upper(tmp2, loga, lnN, s1box_lo, t);

        set_q(abs_lambda,
              lambda_num[i] < 0 ? -lambda_num[i] : lambda_num[i],
              lambda_den[i]);
        exp_minus_sigma_log(tmp3, s1box_lo, logs + d);
        arb_mul(tmp4, abs_lambda, tmp3, wp);
        arb_mul(term, tmp4, tmp2, wp);
        arb_add(OV, OV, term, wp);

        if (N1 < d * (d + 1))
            overshoot_gates = 0;
    }
    upper_point(OV, OV);
    report("OVW: floor(N/d)>=N/(d+1), and moving caps decrease by sigma>1",
           overshoot_gates && arb_gt(s1ext_lo, one));

    /* Mmax = sum |lambda_d| d^{-sigma1}. */
    arb_zero(Mmax);
    for (i = 0; i < NLAMBDA; i++)
    {
        ulong d = divisors[i];
        set_q(abs_lambda,
              lambda_num[i] < 0 ? -lambda_num[i] : lambda_num[i],
              lambda_den[i]);
        if (d == 1)
            arb_one(tmp);
        else
            exp_minus_sigma_log(tmp, s1box_lo, logs + d);
        arb_mul(term, abs_lambda, tmp, wp);
        arb_add(Mmax, Mmax, term, wp);
    }
    upper_point(Mmax, Mmax);
    report("Mmax is strictly positive", arb_gt(Mmax, zero));

    /* G on the lower y-box. */
    set_q(tmp, 2, 100);
    arb_mul(tmp, tmp, ybox, wp);
    arb_exp(tmp, tmp, wp);
    arb_mul(tmp2, ybox, l1, wp);
    arb_div_ui(tmp2, tmp2, 2, wp);
    arb_neg(tmp2, tmp2);
    arb_exp(tmp2, tmp2, wp);
    arb_mul(Gbox, tmp, tmp2, wp);
    upper_point(Gbox, Gbox);

    /* A-side finite head and endpoint cap. */
    arb_one(PA);
    for (n = 2; n <= MHEAD; n++)
    {
        exp_minus_sigma_log(tmp, s2box_lo, logs + n);
        arb_mul(term, bt + n, tmp, wp);
        arb_add(PA, PA, term, wp);
    }
    upper_point(PA, PA);
    cap_upper(capB, logs + MHEAD, lnN, s2box_lo, t);
    arb_add(tmp, PA, capB, wp);
    arb_mul(AB, Gbox, tmp, wp);
    upper_point(AB, AB);

    /* Explicit N-monotonicity gates for the MHEAD A cap. */
    arb_sub(width, lnN, logs + MHEAD, wp);
    arb_mul(gate_a, tlo, logs + MHEAD, wp);
    arb_mul(gate_a, gate_a, width, wp);
    arb_div_ui(gate_a, gate_a, 2, wp);
    arb_sub(gate_b, s2ext_lo, one, wp);
    arb_mul(gate_b, gate_b, width, wp);
    main_cap_gates = arb_gt(gate_a, one) && arb_gt(gate_b, one);
    report("GN-AB: fixed-left MHEAD A-cap decreases for all N>=N1",
           main_cap_gates);

    /* D = P + TR + OV + Mmax*AB. */
    arb_mul(tmp, Mmax, AB, wp);
    arb_add(D, P, TR, wp);
    arb_add(D, D, OV, wp);
    arb_add(D, D, tmp, wp);
    upper_point(D, D);
    arb_sub(one_minus_D, one, D, wp);
    arb_div(flow, one_minus_D, Mmax, wp);
    lower_point(flow, flow);

    /*
     * y-monotonicity: B terms fall because dsigma1/dy=+1/2.
     * G*A terms fall if 0.02-L/2+log(u)/2<0 for u<=N.
     */
    set_q(ygate1, 2, 100);
    arb_div_ui(tmp, l1, 2, wp);
    arb_sub(ygate1, ygate1, tmp, wp);
    arb_div_ui(tmp, lnN, 2, wp);
    arb_add(ygate1, ygate1, tmp, wp);
    upper_point(ygate1, ygate1);

    set_q(ygate2, 2, 100);
    arb_div_ui(tmp, lnN, 2, wp);
    arb_sub(ygate2, ygate2, tmp, wp);
    arb_sub(tmp, one, z16, wp);
    arb_log(tmp, tmp, wp);
    arb_div_ui(tmp, tmp, 2, wp);
    arb_sub(ygate2, ygate2, tmp, wp);
    upper_point(ygate2, ygate2);
    report("YM: D decreases above the lower y-box",
           arb_lt(ygate1, zero) && arb_lt(ygate2, zero));

    /*
     * Error terms.  Delta is a uniform point upper bound for the exact
     * epsilon expression.  The A part uses equation (71) termwise:
     * n^{-Re(kappa)} <= n^{|kappa|}; it is not inferred from the coarser
     * displayed N^{|kappa|} bound.
     */
    arb_mul(tmp, t, t, wp);
    arb_div_ui(tmp, tmp, 16, wp);
    arb_mul(tmp2, l1, l1, wp);
    arb_mul(tmp, tmp, tmp2, wp);
    set_q(tmp2, 626, 1000);
    arb_add(tmp, tmp, tmp2, wp);
    set_q(tmp2, 333, 50);                       /* 6.66 */
    arb_sub(tmp2, x1, tmp2, wp);
    arb_div(tmp, tmp, tmp2, wp);
    upper_point(delerr, tmp);

    arb_one(SB);
    arb_one(PAerr);
    for (n = 2; n <= MERR; n++)
    {
        exp_minus_sigma_log(tmp, s1ext_lo, logs + n);
        arb_mul(term, bt + n, tmp, wp);
        arb_add(SB, SB, term, wp);

        exp_minus_sigma_log(tmp, s2ext_lo, logs + n);
        arb_mul(term, bt + n, tmp, wp);
        arb_add(PAerr, PAerr, term, wp);
    }
    upper_point(SB, SB);
    upper_point(PAerr, PAerr);

    cap_upper(tmp, logs + MERR, lnN, s1ext_lo, t);
    arb_add(SB, SB, tmp, wp);
    upper_point(SB, SB);
    cap_upper(tmp, logs + MERR, lnN, s2ext_lo, t);
    arb_add(PAerr, PAerr, tmp, wp);
    upper_point(PAerr, PAerr);

    set_q(tmp, 2, 100);
    arb_mul(tmp, tmp, yext, wp);
    arb_exp(tmp, tmp, wp);
    arb_mul(tmp2, yext, l1, wp);
    arb_div_ui(tmp2, tmp2, 2, wp);
    arb_neg(tmp2, tmp2);
    arb_exp(tmp2, tmp2, wp);
    arb_mul(Gerr, tmp, tmp2, wp);
    upper_point(Gerr, Gerr);
    arb_mul(ABerr, Gerr, PAerr, wp);
    upper_point(ABerr, ABerr);

    arb_exp(tmp, delerr, wp);
    arb_sub(tmp, tmp, one, wp);
    arb_add(tmp2, SB, ABerr, wp);
    arb_mul(eAB, tmp, tmp2, wp);
    upper_point(eAB, eAB);

    /* Explicit MERR cap monotonicity gates, for sigma1 and sigma2. */
    arb_sub(width, lnN, logs + MERR, wp);
    arb_mul(gate_a, tlo, logs + MERR, wp);
    arb_mul(gate_a, gate_a, width, wp);
    arb_div_ui(gate_a, gate_a, 2, wp);
    arb_sub(gate_b, s1ext_lo, one, wp);
    arb_mul(gate_b, gate_b, width, wp);
    error_cap_gates = arb_gt(gate_a, one) && arb_gt(gate_b, one);
    arb_sub(gate_b, s2ext_lo, one, wp);
    arb_mul(gate_b, gate_b, width, wp);
    error_cap_gates = error_cap_gates && arb_gt(gate_b, one);
    report("GN-error: both MERR=3000 caps decrease for all N>=N1",
           error_cap_gates);

    /*
     * e_C0, using the paper's x-12 denominator.
     */
    arb_add(tmp, one, yext, wp);
    arb_mul(tmp, tmp, l1, wp);
    arb_div_ui(tmp, tmp, 4, wp);
    arb_neg(exponent, tmp);

    arb_mul(tmp, t, l1, wp);
    arb_mul(tmp, tmp, l1, wp);
    arb_div_ui(tmp, tmp, 16, wp);
    arb_sub(exponent, exponent, tmp, wp);

    arb_set_ui(tmp, 3);
    arb_log(log3, tmp, wp);
    arb_mul(tmp, yext, log3, wp);
    arb_exp(tmp2, tmp, wp);
    arb_neg(tmp, tmp);
    arb_exp(tmp3, tmp, wp);
    arb_add(powers3, tmp2, tmp3, wp);
    set_q(tmp, 124, 100);
    arb_mul(tmp, tmp, powers3, wp);
    set_q(tmp2, 1, 8);
    arb_sub(tmp2, nball, tmp2, wp);
    arb_div(tmp, tmp, tmp2, wp);
    arb_add(exponent, exponent, tmp, wp);

    arb_mul(tmp, l1, l1, wp);
    arb_mul(tmp2, pi, pi, wp);
    arb_div_ui(tmp2, tmp2, 4, wp);
    arb_add(tmp, tmp, tmp2, wp);
    arb_sqrt(abslog, tmp, wp);
    arb_mul_ui(tmp, abslog, 3, wp);
    set_q(tmp2, 21, 2);
    arb_add(tmp, tmp, tmp2, wp);
    arb_sub_ui(tmp2, x1, 12, wp);
    arb_div(tmp, tmp, tmp2, wp);
    arb_add(exponent, exponent, tmp, wp);
    arb_exp(eC0, exponent, wp);
    upper_point(eC0, eC0);

    arb_add(err, eAB, eC0, wp);
    upper_point(err, err);
    arb_sub(margin, flow, err, wp);
    lower_point(margin, margin);

    /* Analytic signs for the all-N error reduction. */
    arb_sub_ui(tmp, l1, 2, wp);
    arb_mul(tmp, tmp, l1, wp);                  /* L(L-2) > 0 */
    arb_mul(tmp, tmp, t, wp);
    arb_mul(tmp, tmp, t, wp);
    arb_div_ui(tmp, tmp, 16, wp);
    set_q(tmp2, 626, 1000);
    arb_add(tmp, tmp, tmp2, wp);
    report("Delta N-monotonicity gate: (t^2/16)L(L-2)+0.626 > 0",
           arb_gt(tmp, zero));
    report("eC0 quotient N-monotonicity gate: 3 < 10.50 and X_N>12",
           3 * 2 < 21 && gt_q(x1, 12, 1));

    /*
     * Numerical decisions and deliberately broad two-sided regression
     * corridors.  The upper/lower facts used by the theorem are D<1 and
     * flow>err; the corridors help expose missing or duplicated terms.
     */
    report("P corridor 0.170227 < P < 0.170229",
           gt_q(P, 170227, 1000000) && lt_q(P, 170229, 1000000));
    report("TR corridor 0.262900 < TR < 0.262902",
           gt_q(TR, 262900, 1000000) && lt_q(TR, 262902, 1000000));
    report("OV corridor 0.039241 < OV < 0.039243",
           gt_q(OV, 39241, 1000000) && lt_q(OV, 39243, 1000000));
    report("Mmax corridor 1.608288 < Mmax < 1.608290",
           gt_q(Mmax, 1608288, 1000000) && lt_q(Mmax, 1608290, 1000000));
    report("AB corridor 0.327893 < AB < 0.327895",
           gt_q(AB, 327893, 1000000) && lt_q(AB, 327895, 1000000));
    report("D corridor 0.999719 < D < 0.999721",
           gt_q(D, 999719, 1000000) && lt_q(D, 999721, 1000000));
    report("P interval width is smaller than 1-D", arb_lt(P_width, one_minus_D));
    report("decisive contraction D < 1", arb_lt(D, one));
    report("flow corridor 0.0001735 < flow < 0.0001740",
           gt_q(flow, 1735, 10000000) && lt_q(flow, 1740, 10000000));
    report("error corridor 1.1670e-8 < err < 1.1672e-8",
           gt_q(err, 11670, 1000000000000UL)
           && lt_q(err, 11672, 1000000000000UL));
    report("decisive normalized margin flow > error > 0",
           arb_gt(flow, err) && arb_gt(err, zero) && arb_gt(margin, zero));

    puts("\nDirected Arb enclosures:");
    print_ball("P upper point", P);
    print_ball("TR upper point", TR);
    print_ball("OV upper point", OV);
    print_ball("Mmax upper point", Mmax);
    print_ball("AB upper point", AB);
    print_ball("D upper point", D);
    print_ball("flow lower point", flow);
    print_ball("eAB upper point", eAB);
    print_ball("eC0 upper point", eC0);
    print_ball("error upper point", err);
    print_ball("flow-error lower point", margin);
    print_ball("P enclosure width", P_width);

    printf("\nTOTAL CHECKS: %d; FAILURES: %d\n", checks, failures);
    puts(failures == 0 ? "RESULT: ALL ARB TAIL CHECKS PASS"
                      : "RESULT: ARB TAIL CHECK FAILURE");

    clear_vec(logs, MHEAD + 1);
    clear_vec(bt, MHEAD + 1);
    clear_vec(coefficient, MHEAD + 1);

    arb_clear(zero); arb_clear(one); arb_clear(two); arb_clear(pi);
    arb_clear(t); arb_clear(tlo); arb_clear(thi); arb_clear(ybox); arb_clear(yext);
    arb_clear(lnN); arb_clear(nball); arb_clear(n2); arb_clear(x1); arb_clear(l1);
    arb_clear(z16); arb_clear(delta); arb_clear(kappa);
    arb_clear(base1); arb_clear(base2); arb_clear(s1box); arb_clear(s2box);
    arb_clear(s1ext); arb_clear(s2ext);
    arb_clear(s1box_lo); arb_clear(s2box_lo);
    arb_clear(s1ext_lo); arb_clear(s2ext_lo);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(tmp3); arb_clear(tmp4);
    arb_clear(term); arb_clear(sum); arb_clear(lambda); arb_clear(abs_lambda);
    arb_clear(P_raw); arb_clear(P); arb_clear(P_lower); arb_clear(P_width);
    arb_clear(TR); arb_clear(OV); arb_clear(Mmax); arb_clear(Gbox);
    arb_clear(PA); arb_clear(capB); arb_clear(AB);
    arb_clear(D); arb_clear(flow);
    arb_clear(ygate1); arb_clear(ygate2); arb_clear(threshold);
    arb_clear(delerr); arb_clear(SB); arb_clear(PAerr); arb_clear(Gerr);
    arb_clear(ABerr); arb_clear(eAB); arb_clear(eC0); arb_clear(err);
    arb_clear(log3); arb_clear(abslog); arb_clear(exponent); arb_clear(powers3);
    arb_clear(one_minus_D); arb_clear(margin);
    arb_clear(loga); arb_clear(width); arb_clear(gate_a); arb_clear(gate_b);

    flint_cleanup();
    return failures == 0 ? 0 : 1;
}
