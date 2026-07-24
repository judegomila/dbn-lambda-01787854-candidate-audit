/*
   Uniform numerical upper bound for the displayed error formulas (20)--(24)
   of Polymath 15, arXiv:1904.12438v2, on

       x in [6000000185827, 6000000185828],
       y in [0.1809, 1],
       t in [0, 0.16125].

   This program certifies the evaluation/majorization of the displayed
   formulas.  It does not by itself extend the stated theorem domain
   0 < t <= 1/2 to the endpoint t=0; that analytic endpoint must be supplied
   separately (for example by a proved continuous extension).
*/

#include <stdio.h>
#include "arb.h"

static int
strict_lt(const char *name, const arb_t a, const arb_t b)
{
    int ok = arb_lt(a, b);
    printf("[%s] %s\n", ok ? "PASS" : "FAIL", name);
    return ok;
}

static int
strict_positive(const char *name, const arb_t a)
{
    int ok = arb_is_positive(a);
    printf("[%s] %s\n", ok ? "PASS" : "FAIL", name);
    return ok;
}

static void
print_ball(const char *name, const arb_t x)
{
    printf("%s = ", name);
    arb_printn(x, 40, ARB_STR_MORE);
    printf("\n");
}

/* N(x,t) = floor(sqrt(x/(4*pi) + t/16)). */
static int
compute_exact_N(slong *out, const arb_t x, const arb_t t, slong prec)
{
    arb_t u, v, pi;
    arb_init(u);
    arb_init(v);
    arb_init(pi);
    arb_const_pi(pi, prec);
    arb_mul_2exp_si(pi, pi, 2);
    arb_div(u, x, pi, prec);
    arb_mul_2exp_si(v, t, -4);
    arb_add(u, u, v, prec);
    arb_sqrt(u, u, prec);
    arb_floor(u, u, prec);
    if (!arb_is_int(u))
    {
        arb_clear(u);
        arb_clear(v);
        arb_clear(pi);
        return 0;
    }
    *out = arf_get_si(arb_midref(u), ARF_RND_DOWN);
    arb_clear(u);
    arb_clear(v);
    arb_clear(pi);
    return 1;
}

int
main(void)
{
    const slong prec = 256;
    int ok = 1;
    slong nlo, nhi;

    arb_t X, Xhi, T, ymin, one, fourpi, pi;
    arb_t N, N2, qmin, qmax, Lmin, Lmax, lnN, tmp, tmp2;
    arb_t delta, a, aeff, one_minus_a, Smax;
    arb_t kappa_factor, Pmax, umax, eAB;
    arb_t ec_factor1, ec_exp2, ec_exp3, eC0, total, epsilon;

    arb_init(X); arb_init(Xhi); arb_init(T); arb_init(ymin);
    arb_init(one); arb_init(fourpi); arb_init(pi);
    arb_init(N); arb_init(N2); arb_init(qmin); arb_init(qmax);
    arb_init(Lmin); arb_init(Lmax); arb_init(lnN);
    arb_init(tmp); arb_init(tmp2); arb_init(delta); arb_init(a);
    arb_init(aeff); arb_init(one_minus_a); arb_init(Smax);
    arb_init(kappa_factor); arb_init(Pmax); arb_init(umax);
    arb_init(eAB); arb_init(ec_factor1); arb_init(ec_exp2);
    arb_init(ec_exp3); arb_init(eC0); arb_init(total);
    arb_init(epsilon);

    arb_set_si(X, 6000000185827L);
    arb_add_ui(Xhi, X, 1, prec);
    arb_set_si(T, 129);
    arb_div_ui(T, T, 800, prec);
    arb_set_si(ymin, 1809);
    arb_div_ui(ymin, ymin, 10000, prec);
    arb_one(one);
    arb_const_pi(pi, prec);
    arb_mul_2exp_si(fourpi, pi, 2);
    arb_set_ui(N, 690988);

    arb_zero(tmp);
    if (!compute_exact_N(&nlo, X, tmp, prec))
        nlo = -1;
    if (!compute_exact_N(&nhi, Xhi, T, prec))
        nhi = -1;
    printf("[%s] N is 690988 at both monotone slab corners (%ld,%ld)\n",
           (nlo == 690988 && nhi == 690988) ? "PASS" : "FAIL", nlo, nhi);
    ok &= (nlo == 690988 && nhi == 690988);

    arb_div(qmin, X, fourpi, prec);
    arb_div(qmax, Xhi, fourpi, prec);
    arb_log(Lmin, qmin, prec);
    arb_log(Lmax, qmax, prec);
    arb_log(lnN, N, prec);
    arb_mul(N2, N, N, prec);

    ok &= strict_lt("N^2 < X/(4*pi), hence n^2/(x/(4*pi)) < 1",
                    N2, qmin);
    arb_mul_2exp_si(tmp, lnN, 1);
    ok &= strict_lt("2*log(N) < log(X/(4*pi))", tmp, Lmin);

    /*
       res >= a + (t/4)Lmin - delta, where
       a=(1+ymin)/2 and
       delta <= T(1+8/X^2)/(2X^2).

       For n <= N, log(n)^2-Lmin*log(n) <= 0.  Therefore
       exp((t/4)log(n)^2)/n^res <= n^(-a+delta).
    */
    arb_add(a, one, ymin, prec);
    arb_mul_2exp_si(a, a, -1);

    arb_mul(tmp, X, X, prec);              /* X^2 */
    arb_inv(tmp2, tmp, prec);              /* 1/X^2 */
    arb_mul_ui(delta, tmp2, 8, prec);
    arb_add(delta, delta, one, prec);       /* 1 + 8/X^2 */
    arb_mul(delta, delta, T, prec);
    arb_mul(delta, delta, tmp2, prec);
    arb_mul_2exp_si(delta, delta, -1);      /* delta */
    arb_sub(aeff, a, delta, prec);
    ok &= strict_positive("a_eff=(1+ymin)/2-delta is positive", aeff);
    ok &= strict_lt("a_eff < 1", aeff, one);

    /*
       Sum_{n=1}^N n^(-a_eff)
       <= 1 + integral_1^N x^(-a_eff) dx
       = 1 + (N^(1-a_eff)-1)/(1-a_eff).
    */
    arb_sub(one_minus_a, one, aeff, prec);
    arb_pow(tmp, N, one_minus_a, prec);
    arb_sub(tmp, tmp, one, prec);
    arb_div(tmp, tmp, one_minus_a, prec);
    arb_add(Smax, one, tmp, prec);

    /*
       gamma*n^y <= exp(.02*y)*(n^2/q)^(y/2) <= exp(.02).
       N^kappa <= exp(T*log(N)/(2*(X-6))).
    */
    arb_sub_ui(tmp, X, 6, prec);
    arb_mul(tmp2, T, lnN, prec);
    arb_div(tmp2, tmp2, tmp, prec);
    arb_mul_2exp_si(tmp2, tmp2, -1);
    arb_exp(kappa_factor, tmp2, prec);
    arb_set_str(tmp, "0.02", prec);
    arb_exp(tmp, tmp, prec);
    arb_mul(Pmax, tmp, kappa_factor, prec);
    arb_add(Pmax, Pmax, one, prec);

    /*
       Since 0 <= log(q/n^2) <= Lmax,
       u_n <= ((T^2/16)Lmax^2 + .626)/(X-6.66).
    */
    arb_mul(tmp, T, T, prec);
    arb_mul_2exp_si(tmp, tmp, -4);
    arb_mul(tmp2, Lmax, Lmax, prec);
    arb_mul(tmp, tmp, tmp2, prec);
    arb_set_str(tmp2, "0.626", prec);
    arb_add(tmp, tmp, tmp2, prec);
    arb_set_str(tmp2, "6.66", prec);
    arb_sub(tmp2, X, tmp2, prec);
    arb_div(umax, tmp, tmp2, prec);

    arb_exp(tmp, umax, prec);
    arb_sub(tmp, tmp, one, prec);
    arb_mul(eAB, Pmax, Smax, prec);
    arb_mul(eAB, eAB, tmp, prec);

    /*
       eC0:
       - first factor maximized at x=X,y=ymin;
       - exp(-(t/16)L^2) <= 1;
       - 3^y+3^-y is increasing for y >= 0, so use y=1;
       - use N=690988;
       - separately maximize the last numerator at X+1 and minimize its
         denominator at X.  This avoids a monotonicity assumption.
    */
    arb_add(tmp, one, ymin, prec);
    arb_mul_2exp_si(tmp, tmp, -2);
    arb_neg(tmp, tmp);
    arb_pow(ec_factor1, qmin, tmp, prec);

    arb_set_str(tmp, "1.24", prec);
    arb_set_ui(tmp2, 10);
    arb_div_ui(tmp2, tmp2, 3, prec);        /* 3 + 1/3 = 10/3 */
    arb_mul(ec_exp2, tmp, tmp2, prec);
    arb_set_str(tmp2, "0.125", prec);
    arb_sub(tmp2, N, tmp2, prec);
    arb_div(ec_exp2, ec_exp2, tmp2, prec);

    arb_mul(tmp, Lmax, Lmax, prec);
    arb_mul_2exp_si(tmp2, pi, -1);
    arb_mul(tmp2, tmp2, tmp2, prec);
    arb_add(tmp, tmp, tmp2, prec);
    arb_sqrt(tmp, tmp, prec);
    arb_mul_ui(tmp, tmp, 3, prec);
    arb_set_str(tmp2, "10.44", prec);
    arb_add(tmp, tmp, tmp2, prec);
    arb_sub_ui(tmp2, X, 12, prec);
    arb_div(ec_exp3, tmp, tmp2, prec);

    arb_add(tmp, ec_exp2, ec_exp3, prec);
    arb_exp(tmp, tmp, prec);
    arb_mul(eC0, ec_factor1, tmp, prec);
    arb_add(total, eAB, eC0, prec);
    arb_set_str(epsilon, "0.00125", prec);

    print_ball("a_eff", aeff);
    print_ball("sum core upper", Smax);
    print_ball("prefactor upper", Pmax);
    print_ball("u_n upper", umax);
    print_ball("e_A+e_B upper", eAB);
    print_ball("e_C0 upper", eC0);
    print_ball("uniform displayed-formula total upper", total);
    print_ball("winding allowance", epsilon);

    ok &= strict_lt("uniform displayed-formula total < 0.00125",
                    total, epsilon);

    printf("%s\n", ok
        ? "RESULT: UNIFORM NUMERICAL ERROR-FORMULA BOUND CERTIFIED"
        : "RESULT: FAIL");
    printf("SCOPE NOTE: analytic justification at t=0 remains external.\n");

    arb_clear(X); arb_clear(Xhi); arb_clear(T); arb_clear(ymin);
    arb_clear(one); arb_clear(fourpi); arb_clear(pi);
    arb_clear(N); arb_clear(N2); arb_clear(qmin); arb_clear(qmax);
    arb_clear(Lmin); arb_clear(Lmax); arb_clear(lnN);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(delta); arb_clear(a);
    arb_clear(aeff); arb_clear(one_minus_a); arb_clear(Smax);
    arb_clear(kappa_factor); arb_clear(Pmax); arb_clear(umax);
    arb_clear(eAB); arb_clear(ec_factor1); arb_clear(ec_exp2);
    arb_clear(ec_exp3); arb_clear(eC0); arb_clear(total);
    arb_clear(epsilon);

    flint_cleanup();
    return ok ? 0 : 1;
}
