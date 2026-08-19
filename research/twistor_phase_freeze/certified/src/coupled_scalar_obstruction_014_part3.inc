    return lhs == rhs
        && UINT64_C(24727519) * UINT64_C(800)
           < UINT64_C(129) * UINT64_C(200000000);
}

int main(int argc, char **argv)
{
    slong n, i;
    arb_ptr logs, bt, cb, ca;
    arb_t zero, one, pi, t, y, nball, n2, xN, logN, logN2;
    arb_t z16, delta, sigma, sigmaA, gamma_bound, kappa;
    arb_t tmp, tmp2, tmp3, term, lam, abslam, loga;
    arb_t PB, PA, TRB, TRA, Mmax, center, residual;
    arb_t PBlo, PAlo, TRBlo, TRAlo, residual_lo, center_hi;
    arb_t sumA, capA, Nk, correction;

    if (argc > 2) {
        fprintf(stderr, "usage: %s [precision_bits]\n", argv[0]);
        return 2;
    }
    if (argc == 2) wp = (slong)strtol(argv[1], NULL, 10);
    if (wp < 256) {
        fputs("refusing precision below 256 bits\n", stderr);
        return 2;
    }

    printf("coupled scalar 0.14 obstruction audit: precision=%ld N=%lu M=%d\n",
           (long)wp, N1, MHEAD);

    arb_init(zero); arb_init(one); arb_init(pi); arb_init(t); arb_init(y);
    arb_init(nball); arb_init(n2); arb_init(xN); arb_init(logN); arb_init(logN2);
    arb_init(z16); arb_init(delta); arb_init(sigma); arb_init(sigmaA);
    arb_init(gamma_bound); arb_init(kappa);
    arb_init(tmp); arb_init(tmp2); arb_init(tmp3); arb_init(term);
    arb_init(lam); arb_init(abslam); arb_init(loga);
    arb_init(PB); arb_init(PA); arb_init(TRB); arb_init(TRA); arb_init(Mmax);
    arb_init(center); arb_init(residual);
    arb_init(PBlo); arb_init(PAlo); arb_init(TRBlo); arb_init(TRAlo);
    arb_init(residual_lo); arb_init(center_hi);
    arb_init(sumA); arb_init(capA); arb_init(Nk); arb_init(correction);

    arb_zero(zero); arb_one(one); arb_const_pi(pi, wp);
    set_q(t, 24727519, 200000000UL);
    set_q(y, 1809, 10000UL);
    report("exact target identity and containment in existing barrier time",
           exact_target_checks());
    report("domain 0<t<1/2 and 0<y<1",
           arb_gt(t, zero) && 2 * 24727519UL < 200000000UL
           && arb_gt(y, zero) && arb_lt(y, one));
    report("target canopy square y^2+2t is exactly 7/25 below one",
           UINT64_C(1809) * UINT64_C(1809) + UINT64_C(24727519)
               == UINT64_C(28000000)
           && UINT64_C(28000000) < UINT64_C(100000000));
    report("fixed cutoff N>M>1", N1 > MHEAD && MHEAD > 1);

    logs = new_vec(MHEAD + 1);
    bt = new_vec(MHEAD + 1);
    cb = new_vec(MHEAD + 1);
    ca = new_vec(MHEAD + 1);
    arb_zero(logs); arb_zero(logs + 1);
    arb_one(bt); arb_one(bt + 1);

    for (n = 2; n <= MHEAD; n++) {
        arb_set_ui(tmp, (ulong)n);
        arb_log(logs + n, tmp, wp);
        arb_mul(tmp, logs + n, logs + n, wp);
        arb_mul(tmp, tmp, t, wp);
        arb_div_ui(tmp, tmp, 4, wp);
        arb_exp(bt + n, tmp, wp);
    }

    arb_set_ui(nball, N1);
    arb_log(logN, nball, wp);
    arb_mul(n2, nball, nball, wp);
    arb_div_ui(tmp, t, 16, wp);
    arb_sub(tmp2, n2, tmp, wp);                 /* N^2-t/16 */
    arb_log(logN2, tmp2, wp);
    arb_mul(xN, pi, tmp2, wp);
    arb_mul_ui(xN, xN, 4, wp);
    arb_set_ui(tmp, 200);
    report("x_N>200 and all denominators positive", arb_gt(xN, tmp));

    /* delta and kappa point upper bounds. */
    arb_mul_ui(tmp, n2, 16, wp);
    arb_div(z16, t, tmp, wp);
