#include <flint/arb.h>
#include <errno.h>
#include <limits.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXK 6
#define MAXDIV 64
#ifndef PREC
#define PREC 180
#endif
#define MAXDEPTH 42
#define PAD 2e-12

static const unsigned PRIMES[MAXK] = {2, 3, 5, 7, 11, 13};

typedef struct {
    unsigned long t_num, t_den;
    unsigned long y2_num, y2_den;
    unsigned nlo, nhi;
    int k;
    int all_legs;
} config_t;

typedef struct {
    unsigned mask;
    unsigned value;
    int sign;
    arb_t logd;
    arb_t sum_logp2;
    arb_t kernel;
} divisor_t;

typedef struct {
    double llo, lhi, ylo, yhi;
    int low_branch;
    int depth;
} rect_t;

typedef struct {
    unsigned long patterns;
    unsigned long rects;
    unsigned long splits;
    unsigned long h_nonpositive;
    double worst_ratio;
    unsigned worst_gmask;
    unsigned worst_rprev;
    unsigned worst_rmax;
    rect_t worst_rect;
} stats_t;

static void usage(const char *program)
{
    fprintf(
        stderr,
        "usage: %s [--t-num U] [--t-den U] [--y2-num U] [--y2-den U] "
        "[--all-legs | --nlo U --nhi U --k 1..6]\n"
        "defaults: --t-num 16070 --t-den 100000 "
        "--y2-num 87677 --y2-den 2500000 "
        "and the lower-time P13/P11/P7/P5/P23 finite schedule\n",
        program);
}

static int parse_ulong(const char *text_value, unsigned long *out)
{
    char *end = NULL;
    errno = 0;
    unsigned long value = strtoul(text_value, &end, 10);
    if (errno || !text_value[0] || !end || *end)
        return 0;
    *out = value;
    return 1;
}

static int parse_config(int argc, char **argv, config_t *cfg)
{
    *cfg = (config_t){
        16070, 100000, 87677, 2500000, 690988, 728999, 6, 1
    };
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--help")) {
            usage(argv[0]);
            return -1;
        }
        if (!strcmp(argv[i], "--all-legs")) {
            cfg->all_legs = 1;
            continue;
        }
        if (i + 1 >= argc) {
            fprintf(stderr, "missing value after %s\n", argv[i]);
            return 0;
        }
        const char *flag = argv[i++];
        unsigned long value;
        if (!parse_ulong(argv[i], &value)) {
            fprintf(stderr, "invalid unsigned integer for %s: %s\n",
                    flag, argv[i]);
            return 0;
        }
        if (!strcmp(flag, "--t-num"))
            cfg->t_num = value;
        else if (!strcmp(flag, "--t-den"))
            cfg->t_den = value;
        else if (!strcmp(flag, "--y2-num"))
            cfg->y2_num = value;
        else if (!strcmp(flag, "--y2-den"))
            cfg->y2_den = value;
        else if (!strcmp(flag, "--nlo")) {
            if (value > UINT_MAX)
                return 0;
            cfg->nlo = (unsigned)value;
            cfg->all_legs = 0;
        } else if (!strcmp(flag, "--nhi")) {
            if (value > UINT_MAX)
                return 0;
            cfg->nhi = (unsigned)value;
            cfg->all_legs = 0;
        } else if (!strcmp(flag, "--k")) {
            if (value > INT_MAX)
                return 0;
            cfg->k = (int)value;
            cfg->all_legs = 0;
        } else {
            fprintf(stderr, "unknown option: %s\n", flag);
            return 0;
        }
    }
    if (!cfg->t_den || !cfg->y2_den || !cfg->y2_num
            || cfg->nlo < 2 || cfg->nlo > cfg->nhi
            || cfg->k < 1 || cfg->k > MAXK) {
        fprintf(stderr, "invalid parameter range\n");
        return 0;
    }
    return 1;
}

static void set_rational_ui(
    arb_t out, unsigned long numerator, unsigned long denominator)
{
    arb_set_ui(out, numerator);
    arb_div_ui(out, out, denominator, PREC);
}

static void set_box_d(arb_t out, double lo, double hi)
{
    arf_t a, b;
    arf_init(a);
    arf_init(b);
    arf_set_d(a, lo);
    arf_set_d(b, hi);
    arb_set_interval_arf(out, a, b, PREC);
    arf_clear(a);
    arf_clear(b);
}

static double lower_double(const arb_t value)
{
    arf_t bound;
    arf_init(bound);
    arb_get_lbound_arf(bound, value, PREC);
    double result = arf_get_d(bound, ARF_RND_FLOOR);
    arf_clear(bound);
    return result;
}

static double upper_double(const arb_t value)
{
    arf_t bound;
    arf_init(bound);
    arb_get_ubound_arf(bound, value, PREC);
    double result = arf_get_d(bound, ARF_RND_CEIL);
    arf_clear(bound);
    return result;
}

static int log_padding_covers(unsigned long value)
{
    arb_t exact, enclosure;
    arb_init(exact);
    arb_init(enclosure);
    arb_set_ui(exact, value);
    arb_log(exact, exact, PREC);
    double center = log((double)value);
    set_box_d(enclosure, center - PAD, center + PAD);
    int ok = arb_contains(enclosure, exact);
    arb_clear(exact);
    arb_clear(enclosure);
    return ok;
}

static void init_divisors(divisor_t *table, int k, const arb_t t)
{
    arb_t logs[MAXK];
    arb_t h, s2, tmp;
    arb_init(h);
    arb_init(s2);
    arb_init(tmp);
    for (int bit = 0; bit < k; bit++) {
        arb_init(logs[bit]);
        arb_set_ui(logs[bit], PRIMES[bit]);
        arb_log(logs[bit], logs[bit], PREC);
    }
    for (unsigned mask = 0; mask < (1u << k); mask++) {
        table[mask].mask = mask;
        table[mask].value = 1;
        table[mask].sign = 1;
        arb_init(table[mask].logd);
        arb_init(table[mask].sum_logp2);
        arb_init(table[mask].kernel);
        arb_zero(h);
        arb_zero(s2);
        int bits = 0;
        for (int bit = 0; bit < k; bit++) {
            if (mask & (1u << bit)) {
                table[mask].value *= PRIMES[bit];
                arb_add(h, h, logs[bit], PREC);
                arb_mul(tmp, logs[bit], logs[bit], PREC);
                arb_add(s2, s2, tmp, PREC);
                bits++;
            }
        }
        table[mask].sign = (bits & 1) ? -1 : 1;
        arb_set(table[mask].logd, h);
        arb_set(table[mask].sum_logp2, s2);
        /*
         * Essential signed-composite cross term:
         *   product_{p|d} b_t(p) contributes sum_{p|d} log(p)^2,
         *   while factoring b_t(n) contributes the separate log(d)^2.
         * Replacing the former by log(d)^2 would be invalid for composite d.
         */
        arb_mul(tmp, h, h, PREC);
        arb_add(tmp, tmp, s2, PREC);
        arb_mul(tmp, tmp, t, PREC);
        arb_mul_2exp_si(tmp, tmp, -2);
        arb_exp(table[mask].kernel, tmp, PREC);
    }
    for (int bit = 0; bit < k; bit++)
        arb_clear(logs[bit]);
    arb_clear(h);
    arb_clear(s2);
    arb_clear(tmp);
}

static void clear_divisors(divisor_t *table, int k)
{
    for (unsigned mask = 0; mask < (1u << k); mask++) {
        arb_clear(table[mask].logd);
        arb_clear(table[mask].sum_logp2);
        arb_clear(table[mask].kernel);
    }
}

static int verify_kernel_cross_term(
    const divisor_t *table, int k, const arb_t t)
{
    arb_t expected, factor, logp, tmp, logd2;
    arb_init(expected); arb_init(factor); arb_init(logp);
    arb_init(tmp); arb_init(logd2);
    for (unsigned mask = 0; mask < (1u << k); mask++) {
        arb_mul(logd2, table[mask].logd, table[mask].logd, PREC);
        arb_mul(tmp, t, logd2, PREC);
        arb_mul_2exp_si(tmp, tmp, -2);
        arb_exp(expected, tmp, PREC);
        int bits = 0;
        for (int bit = 0; bit < k; bit++) {
            if (!(mask & (1u << bit)))
                continue;
            bits++;
            arb_set_ui(logp, PRIMES[bit]);
            arb_log(logp, logp, PREC);
            arb_mul(tmp, logp, logp, PREC);
            arb_mul(tmp, tmp, t, PREC);
            arb_mul_2exp_si(tmp, tmp, -2);
            arb_exp(factor, tmp, PREC);
            arb_mul(expected, expected, factor, PREC);
        }
        if (!arb_overlaps(expected, table[mask].kernel)) {
            fprintf(stderr, "kernel factorization gate failed at mask=%u\n",
                    mask);
            goto fail;
        }
        if (bits >= 2 && !arb_lt(table[mask].sum_logp2, logd2)) {
            fprintf(stderr, "composite cross-term gate failed at mask=%u\n",
                    mask);
            goto fail;
        }
    }
    arb_clear(expected); arb_clear(factor); arb_clear(logp);
    arb_clear(tmp); arb_clear(logd2);
    return 1;

fail:
    arb_clear(expected); arb_clear(factor); arb_clear(logp);
    arb_clear(tmp); arb_clear(logd2);
    return 0;
}

/* Portable insertion sort: at most 64 elements. */
static void sort_indices(
    unsigned *indices, int count, const divisor_t *table)
{
    for (int i = 1; i < count; i++) {
        unsigned value = indices[i];
        int j = i - 1;
        while (j >= 0
               && table[indices[j]].value > table[value].value) {
            indices[j + 1] = indices[j];
            j--;
        }
        indices[j + 1] = value;
    }
}

static int evaluate_rect(
    const rect_t *rect,
    const divisor_t *table,
    const unsigned *active,
    int active_count,
    unsigned nlo,
    unsigned rmax,
    const arb_t t,
    double *ratio_upper,
    int *h_nonpositive)
{
    arb_t L, y, q, glogp, z0, z1, c0, c1, cp1;
    arb_t base, term, abs_c0, abs_c1, slope, h, zero, hpos;
    arb_t G, numerator, denominator, tmp, tmp2;
    arf_t numerator_upper, denominator_lower, upper;
    arb_init(L); arb_init(y); arb_init(q); arb_init(glogp);
    arb_init(z0); arb_init(z1); arb_init(c0); arb_init(c1);
    arb_init(cp1); arb_init(base); arb_init(term);
    arb_init(abs_c0); arb_init(abs_c1); arb_init(slope);
    arb_init(h); arb_init(zero); arb_init(hpos); arb_init(G);
    arb_init(numerator); arb_init(denominator);
    arb_init(tmp); arb_init(tmp2);
    arf_init(numerator_upper); arf_init(denominator_lower);
    arf_init(upper);

    set_box_d(L, rect->llo, rect->lhi);
    set_box_d(y, rect->ylo, rect->yhi);
    if (rect->low_branch) {
        arb_set_ui(q, nlo);
        arb_mul(q, q, q, PREC);
        arb_div_ui(tmp, t, 16, PREC);
        arb_sub(q, q, tmp, PREC);
    } else {
        arb_mul_2exp_si(tmp, L, 1);
        arb_exp(q, tmp, PREC);
        arb_div_ui(q, q, (ulong)rmax * (ulong)rmax, PREC);
        arb_div_ui(tmp, t, 16, PREC);
        arb_sub(q, q, tmp, PREC);
    }
    if (!arb_is_positive(q))
        goto unresolved;

    arb_log(glogp, q, PREC);
    arb_mul_2exp_si(glogp, glogp, -1);
    arb_neg(glogp, glogp);
    arb_set_si(tmp, 1);
    arb_div_ui(tmp, tmp, 50, PREC);
    arb_add(glogp, glogp, tmp, PREC);

    arb_mul(z0, t, L, PREC);
    arb_mul_2exp_si(z0, z0, -1);
    arb_add(z1, z0, y, PREC);
    arb_zero(c0);
    arb_zero(c1);
    arb_zero(cp1);
    for (int i = 0; i < active_count; i++) {
        const divisor_t *d = table + active[i];
        arb_set(base, d->kernel);
        if (d->sign < 0)
            arb_neg(base, base);

        arb_mul(tmp, z0, d->logd, PREC);
        arb_neg(tmp, tmp);
        arb_exp(tmp, tmp, PREC);
        arb_mul(tmp, tmp, base, PREC);
        arb_add(c0, c0, tmp, PREC);

        arb_mul(tmp, z1, d->logd, PREC);
        arb_neg(tmp, tmp);
        arb_exp(tmp, tmp, PREC);
        arb_mul(term, tmp, base, PREC);
        arb_add(c1, c1, term, PREC);
        arb_mul(tmp, d->logd, term, PREC);
        arb_sub(cp1, cp1, tmp, PREC);
    }

    arb_abs(abs_c0, c0);
    arb_abs(abs_c1, c1);
    arb_mul(slope, L, c1, PREC);
    arb_add(slope, slope, cp1, PREC);
    arb_abs(slope, slope);
    arb_mul_2exp_si(tmp, L, -1);
    arb_sub(tmp, glogp, tmp, PREC);
    arb_mul(tmp, tmp, abs_c1, PREC);
    arb_add(h, slope, tmp, PREC);

    if (arb_is_nonpositive(h)) {
        *ratio_upper = 0.0;
        *h_nonpositive = 1;
        goto certified;
    }
    arb_zero(zero);
    arb_max(hpos, h, zero, PREC);
    arb_add(tmp, glogp, L, PREC);
    arb_mul(tmp, tmp, y, PREC);
    arb_exp(G, tmp, PREC);
    arb_mul(numerator, G, hpos, PREC);
    arb_mul(denominator, L, abs_c0, PREC);
    arb_mul_2exp_si(denominator, denominator, -1);
    if (!arb_is_positive(denominator))
        goto unresolved;
    arb_get_ubound_arf(numerator_upper, numerator, PREC);
    arb_get_lbound_arf(denominator_lower, denominator, PREC);
    if (arf_cmp(numerator_upper, denominator_lower) >= 0)
        goto unresolved;
    arf_div(upper, numerator_upper, denominator_lower,
            PREC, ARF_RND_CEIL);
    if (arf_cmp_si(upper, 1) >= 0)
        goto unresolved;
    *ratio_upper = arf_get_d(upper, ARF_RND_CEIL);
    *h_nonpositive = 0;

certified:
    arb_clear(L); arb_clear(y); arb_clear(q); arb_clear(glogp);
    arb_clear(z0); arb_clear(z1); arb_clear(c0); arb_clear(c1);
    arb_clear(cp1); arb_clear(base); arb_clear(term);
    arb_clear(abs_c0); arb_clear(abs_c1); arb_clear(slope);
    arb_clear(h); arb_clear(zero); arb_clear(hpos); arb_clear(G);
    arb_clear(numerator); arb_clear(denominator);
    arb_clear(tmp); arb_clear(tmp2);
    arf_clear(numerator_upper); arf_clear(denominator_lower);
    arf_clear(upper);
    return 1;

unresolved:
    arb_clear(L); arb_clear(y); arb_clear(q); arb_clear(glogp);
    arb_clear(z0); arb_clear(z1); arb_clear(c0); arb_clear(c1);
    arb_clear(cp1); arb_clear(base); arb_clear(term);
    arb_clear(abs_c0); arb_clear(abs_c1); arb_clear(slope);
    arb_clear(h); arb_clear(zero); arb_clear(hpos); arb_clear(G);
    arb_clear(numerator); arb_clear(denominator);
    arb_clear(tmp); arb_clear(tmp2);
    arf_clear(numerator_upper); arf_clear(denominator_lower);
    arf_clear(upper);
    return 0;
}

static int certify_rect(
    rect_t rect,
    const divisor_t *table,
    const unsigned *active,
    int active_count,
    unsigned nlo,
    unsigned rprev,
    unsigned rmax,
    unsigned gmask,
    const arb_t t,
    stats_t *stats)
{
    double ratio_upper = 0.0;
    int h_nonpositive = 0;
    if (evaluate_rect(
            &rect, table, active, active_count, nlo, rmax, t,
            &ratio_upper, &h_nonpositive)) {
        stats->rects++;
        stats->h_nonpositive += h_nonpositive;
        if (ratio_upper > stats->worst_ratio) {
            stats->worst_ratio = ratio_upper;
            stats->worst_gmask = gmask;
            stats->worst_rprev = rprev;
            stats->worst_rmax = rmax;
            stats->worst_rect = rect;
        }
        return 1;
    }
    if (rect.depth >= MAXDEPTH) {
        fprintf(
            stderr,
            "UNRESOLVED gmask=%u r=(%u,%u] "
            "L=[%.17g,%.17g] y=[%.17g,%.17g] branch=%d\n",
            gmask, rprev, rmax,
            rect.llo, rect.lhi, rect.ylo, rect.yhi,
            rect.low_branch);
        return 0;
    }

    rect_t left = rect, right = rect;
    left.depth++;
    right.depth++;
    if ((rect.lhi - rect.llo) / 4.0
            >= rect.yhi - rect.ylo) {
        double mid = rect.llo + (rect.lhi - rect.llo) / 2.0;
        left.lhi = mid;
        right.llo = mid;
    } else {
        double mid = rect.ylo + (rect.yhi - rect.ylo) / 2.0;
        left.yhi = mid;
        right.ylo = mid;
    }
    stats->splits++;
    return certify_rect(
               left, table, active, active_count,
               nlo, rprev, rmax, gmask, t, stats)
        && certify_rect(
               right, table, active, active_count,
               nlo, rprev, rmax, gmask, t, stats);
}

static int audit_leg(
    int k, unsigned nlo, unsigned nhi, const arb_t t,
    double ylo, double yhi)
{
    divisor_t table[MAXDIV];
    stats_t stats = {0};
    init_divisors(table, k, t);
    if (!verify_kernel_cross_term(table, k, t)) {
        clear_divisors(table, k);
        return 0;
    }
    const unsigned masks = 1u << k;
    const double log2lo = log(2.0) - PAD;

    for (unsigned gmask = 0; gmask < masks; gmask++) {
        unsigned ds[MAXDIV];
        int count = 0;
        for (unsigned mask = 0; mask < masks; mask++) {
            if ((mask & ~gmask) == 0)
                ds[count++] = mask;
        }
        sort_indices(ds, count, table);
        for (int j = 0; j < count; j++) {
            stats.patterns++;
            unsigned rmax = table[ds[j]].value;
            unsigned rprev = j == 0 ? 0 : table[ds[j - 1]].value;
            unsigned active[MAXDIV];
            int active_count = 0;
            for (int i = j; i < count; i++)
                active[active_count++] = ds[i];
            if (!log_padding_covers((ulong)nhi * rmax)
                    || !log_padding_covers((ulong)nlo * rmax)
                    || (rprev
                        && !log_padding_covers((ulong)nlo * rprev))) {
                fprintf(stderr, "log-domain coverage gate failed\n");
                clear_divisors(table, k);
                return 0;
            }

            double lmin = log2lo;
            if (rprev > 0) {
                double candidate =
                    log((double)nlo * rprev) - PAD;
                if (candidate > lmin)
                    lmin = candidate;
            }
            double lmax = log((double)nhi * rmax) + PAD;
            double transition = log((double)nlo * rmax);
            if (lmin > lmax)
                continue;

            double low_hi = lmax < transition + PAD
                          ? lmax : transition + PAD;
            if (lmin <= low_hi) {
                rect_t rect = {
                    lmin, low_hi, ylo, yhi, 1, 0
                };
                if (!certify_rect(
                        rect, table, active, active_count,
                        nlo, rprev, rmax, gmask, t, &stats)) {
                    clear_divisors(table, k);
                    return 0;
                }
            }
            double high_lo = lmin > transition - PAD
                           ? lmin : transition - PAD;
            if (high_lo <= lmax) {
                rect_t rect = {
                    high_lo, lmax, ylo, yhi, 0, 0
                };
                if (!certify_rect(
                        rect, table, active, active_count,
                        nlo, rprev, rmax, gmask, t, &stats)) {
                    clear_divisors(table, k);
                    return 0;
                }
            }
        }
    }

    unsigned long expected_patterns = 1;
    for (int i = 0; i < k; i++)
        expected_patterns *= 3;
    if (stats.patterns != expected_patterns) {
        fprintf(stderr, "pattern-count gate failed: got=%lu expected=%lu\n",
                stats.patterns, expected_patterns);
        clear_divisors(table, k);
        return 0;
    }

    printf("PASS P={");
    for (int i = 0; i < k; i++)
        printf("%s%u", i ? "," : "", PRIMES[i]);
    printf(
        "} N=%u..%u kernel_cross_term=PASS "
        "patterns=%lu rects=%lu splits=%lu "
        "h_nonpositive=%lu ratio_ub=%.17g "
        "worst={gmask=%u,r=(%u,%u],L=[%.17g,%.17g],"
        "y=[%.17g,%.17g],branch=%d}\n",
        nlo, nhi, stats.patterns, stats.rects, stats.splits,
        stats.h_nonpositive, stats.worst_ratio,
        stats.worst_gmask, stats.worst_rprev, stats.worst_rmax,
        stats.worst_rect.llo, stats.worst_rect.lhi,
        stats.worst_rect.ylo, stats.worst_rect.yhi,
        stats.worst_rect.low_branch);
    clear_divisors(table, k);
    return 1;
}

int main(int argc, char **argv)
{
    config_t cfg;
    int parsed = parse_config(argc, argv, &cfg);
    if (parsed < 0)
        return 0;
    if (!parsed) {
        usage(argv[0]);
        return 2;
    }

    arb_t t, y2, ymax2, yexact_lo, yexact_hi, ybox;
    arb_t x0, inner_prime, tmp, tmp2, gamma_log_prime;
    arb_init(t); arb_init(yexact_lo); arb_init(yexact_hi);
    arb_init(y2); arb_init(ymax2); arb_init(ybox);
    arb_init(x0); arb_init(inner_prime);
    arb_init(tmp); arb_init(tmp2); arb_init(gamma_log_prime);

    set_rational_ui(t, cfg.t_num, cfg.t_den);
    set_rational_ui(y2, cfg.y2_num, cfg.y2_den);
    arb_one(ymax2);
    arb_mul_2exp_si(tmp, t, 1);
    arb_sub(ymax2, ymax2, tmp, PREC);
    if (!arb_is_nonnegative(t) || !arb_is_positive(y2)
            || !arb_is_positive(ymax2) || !arb_lt(y2, ymax2)) {
        fprintf(stderr, "exact domain gate failed: require 0<y2<1-2t\n");
        goto fail;
    }
    arb_sqrt(yexact_lo, y2, PREC);
    arb_sqrt(yexact_hi, ymax2, PREC);
    double ylo = lower_double(yexact_lo);
    double yhi = upper_double(yexact_hi);
    set_box_d(ybox, ylo, yhi);
    if (!isfinite(ylo) || !isfinite(yhi) || ylo <= 0.0 || ylo >= yhi
            || !arb_contains(ybox, yexact_lo)
            || !arb_contains(ybox, yexact_hi)) {
        fprintf(stderr, "outward y-box coverage gate failed\n");
        goto fail;
    }

    arb_set_ui(x0, cfg.nlo);
    arb_mul(x0, x0, x0, PREC);
    arb_div_ui(tmp, t, 16, PREC);
    arb_sub(x0, x0, tmp, PREC);
    if (!arb_is_positive(x0)) {
        fprintf(stderr, "q_N positivity gate failed\n");
        goto fail;
    }
    arb_mul_ui(x0, x0, 4, PREC);
    arb_const_pi(tmp, PREC);
    arb_mul(x0, x0, tmp, PREC);
    arb_mul_2exp_si(tmp, ybox, 1);
    arb_add_ui(tmp, tmp, 1, PREC);
    arb_mul_ui(tmp, tmp, 4, PREC);
    arb_mul(tmp2, x0, x0, PREC);
    arb_div(tmp, tmp, tmp2, PREC);
    arb_sub_ui(inner_prime, tmp, 3, PREC);
    if (!arb_is_negative(inner_prime)) {
        fprintf(stderr, "sigma-prime gate failed\n");
        goto fail;
    }
    arb_set_ui(gamma_log_prime, cfg.nlo);
    arb_mul(gamma_log_prime, gamma_log_prime, gamma_log_prime, PREC);
    arb_div_ui(tmp, t, 16, PREC);
    arb_sub(gamma_log_prime, gamma_log_prime, tmp, PREC);
    arb_log(gamma_log_prime, gamma_log_prime, PREC);
    arb_mul_2exp_si(gamma_log_prime, gamma_log_prime, -1);
    arb_neg(gamma_log_prime, gamma_log_prime);
    arb_set_si(tmp, 1);
    arb_div_ui(tmp, tmp, 50, PREC);
    arb_add(gamma_log_prime, gamma_log_prime, tmp, PREC);
    if (!arb_is_negative(gamma_log_prime)
            || !log_padding_covers(2)) {
        fprintf(stderr, "gamma/log-domain gate failed\n");
        goto fail;
    }

    printf(
        "ROW precision=%d t=%lu/%lu y2=%lu/%lu "
        "ybox=[%.17g,%.17g] sigma_prime>=1/2 "
        "gamma_log_prime<0 kernel_cross_term_gate=enabled\n",
        PREC, cfg.t_num, cfg.t_den, cfg.y2_num, cfg.y2_den,
        ylo, yhi);
    int ok = 1;
    if (cfg.all_legs) {
        ok &= audit_leg(6, 690988, 728999, t, ylo, yhi);
        ok &= audit_leg(5, 729000, 774999, t, ylo, yhi);
        ok &= audit_leg(4, 775000, 849999, t, ylo, yhi);
        ok &= audit_leg(3, 850000, 1074999, t, ylo, yhi);
        ok &= audit_leg(2, 1075000, 4050000, t, ylo, yhi);
    } else {
        ok &= audit_leg(
            cfg.k, cfg.nlo, cfg.nhi, t, ylo, yhi);
    }
    if (ok)
        printf(
            "RESULT PASS: direct-Triangle mass is nonincreasing "
            "on the full y interval for %s\n",
            cfg.all_legs ? "the configured lower-time five-leg schedule"
                         : "the requested leg");

    arb_clear(t); arb_clear(y2); arb_clear(ymax2);
    arb_clear(yexact_lo); arb_clear(yexact_hi); arb_clear(ybox);
    arb_clear(x0); arb_clear(inner_prime); arb_clear(tmp);
    arb_clear(tmp2); arb_clear(gamma_log_prime);
    return ok ? 0 : 1;

fail:
    arb_clear(t); arb_clear(y2); arb_clear(ymax2);
    arb_clear(yexact_lo); arb_clear(yexact_hi); arb_clear(ybox);
    arb_clear(x0); arb_clear(inner_prime); arb_clear(tmp);
    arb_clear(tmp2); arb_clear(gamma_log_prime);
    return 1;
}
