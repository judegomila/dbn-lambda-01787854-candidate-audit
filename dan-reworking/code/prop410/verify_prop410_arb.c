/*
 * Authoritative FLINT/Arb verification of Proposition 4.10: the uniform
 * effective-approximation error budget over the finite region, at
 *
 *   t in [129/800, 161250001/10^9],
 *   y0^2 = 87677/2500000,
 *   ymax^2 = 1 - 2 t0 = 271/400,
 *   N0 = 690988,  m0 = 2000.
 *
 * This is a cross-backend Arb reconstruction of the U1--U5 calculation in
 * verifiers/verify_finite_and_binding.py (and its derived copy
 * independent/prop410/prop410_proof.py).  It implements the mathematics of
 * the Proposition 4.10 proof block directly in Arb ball arithmetic: no
 * Python, no mpmath, no cached decimal, and no serialized coefficient is
 * read.  Every transcendental value (sqrt, log, exp, powers, pi) is a
 * rigorous Arb enclosure, so the proof no longer depends on mpmath.iv
 * providing correctly outward-rounded transcendental values.
 *
 * All decimal constants of the upstream formulas are constructed from
 * exact integers or rationals: 0.02 = 1/50, 0.626 = 313/500, 1.24 = 31/25,
 * 6.66 = 333/50, 10.50 = 21/2, 0.125 = 1/8.  Where the Python program
 * takes upper_point of an enclosure, this program takes the directed Arb
 * upper endpoint (arb_get_ubound_arf) and converts that endpoint into an
 * exact dyadic point before it enters a subsequent monotone majorant.
 *
 * The interval computation bounds each occurrence of an interval-valued
 * quantity independently, exactly as interval arithmetic does.  Where the
 * mpmath implementation relies on directed endpoint arithmetic inside a
 * wide interval operation (t has width 10^-9, sigma1 inherits it), this
 * program substitutes the corresponding directed endpoint explicitly:
 * the exact rational t endpoints tlo/thi where the sign of the
 * coefficient is gated, and the exact dyadic lower endpoint of sigma1
 * where the exponent decreases in sigma1 (log u > 0 is gated).  This is
 * the same lower_point/majorant idiom as verify_tail_arb.c and yields
 * the same mathematical upper bounds as the mpmath interval evaluation,
 * without the second-order radius padding of wide-ball transcendental
 * calls.
 *
 * Every decisive comparison subtracts an exact rational and requires the
 * whole resulting ball to be on the strict side (arb_is_negative /
 * arb_is_positive), so an indeterminate comparison fails closed.  The
 * program reads no stored numerical certificate, refuses precision below
 * 256 bits, requires the precision as an explicit argument, emits all
 * exact parameters and every domain/sign gate, emits directed bounds for
 * e_A+e_B, e_C0, E_max and T_min-E_max, and ends with one unique success
 * line only if every gate passes.
 *
 * The finite floor T_min = 791366/10^12 is the certified global sweep
 * minimum of Proposition 4.3 (recomputed by verify_finite_and_binding.py
 * from the stored rows and by independent/prop43/prop43_proof.c from
 * scratch); it enters here only as an exact rational input to the final
 * margin gate T_min - E_max > 0.
 */

#include <flint/arb.h>
#include <flint/flint.h>
#include <flint/fmpz.h>
#include <stdio.h>
#include <stdlib.h>

#define N0 690988UL
#define M0 2000

static slong wp = 0;
static int checks = 0;
static int failures = 0;

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

/*
 * Certify x < num/10^exp10 by proving the whole ball of
 * x*10^exp10 - num is negative.  The scaling and subtraction are ball
 * operations on exact integer inputs, so the comparison fails closed.
 */
static int
lt_decimal(const arb_t x, slong numerator, ulong exp10)
{
    fmpz_t scale, num;
    arb_t diff;
    int ok;
    fmpz_init(scale);
    fmpz_init(num);
    arb_init(diff);
    fmpz_ui_pow_ui(scale, 10, exp10);
    fmpz_set_si(num, numerator);
    arb_mul_fmpz(diff, x, scale, wp);
    arb_sub_fmpz(diff, diff, num, wp);
    ok = arb_is_negative(diff);
    arb_clear(diff);
    fmpz_clear(num);
    fmpz_clear(scale);
    return ok;
}

static void
print_ball(const char *label, const arb_t x)
{
    printf("%s = ", label);
    arb_printn(x, 30, ARB_STR_MORE);
    putchar('\n');
}

int
main(int argc, char **argv)
{
    slong n;

    arb_t zero, one, two, pi;
    arb_t t, tlo, thi, y0, ymax, nball, n2, q, x0, log0, logn0, logm0;
    arb_t z, one_minus_z, delta1, sigma1, sigma1_lo, y1, kappa, blo;
    arb_t g_t1, g_t2, u1max, pmax, head, term1, term2, cap_u, smax;
    arb_t eAB, eC0, emax, tmin, margin;
    arb_t log3, exponent, powers3;
    arb_t tmp, tmp2, tmp3, logn;

    if (argc != 2)
    {
        fprintf(stderr, "usage: %s precision_bits\n", argv[0]);
        return 2;
    }
    wp = (slong) strtol(argv[1], NULL, 10);
    if (wp < 256)
    {
        fprintf(stderr, "refusing precision below 256 bits\n");
        return 2;
    }

    printf("Prop410 Arb verifier: precision=%ld, N0=%lu, m0=%d\n",
           (long) wp, N0, M0);
    puts("PARAM t0 = 129/800");
    puts("PARAM tbox_lo = 161250000/1000000000");
    puts("PARAM tbox_hi = 161250001/1000000000");
    puts("PARAM y0^2 = 87677/2500000");
    puts("PARAM ymax^2 = 271/400");
    printf("PARAM N0 = %lu\n", N0);
    printf("PARAM m0 = %d\n", M0);
    puts("PARAM Tmin = 791366/1000000000000");
    puts("PARAM budget_Emax = 234/1000000000");
    puts("PARAM stated_eAB = 206/100000000000000");
    puts("PARAM stated_eC0 = 233492848188649183/10^24");
    puts("PARAM stated_Emax = 233494905212337849/10^24");

    arb_init(zero); arb_init(one); arb_init(two); arb_init(pi);
    arb_init(t); arb_init(tlo); arb_init(thi);
    arb_init(y0); arb_init(ymax); arb_init(nball); arb_init(n2);
    arb_init(q); arb_init(x0); arb_init(log0); arb_init(logn0);
    arb_init(logm0);
    arb_init(z); arb_init(one_minus_z); arb_init(delta1);
    arb_init(sigma1); arb_init(sigma1_lo); arb_init(y1); arb_init(kappa);
    arb_init(blo);
    arb_init(g_t1); arb_init(g_t2); arb_init(u1max); arb_init(pmax);
    arb_init(head); arb_init(term1); arb_init(term2); arb_init(cap_u);
    arb_init(smax);
    arb_init(eAB); arb_init(eC0); arb_init(emax); arb_init(tmin);
    arb_init(margin);
    arb_init(log3); arb_init(exponent); arb_init(powers3);
    arb_init(tmp); arb_init(tmp2); arb_init(tmp3); arb_init(logn);

    arb_zero(zero);
    arb_one(one);
    arb_set_ui(two, 2);
    arb_const_pi(pi, wp);

    /* Exact rational parameter identities (integer arithmetic). */
    report("exact candidate identity t0+y0^2/2 = 893927/5000000",
           129UL * 6250UL + 87677UL == 893927UL);
    report("exact t-box: t0 = tbox_lo < tbox_hi <= 1/4",
           129UL * 1250000UL == 161250000UL
           && 161250000UL < 161250001UL
           && 161250001UL * 4UL <= 1000000000UL);
    report("exact y0^2 identity 87677/2500000 = 350708/10^7",
           4UL * 87677UL == 350708UL);
    report("exact floor exceeds coarse budget: 791366/10^12 > 234/10^9",
           791366UL > 234000UL);

    /*
     * The complete rational t-interval as an Arb ball provably containing
     * both endpoints: the union of two balls that each contain their
     * exact rational endpoint.
     */
    set_q(tlo, 161250000, 1000000000UL);
    set_q(thi, 161250001, 1000000000UL);
    arb_union(t, tlo, thi, wp);

    set_q(y0, 87677, 2500000UL);
    arb_sqrt(y0, y0, wp);
    set_q(ymax, 271, 400UL);
    arb_sqrt(ymax, ymax, wp);

    arb_set_ui(nball, N0);
    arb_log(logn0, nball, wp);
    arb_mul(n2, nball, nball, wp);
    arb_div_ui(tmp, t, 16, wp);
    arb_sub(q, n2, tmp, wp);                     /* N0^2 - t/16 */
    arb_log(log0, q, wp);
    arb_mul(x0, pi, q, wp);
    arb_mul_ui(x0, x0, 4, wp);
    arb_set_ui(tmp, M0);
    arb_log(logm0, tmp, wp);

    /* z = t/(16 N0^2). */
    arb_mul_ui(tmp, n2, 16, wp);
    arb_div(z, t, tmp, wp);
    arb_sub(one_minus_z, one, z, wp);

    /* Domain gates for every denominator and log/sqrt argument. */
    report("domain: 0 < t/(16 N0^2) < 1 and 1 - t/(16 N0^2) > 0",
           arb_gt(z, zero) && arb_lt(z, one)
           && arb_gt(one_minus_z, zero));
    report("domain: x0 > 12, x0 > 6.66, x0 > 6",
           gt_q(x0, 12, 1) && gt_q(x0, 333, 50) && gt_q(x0, 6, 1));
    arb_sub(tmp, logn0, logm0, wp);
    report("domain: log N0 - log m0 > 0", arb_gt(tmp, zero));
    report("domain: N0 - 1/8 > 0", gt_q(nball, 1, 8));

    /*
     * delta1 = upper point of (t/4)(-log(1-z)) + t/(2 x0^2), over the
     * whole t-box.
     */
    arb_log(tmp, one_minus_z, wp);
    arb_neg(tmp, tmp);
    arb_mul(tmp, tmp, t, wp);
    arb_div_ui(tmp, tmp, 4, wp);
    arb_mul(tmp2, x0, x0, wp);
    arb_mul_ui(tmp2, tmp2, 2, wp);
    arb_div(tmp2, t, tmp2, wp);
    arb_add(tmp, tmp, tmp2, wp);
    upper_point(delta1, tmp);

    /* sigma1 = (1+y0)/2 + (t/2) log N0 - delta1. */
    arb_add(sigma1, one, y0, wp);
    arb_div_ui(sigma1, sigma1, 2, wp);
    arb_mul(tmp, t, logn0, wp);
    arb_div_ui(tmp, tmp, 2, wp);
    arb_add(sigma1, sigma1, tmp, wp);
    arb_sub(sigma1, sigma1, delta1, wp);
    lower_point(sigma1_lo, sigma1);

    /* Y1 = 1/50 - log0/2 + log N0/2. */
    set_q(y1, 1, 50);
    arb_div_ui(tmp, log0, 2, wp);
    arb_sub(y1, y1, tmp, wp);
    arb_div_ui(tmp, logn0, 2, wp);
    arb_add(y1, y1, tmp, wp);

    /* kappa = upper point of t/(2(x0-6)). */
    arb_sub_ui(tmp, x0, 6, wp);
    arb_mul_ui(tmp, tmp, 2, wp);
    arb_div(tmp, t, tmp, wp);
    upper_point(kappa, tmp);

    /* The twelve domain and sign conditions of the Proposition. */
    arb_mul(tmp, x0, x0, wp);
    arb_set_ui(tmp2, 8);
    arb_div(tmp, tmp2, tmp, wp);
    arb_mul_ui(tmp2, y0, 3, wp);
    report("gate G0_positive_part: 8/x0^2 < 3 y0", arb_lt(tmp, tmp2));
    report("gate sigma1_positive: sigma1 > 0", arb_gt(sigma1, zero));
    report("gate Y1_negative: Y1 < 0", arb_lt(y1, zero));
    report("gate kappa_domain: 0 < kappa < 1",
           arb_gt(kappa, zero) && arb_lt(kappa, one));
    arb_div(tmp, n2, q, wp);
    report("gate G2a_ratio: N0^2/(N0^2-t/16) > 1", arb_gt(tmp, one));
    report("gate U1_log_domain: log(N0^2-t/16) > 2", gt_q(log0, 2, 1));
    report("gate U2_logN: log N0 > 1/2", gt_q(logn0, 1, 2));
    arb_add(tmp, one, y0, wp);
    arb_div_ui(tmp, tmp, 2, wp);
    arb_sub(tmp, tmp, delta1, wp);
    report("gate U3a_tail_decrease: (1+y0)/2 - delta1 > 0",
           arb_gt(tmp, zero));
    report("gate Y_range (exact): 0 < y0^2 < ymax^2 <= 1",
           0UL < 87677UL
           && 87677UL * 400UL < 271UL * 2500000UL
           && 271UL <= 400UL);

    /* g_t1 = -(t/2) log m0 + 1/(log N0 - log m0). */
    arb_mul(g_t1, t, logm0, wp);
    arb_div_ui(g_t1, g_t1, 2, wp);
    arb_neg(g_t1, g_t1);
    arb_sub(tmp, logn0, logm0, wp);
    arb_inv(tmp, tmp, wp);
    arb_add(g_t1, g_t1, tmp, wp);

    /* g_t2 = (1-y0)/2 + delta1 - (t/2) log N0 + 1/(log N0 - log m0). */
    arb_sub(g_t2, one, y0, wp);
    arb_div_ui(g_t2, g_t2, 2, wp);
    arb_add(g_t2, g_t2, delta1, wp);
    arb_mul(tmp2, t, logn0, wp);
    arb_div_ui(tmp2, tmp2, 2, wp);
    arb_sub(g_t2, g_t2, tmp2, wp);
    arb_add(g_t2, g_t2, tmp, wp);

    report("gate U3b_first_endpoint: g_t1 < 0", arb_lt(g_t1, zero));
    report("gate U3c_second_endpoint: g_t2 < 0", arb_lt(g_t2, zero));
    report("gate U5_last_factor (exact): 3/10.50 < 1", 3UL * 2UL < 21UL);

    /* U1max = upper point of ((t^2/16) log0^2 + 0.626)/(x0 - 6.66). */
    arb_mul(tmp, t, t, wp);
    arb_div_ui(tmp, tmp, 16, wp);
    arb_mul(tmp2, log0, log0, wp);
    arb_mul(tmp, tmp, tmp2, wp);
    set_q(tmp2, 313, 500);                       /* 0.626 */
    arb_add(tmp, tmp, tmp2, wp);
    set_q(tmp2, 333, 50);                        /* 6.66 */
    arb_sub(tmp2, x0, tmp2, wp);
    arb_div(tmp, tmp, tmp2, wp);
    upper_point(u1max, tmp);

    /*
     * Pmax = upper point of
     * 1 + e^{1/50} (1-z)^{-1/2} exp(t log N0/(2(x0-6))).
     */
    set_q(tmp, 1, 50);                           /* 0.02 */
    arb_exp(tmp, tmp, wp);
    arb_rsqrt(tmp2, one_minus_z, wp);
    arb_mul(tmp, tmp, tmp2, wp);
    arb_mul(tmp2, t, logn0, wp);
    arb_sub_ui(tmp3, x0, 6, wp);
    arb_mul_ui(tmp3, tmp3, 2, wp);
    arb_div(tmp2, tmp2, tmp3, wp);
    arb_exp(tmp2, tmp2, wp);
    arb_mul(tmp, tmp, tmp2, wp);
    arb_add(tmp, tmp, one, wp);
    upper_point(pmax, tmp);

    /*
     * head = sum_{n=2}^{m0} exp((t/4) log(n)^2 - sigma1 log(n)), bounded
     * above occurrence-by-occurrence: t <= thi in the positive quadratic
     * term and sigma1 >= sigma1_lo in the subtracted term (log n > 0 is
     * gated below), exactly as the interval evaluation bounds it.
     */
    arb_zero(head);
    {
        int logn_positive = 1;
        for (n = 2; n <= M0; n++)
        {
            arb_set_ui(tmp, (ulong) n);
            arb_log(logn, tmp, wp);
            logn_positive = logn_positive && arb_is_positive(logn);
            arb_mul(tmp, logn, logn, wp);
            arb_mul(tmp, tmp, thi, wp);
            arb_div_ui(tmp, tmp, 4, wp);
            arb_mul(tmp2, sigma1_lo, logn, wp);
            arb_sub(tmp, tmp, tmp2, wp);
            upper_point(tmp, tmp);
            arb_exp(tmp, tmp, wp);
            arb_add(head, head, tmp, wp);
        }
        report("majorant domain: log n > 0 for all head terms, log m0 > 0",
               logn_positive && gt_q(logm0, 0, 1));
    }
    upper_point(head, head);

    /*
     * Endpoint caps: exp((1-sigma1) logu + (t/4) logu^2) (log N0-log m0),
     * at logu = log m0 and logu = log N0, bounded above with sigma1 >=
     * sigma1_lo (logu > 0 gated above and via U2) and t <= thi.
     */
    arb_sub(tmp3, logn0, logm0, wp);             /* log N0 - log m0 */

    arb_sub(tmp, one, sigma1_lo, wp);
    arb_mul(tmp, tmp, logm0, wp);
    arb_mul(tmp2, logm0, logm0, wp);
    arb_mul(tmp2, tmp2, thi, wp);
    arb_div_ui(tmp2, tmp2, 4, wp);
    arb_add(tmp, tmp, tmp2, wp);
    upper_point(tmp, tmp);
    arb_exp(tmp, tmp, wp);
    arb_mul(tmp, tmp, tmp3, wp);
    upper_point(term1, tmp);

    arb_sub(tmp, one, sigma1_lo, wp);
    arb_mul(tmp, tmp, logn0, wp);
    arb_mul(tmp2, logn0, logn0, wp);
    arb_mul(tmp2, tmp2, thi, wp);
    arb_div_ui(tmp2, tmp2, 4, wp);
    arb_add(tmp, tmp, tmp2, wp);
    upper_point(tmp, tmp);
    arb_exp(tmp, tmp, wp);
    arb_mul(tmp, tmp, tmp3, wp);
    upper_point(term2, tmp);

    max_upper_point(cap_u, term1, term2);

    /* Smax = upper point of 1 + head + cap. */
    arb_add(tmp, one, head, wp);
    arb_add(tmp, tmp, cap_u, wp);
    upper_point(smax, tmp);

    /* eAB = upper point of Pmax Smax (exp(U1max) - 1). */
    arb_expm1(tmp, u1max, wp);
    arb_mul(tmp, tmp, pmax, wp);
    arb_mul(tmp, tmp, smax, wp);
    upper_point(eAB, tmp);

    /*
     * eC0 = upper point of
     * exp(-(1+y0)/4 log0 - (t/16) log0^2
     *     + 1.24 (3^ymax + 3^-ymax)/(N0 - 1/8)
     *     + (3 sqrt(log0^2 + (pi/2)^2) + 10.50)/(x0 - 12)).
     */
    arb_add(tmp, one, y0, wp);
    arb_mul(tmp, tmp, log0, wp);
    arb_div_ui(tmp, tmp, 4, wp);
    arb_neg(exponent, tmp);

    /*
     * -(t/16) log0^2 <= -(tlo/16) lower(log0^2), valid because both
     * factors are certified positive; tlo is the exact rational left
     * endpoint and lower(log0^2) an exact dyadic directed endpoint.
     */
    arb_mul(tmp, log0, log0, wp);
    lower_point(blo, tmp);
    report("majorant domain: tlo > 0 and lower(log0^2) > 0",
           arb_is_positive(tlo) && arb_is_positive(blo));
    arb_mul(tmp, blo, tlo, wp);
    arb_div_ui(tmp, tmp, 16, wp);
    arb_sub(exponent, exponent, tmp, wp);

    arb_set_ui(tmp, 3);
    arb_log(log3, tmp, wp);
    arb_mul(tmp, ymax, log3, wp);
    arb_exp(tmp2, tmp, wp);
    arb_neg(tmp, tmp);
    arb_exp(tmp3, tmp, wp);
    arb_add(powers3, tmp2, tmp3, wp);
    set_q(tmp, 31, 25);                          /* 1.24 */
    arb_mul(tmp, tmp, powers3, wp);
    set_q(tmp2, 1, 8);                           /* 0.125 */
    arb_sub(tmp2, nball, tmp2, wp);
    arb_div(tmp, tmp, tmp2, wp);
    arb_add(exponent, exponent, tmp, wp);

    arb_mul(tmp, log0, log0, wp);
    arb_mul(tmp2, pi, pi, wp);
    arb_div_ui(tmp2, tmp2, 4, wp);
    arb_add(tmp, tmp, tmp2, wp);
    arb_sqrt(tmp, tmp, wp);
    arb_mul_ui(tmp, tmp, 3, wp);
    set_q(tmp2, 21, 2);                          /* 10.50 */
    arb_add(tmp, tmp, tmp2, wp);
    arb_sub_ui(tmp2, x0, 12, wp);
    arb_div(tmp, tmp, tmp2, wp);
    arb_add(exponent, exponent, tmp, wp);
    upper_point(exponent, exponent);
    arb_exp(tmp, exponent, wp);
    upper_point(eC0, tmp);

    /* E_max = upper point of eAB + eC0. */
    arb_add(tmp, eAB, eC0, wp);
    upper_point(emax, tmp);

    /* Two-sided regression corridors around the certified values. */
    report("eAB corridor 2.057e-12 < eAB < 2.058e-12",
           gt_q(eAB, 2057, 1000000000000000UL)
           && lt_q(eAB, 2058, 1000000000000000UL));
    report("eC0 corridor 2.33492848e-7 < eC0 < 2.33492849e-7",
           gt_q(eC0, 233492848, 1000000000000000UL)
           && lt_q(eC0, 233492849, 1000000000000000UL));
    report("Emax corridor 2.33494905e-7 < Emax < 2.33494906e-7",
           gt_q(emax, 233494905, 1000000000000000UL)
           && lt_q(emax, 233494906, 1000000000000000UL));

    /* The decisive Proposition 4.10 inequalities, against exact rationals. */
    report("decisive eAB < 206/10^14", lt_decimal(eAB, 206, 14));
    report("decisive eC0 < 233492848188649183/10^24",
           lt_decimal(eC0, 233492848188649183L, 24));
    report("decisive Emax < 233494905212337849/10^24",
           lt_decimal(emax, 233494905212337849L, 24));
    report("decisive coarse budget Emax < 234/10^9",
           lt_decimal(emax, 234, 9));

    /* The finite margin T_min - E_max, from the exact rational floor. */
    set_q(tmin, 791366, 1000000000000UL);
    arb_sub(margin, tmin, emax, wp);
    report("decisive finite margin Tmin - Emax > 0",
           arb_is_positive(margin));
    report("decisive binding floor Tmin - Emax > 557/10^9",
           gt_q(margin, 557, 1000000000UL));
    lower_point(margin, margin);

    puts("\nDirected Arb enclosures:");
    print_ball("delta1 upper point", delta1);
    print_ball("kappa upper point", kappa);
    print_ball("sigma1 enclosure", sigma1);
    print_ball("Y1 enclosure", y1);
    print_ball("g_t1 enclosure", g_t1);
    print_ball("g_t2 enclosure", g_t2);
    print_ball("U1max upper point", u1max);
    print_ball("Pmax upper point", pmax);
    print_ball("head upper point", head);
    print_ball("cap upper point", cap_u);
    print_ball("Smax upper point", smax);
    print_ball("eAB upper point", eAB);
    print_ball("eC0 upper point", eC0);
    print_ball("Emax upper point", emax);
    print_ball("Tmin-Emax lower point", margin);

    printf("\nTOTAL CHECKS: %d; FAILURES: %d\n", checks, failures);
    puts(failures == 0 ? "RESULT: ALL ARB PROP410 CHECKS PASS"
                       : "RESULT: ARB PROP410 CHECK FAILURE");

    arb_clear(zero); arb_clear(one); arb_clear(two); arb_clear(pi);
    arb_clear(t); arb_clear(tlo); arb_clear(thi);
    arb_clear(y0); arb_clear(ymax); arb_clear(nball); arb_clear(n2);
    arb_clear(q); arb_clear(x0); arb_clear(log0); arb_clear(logn0);
    arb_clear(logm0);
    arb_clear(z); arb_clear(one_minus_z); arb_clear(delta1);
    arb_clear(sigma1); arb_clear(sigma1_lo); arb_clear(y1); arb_clear(kappa);
    arb_clear(blo);
    arb_clear(g_t1); arb_clear(g_t2); arb_clear(u1max); arb_clear(pmax);
    arb_clear(head); arb_clear(term1); arb_clear(term2); arb_clear(cap_u);
    arb_clear(smax);
    arb_clear(eAB); arb_clear(eC0); arb_clear(emax); arb_clear(tmin);
    arb_clear(margin);
    arb_clear(log3); arb_clear(exponent); arb_clear(powers3);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(tmp3); arb_clear(logn);

    flint_cleanup();
    return failures == 0 ? 0 : 1;
}
