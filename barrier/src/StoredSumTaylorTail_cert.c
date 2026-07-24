#include <stdio.h>
#include <stdlib.h>
#include <flint/flint.h>
#include <flint/arb.h>
#include <flint/acb.h>

/* Independent certificate for the 62 x 62 stored-sum truncation used at
   X=6000000185827.  This does not use numerical quadrature: it sums a
   rigorous termwise exponential-tail majorant over n=1,...,N. */

static void
set_interval_str(arb_t z, const char *lo, const char *hi, slong prec)
{
    arb_t a, b;
    arb_init(a); arb_init(b);
    if (arb_set_str(a, lo, prec) || arb_set_str(b, hi, prec))
        flint_abort();
    arb_union(z, a, b, prec);
    arb_clear(a); arb_clear(b);
}

static void
alpha1(acb_t z, const acb_t s, slong prec)
{
    acb_t a, b;
    arb_t twopi;
    acb_init(a); acb_init(b); arb_init(twopi);

    acb_mul_2exp_si(a, s, 1);       /* 2s */
    acb_inv(a, a, prec);            /* 1/(2s) */
    acb_sub_si(b, s, 1, prec);
    acb_inv(b, b, prec);            /* 1/(s-1) */
    acb_add(z, a, b, prec);

    arb_const_pi(twopi, prec);
    arb_mul_2exp_si(twopi, twopi, 1);
    acb_div_arb(b, s, twopi, prec);
    acb_log(b, b, prec);
    acb_mul_2exp_si(b, b, -1);
    acb_add(z, z, b, prec);

    acb_clear(a); acb_clear(b); arb_clear(twopi);
}

static void
logabs_H01(arb_t z, const acb_t s, slong prec)
{
    acb_t d, q, l;
    arb_t a, b, pi;
    acb_init(d); acb_init(q); acb_init(l);
    arb_init(a); arb_init(b); arb_init(pi);
    arb_const_pi(pi, prec);

    /* log(sqrt(2*pi)/2) + log|s| + log|s-1| */
    arb_mul_2exp_si(a, pi, 1); arb_log(a, a, prec); arb_mul_2exp_si(z, a, -1);
    arb_set_ui(a, 2); arb_log(a, a, prec); arb_sub(z, z, a, prec);
    acb_abs(a, s, prec); arb_log(a, a, prec); arb_add(z, z, a, prec);
    acb_sub_ui(q, s, 1, prec); acb_abs(a, q, prec); arb_log(a, a, prec); arb_add(z, z, a, prec);

    /* Re(-s log(pi)/2). */
    acb_get_real(a, s); arb_log(b, pi, prec); arb_mul(a, a, b, prec);
    arb_mul_2exp_si(a, a, -1); arb_sub(z, z, a, prec);

    /* Re((s/2-1/2) Log(s/2)-s/2). */
    acb_mul_2exp_si(d, s, -1);
    acb_log(l, d, prec);
    acb_sub_ui(q, s, 1, prec); acb_mul_2exp_si(q, q, -1);
    acb_mul(q, q, l, prec); acb_sub(q, q, d, prec);
    acb_get_real(a, q); arb_add(z, z, a, prec);

    acb_clear(d); acb_clear(q); acb_clear(l);
    arb_clear(a); arb_clear(b); arb_clear(pi);
}

static void
assert_lt_str(const arb_t x, const char *bound, slong prec, const char *name)
{
    arb_t b;
    arb_init(b);
    if (arb_set_str(b, bound, prec) || !arb_lt(x, b)) {
        fprintf(stderr, "%s failed: ", name);
        arb_printn(x, 30, 0); fputc('\n', stderr);
        flint_abort();
    }
    arb_clear(b);
}

int
main(void)
{
    const slong prec = 192;
    const ulong N = 690988;
    const ulong first_omitted = 62;
    ulong n;

    arb_t X, x, y, logn0, n0, t0, pi, tmp, tmp2, re, im, dabsre,
          dabsim, wr, wi, wmod, afaclog, afac, coeff, sqrtn0,
          prefactors, L, A, B, fac, IA, IB, expA, expB, term, total,
          nn, half, one, ratio;
    acb_t s, u, al, D, als, alu, q;

    arb_init(X); arb_init(x); arb_init(y); arb_init(logn0); arb_init(n0);
    arb_init(t0); arb_init(pi); arb_init(tmp); arb_init(tmp2); arb_init(re);
    arb_init(im); arb_init(dabsre); arb_init(dabsim); arb_init(wr);
    arb_init(wi); arb_init(wmod); arb_init(afaclog); arb_init(afac);
    arb_init(coeff); arb_init(sqrtn0); arb_init(prefactors); arb_init(L);
    arb_init(A); arb_init(B); arb_init(fac); arb_init(IA); arb_init(IB);
    arb_init(expA); arb_init(expB); arb_init(term); arb_init(total);
    arb_init(nn); arb_init(half); arb_init(one); arb_init(ratio);
    acb_init(s); acb_init(u); acb_init(al); acb_init(D);
    acb_init(als); acb_init(alu); acb_init(q);

    arb_one(one);
    arb_one(half); arb_mul_2exp_si(half, half, -1);
    arb_set_ui(n0, N); arb_mul_2exp_si(n0, n0, -1);
    arb_log(logn0, n0, prec);
    arb_sqrt(sqrtn0, n0, prec);
    arb_set_str(t0, "0.1809", prec);
    arb_const_pi(pi, prec);

    /* Uniform .66 hypothesis.  Here s=(1-y+i*x)/2, with
       x in [X,X+1] and y in [.1809,1].  Both alpha arguments used by
       Tloop are checked in one box. */
    set_interval_str(x, "6000000185827", "6000000185828", prec);
    set_interval_str(y, "0.1809", "1", prec);
    arb_neg(re, y); arb_add_ui(re, re, 1, prec); arb_mul_2exp_si(re, re, -1);
    arb_mul_2exp_si(im, x, -1);
    acb_set_arb_arb(s, re, im);

    /* First u=1-s, then u=conj(s).  D=log(n0)-alpha1(u). */
    for (int which = 0; which < 2; which++) {
        if (which == 0) { acb_neg(u, s); acb_add_ui(u, u, 1, prec); }
        else             acb_conj(u, s);
        alpha1(al, u, prec);
        acb_neg(D, al); acb_add_arb(D, D, logn0, prec);
        acb_get_real(re, D); arb_abs(dabsre, re);
        acb_get_imag(im, D); arb_abs(dabsim, im);
        printf("D%d abs-real upper = ", which + 1); arb_printn(dabsre, 25, 0); putchar('\n');
        printf("D%d abs-imag upper = ", which + 1); arb_printn(dabsim, 25, 0); putchar('\n');
        assert_lt_str(dabsre, "0.694", prec, "abs Re(log(n0)-alpha)");
        assert_lt_str(dabsim, "0.7855", prec, "abs Im(log(n0)-alpha)");
    }

    /* From |Re base|<=1/2, |Im base|<=1/4 and the preceding D bounds,
       |w| <= hypot(1/2+t0*.694/2, 1/4+t0*.7855/2) < .66. */
    arb_set_str(wr, "0.694", prec); arb_mul(wr, wr, t0, prec);
    arb_mul_2exp_si(wr, wr, -1); arb_add(wr, wr, half, prec);
    arb_set_str(wi, "0.7855", prec); arb_mul(wi, wi, t0, prec);
    arb_mul_2exp_si(wi, wi, -1);
    arb_set_ui(tmp, 1); arb_mul_2exp_si(tmp, tmp, -2); arb_add(wi, wi, tmp, prec);
    arb_hypot(wmod, wr, wi, prec);
    assert_lt_str(wmod, "0.66", prec, "uniform expansion parameter");

    /* The same D bound gives Re(alpha) >= log(n0)-.694 > log(n0)/2. */
    arb_set_str(tmp, "0.694", prec); arb_sub(tmp, logn0, tmp, prec);
    arb_mul_2exp_si(tmp2, logn0, -1);
    if (!arb_gt(tmp, tmp2)) flint_abort();

    /* Direct interval check of the exact complex afac from Tloop lines
       465--475, performed in log modulus to avoid huge irrelevant phases.
       Mild subdivision suppresses dependency over the y interval. */
    {
        const ulong nx = 256, ny = 128;
        ulong ix, iy;
        arb_t xlo, xhi, ylo, yhi, zero, exactmax;
        arb_init(xlo); arb_init(xhi); arb_init(ylo); arb_init(yhi);
        arb_init(zero); arb_init(exactmax); arb_zero(zero); arb_zero(exactmax);
        for (ix = 0; ix < nx; ix++) for (iy = 0; iy < ny; iy++) {
            arb_set_str(xlo, "6000000185827", prec);
            arb_set_ui(tmp, ix); arb_div_ui(tmp, tmp, nx, prec); arb_add(xlo, xlo, tmp, prec);
            arb_set_str(xhi, "6000000185827", prec);
            arb_set_ui(tmp, ix + 1); arb_div_ui(tmp, tmp, nx, prec); arb_add(xhi, xhi, tmp, prec);
            arb_union(x, xlo, xhi, prec);

            arb_set_ui(ylo, 1809); arb_set_ui(tmp, 8191 * iy);
            arb_div_ui(tmp, tmp, 10000 * ny, prec); arb_div_ui(ylo, ylo, 10000, prec);
            arb_add(ylo, ylo, tmp, prec);
            arb_set_ui(yhi, 1809); arb_set_ui(tmp, 8191 * (iy + 1));
            arb_div_ui(tmp, tmp, 10000 * ny, prec); arb_div_ui(yhi, yhi, 10000, prec);
            arb_add(yhi, yhi, tmp, prec);
            arb_union(y, ylo, yhi, prec);

            arb_neg(re, y); arb_add_ui(re, re, 1, prec); arb_mul_2exp_si(re, re, -1);
            arb_mul_2exp_si(im, x, -1); acb_set_arb_arb(s, re, im);
            alpha1(als, s, prec); acb_mul_2exp_si(als, als, -1);
            acb_neg(u, s); acb_add_ui(u, u, 1, prec);
            alpha1(alu, u, prec); acb_mul_2exp_si(alu, alu, -1);
            acb_mul(q, als, als, prec); acb_mul(D, alu, alu, prec); acb_sub(q, q, D, prec);
            acb_get_real(re, q); arb_max(re, re, zero, prec); arb_mul(re, re, t0, prec);
            logabs_H01(tmp, s, prec); logabs_H01(tmp2, u, prec);
            arb_sub(tmp, tmp, tmp2, prec); arb_add(tmp, tmp, re, prec);
            if (ix == 0 && iy == 0) { printf("first log-afac cell = "); arb_printn(tmp, 30, 0); putchar('\n'); }
            arb_exp(tmp, tmp, prec);
            if (ix == 0 && iy == 0) { printf("first exact-afac cell = "); arb_printn(tmp, 30, 0); putchar('\n'); }
            assert_lt_str(tmp, "0.089", prec, "exact afac modulus cell");
            arb_max(exactmax, exactmax, tmp, prec);
        }
        printf("exact afac modulus upper = "); arb_printn(exactmax, 30, 0); putchar('\n');
        arb_clear(xlo); arb_clear(xhi); arb_clear(ylo); arb_clear(yhi);
        arb_clear(zero); arb_clear(exactmax);
    }

    /* The implemented gamma/afac bound is
       exp(.02*y)*(x/(4*pi))^(-y/2)*N^(t*y/(2*(x-6))).
       Its log is y times a negative coefficient.  It decreases in x,
       increases in t, and therefore is maximal at X,y0,t0. */
    arb_set_str(X, "6000000185827", prec);
    arb_div_ui(coeff, one, 50, prec);                 /* .02 */
    arb_mul_2exp_si(tmp, pi, 2);                      /* 4*pi */
    arb_div(tmp, X, tmp, prec); arb_log(tmp, tmp, prec);
    arb_mul_2exp_si(tmp, tmp, -1); arb_sub(coeff, coeff, tmp, prec);
    arb_set_ui(tmp, N); arb_log(tmp, tmp, prec); arb_mul(tmp, tmp, t0, prec);
    arb_sub_ui(tmp2, X, 6, prec); arb_div(tmp, tmp, tmp2, prec);
    arb_mul_2exp_si(tmp, tmp, -1); arb_add(coeff, coeff, tmp, prec);
    if (!arb_is_negative(coeff)) flint_abort();
    arb_set_str(tmp, "0.1809", prec); arb_mul(afaclog, coeff, tmp, prec);
    arb_exp(afac, afaclog, prec);
    assert_lt_str(afac, "0.089", prec, "afac upper bound");

    /* Re(alpha)>log(n0)/2 follows from the checked D real bound.  Hence
       the B outer prefactor is <=1, and the A outer prefactor is at most
       afac*sqrt(n0).  Check their sum is below the historic sqrt(n0)
       prefactor used by StoredSumSinglematv1.c. */
    arb_set_str(tmp, "0.089", prec);
    arb_mul(prefactors, tmp, sqrtn0, prec); arb_add_ui(prefactors, prefactors, 1, prec);
    if (!arb_lt(prefactors, sqrtn0)) flint_abort();

    /* Rigorous direct finite sum.  Let A=.66*|log(n/n0)| and
       B=.2*log(n/n0)^2/4.  For m=62, tails are bounded geometrically by
       A^m/m!/(1-A/(m+1)) and B^m/m!/(1-B/(m+1)).  The rectangular
       product remainder is <= exp(B)*IA + exp(A)*IB. */
    arb_fac_ui(fac, first_omitted, prec);
    arb_zero(total);
    for (n = 1; n <= N; n++) {
        arb_set_ui(nn, n); arb_div(L, nn, n0, prec); arb_log(L, L, prec); arb_abs(L, L);

        arb_set_str(A, "0.66", prec); arb_mul(A, A, L, prec);
        arb_mul(B, L, L, prec); arb_mul_2exp_si(B, B, -2);
        arb_div_ui(B, B, 5, prec);                    /* multiply by .2 */

        arb_pow_ui(IA, A, first_omitted, prec); arb_div(IA, IA, fac, prec);
        arb_div_ui(ratio, A, first_omitted + 1, prec); arb_sub(tmp, one, ratio, prec);
        arb_div(IA, IA, tmp, prec);

        arb_pow_ui(IB, B, first_omitted, prec); arb_div(IB, IB, fac, prec);
        arb_div_ui(ratio, B, first_omitted + 1, prec); arb_sub(tmp, one, ratio, prec);
        arb_div(IB, IB, tmp, prec);

        arb_exp(expA, A, prec); arb_exp(expB, B, prec);
        arb_mul(term, expB, IA, prec); arb_mul(tmp, expA, IB, prec);
        arb_add(term, term, tmp, prec);
        arb_sqrt(tmp, nn, prec); arb_div(term, term, tmp, prec);
        arb_add(total, total, term, prec);
    }
    arb_mul(total, total, sqrtn0, prec);
    assert_lt_str(total, "1e-20", prec, "complete Taylor truncation");

    printf("uniform |w| upper = "); arb_printn(wmod, 30, 0); putchar('\n');
    printf("afac upper = "); arb_printn(afac, 30, 0); putchar('\n');
    printf("combined outer prefactors upper = "); arb_printn(prefactors, 30, 0); putchar('\n');
    printf("sqrt(n0) = "); arb_printn(sqrtn0, 30, 0); putchar('\n');
    printf("Taylor truncation upper = "); arb_printn(total, 30, 0); putchar('\n');

    flint_cleanup();
    return EXIT_SUCCESS;
}
