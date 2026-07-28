/*
    Copyright (C) 2018 Association des collaborateurs de D.H.J Polymath
 
    This is free software: you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License (LGPL) as published
    by the Free Software Foundation; either version 2.1 of the License, or
    (at your option) any later version.  See <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
#include "acb_poly.h"
#include "acb_mat.h"
#include "acb_calc.h"
#include "arb_mat.h"
#include "flint/profiler.h"

slong get_N(const arb_t t, const arb_t x, slong prec);

#define DERIVATIVE_HEAD 16

static slong ddz_analytic_calls = 0;
static slong ddt_analytic_calls = 0;

// prepare the function as integrand for the integral
int
f_ddzbound(acb_ptr res, const acb_t z, void *param, slong order, slong prec)
{
    acb_t a, b, c, Nu, logNu, exponent, y_acb;
    int analytic;
    arb_ptr Narb, y, x, t, tdiv4divxmin6, afac, const1, estinit;

    if (order > 1)
    {
        fprintf(stderr, "FAIL: unsupported spatial-integrand Taylor order.\n");
        flint_abort();
    }
    analytic = (order != 0);
    if (analytic)
        ddz_analytic_calls++;

    acb_init(a);
    acb_init(b);
    acb_init(c);
    acb_init(Nu);
    acb_init(logNu);
    acb_init(exponent);
    acb_init(y_acb);

    Narb = ((arb_ptr *)(param))[0];
    y = ((arb_ptr *)(param))[1];
    x = ((arb_ptr *)(param))[2];
    t = ((arb_ptr *)(param))[3];
    tdiv4divxmin6 = ((arb_ptr *)(param))[4];
    afac = ((arb_ptr *)(param))[5];
    const1 = ((arb_ptr *)(param))[6];
    estinit = ((arb_ptr *)(param))[7];

    /* Keep the quadrature callback genuinely holomorphic in z.
       For order=1, the analytic variants fail with a nonfinite result if
       a complex integration ball touches the logarithm branch cut. */
    acb_mul_arb(Nu, z, Narb, prec);
    acb_log_analytic(logNu, Nu, analytic, prec);
    acb_set_arb(y_acb, y);

    //establish the integrand
    acb_pow_analytic(a, Nu, y_acb, analytic, prec);
    acb_mul_arb(b, a, afac, prec);
    acb_add_si(b, b, 1, prec);
    acb_mul_arb(b, b, tdiv4divxmin6, prec);
    acb_one(c);
    acb_mul_2exp_si(c, c, -1);
    acb_add(b, b, c, prec);
    acb_mul(b, logNu, b, prec);
    acb_mul_arb(c, a, estinit, prec);
    acb_add(c, b, c, prec);

    acb_neg(exponent, y_acb);
    acb_sub_si(exponent, exponent, 1, prec);
    acb_mul_2exp_si(exponent, exponent, -1);
    acb_mul_2exp_si(b, logNu, -2);
    acb_sub_arb(b, b, const1, prec);
    acb_mul_arb(b, b, t, prec);
    acb_add(exponent, exponent, b, prec);
    acb_pow_analytic(a, Nu, exponent, analytic, prec);
    acb_mul(res, c, a, prec);

    acb_clear(a);
    acb_clear(b);
    acb_clear(c);
    acb_clear(Nu);
    acb_clear(logNu);
    acb_clear(exponent);
    acb_clear(y_acb);

    return 0;
}

void
generate_ddzbound(arb_t esta, const arb_t x, const arb_t y,
                  const arb_t x_upper, const arb_t y_upper,
                  const arb_t t, arb_t Narb, arb_t afac, arb_t const1,
                  arb_t tdiv4divxmin6, slong prec)

{  
    acb_t tmp, ai, bi, est;
    acb_init(ai);
    acb_init(bi);
    acb_init(tmp);
    acb_init(est);

    arb_t a, b, c, d, e, estinit, pi;
    arb_init(a);
    arb_init(b);
    arb_init(c);
    arb_init(d);
    arb_init(e);
    arb_init(estinit);
    arb_init(pi);
    arb_const_pi(pi, prec);    

    slong goal, head_n;

    //estinit
    /*
       The Lemma 8.4 logarithmic factor

           log(|1+y+i*x|/(4*pi)) + pi + 3/x

       is not maximized by substituting (x,y)=(X,y0) in every
       occurrence.  Use the upper spatial endpoints in the increasing
       modulus and the lower x endpoint in the decreasing reciprocal.
       The remaining y dependence is handled by the explicit A-core
       monotonicity gate in abbeff_t_loop.
    */
    arb_add_si(b, y_upper, 1, prec);
    acb_set_arb_arb(tmp, b, x_upper);
    acb_abs(b, tmp, prec);
    arb_div(b, b, pi, prec);
    arb_mul_2exp_si(b, b, -2);
    arb_log(b, b, prec); 
    arb_add(b, b, pi, prec); 
    arb_set_si(c, 3);
    arb_div(c, c, x, prec);
    arb_add(b, b, c, prec);
    arb_mul(b, b, afac, prec);
    arb_one(d);
    arb_mul_2exp_si(d, d, -1);
    arb_add(d, tdiv4divxmin6, d, prec);
    arb_mul(estinit, b, d, prec);

    //evaluate the integral
    acb_calc_integrate_opt_t options;
    acb_calc_integrate_opt_init(options);

    mag_t tol;
    mag_init(tol);

    goal = prec;
    mag_set_ui_2exp_si(tol, 1, -prec);

    /* The derivative majorant is a discrete sum, not an integral.
       Its continuous summand is certified decreasing only from
       DERIVATIVE_HEAD onward.  Integrate the decreasing tail and add
       the complete finite head exactly below. */
    arb_set_si(a, DERIVATIVE_HEAD);
    arb_div(a, a, Narb, prec);
    arb_zero(b);
    acb_set_arb_arb(ai, a, b);
    arb_one(a);
    acb_set_arb_arb(bi, a, b);

    void *param[8];

    param[0] = (void *) Narb;
    param[1] = (void *) y;
    param[2] = (void *) x;
    param[3] = (void *) t;
    param[4] = (void *) tdiv4divxmin6;
    param[5] = (void *) afac;
    param[6] = (void *) const1;
    param[7] = (void *) estinit;

    ddz_analytic_calls = 0;
    if (acb_calc_integrate(est, f_ddzbound, param, ai, bi, goal, tol, NULL, prec) != 0)
    {
        fprintf(stderr, "FAIL: spatial-derivative quadrature did not converge.\n");
        flint_abort();
    }
    if (ddz_analytic_calls == 0)
    {
        fprintf(stderr, "FAIL: spatial quadrature never requested an analytic enclosure.\n");
        flint_abort();
    }
    acb_mul_arb(est, est, Narb, prec);
    for (head_n = 1; head_n <= DERIVATIVE_HEAD; head_n++)
    {
        arb_set_si(a, head_n);
        arb_div(a, a, Narb, prec);
        arb_zero(b);
        acb_set_arb_arb(ai, a, b);
        if (f_ddzbound(tmp, ai, param, 0, prec) != 0)
        {
            fprintf(stderr, "FAIL: spatial-derivative head evaluation failed.\n");
            flint_abort();
        }
        acb_add(est, est, tmp, prec);
    }
    acb_abs(esta, est, prec);

    mag_clear(tol);

    acb_clear(tmp);
    acb_clear(ai);
    acb_clear(bi);
    acb_clear(est);

    arb_clear(a);
    arb_clear(b);
    arb_clear(c);
    arb_clear(d);
    arb_clear(e);
    arb_clear(estinit);
    arb_clear(pi);
}

// prepare the function as integrand for the integral
int
f_ddtbound(acb_ptr res, const acb_t z, void *param, slong order, slong prec)
{
    acb_t a, b, c, d, Nu, logNu, exponent, y_acb;
    int analytic;
    arb_ptr Narb, y, t, afac, const1, const2, estinit;

    if (order > 1)
    {
        fprintf(stderr, "FAIL: unsupported time-integrand Taylor order.\n");
        flint_abort();
    }
    analytic = (order != 0);
    if (analytic)
        ddt_analytic_calls++;

    acb_init(a);
    acb_init(b);
    acb_init(c);
    acb_init(d);
    acb_init(Nu);
    acb_init(logNu);
    acb_init(exponent);
    acb_init(y_acb);

    Narb = ((arb_ptr *)(param))[0];
    y = ((arb_ptr *)(param))[1];
    t = ((arb_ptr *)(param))[2];
    afac = ((arb_ptr *)(param))[3];
    const1 = ((arb_ptr *)(param))[4];
    const2 = ((arb_ptr *)(param))[5];
    estinit = ((arb_ptr *)(param))[6];

    acb_mul_arb(Nu, z, Narb, prec);
    acb_log_analytic(logNu, Nu, analytic, prec);
    acb_set_arb(y_acb, y);

    //establish the integrand
    acb_mul_2exp_si(a, logNu, -2);
    acb_neg(a, a);
    acb_add_arb(a, a, const2, prec);
    acb_mul(a, a, logNu, prec);
    acb_pow_analytic(d, Nu, y_acb, analytic, prec);
    acb_mul_arb(b, d, afac, prec);
    acb_add_si(b, b, 1, prec);
    acb_mul(a, b, a, prec);
    acb_mul_arb(c, d, estinit, prec);
    acb_add(c, c, a, prec);

    acb_neg(exponent, y_acb);
    acb_sub_si(exponent, exponent, 1, prec);
    acb_mul_2exp_si(exponent, exponent, -1);
    acb_mul_2exp_si(b, logNu, -2);
    acb_sub_arb(b, b, const1, prec);
    acb_mul_arb(b, b, t, prec);
    acb_add(exponent, exponent, b, prec);
    acb_pow_analytic(a, Nu, exponent, analytic, prec);
    acb_mul(res, c, a, prec);

    acb_clear(a);
    acb_clear(b);
    acb_clear(c);
    acb_clear(d);
    acb_clear(Nu);
    acb_clear(logNu);
    acb_clear(exponent);
    acb_clear(y_acb);

    return 0;
}

void
generate_ddtbound(arb_t esta, const arb_t x, const arb_t y, const arb_t t, arb_t Narb, arb_t afac, arb_t const1,
                  arb_t xdiv4pi, arb_t logxdiv4pi,
                  arb_t logxdiv4pi_upper,
                  arb_t onedivxmin6, slong prec)

{  
    arb_t a, b, c, d, const2, estinit, pi;
    arb_init(a);
    arb_init(b);
    arb_init(c);
    arb_init(d);
    arb_init(const2);
    arb_init(estinit);
    arb_init(pi);
    arb_const_pi(pi, prec);    

    acb_t ai, bi, est, tmp;
    acb_init(ai);
    acb_init(bi);
    acb_init(est);
    acb_init(tmp);

    slong goal, head_n;

    //const2
    /*
       log(x/(4*pi)) increases across [X,X+1], while 1/(x-6)
       decreases.  Bound the two occurrences independently in their
       conservative directions.  At t=0 this separation is essential:
       the logarithmic factor can increase even though the heat exponent
       supplies no compensating x-decay.
    */
    arb_mul_2exp_si(a, logxdiv4pi_upper, -2);
    arb_mul_2exp_si(b, pi, -3);
    arb_add(a, a, b, prec);
    arb_mul_2exp_si(b, onedivxmin6, 1);
    arb_add(const2, a, b, prec);
    arb_log(a, Narb, prec);
    arb_mul_2exp_si(a, a, -2);
    arb_sub(b, const2, a, prec);
    if (!arb_is_positive(b))
    {
        fprintf(stderr, "FAIL: time-derivative logarithmic bracket is not positive.\n");
        flint_abort();
    }

    //estinit
    arb_mul_2exp_si(a, onedivxmin6, 3);
    arb_mul_2exp_si(b, pi, -1);
    arb_add(b, a, b, prec);
    arb_add(c, logxdiv4pi_upper, a, prec);
    arb_mul(c, b, c, prec);
    arb_mul(c, c, afac, prec);
    arb_mul_2exp_si(estinit, c, -2);

    //evaluate the integral
    acb_calc_integrate_opt_t options;
    acb_calc_integrate_opt_init(options);

    mag_t tol;
    mag_init(tol);

    goal = prec;
    mag_set_ui_2exp_si(tol, 1, -prec);

    /* Exact finite head plus the integral of the certified decreasing
       tail.  For decreasing F,
         sum_{n=K+1}^N F(n) <= integral_K^N F(u) du. */
    arb_set_si(a, DERIVATIVE_HEAD);
    arb_div(a, a, Narb, prec);
    arb_zero(b);
    acb_set_arb_arb(ai, a, b);
    arb_one(a);
    acb_set_arb_arb(bi, a, b);

    void *param[7];

    param[0] = (void *) Narb;
    param[1] = (void *) y;
    param[2] = (void *) t;
    param[3] = (void *) afac;
    param[4] = (void *) const1;
    param[5] = (void *) const2;
    param[6] = (void *) estinit;

    ddt_analytic_calls = 0;
    if (acb_calc_integrate(est, f_ddtbound, param, ai, bi, goal, tol, NULL, prec) != 0)
    {
        fprintf(stderr, "FAIL: time-derivative quadrature did not converge.\n");
        flint_abort();
    }
    if (ddt_analytic_calls == 0)
    {
        fprintf(stderr, "FAIL: time quadrature never requested an analytic enclosure.\n");
        flint_abort();
    }
    acb_mul_arb(est, est, Narb, prec);
    for (head_n = 1; head_n <= DERIVATIVE_HEAD; head_n++)
    {
        arb_set_si(a, head_n);
        arb_div(a, a, Narb, prec);
        arb_zero(b);
        acb_set_arb_arb(ai, a, b);
        if (f_ddtbound(tmp, ai, param, 0, prec) != 0)
        {
            fprintf(stderr, "FAIL: time-derivative head evaluation failed.\n");
            flint_abort();
        }
        acb_add(est, est, tmp, prec);
    }
    acb_abs(esta, est, prec);

    mag_clear(tol);

    arb_clear(a);
    arb_clear(b);
    arb_clear(c);
    arb_clear(d);
    arb_clear(const2);
    arb_clear(estinit);
    arb_clear(pi);

    acb_clear(ai);
    acb_clear(bi);
    acb_clear(est);
    acb_clear(tmp);
} 

void H01(acb_t z, const acb_t s, slong prec)
{
    acb_t a, b, c, d, half, piacb;
    acb_init(a);
    acb_init(b);
    acb_init(c);
    acb_init(d);
    acb_init(half);
    acb_init(piacb);

    arb_t ab, pi;
    arb_init(ab);
    arb_init(pi);
    arb_const_pi(pi, prec);  
 
    acb_set_arb(piacb, pi);
    acb_one(a);
    acb_mul_2exp_si(half, a, -1);
 
    acb_mul_2exp_si(d, s, -1);
    acb_sub_si(b, s, 1, prec);
    acb_mul(b, b, d, prec);   

    acb_neg(a, s);
    acb_mul_2exp_si(a, a, -1);
    acb_pow(a, piacb, a, prec);
    acb_mul(b, b, a, prec); 

    arb_mul_2exp_si(ab, pi, 1);
    arb_sqrt(ab, ab, prec);
    acb_mul_arb(b, b, ab, prec); 

    acb_log(a, d, prec);
    acb_sub(c, d, half, prec);
    acb_mul(c, c, a, prec);
    acb_sub(c, c, d, prec);
    acb_exp(c, c, prec);
    acb_mul(z, c, b, prec); 
 
    acb_clear(a);
    acb_clear(b);
    acb_clear(c);
    acb_clear(d);
    acb_clear(half);
    acb_clear(piacb);

    arb_clear(ab);
    arb_clear(pi);
}

void alpha1(acb_t z, const acb_t s, slong prec)
{
    acb_t a, b;
    acb_init(a);
    acb_init(b);

    arb_t ab, pi;
    arb_init(ab);
    arb_init(pi);
    arb_const_pi(pi, prec);  
 
    acb_mul_2exp_si(a, s, 1);
    acb_inv(a, a, prec);
 
    acb_sub_si(b, s, 1, prec);
    acb_inv(b, b, prec);   

    acb_add(a, a, b, prec);

    arb_mul_2exp_si(ab, pi , 1);
    acb_div_arb(b, s, ab, prec);
    acb_log(b, b, prec);   
    acb_mul_2exp_si(b, b, -1);

    acb_add(z, a, b, prec);
 
    acb_clear(a);
    acb_clear(b);

    arb_clear(ab);
    arb_clear(pi);
}

static void
bexpo_aexpo_afac_bsums_asums(acb_mat_t ests, acb_mat_t sarr, acb_mat_t bexpo, acb_mat_t aexpo, const acb_t ssexpo, 
               acb_mat_t afac, acb_mat_t asums, acb_mat_t bsums, const acb_poly_t finpoly, const arb_t t, const arb_t logtn0, 
               const arb_t n0, arb_t minmodabb, const slong k, const slong prec)

{
    acb_t a, b, c, d, s, negs, conjs, onemins, alphas, alphaconjs, alpha1mins, one;
    acb_init(a);
    acb_init(b);
    acb_init(c);
    acb_init(d);
    acb_init(s);
    acb_init(negs);
    acb_init(conjs);
    acb_init(onemins);
    acb_init(alphas);
    acb_init(alpha1mins);
    acb_init(alphaconjs);
    acb_init(one);
    acb_one(one);

    arb_t ab, negt, truncation_error;
    arb_init(ab);
    arb_init(negt);
    arb_init(truncation_error);

    /* The independently certified 62 by 62 Taylor-tail remainder is
       below 1e-20 uniformly on the complete barrier domain.  Carry that
       error through every value enclosure used for modulus, phase, and
       winding calculations. */
    arb_set_str(truncation_error, "1e-20", prec);

    arb_neg(negt, t);

    //set alpha1(sarr(k))/2, alpha1(1-sarr(k))/2, alpha1conj(sarr(k))/2
    acb_set(s, acb_mat_entry(sarr, k, 0));
    alpha1(alphas, s, prec);
    acb_mul_2exp_si(alphas, alphas, -1);

    acb_conj(conjs, s);
    alpha1(alphaconjs, conjs, prec);
    acb_mul_2exp_si(alphaconjs, alphaconjs, -1);

    acb_neg(negs, s);
    acb_add_si(onemins, negs, 1, prec);
    alpha1(alpha1mins, onemins, prec);
    acb_mul_2exp_si(alpha1mins, alpha1mins, -1);

    //bexpo
    acb_mul_arb(b, alpha1mins, negt, prec);
    acb_sub(b, b, onemins, prec);
    acb_add(b, b, ssexpo, prec);
    acb_set(acb_mat_entry(bexpo, k, 0), b);

    //aexpo
    acb_mul_arb(b, alphaconjs, negt, prec);
    acb_sub(b, b, conjs, prec);
    acb_add(b, b, ssexpo, prec);
    acb_set(acb_mat_entry(aexpo, k, 0), b);

    //afac
    acb_pow_ui(b, alphas, 2, prec);
    acb_pow_ui(d, alpha1mins, 2, prec);
    acb_sub(b, b, d, prec);
    acb_mul_arb(b, b, t, prec);
    acb_exp(a, b, prec);
    H01(b, s, prec);            
    H01(d, onemins, prec);   
    acb_div(b, b, d, prec);
    acb_mul(b, b, a, prec);
    acb_set(acb_mat_entry(afac, k, 0), b);

    //bsums
    arb_mul_2exp_si(ab, logtn0, -1);
    acb_add_arb(a, acb_mat_entry(bexpo, k, 0), ab, prec);
    acb_set_arb(b, n0);
    acb_pow(a, b, a, prec);
    acb_add_arb(b, acb_mat_entry(bexpo, k, 0), logtn0, prec);
    acb_poly_evaluate(c, finpoly, b, prec);
    acb_mul(b, c, a, prec);
    acb_set(acb_mat_entry(bsums, k, 0), b);

    //asums
    acb_add_arb(a, acb_mat_entry(aexpo, k, 0), ab, prec);
    acb_set_arb(b, n0);
    acb_pow(a, b, a, prec);
    acb_add_arb(b, acb_mat_entry(aexpo, k, 0), logtn0, prec);
    acb_poly_evaluate(c, finpoly, b, prec);
    acb_mul(b, c, a, prec);
    acb_set(acb_mat_entry(asums, k, 0), b);

    //ests
    acb_conj(b, acb_mat_entry(asums, k, 0));
    acb_mul(a, acb_mat_entry(afac, k, 0), b, prec);
    acb_add(a, a, acb_mat_entry(bsums, k, 0), prec);
    acb_add_error_arb(a, truncation_error);
    acb_set(acb_mat_entry(ests, k, 0), a);

    //establish minimum value of modabb
    acb_abs(ab, acb_mat_entry(ests, k, 0), prec);
    /* Enclose the true minimum of all modulus balls seen so far.  The
       historical `if (arb_lt(...))` skipped overlapping candidates and
       therefore did not necessarily retain the smallest lower endpoint. */
    arb_min(minmodabb, minmodabb, ab, prec);

    arb_clear(ab);
    arb_clear(negt);
    arb_clear(truncation_error);

    acb_clear(a);
    acb_clear(b);
    acb_clear(c);
    acb_clear(d);
    acb_clear(s);
    acb_clear(negs);
    acb_clear(conjs);
    acb_clear(onemins);
    acb_clear(alphas);
    acb_clear(alpha1mins);
    acb_clear(alphaconjs);
    acb_clear(one);
}

static void
print_details(slong res, const arb_t t, const arb_t a, const arb_t b, const acb_t c)

{
    arf_printd(arb_midref(t), 20);
    printf(", ");
    arf_printd(arb_midref(a), 30);
    printf(", ");
    arf_printd(arb_midref(b), 30);
    printf(", ");
    acb_printn(c, 30, ARB_STR_NO_RADIUS);
    printf("\n");
}

//process a rectangle for each t
void
abbeff_symmetric_rectangle(acb_mat_t ests, const arb_t x, const arb_t y,  const arb_t t, const slong num, 
                           const acb_poly_t finpoly, const arb_t n0, const arb_t logtn0, const acb_t ssexpo, 
                           arb_t minmodabb, const slong prt, const slong prec)
{        
    acb_mat_t sarr, bexpo, aexpo, afac, bsums, asums; 
    arb_mat_t thtarr, zarr;

    acb_t a, b, c, one, onei, Idiv4, IXdiv2;
    acb_init(a);
    acb_init(b);
    acb_init(c);
    acb_init(Idiv4);
    acb_init(IXdiv2);
    acb_init(one);
    acb_one(one);
    acb_init(onei);
    acb_onei(onei);

    arb_t ab, ac, ad, half, oneminy, oneminydiv2, ydiv2, numarb, nummin1, varb;
    arb_init(ab);
    arb_init(ac);
    arb_init(ad);
    arb_init(half);
    arb_init(numarb);
    arb_init(nummin1);
    arb_init(varb);
    arb_init(oneminy);
    arb_init(oneminydiv2);
    arb_init(ydiv2);

    slong k, v, result;
    result = 0;

    //shared values     
    acb_mul_2exp_si(Idiv4, onei, -2); 
    arb_neg(ab, y); 
    arb_add_si(oneminy, ab, 1, prec); 
    arb_mul_2exp_si(oneminydiv2, oneminy, -1);
    acb_set_arb(b, x); 
    acb_mul_onei(a, b); 
    acb_mul_2exp_si(IXdiv2, a, -1);
    arb_mul_2exp_si(ydiv2, y, -1);
    arb_one(ab);
    arb_mul_2exp_si(half, ab, -1);	
    arb_set_ui(numarb, num);
    arb_sub_si(nummin1, numarb, 1, prec); 

    //run along all four sides of the rectangle
    arb_mat_init(thtarr, num, 1);
    arb_mat_init(zarr, num, 1);
    acb_mat_init(sarr, 4*num-4, 1);
    acb_mat_init(afac, 4*num-4, 1); 
    acb_mat_init(bexpo, 4*num-4, 1);
    acb_mat_init(aexpo, 4*num-4, 1);
    acb_mat_init(bsums, 4*num-4, 1);
    acb_mat_init(asums, 4*num-4, 1);

    arb_mul_2exp_si(ab, half, -1);
    arb_neg(ab, ab);
    arb_set(arb_mat_entry(thtarr, 0, 0), ab);  
    arb_neg(ab, oneminydiv2);
    arb_set(arb_mat_entry(zarr, 0, 0), ab); 

    for (v = 0; v < num-1; v++)
    { 
       arb_set_ui(varb, v); 
       arb_add_si(varb, varb, 1, prec); 
       arb_div(ad, varb, nummin1, prec);

       //thtarr
       arb_sub(ac, ad, half, prec);
       arb_mul_2exp_si(ac, ac, -1);
       arb_set(arb_mat_entry(thtarr, v+1, 0), ac);

       //zarr 
       arb_mul(ac, oneminydiv2, ad, prec);
       arb_mul_2exp_si(ac, ac, 1);
       arb_sub(ac, ac, oneminydiv2, prec);
       arb_set(arb_mat_entry(zarr, v+1, 0), ac);

       //x lower constant
       k = v;
       acb_add_arb(a, IXdiv2, oneminydiv2, prec);
       acb_sub_arb(a, a, arb_mat_entry(zarr, v, 0), prec);
       acb_sub(a, a, Idiv4, prec);
       acb_set(acb_mat_entry(sarr, k, 0), a);
       bexpo_aexpo_afac_bsums_asums(ests, sarr, bexpo, aexpo, ssexpo, afac, asums, bsums, finpoly, t, logtn0, n0, minmodabb, k, prec);

       if (prt==1)
       {      
          arb_mul_2exp_si(ab, arb_mat_entry(zarr, v, 0), 1);
          arb_add(ab, y, ab, prec); 
          acb_set_arb(acb_mat_entry(ests, k, 1), ab);
          arb_sub(ad, x, half, prec);
          acb_set_arb(acb_mat_entry(ests, k, 2), ad);
        }

       //y upper constant
       k = num+v-1;
       acb_set_arb(a, arb_mat_entry(thtarr, v, 0));
       acb_mul_onei(a, a);
       acb_add(a, IXdiv2, a, prec);
       acb_set(acb_mat_entry(sarr, k, 0), a);
       bexpo_aexpo_afac_bsums_asums(ests, sarr, bexpo, aexpo, ssexpo, afac, asums, bsums, finpoly, t, logtn0, n0, minmodabb, k, prec);

       if (prt==1)
       {      
          arb_set_si(ab, 1);
          acb_set_arb(acb_mat_entry(ests, k, 1), ab);
          arb_mul_2exp_si(ad, arb_mat_entry(thtarr, v, 0), 1);
          arb_add(ad, x, ad, prec);
          acb_set_arb(acb_mat_entry(ests, k, 2), ad);
       }

       //x upper and output to be attached in reverse order
       k = 3*num-(v+1)-3;
       acb_add_arb(a, IXdiv2, oneminydiv2, prec);
       acb_sub_arb(a, a, arb_mat_entry(zarr, v+1, 0), prec);
       acb_add(a, a, Idiv4, prec);
       acb_set(acb_mat_entry(sarr, k, 0), a);
       bexpo_aexpo_afac_bsums_asums(ests, sarr, bexpo, aexpo, ssexpo, afac, asums, bsums, finpoly, t, logtn0, n0, minmodabb, k, prec);

       if (prt==1)
       {  
          arb_mul_2exp_si(ab, arb_mat_entry(zarr, v+1, 0), 1);    
          arb_add(ab, y, ab, prec);
          acb_set_arb(acb_mat_entry(ests, k, 1), ab);
          arb_add(ad, x, half, prec);
          acb_set_arb(acb_mat_entry(ests, k, 2), ad);
       }

       //y lower and output to be attached in reverse order
       k = 4*num-(v+1)-4;
       acb_add_arb(a, IXdiv2, oneminydiv2, prec);
       acb_set_arb(b, arb_mat_entry(thtarr, v+1, 0));
       acb_mul_onei(b, b);
       acb_add(a, a, b, prec);
       acb_add_arb(a, a, oneminydiv2, prec);
       acb_set(acb_mat_entry(sarr, k, 0), a);
       bexpo_aexpo_afac_bsums_asums(ests, sarr, bexpo, aexpo, ssexpo, afac, asums, bsums, finpoly, t, logtn0, n0, minmodabb, k, prec);

       if (prt==1)
       {      
          arb_add_si(ab, y, -1, prec);
          arb_add(ab, ab, y, prec);
          acb_set_arb(acb_mat_entry(ests, k, 1), ab);
          arb_mul_2exp_si(ad, arb_mat_entry(thtarr, v+1, 0), 1);
          arb_add(ad, x, ad, prec);
          acb_set_arb(acb_mat_entry(ests, k, 2), ad);
       }
    }

    acb_mat_clear(sarr);
    acb_mat_clear(afac);
    acb_mat_clear(bexpo);
    acb_mat_clear(aexpo);
    acb_mat_clear(bsums);
    acb_mat_clear(asums);

    arb_mat_clear(thtarr);
    arb_mat_clear(zarr);

    acb_clear(a);
    acb_clear(b);
    acb_clear(c);
    acb_clear(one);
    acb_clear(onei);
    acb_clear(Idiv4);
    acb_clear(IXdiv2);

    arb_clear(ab);
    arb_clear(ac);
    arb_clear(ad);
    arb_clear(half);
    arb_clear(oneminy);
    arb_clear(oneminydiv2);
    arb_clear(ydiv2);
    arb_clear(numarb);
    arb_clear(nummin1);
    arb_clear(varb);
}

//procedure to transform the matrix into a poly
static void
mattopoly(acb_poly_t polyres, const arb_t tval, const slong expterms, const slong taylorterms, 
           const acb_mat_t mattmp, const slong prec)
{

    arb_t ab;
    acb_t a, b;

    arb_init(ab);
    acb_init(a);
    acb_init(b);

    slong e, t;

    acb_poly_zero(polyres);

    for (e = 0; e < expterms; e++)
    {
        for (t = 0; t < taylorterms; t++)
        {
            arb_pow_ui(ab, tval, t, prec);
            acb_set_arb(a, ab);
            acb_mul(b, a, acb_mat_entry(mattmp, e, t), prec);
            acb_poly_get_coeff_acb(a, polyres, e);
            acb_add(b, b, a, prec);
            acb_poly_set_coeff_acb(polyres, e, b);
        }
    }

    arb_clear(ab);
    acb_clear(a);
    acb_clear(b);
}

int
abbeff_t_loop(slong res, const arb_t X, const arb_t y0, const arb_t ts, const arb_t te, const slong N, 
              const slong taylorterms, const slong expterms, const acb_mat_t finalmat,
              const slong prt, const slong digits, const slong prec)

{
    acb_mat_t ests;

    arb_t a, b, c, d, x, y, t, pi, ab, bb, Narb;
    arb_t x_upper, y_upper, xdiv4pi, xdiv4pi_upper;
    arb_t logxdiv4pi, logxdiv4pi_upper;
    arb_t onedivxmin6, tdiv4divxmin6, logtn0, n0;
    arb_t minmodabb, windnum, windtot, dzabb, dtabb, afac, const1;
    arb_t minrealright, maximagright, rightrealcert, rightimagcert;
    arb_t target_cover, t_next, delta, spatial_error, time_error;
    arb_t approximation_error, proof_lhs, proof_margin, step_cap;
    arb_t t_box, dtabb_prism;
    arb_init(a);
    arb_init(b);
    arb_init(c);
    arb_init(d);
    arb_init(x);
    arb_init(y);
    arb_init(t);
    arb_init(ab);
    arb_init(bb);
    arb_init(Narb);
    arb_init(x_upper);
    arb_init(y_upper);
    arb_init(xdiv4pi);
    arb_init(xdiv4pi_upper);
    arb_init(logxdiv4pi);
    arb_init(logxdiv4pi_upper);
    arb_init(onedivxmin6);
    arb_init(tdiv4divxmin6);
    arb_init(n0);
    arb_init(logtn0);
    arb_init(minmodabb);
    arb_init(windnum);
    arb_init(windtot);
    arb_init(dzabb);
    arb_init(dtabb);
    arb_init(afac);
    arb_init(const1);
    arb_init(minrealright);
    arb_init(maximagright);
    arb_init(rightrealcert);
    arb_init(rightimagcert);
    arb_init(target_cover);
    arb_init(t_next);
    arb_init(delta);
    arb_init(spatial_error);
    arb_init(time_error);
    arb_init(approximation_error);
    arb_init(proof_lhs);
    arb_init(proof_margin);
    arb_init(step_cap);
    arb_init(t_box);
    arb_init(dtabb_prism);
    arb_init(pi);
    arb_const_pi(pi, prec);

    arf_t target_hi_arf, step_lo_arf, candidate_arf;
    arf_init(target_hi_arf);
    arf_init(step_lo_arf);
    arf_init(candidate_arf);

    acb_t ca, argdiv, ssexpo, one;
    acb_init(ca);
    acb_init(argdiv);
    acb_init(ssexpo);
    acb_init(one);
    acb_one(one);

    acb_poly_t finpoly;
    acb_poly_init(finpoly);
   
    arb_set_si(Narb, N);

    printf("\n");
    printf("Processing the barrier for X= ");
    arf_printd(arb_midref(X), 20);
    printf("...");
    arb_add_si(a, X, 1, prec);
    arf_printd(arb_midref(a), 20);
    printf(" (N = %ld)", N);
    printf(", y0 = ");
    arf_printd(arb_midref(y0), 10);
    printf("...1 ");
    printf(", t = ");
    arf_printd(arb_midref(ts), 10);
    printf("...");
    arf_printd(arb_midref(te), 10);
    printf("\n");
    printf("\n");

    slong idx, count, rectmesh, num, prtresult, n_lo, n_hi;
    int certified, covered, ests_live;
    prtresult = 0;
    certified = 0;
    covered = 0;
    ests_live = 0;

    /* Cover a dyadic upper enclosure of the requested decimal endpoint.
       Every adaptive seam below is also an exact dyadic Arb number. */
    arb_get_ubound_arf(target_hi_arf, te, prec);
    arb_set_arf(target_cover, target_hi_arf);

    /* This is the Riemann--Siegel error-ball allowance.  A final package
       must separately replay (20)--(23) and the conservative Proposition
       6.6(vi) corollary uniformly and prove their sum is below this number. */
    if (arb_set_str(approximation_error, "0.00125", prec) != 0)
    {
        fprintf(stderr, "FAIL: could not parse approximation allowance.\n");
        goto end;
    }

    arb_set_si(a, 1);
    arb_div_ui(a, a, 5, prec);
    if (!arb_is_zero(ts) || !arb_gt(target_cover, ts) ||
        !arb_le(target_cover, a) || !arb_is_positive(y0))
    {
        fprintf(stderr, "FAIL: invalid closed-slab endpoints.\n");
        goto end;
    }

    /* N is monotone in x and t.  Equality at these opposite corners proves
       constancy throughout [X,X+1] x [0,target_cover]. */
    arb_add_si(a, X, 1, prec);
    n_lo = get_N(ts, X, prec);
    n_hi = get_N(target_cover, a, prec);
    if (n_lo != N || n_hi != N)
    {
        fprintf(stderr, "FAIL: N is not constant on the closed slab.\n");
        goto end;
    }

    printf("Closed target enclosure: ");
    arb_printn(target_cover, 30, ARB_STR_MORE);
    printf("; N-corners=%ld,%ld; H/B approximation allowance=", n_lo, n_hi);
    arb_printn(approximation_error, 20, ARB_STR_MORE);
    printf("\n");

    //change X and y to midpoints
    arb_one(b);
    arb_mul_2exp_si(a, b, -1);  
    arb_add(x, X, a, prec); 
    arb_add_si(a, y0, 1, prec);
    arb_mul_2exp_si(y, a, -1);

    //n0
    arb_mul_2exp_si(n0, Narb, -1);

    //ssexpo
    acb_set_arb(ca, x);
    acb_mul_onei(ca, ca);   
    acb_neg(ca, ca);
    acb_add_si(ca, ca, 1, prec);
    acb_mul_2exp_si(ssexpo, ca, -1);   
    
    //shared values for the ddz and ddtbounds
    arb_set_si(Narb, N);
    arb_mul_2exp_si(a, pi, 2);
    arb_div(xdiv4pi, X, a, prec);
    arb_log(logxdiv4pi, xdiv4pi, prec);
    arb_add_si(x_upper, X, 1, prec);
    arb_one(y_upper);
    arb_div(xdiv4pi_upper, x_upper, a, prec);
    arb_log(logxdiv4pi_upper, xdiv4pi_upper, prec);
    arb_sub_si(b, X, 6, prec);
    arb_inv(onedivxmin6, b, prec);

    /* Fail closed on an explicit lower bound for the x-derivative of
       c(x,y)=log(x/(4*pi))/4-h(x,y)_+/(2*x^2).  On 0<=y<=1,
       |d_x(h_+/(2*x^2))| <= 2/x^3 on this domain, so throughout
       [X,X+1] one has c_x >= 1/(4*(X+1))-2/X^3. */
    arb_mul(c, X, X, prec);
    arb_sub_ui(c, c, 8, prec);
    if (!arb_is_positive(c))
    {
        fprintf(stderr, "FAIL: derivative-box c derivative prerequisite failed.\n");
        goto end;
    }
    arb_add_si(a, X, 1, prec);
    arb_inv(a, a, prec);
    arb_mul_2exp_si(a, a, -2);
    arb_mul(b, X, X, prec);
    arb_mul(b, b, X, prec);
    arb_inv(b, b, prec);
    arb_mul_2exp_si(b, b, 1);
    arb_sub(a, a, b, prec);
    if (!arb_is_positive(a))
    {
        fprintf(stderr, "FAIL: derivative-box c x-monotonicity gate is not strict.\n");
        goto end;
    }

    /*
       The A-side core in Lemma 8.4 is

         |gamma| N^|kappa| n^y n^(-Re(s_*)).

       Its upper logarithmic y-slope is at most

         .02 - log(X/(4*pi))/2
              + t_top log(N)/(2(X-6)) + log(N)/2.

       Strict negativity proves that the complete A core is maximized
       at y=y0 for every n<=N.  This is the only coupled y-freeze used
       below; all explicit increasing y factors are separately evaluated
       at y=1.
    */
    arb_set_str(a, "0.02", prec);
    arb_mul_2exp_si(b, logxdiv4pi, -1);
    arb_sub(a, a, b, prec);
    arb_log(b, Narb, prec);
    arb_mul(c, target_cover, b, prec);
    arb_mul(c, c, onedivxmin6, prec);
    arb_mul_2exp_si(c, c, -1);
    arb_add(a, a, c, prec);
    arb_mul_2exp_si(b, b, -1);
    arb_add(a, a, b, prec);
    if (!arb_is_negative(a))
    {
        fprintf(stderr, "FAIL: A-core y-monotonicity gate is not strict.\n");
        goto end;
    }

    /* The time-derivative integrand is accumulated as a nonnegative
       majorant.  N^2 < X/(4*pi) implies log(N) < log(X/(4*pi))/2,
       and in particular const2-log(n)/4 is positive for every n<=N. */
    arb_log(b, Narb, prec);
    arb_mul_2exp_si(b, b, 1);
    if (!arb_lt(b, logxdiv4pi))
    {
        fprintf(stderr, "FAIL: derivative-bracket positivity gate failed.\n");
        goto end;
    }

    /* h_y=-3+4(1+2y)/x^2<0 on the whole slab.  Hence the
       positive-part correction in Re(s_*) decreases with y and the
       coefficient of t in the sigma lower bound is minimized at
       (X,y0). */
    arb_mul(b, X, X, prec);
    arb_set_si(a, 12);
    arb_div(a, a, b, prec);
    arb_sub_si(a, a, 3, prec);
    if (!arb_is_negative(a))
    {
        fprintf(stderr, "FAIL: sigma y-monotonicity gate is not strict.\n");
        goto end;
    }

    //const1 required for the ddz and ddtbounds
    arb_mul_2exp_si(a, logxdiv4pi, -2);
    arb_set_si(b, -3);
    arb_mul(b, b, y0, prec);
    arb_add_si(b, b, 1, prec);
    arb_mul_2exp_si(c, y0, 2);
    arb_add_si(d, y0, 1, prec);
    arb_mul(c, c, d, prec);
    arb_mul(d, X, X, prec);
    arb_div(c, c, d, prec);
    arb_add(c, c, b, prec);
    arb_zero(b);
    arb_max(c, b, c, prec);
    arb_div(c, c, d, prec);
    arb_mul_2exp_si(c, c, -1);
    arb_sub(const1, a, c, prec);

    /* Let
         P(n)=n^{-(1+y0)/2+t(log(n)/4-const1)}.
       Its logarithmic derivative with respect to log(n) is
         p=-(1+y0)/2+t(log(n)/2-const1).
       The first gate makes p<=-(1+y0)/2 for every n<=N and t>=0.
       Every component in both derivative integrands then has logarithmic
       derivative at most p+y0+1/log(n).  The second strict gate makes
       all components decrease for n>=DERIVATIVE_HEAD. */
    arb_log(b, Narb, prec);
    arb_mul_2exp_si(b, b, -1);
    arb_sub(a, const1, b, prec);
    if (!arb_is_positive(a))
    {
        fprintf(stderr, "FAIL: derivative-tail exponent gate is not strict.\n");
        goto end;
    }
    arb_sub_si(a, y0, 1, prec);
    arb_mul_2exp_si(a, a, -1);
    arb_set_si(b, DERIVATIVE_HEAD);
    arb_log(b, b, prec);
    arb_inv(b, b, prec);
    arb_add(a, a, b, prec);
    if (!arb_is_negative(a))
    {
        fprintf(stderr, "FAIL: derivative-tail monotonicity gate is not strict.\n");
        goto end;
    }

    //perform the t-loop over all the X..X+1, y0..1 rectangles
    arb_set(t, ts);
    arb_zero(windtot);
    count = 0;

    while(!covered)
    {
        count=count+1;
        arb_set_si(minmodabb, 1000);

        //logtn0
        arb_mul_2exp_si(a, t, -1);
        arb_log(b, n0, prec);
        arb_mul(logtn0, b, a, prec);

        mattopoly(finpoly, t, expterms, taylorterms, finalmat, prec);

        //calculate ddz and ddt bounds
        arb_mul_2exp_si(a, t, -2);
        arb_mul(tdiv4divxmin6, a, onedivxmin6, prec);

        //afac-term
        arb_set_si(a, 2);
        arb_set_si(b, 100);
        arb_div(a, a, b, prec);
        arb_mul(a, y0, a, prec);
        arb_exp(a, a, prec);
        arb_neg(b, y0);
        arb_mul_2exp_si(b, b, -1); 
        arb_pow(b, xdiv4pi, b, prec);
        arb_mul(d, a, b, prec);
        arb_mul(a, t, y0, prec);
        arb_mul(a, a, onedivxmin6, prec);
        arb_mul_2exp_si(a, a, -1);
        arb_pow(b, Narb, a, prec); 
        arb_mul(afac, d, b, prec);

        generate_ddzbound(dzabb, X, y0, x_upper, y_upper, t,
                          Narb, afac, const1, tdiv4divxmin6, prec);
        generate_ddtbound(dtabb, X, y0, t, Narb, afac, const1,
                          xdiv4pi, logxdiv4pi,
                          logxdiv4pi_upper, onedivxmin6, prec);
        arb_ceil(dzabb, dzabb, prec);
        arb_ceil(dtabb, dtabb, prec);

        /* A midpoint-to-double cast is not an admissible proof step.
           Require exact positive integer derivative ceilings and convert
           directly from the exact arf midpoint. */
        if (!arb_is_int(dzabb) || !arb_is_int(dtabb) ||
            !arb_is_positive(dzabb) || !arb_is_positive(dtabb))
        {
            fprintf(stderr, "FAIL: derivative ceiling is not an exact positive integer.\n");
            goto end;
        }
        num = arf_get_si(arb_midref(dzabb), ARF_RND_NEAR);
        if (num < 2)
        {
            fprintf(stderr, "FAIL: spatial mesh has fewer than two points per edge.\n");
            goto end;
        }
        rectmesh = 4 * num - 4;

        acb_mat_init(ests, rectmesh, 3);
        ests_live = 1;

        //evaluate the rectangle
        abbeff_symmetric_rectangle(ests, x, y, t, num, finpoly, n0, logtn0, ssexpo, minmodabb, prt, prec);

        /* Rigorous right-edge phase data.  The right edge occupies rows
           2*num-2 through 3*num-3 of the rectangular mesh.  Expand the
           mesh extrema by D_z times half a mesh spacing to cover every
           point between adjacent samples. */
        arb_set_si(minrealright, 1000);
        arb_zero(maximagright);
        for (idx = 2*num-2; idx <= 3*num-3; idx++)
        {
            acb_get_real(a, acb_mat_entry(ests, idx, 0));
            arb_min(minrealright, minrealright, a, prec);
            acb_get_imag(a, acb_mat_entry(ests, idx, 0));
            arb_abs(a, a);
            arb_max(maximagright, maximagright, a, prec);
        }
        arb_one(a);
        arb_sub(a, a, y0, prec);
        arb_div_ui(a, a, num-1, prec);
        arb_mul(a, a, dzabb, prec);
        arb_mul_2exp_si(a, a, -1);
        arb_sub(rightrealcert, minrealright, a, prec);
        arb_add(rightimagcert, maximagright, a, prec);

        //calculate and print the winding number for this x,y rectangle
        arb_zero(windnum);
        for (idx = 0; idx < rectmesh-1; idx++)
        { 
            if (acb_contains_zero(acb_mat_entry(ests, idx, 0)) ||
                acb_contains_zero(acb_mat_entry(ests, idx+1, 0)))
            {
                fprintf(stderr, "FAIL: a boundary mesh enclosure contains zero.\n");
                goto end;
            }
            acb_div(argdiv, acb_mat_entry(ests, idx, 0), acb_mat_entry(ests, idx+1, 0), prec);
            acb_arg(a, argdiv, prec);
            arb_abs(b, a);
            if (!arb_lt(b, pi))
            {
                fprintf(stderr, "FAIL: a polygon argument increment is not strictly inside (-pi,pi).\n");
                goto end;
            }
            arb_add(windnum, windnum, a, prec);
        }   

        if (acb_contains_zero(acb_mat_entry(ests, rectmesh-1, 0)) ||
            acb_contains_zero(acb_mat_entry(ests, 0, 0)))
        {
            fprintf(stderr, "FAIL: the closing mesh enclosure contains zero.\n");
            goto end;
        }
        acb_div(argdiv, acb_mat_entry(ests, rectmesh-1, 0), acb_mat_entry(ests, 0, 0), prec);
        acb_arg(a, argdiv, prec);
        arb_abs(b, a);
        if (!arb_lt(b, pi))
        {
            fprintf(stderr, "FAIL: the closing argument increment is not strictly inside (-pi,pi).\n");
            goto end;
        }
        arb_add(windnum, windnum, a, prec);
        arb_div(windnum, windnum, pi, prec);
        arb_mul_2exp_si(windnum, windnum, -1);

        /* A winding number is an integer.  Require the complete Arb
           enclosure to lie strictly inside (-1/4, 1/4), which certifies
           that this rectangle's winding number is exactly zero. */
        arb_abs(a, windnum);
        arb_set_si(b, 1);
        arb_mul_2exp_si(b, b, -2);
        if (!arb_lt(a, b))
        {
            fprintf(stderr, "FAIL: winding interval does not certify the integer zero.\n");
            goto end;
        }

        arb_add(windtot, windtot, windnum, prec);

        if (prt==1)
        {      
           arb_set_ui(a, 9);
           arb_div_ui(a, a, 10, prec);
           if (!arb_gt(rightrealcert, a))
           {
               fprintf(stderr, "Right-edge real-part certificate did not exceed 0.9.\n");
               flint_abort();
           }
           arb_set_ui(a, 6);
           arb_div_ui(a, a, 5, prec);
           if (!arb_lt(rightimagcert, a))
           {
               fprintf(stderr, "Right-edge imaginary-part certificate did not stay below 1.2.\n");
               flint_abort();
           }
           printf("Right-edge certified real lower interval: ");
           arb_printn(rightrealcert, 20, 0);
           printf("\nRight-edge certified abs-imag upper interval: ");
           arb_printn(rightimagcert, 20, 0);
           printf("\n");
           for (idx = 0; idx < rectmesh; idx++)
           { 
               acb_get_real(a, acb_mat_entry(ests, idx, 1));
               acb_get_real(b, acb_mat_entry(ests, idx, 2));
               acb_set(ca, acb_mat_entry(ests, idx, 0));
               print_details(prtresult, t, a, b, ca);
           }
        }

        /* If h is the largest physical edge spacing, the true boundary
           curve and its polygonal interpolation differ by at most
               D_z h / 2.
           Here h <= 1/(num-1); using num (as the historical code did)
           would leave a small but real spatial gap. */
        arb_set_si(a, 2 * (num - 1));
        arb_div(spatial_error, dzabb, a, prec);

        /* Available strict time-motion budget after spatial interpolation
           and the H/B-to-f approximation error. */
        arb_sub(step_cap, minmodabb, spatial_error, prec);
        arb_sub(step_cap, step_cap, approximation_error, prec);
        if (!arb_is_positive(step_cap))
        {
            fprintf(stderr, "FAIL: no positive certified time-motion budget.\n");
            goto end;
        }
        arb_div(step_cap, step_cap, dtabb, prec);

        /* Take half of a directed lower bound for strict slack.  Add with
           downward rounding to obtain the next exact dyadic seam. */
        arb_get_lbound_arf(step_lo_arf, step_cap, prec);
        arf_mul_2exp_si(step_lo_arf, step_lo_arf, -1);
        if (arf_sgn(step_lo_arf) <= 0)
        {
            fprintf(stderr, "FAIL: adaptive step has no positive lower bound.\n");
            goto end;
        }
        arf_add(candidate_arf, arb_midref(t), step_lo_arf, prec, ARF_RND_FLOOR);
        if (arf_cmp(candidate_arf, arb_midref(t)) <= 0)
        {
            fprintf(stderr, "FAIL: adaptive time march did not advance.\n");
            goto end;
        }

        if (arf_cmp(candidate_arf, arb_midref(target_cover)) >= 0)
        {
            arb_set(t_next, target_cover);
            covered = 1;
        }
        else
        {
            arb_set_arf(t_next, candidate_arf);
        }

        /* Certify D_t on the whole closed time prism, not merely at its
           left endpoint.  This removes any dependence on an unproved
           monotonicity assertion for the derivative-majorant formula.
           Since both seams are exact points, their union is exactly the
           interval [t,t_next]. */
        arb_union(t_box, t, t_next, prec);

        /* Recompute afac with the interval-valued time parameter. */
        arb_set_si(a, 2);
        arb_set_si(b, 100);
        arb_div(a, a, b, prec);
        arb_mul(a, y0, a, prec);
        arb_exp(a, a, prec);
        arb_neg(b, y0);
        arb_mul_2exp_si(b, b, -1);
        arb_pow(b, xdiv4pi, b, prec);
        arb_mul(d, a, b, prec);
        arb_mul(a, t_box, y0, prec);
        arb_mul(a, a, onedivxmin6, prec);
        arb_mul_2exp_si(a, a, -1);
        arb_pow(b, Narb, a, prec);
        arb_mul(afac, d, b, prec);

        generate_ddtbound(dtabb_prism, X, y0, t_box, Narb, afac,
                          const1, xdiv4pi, logxdiv4pi,
                          logxdiv4pi_upper,
                          onedivxmin6, prec);
        if (!arb_is_finite(dtabb_prism) ||
            !arb_is_positive(dtabb_prism))
        {
            fprintf(stderr, "FAIL: closed-prism D_t bound is not finite and strictly positive.\n");
            goto end;
        }
        /* An interval evaluation naturally gives a range of possible
           majorants.  Round its directed upper endpoint upward to an
           exact integer majorant for the whole prism. */
        arb_get_ubound_arf(candidate_arf, dtabb_prism, prec);
        arf_ceil(candidate_arf, candidate_arf);
        arb_set_arf(dtabb, candidate_arf);
        if (!arb_is_int(dtabb) || !arb_is_positive(dtabb))
        {
            fprintf(stderr, "FAIL: could not form an exact closed-prism D_t ceiling.\n");
            goto end;
        }

        /* Recheck the complete closed prism from scratch.  This is the
           decisive predicate:
             min_mesh |f(t_i)| >
             spatial interpolation + D_t (t_{i+1}-t_i) + H/B error.
           An indeterminate comparison is a hard failure. */
        arb_sub(delta, t_next, t, prec);
        arb_mul(time_error, dtabb, delta, prec);
        arb_add(proof_lhs, spatial_error, time_error, prec);
        arb_add(proof_lhs, proof_lhs, approximation_error, prec);
        arb_sub(proof_margin, minmodabb, proof_lhs, prec);
        if (!arb_is_positive(delta) || !arb_is_positive(proof_margin))
        {
            fprintf(stderr, "FAIL: closed-prism nonvanishing inequality is not strict.\n");
            goto end;
        }

        printf("Prism(%ld) t=[", count);
        arb_printn(t, 30, ARB_STR_MORE);
        printf(",");
        arb_printn(t_next, 30, ARB_STR_MORE);
        printf("] winding=");
        arb_printn(windnum, 20, ARB_STR_MORE);
        printf(" min_mesh=");
        arb_printn(minmodabb, 20, ARB_STR_MORE);
        printf(" Dz=");
        arb_printn(dzabb, 20, ARB_STR_MORE);
        printf(" Dt=");
        arb_printn(dtabb, 20, ARB_STR_MORE);
        printf(" spatial=");
        arb_printn(spatial_error, 20, ARB_STR_MORE);
        printf(" time=");
        arb_printn(time_error, 20, ARB_STR_MORE);
        printf(" eps=");
        arb_printn(approximation_error, 20, ARB_STR_MORE);
        printf(" margin=");
        arb_printn(proof_margin, 20, ARB_STR_MORE);
        printf(" mesh=%ld PASS\n", rectmesh);

        acb_mat_clear(ests);
        ests_live = 0;
        if (!covered)
            arb_set(t, t_next);
    }

    flint_printf("\n");
    printf("Overall winding number: %f \n", arf_get_d(arb_midref(windtot), ARF_RND_NEAR));
    printf("Rigorous winding interval: ");
    arb_printn(windtot, 20, 0);
    printf("\n");
    printf("Closed coverage endpoint: ");
    arb_printn(target_cover, 30, ARB_STR_MORE);
    printf("\n");

    arb_abs(a, windtot);
    arb_set_si(b, 1);
    arb_mul_2exp_si(b, b, -2);
    if (!covered || !arb_lt(a, b))
    {
        fprintf(stderr, "FAIL: final coverage or aggregate winding gate failed.\n");
        goto end;
    }
    certified = 1;
    printf("RESULT: CLOSED SLAB CERTIFIED\n\n");

end:

    if (ests_live)
        acb_mat_clear(ests);

    arb_clear(a);
    arb_clear(b);
    arb_clear(c);
    arb_clear(d);
    arb_clear(x);
    arb_clear(y);
    arb_clear(t);
    arb_clear(Narb);
    arb_clear(x_upper);
    arb_clear(y_upper);
    arb_clear(xdiv4pi);
    arb_clear(xdiv4pi_upper);
    arb_clear(logxdiv4pi);
    arb_clear(logxdiv4pi_upper);
    arb_clear(onedivxmin6);
    arb_clear(tdiv4divxmin6);
    arb_clear(n0);
    arb_clear(logtn0);
    arb_clear(minmodabb);
    arb_clear(windnum);
    arb_clear(windtot);
    arb_clear(dzabb);
    arb_clear(dtabb);
    arb_clear(afac);
    arb_clear(const1);
    arb_clear(minrealright);
    arb_clear(maximagright);
    arb_clear(rightrealcert);
    arb_clear(rightimagcert);
    arb_clear(target_cover);
    arb_clear(t_next);
    arb_clear(delta);
    arb_clear(spatial_error);
    arb_clear(time_error);
    arb_clear(approximation_error);
    arb_clear(proof_lhs);
    arb_clear(proof_margin);
    arb_clear(step_cap);
    arb_clear(t_box);
    arb_clear(dtabb_prism);
    arb_clear(pi);

    arf_clear(target_hi_arf);
    arf_clear(step_lo_arf);
    arf_clear(candidate_arf);

    acb_clear(ca);
    acb_clear(argdiv);
    acb_clear(ssexpo);
    acb_clear(one);

    acb_poly_clear(finpoly);

    return certified;
}

slong get_N(const arb_t t, const arb_t x, slong prec)
{
    arb_t pi, u;
    slong N;
    slong result;
 
    arb_init(pi);
    arb_init(u);
 
    arb_const_pi(pi, prec);
    arb_mul(u, pi, t, prec);
    arb_mul_2exp_si(u, u, -2);
    arb_add(u, u, x, prec);
    arb_div(u, u, pi, prec);
    arb_mul_2exp_si(u, u, -2);
    arb_sqrt(u, u, prec);
    arb_floor(u, u, prec);
 
    if (!arb_is_int(u))
    {
        fprintf(stderr, "FAIL: could not determine an exact N value.\n");
        flint_abort();
    }
    N = arf_get_si(arb_midref(u), ARF_RND_DOWN);
 
    if (arb_contains_si(u, N) &&
        !arb_contains_si(u, N-1) &&
        !arb_contains_si(u, N+1))
    {
        result = N;
    }
    else
    {
        fprintf(stderr, "Unexpected error: could not compute N\n");
        flint_abort();
    }
   
    arb_clear(pi);
    arb_clear(u);
 
    return result;
}

const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ",");
            tok && *tok;
            tok = strtok(NULL, ",\n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}

static int
parse_arb_field(arb_t out, const char *line, int field, slong prec)
{
    char *copy = strdup(line);
    const char *value;
    int ok;
    if (copy == NULL)
        return 0;
    value = getfield(copy, field);
    ok = value != NULL && arb_set_str(out, value, prec) == 0;
    free(copy);
    return ok;
}

static int
parse_slong_field(slong *out, const char *line, int field)
{
    char *copy = strdup(line);
    const char *value;
    char *end;
    long parsed;
    int ok;
    if (copy == NULL)
        return 0;
    value = getfield(copy, field);
    if (value == NULL)
    {
        free(copy);
        return 0;
    }
    parsed = strtol(value, &end, 10);
    ok = end != value;
    while (ok && (*end == ' ' || *end == '\t' || *end == '\r' || *end == '\n'))
        end++;
    ok = ok && *end == '\0';
    if (ok)
        *out = (slong) parsed;
    free(copy);
    return ok;
}
 
int main(int argc, char *argv[])
{
    acb_mat_t finalmat;
    arb_t X, y0, ts, te, re, im, serialization_scale, serialization_error, absval, one;
    arb_init(X);
    arb_init(y0);
    arb_init(ts);
    arb_init(te);
    arb_init(re);
    arb_init(im);
    arb_init(serialization_scale);
    arb_init(serialization_error);
    arb_init(absval);
    arb_init(one);

    acb_t tmp;
    acb_init(tmp);

    const char *ts_str, *te_str, *y0_str, *prt_str;

    slong e, t, N, prec, expterms, taylorterms, prt, res, linesize, digits;

    FILE *f = NULL;
    int result = EXIT_SUCCESS;
    int finalmat_initialized = 0;
    res = 0;
    expterms = 0;
    taylorterms = 0;
    N = 0;
    prec = 0;

    linesize=100000;
    char line[linesize];

    if (argc != 6)
    {
        result = EXIT_FAILURE;
        goto finish;
    }

    ts_str = argv[1];
    te_str = argv[2];
    y0_str = argv[3];
    prt_str = argv[4];

    prec = 128;

    if (arb_set_str(ts, ts_str, prec) != 0 ||
        arb_set_str(te, te_str, prec) != 0 ||
        arb_set_str(y0, y0_str, prec) != 0)
    {
        fprintf(stderr, "FAIL: could not parse a slab parameter.\n");
        result = EXIT_FAILURE;
        goto finish;
    }

    prt = atol(prt_str);

    //process finalmata and finalmatb file
    f = fopen(argv[5], "r");
    if (f == NULL || fgets(line, linesize, f) == NULL)
    {
        fprintf(stderr, "FAIL: could not open or read the stored-sum file.\n");
        result = EXIT_FAILURE;
        goto finish;
    }

    //recover X, y0, expterms, taylorterms, digits
    if (!parse_arb_field(X, line, 1, prec) ||
        !parse_slong_field(&expterms, line, 2) ||
        !parse_slong_field(&taylorterms, line, 3) ||
        !parse_slong_field(&digits, line, 4) ||
        expterms <= 0 || taylorterms <= 0 || digits <= 0)
    {
        fprintf(stderr, "FAIL: malformed stored-sum header.\n");
        result = EXIT_FAILURE;
        goto finish;
    }

    acb_mat_init(finalmat, expterms, taylorterms);
    finalmat_initialized = 1;

    //precision
    prec = digits * 3.32192809488736 + 60;
    if (arb_set_str(serialization_scale, "1e-20", prec) != 0)
    {
        fprintf(stderr, "FAIL: could not set serialization allowance.\n");
        result = EXIT_FAILURE;
        goto finish;
    }
    arb_one(one);

    //fill finalmat
    printf("\n");
    printf("Filling stored sums matrix with %ld X %ld terms guaranteeing %ld digits accuracy...\n", expterms, taylorterms, digits);
    e=1;
    while (e <= expterms)
    {
        if (fgets(line, linesize, f) == NULL)
        {
            fprintf(stderr, "FAIL: stored-sum matrix ended early at row %ld.\n", e);
            result = EXIT_FAILURE;
            goto finish;
        }
        t=1;
        while (t <= 2*taylorterms)
        {
            if (!parse_arb_field(re, line, t, prec) ||
                !parse_arb_field(im, line, t+1, prec))
            {
                fprintf(stderr, "FAIL: malformed stored-sum entry at row %ld, field %ld.\n", e, t);
                result = EXIT_FAILURE;
                goto finish;
            }
            /* The upstream writer suppresses Arb radii while claiming
               20 decimal digits of stored-sum accuracy.  Restore an
               explicit, conservative 20-digit relative-or-absolute ball
               instead of treating the serialized midpoint as exact. */
            arb_abs(absval, re);
            arb_max(absval, absval, one, prec);
            arb_mul(serialization_error, absval, serialization_scale, prec);
            arb_add_error(re, serialization_error);
            arb_abs(absval, im);
            arb_max(absval, absval, one, prec);
            arb_mul(serialization_error, absval, serialization_scale, prec);
            arb_add_error(im, serialization_error);
            acb_set_arb_arb(tmp, re, im);
            acb_set(acb_mat_entry(finalmat, e-1, (t-1)/2), tmp);
            t=t+2;
        }
        e=e+1;
    }

    fclose(f);
    f = NULL;

    N = get_N(ts, X, prec);

TIMEIT_ONCE_START

    if (!abbeff_t_loop(res, X, y0, ts, te, N, taylorterms, expterms,
                       finalmat, prt, digits, prec))
        result = EXIT_FAILURE;

TIMEIT_ONCE_STOP;

finish: 

    if (f != NULL)
        fclose(f);
 
    if (result == EXIT_FAILURE)
    {
        flint_printf("Required inputs:\n");
        flint_printf("%s ts te y0 Prt singlematfile\n\n", argv[0]);
        flint_printf(
    " This script computes the winding number for a '3D-Barrier',\n"
    " that runs along rectangle: [X <= x <= X+1] + i[y0 <= y <= 1],\n"
    " and along: [ts <= t <= te]. It takes X and the required number\n"
    " of Taylor expansion terms from the singlematfile, that contains\n" 
    " a matrix with polynomial coefficients for precalculated sums.\n"
	" With parameter Prt the output can be controlled:\n"
    " 0 = prints rectangle summary only, 1 = prints full details.\n");
    }

    arb_clear(X);
    arb_clear(y0);
    arb_clear(ts);
    arb_clear(te);
    arb_clear(re);
    arb_clear(im);
    arb_clear(serialization_scale);
    arb_clear(serialization_error);
    arb_clear(absval);
    arb_clear(one);

    acb_clear(tmp);

    if (finalmat_initialized)
        acb_mat_clear(finalmat);
 
    flint_cleanup();

    return result;
}
