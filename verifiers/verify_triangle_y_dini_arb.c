#include <flint/arb.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MAXK 5
#define MAXDIV 32
#ifndef PREC
#define PREC 180
#endif
#define MAXDEPTH 42
#define PAD 2e-12

typedef struct {
    unsigned mask;
    unsigned value;
    int sign;
    arb_t logd;
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
    static const unsigned primes[MAXK] = {2, 3, 5, 7, 11};
    arb_t logs[MAXK];
    arb_t h, s2, tmp;
    arb_init(h);
    arb_init(s2);
    arb_init(tmp);
    for (int bit = 0; bit < k; bit++) {
        arb_init(logs[bit]);
        arb_set_ui(logs[bit], primes[bit]);
        arb_log(logs[bit], logs[bit], PREC);
    }
    for (unsigned mask = 0; mask < (1u << k); mask++) {
        table[mask].mask = mask;
        table[mask].value = 1;
        table[mask].sign = 1;
        arb_init(table[mask].logd);
        arb_init(table[mask].kernel);
        arb_zero(h);
        arb_zero(s2);
        int bits = 0;
        for (int bit = 0; bit < k; bit++) {
            if (mask & (1u << bit)) {
                table[mask].value *= primes[bit];
                arb_add(h, h, logs[bit], PREC);
                arb_mul(tmp, logs[bit], logs[bit], PREC);
                arb_add(s2, s2, tmp, PREC);
                bits++;
            }
        }
        table[mask].sign = (bits & 1) ? -1 : 1;
        arb_set(table[mask].logd, h);
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
        arb_clear(table[mask].kernel);
    }
}

/* Portable insertion sort: at most 32 elements. */
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
    arb_t G, numerator, denominator, ratio, tmp, tmp2;
    arf_t upper;
    arb_init(L); arb_init(y); arb_init(q); arb_init(glogp);
    arb_init(z0); arb_init(z1); arb_init(c0); arb_init(c1);
    arb_init(cp1); arb_init(base); arb_init(term);
    arb_init(abs_c0); arb_init(abs_c1); arb_init(slope);
    arb_init(h); arb_init(zero); arb_init(hpos); arb_init(G);
    arb_init(numerator); arb_init(denominator); arb_init(ratio);
    arb_init(tmp); arb_init(tmp2); arf_init(upper);

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
    if (!arb_lt(numerator, denominator))
        goto unresolved;

    arb_div(ratio, numerator, denominator, PREC);
    arb_get_ubound_arf(upper, ratio, PREC);
    *ratio_upper = arf_get_d(upper, ARF_RND_CEIL);
    *h_nonpositive = 0;

certified:
    arb_clear(L); arb_clear(y); arb_clear(q); arb_clear(glogp);
    arb_clear(z0); arb_clear(z1); arb_clear(c0); arb_clear(c1);
    arb_clear(cp1); arb_clear(base); arb_clear(term);
    arb_clear(abs_c0); arb_clear(abs_c1); arb_clear(slope);
    arb_clear(h); arb_clear(zero); arb_clear(hpos); arb_clear(G);
    arb_clear(numerator); arb_clear(denominator); arb_clear(ratio);
    arb_clear(tmp); arb_clear(tmp2); arf_clear(upper);
    return 1;

unresolved:
    arb_clear(L); arb_clear(y); arb_clear(q); arb_clear(glogp);
    arb_clear(z0); arb_clear(z1); arb_clear(c0); arb_clear(c1);
    arb_clear(cp1); arb_clear(base); arb_clear(term);
    arb_clear(abs_c0); arb_clear(abs_c1); arb_clear(slope);
    arb_clear(h); arb_clear(zero); arb_clear(hpos); arb_clear(G);
    arb_clear(numerator); arb_clear(denominator); arb_clear(ratio);
    arb_clear(tmp); arb_clear(tmp2); arf_clear(upper);
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
    int k, unsigned nlo, unsigned nhi, const arb_t t)
{
    divisor_t table[MAXDIV];
    stats_t stats = {0};
    init_divisors(table, k, t);
    const unsigned masks = 1u << k;
    const double ylo = 0.187271994702891;
    const double yhi = 0.823103881657717;
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

    printf(
        "PASS P=");
    for (int i = 0; i < k; i++)
        printf("%u", (unsigned[]){2,3,5,7,11}[i]);
    printf(
        " N=%u..%u patterns=%lu rects=%lu splits=%lu "
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

int main(void)
{
    arb_t t, yexact_lo, yexact_hi, ybox, x0, inner_prime;
    arb_t tmp, tmp2, gamma_log_prime;
    arb_init(t); arb_init(yexact_lo); arb_init(yexact_hi);
    arb_init(ybox); arb_init(x0); arb_init(inner_prime);
    arb_init(tmp); arb_init(tmp2); arb_init(gamma_log_prime);
    arb_set_ui(t, 16125);
    arb_div_ui(t, t, 100000, PREC);
    arb_set_ui(yexact_lo, 350708);
    arb_div_ui(yexact_lo, yexact_lo, 10000000, PREC);
    arb_sqrt(yexact_lo, yexact_lo, PREC);
    arb_set_ui(yexact_hi, 1);
    arb_mul_2exp_si(tmp, t, 1);
    arb_sub(yexact_hi, yexact_hi, tmp, PREC);
    arb_sqrt(yexact_hi, yexact_hi, PREC);
    set_box_d(
        ybox,
        0.187271994702891,
        0.823103881657717);
    if (!arb_contains(ybox, yexact_lo)
            || !arb_contains(ybox, yexact_hi)) {
        fprintf(stderr, "y-box coverage failed\n");
        return 1;
    }

    arb_set_ui(x0, 690988);
    arb_mul(x0, x0, x0, PREC);
    arb_div_ui(tmp, t, 16, PREC);
    arb_sub(x0, x0, tmp, PREC);
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
        return 1;
    }
    arb_set_ui(gamma_log_prime, 690988);
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
        return 1;
    }

    printf(
        "ROW t=16125/100000 y2=350708/10000000 "
        "ybox=[0.187271994702891,0.823103881657717] "
        "sigma_prime>=1/2 gamma_log_prime<0\n");
    int ok = 1;
    ok &= audit_leg(5, 690988, 728999, t);
    ok &= audit_leg(4, 729000, 818999, t);
    ok &= audit_leg(3, 819000, 1027999, t);
    ok &= audit_leg(2, 1028000, 3840000, t);
    if (ok)
        printf(
            "RESULT PASS: direct-Triangle mass is nonincreasing "
            "on the full y interval\n");

    arb_clear(t); arb_clear(yexact_lo); arb_clear(yexact_hi);
    arb_clear(ybox); arb_clear(x0); arb_clear(inner_prime);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(gamma_log_prime);
    return ok ? 0 : 1;
}
