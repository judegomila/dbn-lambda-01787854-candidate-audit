    printf("%s = ", name);
    arb_printn(x, 35, ARB_STR_MORE);
    putchar('\n');
}

static arb_ptr new_vec(slong n)
{
    slong i;
    arb_ptr v = flint_malloc((size_t)n * sizeof(arb_struct));
    if (v == NULL) {
        fputs("allocation failure\n", stderr);
        exit(2);
    }
    for (i = 0; i < n; i++) arb_init(v + i);
    return v;
}

static void clear_vec(arb_ptr v, slong n)
{
    slong i;
    for (i = 0; i < n; i++) arb_clear(v + i);
    flint_free(v);
}

/* exp((1-sigma) log u + (t/4) log(u)^2). */
static void endpoint_weight(arb_t out, const arb_t logu,
                            const arb_t sigma, const arb_t t)
{
    arb_t z, w;
    arb_init(z); arb_init(w);
    arb_one(z);
    arb_sub(z, z, sigma, wp);
    arb_mul(z, z, logu, wp);
    arb_mul(w, logu, logu, wp);
    arb_mul(w, w, t, wp);
    arb_div_ui(w, w, 4, wp);
    arb_add(z, z, w, wp);
    arb_exp(out, z, wp);
    arb_clear(z); arb_clear(w);
}

static void max_upper_point(arb_t out, const arb_t a, const arb_t b)
{
    arf_t au, bu;
    arf_init(au); arf_init(bu);
    arb_get_ubound_arf(au, a, wp);
    arb_get_ubound_arf(bu, b, wp);
    arb_set_arf(out, arf_cmp(au, bu) >= 0 ? au : bu);
    arf_clear(au); arf_clear(bu);
}

static void cap_upper(arb_t out, const arb_t loga, const arb_t logc,
                      const arb_t sigma, const arb_t t)
{
    arb_t ea, ec, mx, width, product;
    arb_init(ea); arb_init(ec); arb_init(mx); arb_init(width); arb_init(product);
    endpoint_weight(ea, loga, sigma, t);
    endpoint_weight(ec, logc, sigma, t);
    max_upper_point(mx, ea, ec);
    arb_sub(width, logc, loga, wp);
    arb_mul(product, mx, width, wp);
    upper_point(out, product);
    arb_clear(ea); arb_clear(ec); arb_clear(mx); arb_clear(width); arb_clear(product);
}

static void exp_minus_sigma_log(arb_t out, const arb_t sigma, const arb_t logu)
{
    arb_t z;
    arb_init(z);
    arb_mul(z, sigma, logu, wp);
    arb_neg(z, z);
    arb_exp(out, z, wp);
    arb_clear(z);
}

static int exact_target_checks(void)
{
    /* t0=24727519/200000000, y0=1809/10000, objective 7/50. */
    uint64_t lhs = UINT64_C(24727519) + UINT64_C(1809) * UINT64_C(1809);
    uint64_t rhs = UINT64_C(28000000);
