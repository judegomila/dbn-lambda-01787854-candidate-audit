/* ===========================================================================
 * prop65_proof.c
 *
 * The computation constituting the computer-assisted proof of
 * Proposition 6.5 of the review manuscript
 * (dan-reworking/latex/exposition/gomila-proof-exposition.tex): the certified
 * tail-exponent inequality
 *
 *     (1/4) log( q(X) / N^2 )  >  h(X, y_min)_+ / (2 X^2),
 *
 * at the exact barrier parameters X = 6000000185827, N = 690988,
 * y_min = 1809/10000, where q(x) = x/(4 pi) and
 * h(x,y) = 1 - 3y + 4y(1+y)/x^2.
 *
 * The inequality is tight in the sense that the left side is of
 * order 1e-7 (q(X)/N^2 - 1 is of order 3e-7); the strict Arb ball
 * comparison separates the two sides rigorously and fails closed.
 * The program reads no input files.
 *
 * PROVENANCE AND MODIFICATIONS
 * ----------------------------
 * Written for this review as a standalone extraction of the
 * "derivative-tail exponent gate" of
 * barrier/src/TloopSinglemat_closed_cert.c in the candidate
 * repository (the computation of const1 and the strict comparison
 * const1 > log(N)/2, which is algebraically identical to the
 * displayed inequality); the arithmetic mirrors that gate line for
 * line, restated in the form of the proposition. The same gate is
 * also re-checked at run time by the barrier program
 * (code/prop612), harmlessly.
 * =========================================================================== */

#include <stdio.h>
#include <flint/arb.h>

int main(void)
{
    const slong prec = 256;
    int ok;

    arb_t X, ymin, N2, q, lhs, h, rhs, tmp, tmp2, zero;
    arb_init(X); arb_init(ymin); arb_init(N2); arb_init(q);
    arb_init(lhs); arb_init(h); arb_init(rhs);
    arb_init(tmp); arb_init(tmp2); arb_init(zero);

    arb_set_si(X, 6000000185827L);
    arb_set_si(ymin, 1809);
    arb_div_ui(ymin, ymin, 10000, prec);
    arb_set_ui(N2, 690988);
    arb_mul(N2, N2, N2, prec);
    arb_zero(zero);

    /* q(X) = X/(4 pi); lhs = (1/4) log(q(X)/N^2). */
    arb_const_pi(tmp, prec);
    arb_mul_2exp_si(tmp, tmp, 2);
    arb_div(q, X, tmp, prec);
    arb_div(lhs, q, N2, prec);
    arb_log(lhs, lhs, prec);
    arb_mul_2exp_si(lhs, lhs, -2);

    /* h = 1 - 3 y + 4 y (1+y)/X^2; rhs = max(h,0)/(2 X^2). */
    arb_set_si(h, -3);
    arb_mul(h, h, ymin, prec);
    arb_add_si(h, h, 1, prec);
    arb_add_si(tmp, ymin, 1, prec);
    arb_mul(tmp, tmp, ymin, prec);
    arb_mul_2exp_si(tmp, tmp, 2);
    arb_mul(tmp2, X, X, prec);
    arb_div(tmp, tmp, tmp2, prec);
    arb_add(h, h, tmp, prec);
    arb_max(rhs, h, zero, prec);
    arb_div(rhs, rhs, tmp2, prec);
    arb_mul_2exp_si(rhs, rhs, -1);

    printf("lhs = (1/4) log(q(X)/N^2)      = ");
    arb_printn(lhs, 25, ARB_STR_MORE);
    printf("\nrhs = h(X,ymin)_+ / (2 X^2)    = ");
    arb_printn(rhs, 25, ARB_STR_MORE);
    printf("\n");

    ok = arb_gt(lhs, rhs);
    printf("[%s] (1/4) log(q(X)/N^2) > h(X,ymin)_+/(2 X^2)\n",
           ok ? "PASS" : "FAIL");
    printf(ok ? "RESULT PASS: certified tail-exponent inequality "
                "(Proposition 6.5)\n"
              : "RESULT FAIL\n");

    arb_clear(X); arb_clear(ymin); arb_clear(N2); arb_clear(q);
    arb_clear(lhs); arb_clear(h); arb_clear(rhs);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(zero);
    flint_cleanup();
    return ok ? 0 : 1;
}
