        arb_set(loga, logs + a);
        set_q(abslam,
              lambda_num[i] < 0 ? -lambda_num[i] : lambda_num[i],
              lambda_den[i]);
        if (d == 1) arb_one(tmp);
        else exp_minus_sigma_log(tmp, sigma, logs + d);
        arb_mul(tmp2, abslam, tmp, wp);          /* |lambda|d^-sigma */
        arb_add(Mmax, Mmax, tmp2, wp);

        cap_upper(tmp, loga, logN, sigma, t);
        arb_mul(term, tmp2, tmp, wp);
        arb_add(TRB, TRB, term, wp);
        cap_upper(tmp, loga, logN, sigmaA, t);
        arb_mul(term, tmp2, tmp, wp);
        arb_add(TRA, TRA, term, wp);
    }

    /* kappa correction: G*Mmax*(N^k-1)*sum b(n)n^{y-sigma}. */
    arb_one(sumA);
    for (n = 2; n <= MHEAD; n++) {
        exp_minus_sigma_log(tmp, sigmaA, logs + n);
        arb_mul(term, bt + n, tmp, wp);
        arb_add(sumA, sumA, term, wp);
    }
    cap_upper(capA, logs + MHEAD, logN, sigmaA, t);
    arb_add(sumA, sumA, capA, wp);
    arb_mul(tmp, kappa, logN, wp);
    arb_exp(Nk, tmp, wp);
    arb_sub(Nk, Nk, one, wp);
    arb_mul(correction, gamma_bound, Mmax, wp);
    arb_mul(correction, correction, Nk, wp);
    arb_mul(correction, correction, sumA, wp);

    /* Rmajor = PB+TRB+G(PA+TRA)+correction. */
    arb_add(residual, PB, TRB, wp);
    arb_add(tmp, PA, TRA, wp);
    arb_mul(tmp, tmp, gamma_bound, wp);
    arb_add(residual, residual, tmp, wp);
    arb_add(residual, residual, correction, wp);

    lower_point(PBlo, PB); lower_point(PAlo, PA);
    lower_point(TRBlo, TRB); lower_point(TRAlo, TRA);
    lower_point(residual_lo, residual);
    upper_point(center_hi, center);

    report("current scalar gate is rigorously impossible at this cutoff/head",
           arb_gt(residual_lo, center_hi));
    report("the sufficient nonvanishing gate does not pass",
           !arb_lt(residual, center));

    puts("\nDirected Arb enclosures:");
    print_ball("sigma lower point", sigma);
    print_ball("gamma G upper point", gamma_bound);
    print_ball("center 1-G lower point", center);
    print_ball("PB", PB); print_ball("TRB", TRB);
    print_ball("PA", PA); print_ball("TRA", TRA);
    print_ball("Mmax", Mmax); print_ball("kappa correction", correction);
    print_ball("residual majorant", residual);
    print_ball("residual lower point", residual_lo);

    printf("\nTOTAL CHECKS: %d; FAILURES: %d\n", checks, failures);
    puts(failures == 0
         ? "RESULT: CERTIFIED SCALAR OBSTRUCTION FOR 0.14 PHASE-FREEZE LANE"
         : "RESULT: FAIL");

    clear_vec(logs, MHEAD + 1); clear_vec(bt, MHEAD + 1);
    clear_vec(cb, MHEAD + 1); clear_vec(ca, MHEAD + 1);
    arb_clear(zero); arb_clear(one); arb_clear(pi); arb_clear(t); arb_clear(y);
    arb_clear(nball); arb_clear(n2); arb_clear(xN); arb_clear(logN); arb_clear(logN2);
    arb_clear(z16); arb_clear(delta); arb_clear(sigma); arb_clear(sigmaA);
    arb_clear(gamma_bound); arb_clear(kappa);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(tmp3); arb_clear(term);
    arb_clear(lam); arb_clear(abslam); arb_clear(loga);
    arb_clear(PB); arb_clear(PA); arb_clear(TRB); arb_clear(TRA); arb_clear(Mmax);
    arb_clear(center); arb_clear(residual); arb_clear(PBlo); arb_clear(PAlo);
    arb_clear(TRBlo); arb_clear(TRAlo); arb_clear(residual_lo); arb_clear(center_hi);
    arb_clear(sumA); arb_clear(capA); arb_clear(Nk); arb_clear(correction);
    flint_cleanup();
    return failures == 0 ? 0 : 1;
}
