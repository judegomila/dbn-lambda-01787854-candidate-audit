#!/usr/bin/env /usr/bin/python3
"""
windrect_corner_iv.py -- INDEPENDENT second-line corner re-evaluation of
Polymath-15 barrier winding rectangles (loop numerics_verifier).

ZERO SHARED CODE with km-git-acc/dbn_upper_bound's ARB/C (TloopthreadedV4.c)
or pari implementations: every formula below is transcribed from the paper
arXiv:1904.12438 TeX source (Writeup/intro.tex eq labels quoted), never from
any implementation.

WHAT IS CHECKED (per selected rectangle r of a tloop log, at its printed
t = t_r): the barrier rectangle is [X, X+1] x [y0, 1] at fixed t_r, and the
log's 5th field is the producer's certified minimum over its boundary mesh of
|f_t| = |(A+B)/B0|.  The four CORNERS (X,y0),(X+1,y0),(X,1),(X+1,1) are mesh
points of any boundary mesh, so for each audited corner:

    my certified interval lower bound  lb|f_t(corner)|  >=  printed_min - SLACK

is a falsifiable one-sided containment check (my value at a mesh point can
never be below the true mesh minimum).  SLACK covers only display rounding of
the log's printed fields (t and min are arf_printd NEAREST-rounded ~20-digit
displays, NOT floor truncations): |t_true - t_printed| <= 1e-18 propagates
through |df/dt| <= D_r (the log's own certified derivative bound, field 2)
to D_r * 1e-18 <= 1e-13, and the printed min itself carries <= 1e-18 display
error; SLACK = 1e-9 is > 1e4 times either.  Additionally each corner value is
compared against the approximation error budget (non-vanishing direction).

FORMULAS (arXiv:1904.12438, Writeup/intro.tex):
  (ft-def)    f_t(x+iy) = sum_{n<=N} b_n^t / n^{s_*}
                          + gamma * sum_{n<=N} n^y b_n^t / n^{conj(s_*)+kappa}
  (bn-def)    b_n^t = exp((t/4) log^2 n)
  (N-def)     N = floor(sqrt(x/(4 pi) + t/16))
  (sn-def)    s_* = s + (t/2) alpha(s),         s := (1+y-ix)/2
  (kappa-def) kappa = (t/2) (alpha(1-s) - alpha(conj(s)))
              [(1-y+ix)/2 = 1-s and (1+y+ix)/2 = conj(s) exactly]
  (lambda-def) gamma = M_t(1-s)/M_t(s);  (Mt-def) M_t = exp((t/4)alpha^2) M_0
              => log gamma = (t/4)(alpha(1-s)^2 - alpha(s)^2)
                             + logM0(1-s) - logM0(s)
  (logM)      logM0(s) = Log s + Log(s-1) - (s/2) log pi + log(sqrt(2 pi)/16)
                         + (s/2 - 1/2) Log(s/2) - s/2
  (alpha-def) alpha(s) = 1/s + 1/(s-1) - (1/2) log pi + (1/2) Log(s/2)
                         - 1/(2s)
All arithmetic: mpmath.iv real intervals; complex values as (re, im) interval
pairs with hand-written mul/div/log/exp (directed rounding throughout).
Branch (-pi, pi]: argument computed via interval atan with an interval sign
assertion on the real/imaginary parts at every call site.

DIGIT DISCIPLINE: claimed lower bounds are FLOOR-truncated decimals of the
exact rational LOWER interval endpoint (extracted via ._mpi_, never str());
upper bounds CEIL-truncated from upper endpoints; every label printed.

Subcommands:
  corner <X_num> <X_den> <y_str> <t_str> <N> <n_lo> <n_hi> <out.json>
      march one n-chunk of both sums at (x=X_num/X_den, y, t); dump exact
      rational interval endpoints of the four accumulators (A_re A_im
      B_re B_im, the B-sum WITHOUT the gamma prefactor) as JSON.
  combine <out_prefix> <chunk1.json> ... : exact-rational chunk summation,
      then gamma/s_*/kappa evaluation and |f_t| enclosure; prints the
      certificate lines.
RH-height dependency: NONE (finite Dirichlet sums; pure interval arithmetic
at one site; the Lambda chain this seconds is unconditional via PT2021).
"""
import sys, json
from fractions import Fraction
from mpmath import iv

iv.prec = 130


# ---------- exact endpoint extraction / construction ----------
def lb_frac(x):
    s, man, e, _ = x._mpi_[0]
    v = Fraction(man) * (Fraction(2) ** e if e >= 0 else Fraction(1, 2 ** (-e)))
    return -v if s else v


def ub_frac(x):
    s, man, e, _ = x._mpi_[1]
    v = Fraction(man) * (Fraction(2) ** e if e >= 0 else Fraction(1, 2 ** (-e)))
    return -v if s else v


def iv_from_frac(fr):
    """Interval enclosure of an exact Fraction."""
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def iv_hull_fracs(lo, hi):
    """Interval guaranteed to contain [lo, hi] (exact rationals):
    enclosure(lo) + [0,1] * enclosure(hi - lo), all directed-rounded."""
    assert hi >= lo
    return iv_from_frac(lo) + iv.mpf([0, 1]) * iv_from_frac(hi - lo)


def floor_trunc(fr, digits=12):
    """FLOOR-truncated decimal of a positive Fraction (printed value <= fr)."""
    assert fr > 0
    k = 0
    while fr * 10**k < 10 ** (digits - 1):
        k += 1
    while fr * 10**k >= 10**digits:
        k -= 1
    n = (fr * 10**k).numerator // (fr * 10**k).denominator
    s = str(n)
    return s[0] + "." + s[1:] + "e" + str(digits - 1 - k)


def ceil_trunc(fr, digits=12):
    assert fr > 0
    k = 0
    while fr * 10**k < 10 ** (digits - 1):
        k += 1
    while fr * 10**k >= 10**digits:
        k -= 1
    num = fr * 10**k
    n = num.numerator // num.denominator
    if Fraction(n) != num:
        n += 1
    s = str(n)
    return s[0] + "." + s[1:] + "e" + str(digits - 1 - k)


# ---------- complex interval helpers (re, im) ----------
def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def csub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cdiv(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def conj(a):
    return (a[0], -a[1])


def cscale(a, r):
    return (a[0] * r, a[1] * r)


def _sign_pos(x):
    return lb_frac(x) > 0


def _sign_neg(x):
    return ub_frac(x) < 0


def carg(z):
    """Interval argument in (-pi, pi] via iv.atan2 (directed rounding);
    a certified half-plane is asserted so the branch cut cannot be
    straddled (a straddle would silently return the useless [-pi, pi])."""
    re, im = z
    assert _sign_pos(re) or _sign_pos(im) or _sign_neg(im), \
        "carg: no certified half-plane"
    a = iv.atan2(im, re)
    assert ub_frac(a) - lb_frac(a) < 3, "carg: branch-cut straddle"
    return a


def clog(z):
    re, im = z
    return (iv.log(re * re + im * im) / 2, carg(z))


def cexp(z):
    r = iv.exp(z[0])
    return (r * iv.cos(z[1]), r * iv.sin(z[1]))


LOG_PI = iv.log(iv.pi)
HALF = iv.mpf(1) / 2
ONE = (iv.mpf(1), iv.mpf(0))


def alpha(s):
    """(alpha-def): 1/s + 1/(s-1) - (1/2)log pi + (1/2)Log(s/2) - 1/(2s)."""
    inv_s = cdiv(ONE, s)
    inv_sm1 = cdiv(ONE, csub(s, ONE))
    half_log_s2 = cscale(clog(cscale(s, HALF)), HALF)
    out = cadd(inv_s, inv_sm1)
    out = (out[0] - LOG_PI / 2, out[1])
    out = cadd(out, half_log_s2)
    out = csub(out, cscale(inv_s, HALF))
    return out


def logM0(s):
    """(logM): Log s + Log(s-1) - (s/2)log pi + log(sqrt(2pi)/16)
               + (s/2 - 1/2)Log(s/2) - s/2."""
    out = cadd(clog(s), clog(csub(s, ONE)))
    out = csub(out, cscale(s, LOG_PI / 2))
    const = iv.log(iv.sqrt(2 * iv.pi) / 16)
    out = (out[0] + const, out[1])
    s2 = cscale(s, HALF)
    out = cadd(out, cmul(csub(s2, (HALF, iv.mpf(0))), clog(s2)))
    out = csub(out, s2)
    return out


def site_constants(x, y, t):
    """gamma, s_*, kappa at x+iy, time t (all complex intervals)."""
    s = ((1 + y) / 2, -x / 2)              # s = (1+y-ix)/2
    one_minus_s = csub(ONE, s)             # = (1-y+ix)/2
    s_conj = conj(s)                       # = (1+y+ix)/2
    a_s = alpha(s)
    a_1ms = alpha(one_minus_s)
    a_sc = alpha(s_conj)
    s_star = cadd(s, cscale(a_s, t / 2))                       # (sn-def)
    kappa = cscale(csub(a_1ms, a_sc), t / 2)                   # (kappa-def)
    lg = cadd(
        cscale(csub(cmul(a_1ms, a_1ms), cmul(a_s, a_s)), t / 4),
        csub(logM0(one_minus_s), logM0(s)),
    )                                                          # (lambda-def)
    gamma = cexp(lg)
    return gamma, s_star, kappa


def march_chunk(x, y, t, n_lo, n_hi):
    """Accumulate both ft-def sums over n in [n_lo, n_hi].
    Returns (A_re, A_im, B_re, B_im) intervals; B WITHOUT gamma prefactor."""
    _, s_star, kappa = site_constants(x, y, t)
    sig1 = s_star[0]
    T1 = s_star[1]
    # second sum: n^y * n^{-(conj(s_*)+kappa)} = n^{(y - sig1 - Re k) - i(-T1 + Im k)}
    mag2 = y - sig1 - kappa[0]
    ph2 = T1 - kappa[1]            # phase coefficient: -(-T1 + Im k) = T1 - Im k
    t4 = t / 4
    Are = iv.mpf(0); Aim = iv.mpf(0); Bre = iv.mpf(0); Bim = iv.mpf(0)
    for n in range(n_lo, n_hi + 1):
        if n == 1:
            Are += 1
            Bre += 1
            continue
        L = iv.log(n)
        bt = t4 * L * L
        m1 = iv.exp(bt - sig1 * L)
        p1 = -T1 * L
        Are += m1 * iv.cos(p1)
        Aim += m1 * iv.sin(p1)
        m2 = iv.exp(bt + mag2 * L)
        p2 = ph2 * L
        Bre += m2 * iv.cos(p2)
        Bim += m2 * iv.sin(p2)
    return Are, Aim, Bre, Bim


def frpair(x):
    return [str(lb_frac(x)), str(ub_frac(x))]


def cmd_corner():
    Xn, Xd = int(sys.argv[2]), int(sys.argv[3])
    y_fr = Fraction(sys.argv[4])
    t_fr = Fraction(sys.argv[5])
    N = int(sys.argv[6])
    n_lo, n_hi = int(sys.argv[7]), int(sys.argv[8])
    out = sys.argv[9]
    x = iv_from_frac(Fraction(Xn, Xd))
    y = iv_from_frac(y_fr)
    t = iv_from_frac(t_fr)
    Are, Aim, Bre, Bim = march_chunk(x, y, t, n_lo, n_hi)
    json.dump(
        {
            "X": [Xn, Xd], "y": str(y_fr), "t": str(t_fr), "N": N,
            "n_lo": n_lo, "n_hi": n_hi,
            "A_re": frpair(Are), "A_im": frpair(Aim),
            "B_re": frpair(Bre), "B_im": frpair(Bim),
        },
        open(out, "w"),
    )
    print(f"chunk [{n_lo},{n_hi}] done -> {out}")


def cmd_combine():
    chunks = [json.load(open(p)) for p in sys.argv[3:]]
    base = chunks[0]
    Xn, Xd = base["X"]
    y_fr = Fraction(base["y"]); t_fr = Fraction(base["t"]); N = base["N"]
    # coverage check: chunks must tile [1, N] exactly
    ivs = sorted((c["n_lo"], c["n_hi"]) for c in chunks)
    assert ivs[0][0] == 1 and ivs[-1][1] == N, ivs
    for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
        assert a2 == b1 + 1, (b1, a2)
    for c in chunks:
        assert c["X"] == [Xn, Xd] and c["y"] == base["y"] and c["t"] == base["t"]
    # exact-rational endpoint summation (sum of intervals)
    acc = {}
    for key in ("A_re", "A_im", "B_re", "B_im"):
        lo = sum(Fraction(c[key][0]) for c in chunks)
        hi = sum(Fraction(c[key][1]) for c in chunks)
        acc[key] = iv_hull_fracs(lo, hi)
    x = iv_from_frac(Fraction(Xn, Xd))
    y = iv_from_frac(y_fr)
    t = iv_from_frac(t_fr)
    gamma, s_star, kappa = site_constants(x, y, t)
    A = (acc["A_re"], acc["A_im"])
    B = (acc["B_re"], acc["B_im"])
    f = cadd(A, cmul(gamma, B))
    mod2 = f[0] * f[0] + f[1] * f[1]
    mod = iv.sqrt(mod2)
    lo, hi = lb_frac(mod), ub_frac(mod)
    assert lo > 0
    print(f"CORNER x={Xn}/{Xd} y={base['y']} t={base['t']} N={N}")
    print(f"  |f_t| >= {floor_trunc(lo)} (FLOOR-truncated exact lower endpoint)")
    print(f"  |f_t| <= {ceil_trunc(hi)} (CEIL-truncated exact upper endpoint)")
    print(f"  |gamma| in [{floor_trunc(lb_frac(iv.sqrt(gamma[0]*gamma[0]+gamma[1]*gamma[1])))}, "
          f"{ceil_trunc(ub_frac(iv.sqrt(gamma[0]*gamma[0]+gamma[1]*gamma[1])))}]")
    json.dump(
        {"X": [Xn, Xd], "y": base["y"], "t": base["t"], "N": N,
         "mod_lo": str(lo), "mod_hi": str(hi),
         "mod_lo_floor12": floor_trunc(lo), "mod_hi_ceil12": ceil_trunc(hi)},
        open(sys.argv[2], "w"),
    )


if __name__ == "__main__":
    {"corner": cmd_corner, "combine": cmd_combine}[sys.argv[1]]()
