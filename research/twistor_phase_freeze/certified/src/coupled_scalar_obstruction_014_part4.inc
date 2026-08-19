    arb_sub(tmp, one, z16, wp);
    arb_log(tmp, tmp, wp);
    arb_neg(tmp, tmp);
    arb_mul(tmp, tmp, t, wp);
    arb_div_ui(tmp, tmp, 4, wp);
    arb_mul(tmp2, xN, xN, wp);
    arb_mul_ui(tmp2, tmp2, 2, wp);
    arb_div(tmp2, t, tmp2, wp);
    arb_add(tmp, tmp, tmp2, wp);
    upper_point(delta, tmp);

    arb_sub_ui(tmp, xN, 6, wp);
    arb_mul_ui(tmp, tmp, 2, wp);
    arb_div(tmp, t, tmp, wp);
    upper_point(kappa, tmp);

    /* sigma=(1+y)/2 + (t/2)log N - delta. */
    arb_add(tmp, one, y, wp);
    arb_div_ui(sigma, tmp, 2, wp);
    arb_mul(tmp, t, logN, wp);
    arb_div_ui(tmp, tmp, 2, wp);
    arb_add(sigma, sigma, tmp, wp);
    arb_sub(sigma, sigma, delta, wp);
    lower_point(sigma, sigma);
    arb_sub(sigmaA, sigma, y, wp);              /* for b(k)k^{y-sigma} */
    lower_point(sigmaA, sigmaA);
    report("cap exponents sigma and sigma-y exceed one",
           arb_gt(sigma, one) && arb_gt(sigmaA, one));

    /* G=e^{0.02y}(N^2-t/16)^(-y/2). */
    set_q(tmp, 2, 100);
    arb_mul(tmp, tmp, y, wp);
    arb_exp(tmp, tmp, wp);
    arb_mul(tmp3, y, logN2, wp);
    arb_div_ui(tmp3, tmp3, 2, wp);
    arb_neg(tmp3, tmp3);
    arb_exp(tmp3, tmp3, wp);
    arb_mul(gamma_bound, tmp, tmp3, wp);
    upper_point(gamma_bound, gamma_bound);
    arb_sub(center, one, gamma_bound, wp);
    lower_point(center, center);
    report("two-ladder center lower bound 1-G is positive", arb_gt(center, zero));

    /* Exact settled convolution heads m<=M. */
    for (i = 0; i < NLAMBDA; i++) {
        ulong d = divisors[i];
        ulong kmax = MHEAD / d;
        set_q(lam, lambda_num[i], lambda_den[i]);
        for (ulong k = 1; k <= kmax; k++) {
            ulong m = d * k;
            if (m < 2) continue;
            if (k == 1) arb_set(tmp, lam);
            else arb_mul(tmp, lam, bt + k, wp);
            arb_add(cb + m, cb + m, tmp, wp);
            if (k == 1) arb_set(tmp2, one);
            else {
                arb_mul(tmp2, y, logs + k, wp);
                arb_exp(tmp2, tmp2, wp);
            }
            arb_mul(tmp3, tmp, tmp2, wp);
            arb_add(ca + m, ca + m, tmp3, wp);
        }
    }

    arb_zero(PB); arb_zero(PA);
    for (n = 2; n <= MHEAD; n++) {
        exp_minus_sigma_log(tmp, sigma, logs + n);
        arb_abs(tmp2, cb + n);
        arb_mul(term, tmp, tmp2, wp);
        arb_add(PB, PB, term, wp);
        arb_abs(tmp2, ca + n);
        arb_mul(term, tmp, tmp2, wp);
        arb_add(PA, PA, term, wp);
    }

    /* Complete routed remainders; no redundant OV padding. */
    arb_zero(TRB); arb_zero(TRA); arb_zero(Mmax);
    for (i = 0; i < NLAMBDA; i++) {
        ulong d = divisors[i];
        ulong a = MHEAD / d;
