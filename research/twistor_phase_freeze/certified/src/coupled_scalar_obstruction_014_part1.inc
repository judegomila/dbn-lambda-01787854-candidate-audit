/*
 * Fail-closed FLINT/Arb audit of the conjugate-mollified two-ladder
 * scalar certificate at the exact Lambda <= 0.14 target row.
 *
 * This program does NOT certify Lambda <= 0.14.  It certifies, with directed
 * ball arithmetic, the exact arithmetic reduction and the numerical value of
 * the strongest currently implemented all-N scalar majorant built from:
 *
 *   M(s*) F_B = 1 + R_B,
 *   conjugate(M(s*)) C_0 = 1 + R_A,
 *
 * so that the leading two ladders are centered at
 *
 *   1 + gamma M/conjugate(M),
 *
 * whose modulus is at least 1-|gamma|.  The residual gate would be
 *
 *   |R_B| + |gamma||R_A| + kappa_correction < 1-|gamma|.
 *
 * The calculation below proves that the present endpoint-cap realization of
 * this gate fails structurally at N=4,050,000 and M=153,814; the lower end of
 * the computed majorant lies strictly above the upper end of the center
 * margin.  This is a certified negative result about this majorant, not about
 * H_t and not about the existence of a stronger phase-sensitive theorem.
 */

#include <flint/arb.h>
#include <flint/flint.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MHEAD 153814
#define N1 4050000UL
#define NLAMBDA 11

static slong wp = 320;
static int checks = 0;
static int failures = 0;

static const ulong divisors[NLAMBDA] =
    {1, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14};
static const slong lambda_num[NLAMBDA] =
    {1, -1021, -1054, -9, -1119, 1001, -1043, 128, -161, -447, 456373};
static const ulong lambda_den[NLAMBDA] =
    {1, 1000, 1000, 200, 1000, 1000, 1000, 125, 200, 500, 500000};

static void report(const char *name, int ok)
{
    checks++;
    if (!ok) failures++;
    printf("[%s] %s\n", ok ? "PASS" : "FAIL", name);
}

static void set_q(arb_t out, slong num, ulong den)
{
    arb_set_si(out, num);
    arb_div_ui(out, out, den, wp);
}

static void upper_point(arb_t out, const arb_t in)
{
    arf_t x;
    arf_init(x);
    arb_get_ubound_arf(x, in, wp);
    arb_set_arf(out, x);
    arf_clear(x);
}

static void lower_point(arb_t out, const arb_t in)
{
    arf_t x;
    arf_init(x);
    arb_get_lbound_arf(x, in, wp);
    arb_set_arf(out, x);
    arf_clear(x);
}

static void print_ball(const char *name, const arb_t x)
{
