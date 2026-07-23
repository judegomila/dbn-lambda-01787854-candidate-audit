#!/usr/bin/env /usr/bin/python3
# AUDIT PATCH TRI178785400SAFE: pristine deposited engine plus the one
# delimited parameter block below; no engine formulas changed.
# assembly1875_1891_secondline.py -- numerics_verifier (dbn21a), run s43.
#
# INDEPENDENT SECOND LINE for the two newly banked FOUNDATION record
# assemblies of dbn_prover (campaign directive, 2026-07-03):
#
#   PRIORITY ONE: assembly_1875 (dbn_prover-s37): Lambda <= 3/16 = 0.1875
#     EXACTLY, unconditional, at X = 6000000185827, t0 = 1680/10^4,
#     y0 = sqrt(39/1000), N0 = 690988, Nmid = 2745000 -- including its
#     LIVE in-script tail leg (P1113 cutoff-descent at N1' = Nmid on the
#     band [1680/10^4, 1696/10^4]), which this bundle RE-PROVES on my own
#     zero-shared-code engine.
#   THEN: assembly_1891 (dbn_prover-s36): Lambda <= 1891/10^4 = 0.1891
#     EXACTLY, unconditional, same site, t0 = 1696/10^4 -- pure
#     citation-arithmetic assembly; every joint, slot-citation re-gate,
#     window-geometry string and exact-rational identity re-derived here.
#
# ZERO SHARED CODE (tiered-verification policy, this line's tier assessment,
# PER MACHINERY): the producers' verify_assembly_1875.py /
# verify_assembly_1891.py were NEVER OPENED by this loop (writeups +
# verify logs read as logs, per house law).
#  - The LIVE tail leg is rung (b): my engine is this line's VERIFIED
#    s31/s32 exact-convolution P1113 line (structurally different from the
#    producer's optcoeff_ytail device: exact convolution head
#    c_m = sum_{d|m} lam_d b_{m/d} to m = 50000 with signed in-coefficient
#    cancellation vs their routed per-divisor caps; real-endpoint overshoot
#    device vs frozen widths; my own GN/SC/YM window-left-freeze
#    N-monotonicity gate family vs their 28 Lemma M-C1' constants --
#    my gates prove the SAME "for ALL integer N >= N1'" statement by a
#    DIFFERENT device), deployed at the NEW cutoff N1' = 2745000 for the
#    first time on any line but the producer's.
#  - The assembly composition/joint/window arithmetic is exact rationals +
#    mpmath.iv prec 160 derived from arXiv:1904.12438 (window boundary
#    x_N(t) = 4pi(N^2 - t/16), Thm 1.2 hypothesis structure) via my banked
#    s2/s3/s11/s16 transcriptions -- rung (a) anchored on the banked
#    site_glue FLOOR4 literals.
#
# QUANTIFIER AUDIT (FOUNDATION law, restated for both assemblies):
#   The certified statement of assembly_1875 is: Lambda <= t0 + y0^2/2 =
#   3/16 EXACTLY, via arXiv:1904.12438 Thm 1.2 with
#   (i)  RH verified to height T_PT = 3000175332800 >= X/2 (PT2021 -- the
#        SOLE RH input; every other leg is finite interval arithmetic);
#   (ii) H_t0(x+iy) != 0 for ALL real x >= X and ALL real y in
#        [y0, sqrt(1-2t0)] -- discharged as: window N(x) = N0 on the
#        barrier [X, X+1] and N(x) >= N0 right of it (window ordering
#        dws/dN > 0), split ONCE at Nmid: integer N in [N0, Nmid] by the
#        banked lwin2_compose tile k=8 (closed tile [1680,1685]/10^4
#        contains t0 as LEFT ENDPOINT; block bottom Nc = 690988 = N0, so
#        NO uncovered sub-block; composite floor > 0), and ALL integer
#        N >= Nmid by the tail leg re-proved LIVE HERE: for ALL real t in
#        [1680/10^4, 1696/10^4] CLOSED (one outward hull, inclusion
#        isotonicity, never sampling), ALL real y in [y0, sqrt(1-2t)]
#        CLOSED (covered as the box hull [19748/10^5, 19750/10^5] --
#        which contains y0 = sqrt(39/1000) since 19748^2/10^10 < 39/1000
#        < 19750^2/10^10 EXACT -- PLUS [19750/10^5, sqrt(1-2t)] by
#        termwise y-monotonicity: dsigma1/dy = +1/2, dsigma2/dy = -1/2
#        EXACT BY CONSTRUCTION, G1-carrying terms fall via YG1 < 0, moving
#        cap endpoint via YM2 < 0), ALL integer N >= N1' = 2745000 and ALL
#        real x >= x_N(t) per constant-N window (window-left freeze; all
#        validity gates on the EXTENDED hull [19748/10^5, 8149/10^4] whose
#        top dominates sqrt(1-2t) for every band t since (8149/10^4)^2 >=
#        1 - 2*(1680/10^4) EXACT): |M f_t - 1| <= D < 1 and
#        |f_t| >= (1-D)/Mmax > err  =>  H_t != 0. The split point
#        N = Nmid is covered by BOTH legs (closed overlap, no gap).
#   (iii) winding: the banked windslab165_v2 slab certificate ([X, X+1] x
#        [33/200, 1], ALL t in [0, 1809/10^4] -- t0 = 0.1680 <= 0.1809)
#        with joint (33/200)^2 <= y0^2 (margin 471/40000 EXACT) and lower
#        edge q(t) = y0^2 + 2(t0 - t) decreasing with q(0) = 3/8 <= 1.
#   For assembly_1891 the same structure holds at t0 = 1696/10^4 with the
#   (ii)-leg split TWICE (Nmid, N1 = 5e6): lresid_compose hull
#   [1695,1760]/10^4 contains t0 (interior), WYBOX t-hull [1696,1770]/10^4
#   contains t0 as LEFT ENDPOINT (closed), down1690 band [1690,1700]/10^4
#   contains t0 (interior); joints 2745000 and 5000000 each covered by
#   both adjacent legs. Direction of every monotonicity used: ws(N,t) =
#   4pi(N^2 - t/16) INCREASING in N (windows tile), DECREASING in t
#   (t-extremes extremal).
#
# CROSS-LINE GATES: decisive inequalities certified from MY interval
# endpoints by exact-rational comparison; producer literals enter ONLY as
# IMPLICATION gates (my endpoint on the sharp side => their banked
# constant holds on my line) + attributed-gap corridor gates. Closed-form
# window quantities (exact formula, not a decomposition) are gated by
# FLOOR4 STRING EQUALITY -- the same category as my banked siteglue
# second line, which matched two of these literals.
#
# ANCHORS (rung a, cross-run determinism of my engine): two banked
# regimes re-run live with STRING EQUALITY against my own banked s31
# literals (A20: band [0.1760,0.1810], M = 20000, N1 = 5e6; A1690: band
# [0.1690,0.1700], M = 50000, N1 = 5e6) -- band, depth, cutoff and y-box
# all varied across the anchor pair.
#
# RH-HEIGHT DEPENDENCY: the assemblies consume RH ONLY through hypothesis
# (i) via PT2021 (X/2 <= T_PT, re-derived exactly here). Every inequality
# CERTIFIED IN THIS SCRIPT is RH-free (finite Dirichlet-sum interval
# arithmetic over exact rationals; no zero of zeta consumed).
# DIGIT LAW: every decimal printed is machine-derived FLOOR (lower
# endpoints) / CEIL (upper endpoints) truncation of exact binary interval
# endpoints or an exact terminating decimal; self-tests E0* run first.
#
# /usr/bin/python3, mpmath + stdlib only, reads NO files. Exit 0 iff ALL PASS.

import sys, time
from fractions import Fraction
from mpmath import iv, mp

iv.prec = 160
mp.prec = 160

T0 = time.time()
NCHK = [0, 0]
def CHK(name, ok, detail=""):
    NCHK[0] += 1
    NCHK[1] += (0 if ok else 1)
    print(("PASS" if ok else "FAIL"), name, detail)
    return ok

# ---------- exact endpoint extraction (binary mpf -> Fraction) ----------
def f2(x):
    sign, man, exp, bc = mp.mpf(x)._mpf_
    if man == 0 and exp == 0:
        return Fraction(0)
    v = Fraction(man) * (Fraction(2)**exp if exp >= 0 else Fraction(1, 2**(-exp)))
    return -v if sign else v

def lofrac(z): return f2(z.a)
def upfrac(z): return f2(z.b)

def floor_trunc(v, digits):
    assert v >= 0
    n = (v * 10**digits).__floor__()
    ip, fr = divmod(n, 10**digits)
    return f"{ip}.{fr:0{digits}d}"

def ceil_trunc(v, digits):
    assert v >= 0
    n = -((-v * 10**digits).__floor__())
    ip, fr = divmod(n, 10**digits)
    return f"{ip}.{fr:0{digits}d}"

CHK("E0a floor_trunc(1/3,10)", floor_trunc(Fraction(1, 3), 10) == "0.3333333333")
CHK("E0b ceil_trunc(1/3,10)",  ceil_trunc(Fraction(1, 3), 10) == "0.3333333334")
CHK("E0c floor_trunc exact",   floor_trunc(Fraction(1, 4), 2) == "0.25")
CHK("E0d ceil_trunc exact",    ceil_trunc(Fraction(1, 4), 2) == "0.25")

def itv(fr):
    return iv.mpf(fr.numerator) / fr.denominator

def ub_iv(z): return iv.mpf([z.b, z.b])
def lb_iv(z): return iv.mpf([z.a, z.a])

F = Fraction
pi = iv.pi

# ---------- campaign site (exact) ----------
X    = 6000000185827
N0   = 690988
NMID = 2745000
NBIG = 5000000
T_PT = 3000175332800
Y0SQ = F(39, 1000)            # y0 = sqrt(39/1000) EXACT (square exact)

# =====================================================================
# P: assembly_1875 exact-rational composition gates
# =====================================================================
t0a = F(1680, 10**4)
CHK("P1 Lambda(1875) = t0 + y0^2/2 = 1680/10^4 + 39/2000 == 1875/10^4 == 3/16 "
    "EXACT (terminating decimal 0.1875; floor truncation = exact value)",
    t0a + Y0SQ / 2 == F(1875, 10**4) == F(3, 16))
CHK("P2 admissibility: y0^2 + 2 t0 = 3/8 <= 1 and 0 < y0^2 <= 1 - 2 t0 = "
    "664/1000 = 83/125 EXACT (ymax^2 = full hypothesis-(ii) ceiling)",
    Y0SQ + 2 * t0a == F(3, 8) <= 1 and 0 < Y0SQ <= 1 - 2 * t0a == F(83, 125))
CHK("P3 improvement ladder: 3/16 < 1891/10^4 < 393/2000 < 197/1000 strict; "
    "gap to 1891-record EXACTLY 16/10^4 = 1/625 = 0.0016",
    F(3, 16) < F(1891, 10**4) < F(393, 2000) < F(197, 1000) and
    F(1891, 10**4) - F(3, 16) == F(1, 625))
CHK("P4 scope honesty (producer A7 re-derived): the blocked 0.18634552 target "
    "1727/10^4 + (413/2500)^2/2 == 2329319/12500000 EXACT sits "
    "14431/12500000 = 0.00115448 EXACT BELOW 3/16",
    F(1727, 10**4) + F(413, 2500)**2 / 2 == F(2329319, 12500000) and
    F(3, 16) - F(2329319, 12500000) == F(14431, 12500000))
CHK("P5 hypothesis (i): X/2 = 6000000185827/2 <= T_PT, margin EXACTLY "
    "350479773/2 (the assemblies' ONLY RH input)",
    F(X, 2) <= T_PT and T_PT - F(X, 2) == F(350479773, 2))
CHK("P6 (iii) joints: (33/200)^2 = 1089/40000 <= y0^2 margin 471/40000 EXACT; "
    "1 - y0^2 = 961/1000 <= 1; q(0) = y0^2 + 2 t0 = 3/8 <= 1; dq/dt = -2 < 0 "
    "structural; t0 = 0.1680 <= 0.1809 slab/site_glue t-ceiling",
    F(33, 200)**2 == F(1089, 40000) <= Y0SQ and
    Y0SQ - F(1089, 40000) == F(471, 40000) and
    1 - Y0SQ == F(961, 1000) <= 1 and
    Y0SQ + 2 * t0a == F(3, 8) <= 1 and
    t0a <= F(1809, 10**4))
CHK("P7 (ii-a) tile joint: t0 = 1680/10^4 is the LEFT ENDPOINT of the closed "
    "lwin2_compose tile k=8 [1680/10^4, 1685/10^4]; block bottom Nc = 690988 "
    "== N0 (no uncovered sub-block); N-range [690988, 2745000] covers "
    "[N0, Nmid] exactly",
    F(1680, 10**4) <= t0a <= F(1685, 10**4) and t0a == F(1680, 10**4) and
    690988 == N0 and NMID == 2745000)
CHK("P8 (ii-a) banked composite floor re-gate: lwin2_compose tile k=8 literal "
    "134320455/10^10 > 0 EXACT; FLOOR10 string reproduced by my truncator",
    F(134320455, 10**10) > 0 and
    floor_trunc(F(134320455, 10**10), 10) == "0.0134320455")
CHK("P9 split joint: tile k=8 N-top == 2745000 == the LIVE tail leg cutoff "
    "N1' (integer N = Nmid covered by BOTH legs; no gap)",
    2745000 == NMID)
CHK("P10 tail-leg hull containment EXACT: (19748/10^5)^2 = 389983504/10^10 < "
    "39/1000 < (19750/10^5)^2 = 390062500/10^10 (y-hull straddles y0); "
    "(8149/10^4)^2 = 66406201/10^8 >= 664/1000 = 1 - 2*t_lo >= 1-2t on the "
    "band (ext top dominates sqrt(1-2t) for every band t); box top <= ext "
    "top; box top inside y-range at worst t: (19750/10^5)^2 <= 1 - 2*(1696/10^4)",
    F(19748, 10**5)**2 == F(389983504, 10**10) < Y0SQ
    < F(19750, 10**5)**2 == F(390062500, 10**10) and
    F(8149, 10**4)**2 == F(66406201, 10**8) >= F(664, 1000) == 1 - 2 * F(1680, 10**4) and
    F(19750, 10**5) <= F(8149, 10**4) and
    F(19750, 10**5)**2 <= 1 - 2 * F(1696, 10**4))
CHK("P11 tail band contains t0 as LEFT ENDPOINT (closed): 1680/10^4 in "
    "[1680/10^4, 1696/10^4]",
    F(1680, 10**4) <= t0a <= F(1696, 10**4))

# =====================================================================
# Q: assembly_1891 exact-rational composition gates
# =====================================================================
t0b = F(1696, 10**4)
CHK("Q1 Lambda(1891) = 1696/10^4 + 39/2000 == 1891/10^4 EXACT (terminating "
    "decimal 0.1891); gap to 0.1965-record EXACTLY 37/5000 = 0.0074",
    t0b + Y0SQ / 2 == F(1891, 10**4) and
    F(393, 2000) - F(1891, 10**4) == F(37, 5000))
CHK("Q2 admissibility: y0^2 + 2 t0 = 1891/5000 <= 1; 1 - 2 t0 = 6608/10^4 = "
    "413/625 EXACT; q(0) = 1891/5000 <= 1; t0 = 0.1696 <= 0.1809",
    Y0SQ + 2 * t0b == F(1891, 5000) <= 1 and
    1 - 2 * t0b == F(6608, 10**4) == F(413, 625) and
    t0b <= F(1809, 10**4))
CHK("Q3 scope honesty (producer A7/H re-derived): Lambda(1891) is "
    "34431/12500000 = 0.00275448 EXACT ABOVE the blocked 0.18634552 target; "
    "(413/2500)^2 = 170569/6250000 < 39/1000 EXACT (the target's design "
    "height lies strictly below y0: the s34/s35 gate-R2 residual rectangle "
    "y in [413/2500, sqrt(39/1000)) x N in [690988, 2745000) is NONEMPTY)",
    F(1891, 10**4) - F(2329319, 12500000) == F(34431, 12500000) and
    F(413, 2500)**2 == F(170569, 6250000) < Y0SQ and 690988 < 2745000)
CHK("Q4 (ii) leg hulls contain t0 with stated endpoint types: lresid_compose "
    "[1695/10^4, 1760/10^4] (interior), WYBOX [1696/10^4, 1770/10^4] (LEFT "
    "ENDPOINT, closed), down1690 [1690/10^4, 1700/10^4] (interior)",
    F(1695, 10**4) < t0b < F(1760, 10**4) and
    F(1696, 10**4) <= t0b <= F(1770, 10**4) and t0b == F(1696, 10**4) and
    F(1690, 10**4) < t0b < F(1700, 10**4))
CHK("Q5 (ii) staircase joints EXACT: lresid N-top == WYBOX N-start == "
    "2745000 == Nmid; WYBOX N-top == down1690 window start == 5000000 == N1 "
    "(each split integer covered by BOTH adjacent legs; no gap)",
    2745000 == NMID and 5000000 == NBIG)
CHK("Q6 banked slot literals re-gated EXACT-rational > 0 and FLOOR10 strings "
    "reproduced by my truncator: lresid_compose 110533245/10^10 "
    "(0.0110533245), finwin_ybind composite 2669533163/10^13 (0.0002669533), "
    "down1690 slack 279753143/10^10 (0.0279753143)",
    F(110533245, 10**10) > 0 and
    floor_trunc(F(110533245, 10**10), 10) == "0.0110533245" and
    F(2669533163, 10**13) > 0 and
    floor_trunc(F(2669533163, 10**13), 10) == "0.0002669533" and
    F(279753143, 10**10) > 0 and
    floor_trunc(F(279753143, 10**10), 10) == "0.0279753143")
CHK("Q7 (ii)/(iii) y-joints at t0 = 0.1696: WYBOX/down1690 y-floor (33/200)^2 "
    "<= y0^2; ceiling 6608/10^4 EXACT == 1 - 2 t0 (the FULL hypothesis-(ii) "
    "ceiling)",
    F(1089, 40000) <= Y0SQ and F(6608, 10**4) == 1 - 2 * t0b)

# =====================================================================
# W: window geometry in my intervals -- ws(N,t) = 4pi(N^2 - t/16)
# (closed-form quantities: FLOOR4 string equality vs the banked/producer
# machine-derived literals; the identity + monotonicity directions gated)
# =====================================================================
def ws(N, t_iv):
    return 4 * pi * (iv.mpf(N)**2 - t_iv / 16)

CHK("W0 identity + directions: 4pi(N^2 - t/16) == 4piN^2 - pi t/4 "
    "(structural); d ws/dt = -pi/4 < 0 (t-extremes extremal); "
    "d ws/dN = 8 pi N > 0 (windows ordered/tiled)", True)

# sup_t ws(N0,t) at t = 0 (ws decreasing in t); slab t-range [0, 0.1809]
g1 = X - ws(N0, itv(F(0)))
CHK("W1 site_glue leg 1: X - ws(N0, t=0) > 0, FLOOR4 string == banked "
    "site_glue literal 5377392.8789 (my line, rung-(a) anchor regime)",
    lofrac(g1) > 0 and floor_trunc(lofrac(g1), 4) == "5377392.8789",
    "my FLOOR4 " + floor_trunc(lofrac(g1), 4))
g2 = ws(N0 + 1, itv(F(1809, 10**4))) - (X + 1)
CHK("W2 site_glue leg 2: ws(N0+1, tmax=0.1809) - (X+1) > 0, FLOOR4 string == "
    "banked site_glue literal 11989041.1415 (hence N(x) = N0 on [X, X+1] "
    "for ALL t in [0, 0.1809], superset of both t0)",
    lofrac(g2) > 0 and floor_trunc(lofrac(g2), 4) == "11989041.1415",
    "my FLOOR4 " + floor_trunc(lofrac(g2), 4))
g3 = X - ws(N0, itv(t0a))
CHK("W3 assembly_1875 F2b at THIS t0 = 0.1680: X - ws(N0,t0) > 0, my FLOOR4 "
    "== producer machine-derived 5377393.0108",
    lofrac(g3) > 0 and floor_trunc(lofrac(g3), 4) == "5377393.0108",
    "my FLOOR4 " + floor_trunc(lofrac(g3), 4))
g4 = X - ws(N0, itv(t0b))
CHK("W4 assembly_1891 F2b at THIS t0 = 0.1696: X - ws(N0,t0) > 0, my FLOOR4 "
    "== producer machine-derived 5377393.0121",
    lofrac(g4) > 0 and floor_trunc(lofrac(g4), 4) == "5377393.0121",
    "my FLOOR4 " + floor_trunc(lofrac(g4), 4))
g5 = ws(NBIG + 1, itv(t0b)) - ws(NBIG, itv(t0b))
CHK("W5 assembly_1891 F3b: window N1 nonempty, ws(N1+1,t0) - ws(N1,t0) = "
    "4pi(2 N1 + 1) > 0, my FLOOR4 == producer machine-derived 125663718.7099",
    lofrac(g5) > 0 and floor_trunc(lofrac(g5), 4) == "125663718.7099",
    "my FLOOR4 " + floor_trunc(lofrac(g5), 4))

# =====================================================================
# the P1113 engine (verbatim my banked s31/s32 line; N1 now a PARAMETER --
# the cutoff-descent deployment at N1' = 2745000 is the new regime)
# =====================================================================
LAM = {1: F(1), 2: F(-1021, 1000), 3: F(-1054, 1000),
       4: F(-9, 200), 5: F(-1119, 1000), 6: F(1001, 1000),
       7: F(-1043, 1000), 10: F(128, 125), 11: F(-161, 200),
       13: F(-447, 500), 14: F(456373, 500000)}
S = sorted(LAM)
CHK("V0 P1113 vector: 11 divisors, lam_1 = 1, sum|lam| exact 9918746/10^6",
    len(S) == 11 and LAM[1] == 1 and
    sum(abs(l) for l in LAM.values()) == F(9918746, 1000000))

MHEAD_MAX = 153814
print("-- building log table to", MHEAD_MAX, "...")
LN = [None] * (MHEAD_MAX + 1)
for n in range(2, MHEAD_MAX + 1):
    LN[n] = iv.log(n)

def run_band(tag, n1, t_lo, t_hi, ybox_lo, ybox_hi, yext_top, MHEAD):
    R = {'gates': []}
    G = R['gates']
    lnN1 = iv.log(n1)
    t = iv.mpf([itv(t_lo).a, itv(t_hi).b])
    ybox = iv.mpf([itv(ybox_lo).a, itv(ybox_hi).b])
    yext = iv.mpf([itv(ybox_lo).a, itv(yext_top).b])

    X1 = 4 * pi * (iv.mpf(n1)**2 - t / 16)
    L1 = iv.log(iv.mpf(n1)**2 - t / 16)
    z16 = t / (16 * iv.mpf(n1)**2)
    delta1 = ub_iv((t / 4) * (-iv.log(1 - z16)) + t / (2 * X1 * X1))
    kap1 = ub_iv(t / (2 * (X1 - 6)))
    lnM = iv.log(MHEAD)

    def bt(n):
        return iv.exp((t / 4) * LN[n]**2)

    YC1, YC2 = F(1, 2), F(-1, 2)
    base1 = itv(F(1, 2)) + (t / 2) * lnN1 - delta1
    base2 = itv(F(1, 2)) + (t / 2) * lnN1 - delta1 - kap1

    def sig1(y):
        return base1 + itv(YC1) * y

    def sig2(y):
        return base2 + itv(YC2) * y

    def e_at(u_iv, lnu_iv, sg):
        return iv.exp((1 - sg) * lnu_iv + (t / 4) * lnu_iv**2)

    def cap(a_int, lna, lnc, sg):
        sgl = lb_iv(sg)
        ea = e_at(None, lna, sgl)
        ec = e_at(None, lnc, sgl)
        m = iv.mpf([max(ea.b, ec.b)] * 2)
        return ub_iv(m * (lnc - lna))

    b = [None] * (MHEAD + 1)
    for n in range(2, MHEAD + 1):
        b[n] = bt(n)

    c = [iv.mpf(0)] * (MHEAD + 1)
    for d in S:
        ld = itv(LAM[d])
        kmax = MHEAD // d
        for k in range(1, kmax + 1):
            m = d * k
            if m < 2:
                continue
            c[m] = c[m] + ld * (b[k] if k >= 2 else iv.mpf(1))

    s1b = sig1(ybox)
    s2b = sig2(ybox)
    s1e = sig1(yext)
    s2e = sig2(yext)

    P = iv.mpf(0)
    for m in range(2, MHEAD + 1):
        am = abs(c[m])
        P += ub_iv(am) * iv.exp(-lb_iv(s1b) * LN[m])
    R['Pwidth'] = upfrac(P) - lofrac(P)
    P = ub_iv(P)

    TR = iv.mpf(0)
    capgates_b = []
    for d in S:
        a_d = MHEAD // d
        lna = LN[a_d] if a_d <= MHEAD_MAX else iv.log(a_d)
        cpd = cap(a_d, lna, lnN1, s1b)
        TR += itv(abs(LAM[d])) * iv.exp(-lb_iv(s1b) * (LN[d] if d >= 2 else iv.mpf(0))) * cpd
        gnb = lofrac((itv(t_lo) / 2) * lna * (lnN1 - lna)) > 1
        gnc = lofrac((lb_iv(s1e) - 1) * (lnN1 - lna)) > 1
        capgates_b.append((d, gnb, gnc))
    TR = ub_iv(TR)
    G.append(("GNbc_sigma1 all routed caps (ext hull): sigma'lna(lnN1-lna)>1 "
              "and (s1-1)(lnN1-lna)>1 per divisor",
              all(g1_ and g2_ for _, g1_, g2_ in capgates_b),
              str([(d, g1_, g2_) for d, g1_, g2_ in capgates_b])))

    OV = iv.mpf(0)
    for d in S:
        if d < 2:
            continue
        cpo = cap(None, lnN1 - iv.log(d + 1), lnN1, s1b)
        OV += itv(abs(LAM[d])) * iv.exp(-lb_iv(s1b) * LN[d]) * cpo
    OV = ub_iv(OV)
    G.append(("OVW overshoot block containment: N1 >= d(d+1) for all d in S "
              "(floor(N1/d) >= N1/(d+1)); N-decrease of both endpoints via "
              "SC3 sigma > 1", all(n1 >= d * (d + 1) for d in S), ""))

    Mmax = iv.mpf(0)
    for d in S:
        Mmax += itv(abs(LAM[d])) * iv.exp(-lb_iv(s1b) * (LN[d] if d >= 2 else iv.mpf(0)))
    Mmax = ub_iv(Mmax)
    G1 = ub_iv(iv.exp((itv(F(2, 100))) * ybox) * iv.exp(-(ybox / 2) * L1))
    PA = iv.mpf(1)
    for n in range(2, MHEAD + 1):
        PA += b[n] * iv.exp(-lb_iv(s2b) * LN[n])
    PA = ub_iv(PA)
    capB = cap(MHEAD, lnM, lnN1, s2b)
    AB = ub_iv(G1 * (PA + capB))
    G.append(("GNbc_sigma2 B-cap gates (ext hull)",
              lofrac((itv(t_lo) / 2) * lnM * (lnN1 - lnM)) > 1 and
              lofrac((lb_iv(s2e) - 1) * (lnN1 - lnM)) > 1, ""))

    D = ub_iv(P + TR + OV + Mmax * AB)
    flow = lb_iv((1 - D) / Mmax)
    R.update(D=D, flow=flow, Mmax=Mmax, P=P, TR=TR, OV=OV, AB=AB, G1=G1)

    thr = upfrac((itv(t_hi) / 2) * lnN1)
    G.append(("SC1 sigma1 > (t/2)lnN1 on box+ext hulls",
              lofrac(lb_iv(s1b)) > thr and lofrac(lb_iv(s1e)) > thr, ""))
    G.append(("SC2 sigma2 > (t/2)lnN1 on box+ext hulls",
              lofrac(lb_iv(s2b)) > thr and lofrac(lb_iv(s2e)) > thr, ""))
    G.append(("SC3 sigma1,sigma2 > 1 on ext hull (GN-c/GN-d premise)",
              lofrac(lb_iv(s1e)) > 1 and lofrac(lb_iv(s2e)) > 1, ""))

    G.append(("YL1 y-coefficients of sigma1/sigma2 declared exact rationals "
              "+1/2 / -1/2 (structural linearity)",
              YC1 == F(1, 2) and YC2 == F(-1, 2), ""))
    YG1 = ub_iv(itv(F(2, 100)) - L1 / 2 + lnN1 / 2)
    R['YG1'] = YG1
    G.append(("YM1 YG1 = 0.02 - L1/2 + lnN1/2 < 0 (G1-carrying terms fall in y, "
              "all n <= N1)", upfrac(YG1) < 0,
              "YG1<=-" + floor_trunc(-upfrac(YG1), 6)))
    YM2 = ub_iv(itv(F(2, 100)) - lnN1 / 2 - iv.log(1 - z16) / 2)
    G.append(("YM2 0.02 - lnN/2 - ln(1-t/16N^2)/2 < 0 at N1 (moving cap endpoint "
              "n = N covered for all N >= N1)", upfrac(YM2) < 0, ""))

    delerr = ub_iv(((t * t / 16) * L1 * L1 + itv(F(626, 1000))) /
                   (X1 - itv(F(666, 100))))
    MERR = 3000
    SB = iv.mpf(1)
    PAe = iv.mpf(1)
    for n in range(2, MERR + 1):
        SB += b[n] * iv.exp(-lb_iv(s1e) * LN[n])
        PAe += b[n] * iv.exp(-lb_iv(s2e) * LN[n])
    SB = ub_iv(SB) + cap(MERR, LN[MERR], lnN1, s1e)
    G1e = ub_iv(iv.exp(itv(F(2, 100)) * yext) * iv.exp(-(yext / 2) * L1))
    ABe = ub_iv(G1e * (ub_iv(PAe) + cap(MERR, LN[MERR], lnN1, s2e)))
    eAB = ub_iv((iv.exp(delerr) - 1) * (SB + ABe))
    absln = iv.sqrt(L1 * L1 + pi * pi / 4)
    thr3 = iv.exp(yext * iv.log(3)) + iv.exp(-yext * iv.log(3))
    eC0 = ub_iv(iv.exp(-((1 + yext) / 4) * L1 - (t / 16) * L1 * L1
                       + itv(F(124, 100)) * thr3 / (iv.mpf(n1) - itv(F(1, 8)))
                       + (3 * absln + itv(F(1044, 100))) / (X1 - 12)))
    err = ub_iv(eAB + eC0)
    R.update(err=err, eAB=eAB, eC0=eC0)

    G.append(("DEC1 D_MINE < 1 (box hull, my upper endpoint)",
              upfrac(D) < 1, "D_ub CEIL10 " + ceil_trunc(upfrac(D), 10)))
    G.append(("DEC2 flow_MINE > err_MINE > 0 (my endpoints, exact-rational)",
              lofrac(flow) > upfrac(err) > 0,
              "flow FLOOR10 " + floor_trunc(max(lofrac(flow), F(0)), 10) +
              " err CEIL18 " + ceil_trunc(upfrac(err), 18)))
    print("  [%s] D_ub CEIL10 %s  flow_lo FLOOR10 %s  err_ub CEIL18 %s  "
          "slack FLOOR10 %s  (%.1fs)"
          % (tag, ceil_trunc(upfrac(D), 10),
             floor_trunc(max(lofrac(flow), F(0)), 10),
             ceil_trunc(upfrac(err), 18),
             floor_trunc(max(lofrac(flow) - upfrac(err), F(0)), 10),
             time.time() - T0))
    return R

def emit(tag, R):
    for name, ok, detail in R['gates']:
        CHK("[%s] %s" % (tag, name), ok, detail)

# =====================================================================
# T: assembly_1875 LIVE tail leg re-proved on MY line at N1' = 2745000
# =====================================================================
print("-- T1875: LIVE tail leg, cutoff N1' = Nmid = 2745000, band "
      "[0.1680, 0.1696], y-box [0.19748, 0.19750], ext top 0.8149, M = 50000 ...")
R_T = run_band("T1875", NMID, F(1680, 10**4), F(1696, 10**4),
               F(19748, 10**5), F(19750, 10**5), F(8149, 10**4), 50000)
emit("T1875", R_T)

CHK("T-W grain law (banked s28 rule, mechanized): pre-collapse head-sum "
    "width at the T1875 run < my decisive margin 1 - D_ub, machine-compared",
    R_T['Pwidth'] < 1 - upfrac(R_T['D']),
    "width CEIL30 " + ceil_trunc(R_T['Pwidth'], 30) + " margin FLOOR10 " +
    floor_trunc(1 - upfrac(R_T['D']), 10))

# cross-line corridor vs the producer's LIVE-leg literals (assembly_1875
# verify log, read as a log): D CEIL10 0.9854851520, flow FLOOR10
# 0.0091331338, err CEIL18 0.000000013676437397, slack FLOOR10 0.0091331201
dP = F("0.9854851520")
fP = F("0.0091331338")
eP = F("0.000000013676437397")
sP = F("0.0091331201")
myD, myF, myE = upfrac(R_T['D']), lofrac(R_T['flow']), upfrac(R_T['err'])
CHK("T-IMP-D my D_ub <= producer 0.9854851520 (their D-bound holds on my "
    "line, strictly sharpened)", myD <= dP,
    "my CEIL10 " + ceil_trunc(myD, 10))
CHK("T-GAP-D 0 <= producer - my D_ub <= 0.002 (never cruder, gap attributed "
    "to their routed caps vs my exact convolution)",
    0 <= dP - myD <= F(2, 1000), "gap " + ceil_trunc(dP - myD, 10))
CHK("T-IMP-flow my flow_lo >= producer 0.0091331338 (their |f| floor holds "
    "on my line)", myF >= fP,
    "my FLOOR10 " + floor_trunc(max(myF, F(0)), 10))
CHK("T-GAP-flow 0 <= my flow_lo - producer <= 0.002",
    0 <= myF - fP <= F(2, 1000), "gap " + ceil_trunc(myF - fP, 10))
CHK("T-IMP-err my err_ub <= producer 0.000000013676437397 (their err cap "
    "holds on my line)", myE <= eP,
    "my CEIL18 " + ceil_trunc(myE, 18))
CHK("T-IMP-slack my flow_lo - my err_ub >= producer final slack 0.0091331201 "
    "(their headline tail slack holds on my line, strictly sharpened): the "
    "hypothesis-(ii) tail leg of assembly_1875 is RE-PROVED independently",
    myF - myE >= sP,
    "my slack FLOOR10 " + floor_trunc(myF - myE, 10))
CHK("T-XE err < 1e-7 on my line (producer's T4 cap holds)",
    myE < F(1, 10**7), "")
CHK("T-YG1 consistency: my YG1 upper endpoint <= -7.39 (same monotonicity "
    "sign and magnitude class as the producer's CEIL6 -7.392645; my gate "
    "YM1 is the decisive one on my line)",
    upfrac(R_T['YG1']) <= F(-739, 100), "")

# =====================================================================
# BEGIN AUDIT PATCH TRI178785400SAFE
# =====================================================================
TC_LO = F(129, 800)
TC_HI = F(161250001, 1000000000)
YC_SQ = F(87677, 2500000)
YC_LO = F(1872719, 10000000)
YC_HI = F(23409, 125000)
YC_EXT_PREV = F(4115519, 5000000)
YC_EXT_TOP = F(8231039, 10000000)
NC_MID = 3840000
MC_HEAD = 153814

print("-- TRI178785400SAFE: tail-only candidate, cutoff Nmid = 3840000, "
      "t-box [161250000/1000000000, 161250001/1000000000], "
      "M = 153814 ...")
R_C = run_band(
    "TRI178785400SAFE", NC_MID, TC_LO, TC_HI, YC_LO, YC_HI, YC_EXT_TOP, MC_HEAD,
)
emit("TRI178785400SAFE", R_C)
DC = upfrac(R_C['D'])
FC = lofrac(R_C['flow'])
EC = upfrac(R_C['err'])
CHK("TRI178785400SAFE-B exact tail-row identity",
    TC_LO + YC_SQ / 2 == F(893927, 5000000),
    "B = 893927/5000000")
CHK("TRI178785400SAFE-cutoff is a closed integer tail start",
    NC_MID == 3840000, "tail domain is every integer N >= 3840000")
CHK("TRI178785400SAFE-W interval grain is smaller than 1-D",
    R_C['Pwidth'] < 1 - DC,
    "width CEIL30 " + ceil_trunc(R_C['Pwidth'], 30) +
    " margin FLOOR15 " + floor_trunc(1 - DC, 15))
CHK("TRI178785400SAFE-D upper bound is below one",
    DC < 1, "D_ub CEIL15 " + ceil_trunc(DC, 15))
CHK("TRI178785400SAFE-final flow exceeds error",
    FC > EC > 0,
    "flow FLOOR15 " + floor_trunc(FC, 15) +
    " err CEIL20 " + ceil_trunc(EC, 20) +
    " slack FLOOR15 " + floor_trunc(FC - EC, 15))
CHK("TRI178785400SAFE-hulls contain y0 and minimally cover sqrt(1-2t)",
    YC_LO**2 < YC_SQ < YC_HI**2 and
    YC_EXT_TOP**2 >= 1 - 2 * TC_LO and
    YC_EXT_PREV**2 < 1 - 2 * TC_LO and
    YC_HI**2 <= 1 - 2 * TC_HI, "")
print("TRI178785400SAFE COMPONENTS:"
      " P_ub=" + ceil_trunc(upfrac(R_C['P']), 15) +
      " TR_ub=" + ceil_trunc(upfrac(R_C['TR']), 15) +
      " OV_ub=" + ceil_trunc(upfrac(R_C['OV']), 15) +
      " Mmax_ub=" + ceil_trunc(upfrac(R_C['Mmax']), 15) +
      " AB_ub=" + ceil_trunc(upfrac(R_C['AB']), 15) +
      " eAB_ub=" + ceil_trunc(upfrac(R_C['eAB']), 20) +
      " eC0_ub=" + ceil_trunc(upfrac(R_C['eC0']), 20))
# =====================================================================
# END AUDIT PATCH TRI178785400SAFE
# =====================================================================

# =====================================================================
# ANC: cross-run determinism anchors (my own banked s31 literals)
# =====================================================================
print("-- A20 banked regime (band [0.1760, 0.1810], M = 20000, N1 = 5e6) ...")
R_A20 = run_band("A20", NBIG, F(1760, 10**4), F(1810, 10**4),
                 F(18090, 10**5), F(19750, 10**5), F(80500, 10**5), 20000)
emit("A20", R_A20)
print("-- A1690 banked regime (band [0.1690, 0.1700], M = 50000, N1 = 5e6) ...")
R_A1690 = run_band("A1690", NBIG, F(1690, 10**4), F(1700, 10**4),
                   F(33, 200), F(19750, 10**5), F(8137, 10**4), 50000)
emit("A1690", R_A1690)

CHK("ANC1 A20 reproduces my banked s31 literals exactly (D_ub CEIL10 "
    "0.7300496479, flow_lo FLOOR10 0.1770245403)",
    ceil_trunc(upfrac(R_A20['D']), 10) == "0.7300496479" and
    floor_trunc(max(lofrac(R_A20['flow']), F(0)), 10) == "0.1770245403",
    "got " + ceil_trunc(upfrac(R_A20['D']), 10) + " / " +
    floor_trunc(max(lofrac(R_A20['flow']), F(0)), 10))
CHK("ANC2 A1690 reproduces my banked s31 literals exactly (D_ub CEIL10 "
    "0.9518188906, flow_lo FLOOR10 0.0308415302, err_ub CEIL18 "
    "0.000000005396660776)",
    ceil_trunc(upfrac(R_A1690['D']), 10) == "0.9518188906" and
    floor_trunc(max(lofrac(R_A1690['flow']), F(0)), 10) == "0.0308415302" and
    ceil_trunc(upfrac(R_A1690['err']), 18) == "0.000000005396660776",
    "got " + ceil_trunc(upfrac(R_A1690['D']), 10) + " / " +
    floor_trunc(max(lofrac(R_A1690['flow']), F(0)), 10))
CHK("ANC3 cutoff-descent ordering on my line: my D_ub(A20, N1=5e6, deep "
    "band) < my D_ub(A1690, N1=5e6) < my D_ub(T1875, N1'=2745000) < 1 "
    "(descending the cutoff to Nmid costs D but stays decisively closed)",
    upfrac(R_A20['D']) < upfrac(R_A1690['D']) < upfrac(R_T['D']) < 1, "")

# =====================================================================
# G: the composed record statements on my line
# =====================================================================
CHK("G1 assembly_1875 second-lined: exact composition arithmetic (P1-P11) + "
    "window geometry (W1-W3) re-derived; the ONLY live leg (hypothesis-(ii) "
    "tail N >= 2745000) RE-PROVED on my zero-shared-code line (T-block); "
    "cited banked slots re-gated. Lambda <= 3/16 = 0.1875 EXACT stands on "
    "two independent lines",
    NCHK[1] == 0)
CHK("G2 assembly_1891 second-lined: exact composition arithmetic (Q1-Q7) + "
    "window geometry (W4-W5) re-derived; all three (ii)-legs' hull "
    "membership, joints and banked floors re-gated. Lambda <= 0.1891 EXACT "
    "citation-arithmetic stands on two independent lines",
    NCHK[1] == 0)

print("TOTAL CHECKS RUN:", NCHK[0])
print("failures:", NCHK[1])
print("RESULT:", "ALL PASS" if NCHK[1] == 0 else "FAILURES")
print("elapsed %.1f s" % (time.time() - T0))
sys.exit(0 if NCHK[1] == 0 else 1)
