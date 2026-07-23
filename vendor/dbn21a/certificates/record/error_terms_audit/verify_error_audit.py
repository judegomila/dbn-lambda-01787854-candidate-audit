#!/usr/bin/env python3
"""Standalone verifier for ERROR_TERMS_AUDIT.md (package error_terms_audit).

Two mechanically independent transcriptions (T1: direct from the displayed
bounds (20)-(24) of arXiv:1904.12438 Theorem 1.3, summing in interval
arithmetic head-first; T2: log-space implementation written separately,
summing tail-first with its own tail-enclosure derivation) of the SAME
mathematical quantities:

  (20) |gamma|  <= e^{0.02 y} (x/4pi)^{-y/2}                       [gamma-bound]
  (21) Re s_*   >= (1+y)/2 + (t/4) log(x/4pi)
                  - t (1-3y+4y(1+y)/x^2)_+ / (2x^2)                [res-bound]
  (22) |kappa|  <= t y / (2(x-6))                                  [kappa-bound]
  (23) e_A+e_B  <= sum_{n=1}^N (1+|gamma| N^|kappa| n^y) b_n^t/n^{Re s_*}
                   * (exp(((t^2/16) log^2(x/4pi n^2) + 0.626)/(x-6.66)) - 1)
  (24) e_{C,0}  <= (x/4pi)^{-(1+y)/4} exp(-(t/16) log^2(x/4pi)
                   + 1.24(3^y+3^{-y})/(N-0.125)
                   + (3|log(x/4pi)+i pi/2| + 10.44)/(x-12))
  with b_n^t := exp((t/4) log^2 n), N := floor(sqrt(x/4pi + t/16)).

Each transcription produces a rigorous interval ENCLOSURE of each bound
(the (23) sum is enclosed as [head, head + tail-upper] with the tail over
n in (M, N] bounded by monotonicity of the summand in interval arithmetic).
Cross-check: at every point the two enclosures must INTERSECT and agree to
relative width < 1e-6 (any formula-transcription mismatch at these x ~ 5e12
scales would shift values at relative O(1), not O(1e-6)).
Evaluated at 5 representative (x, y, t) points of the dbn21a campaign region.

Also FLAGS (as a documented mismatch, not a failure of this audit's own
transcriptions) the repo discrepancy: dbn_upper_bound/pari/error_bounds.txt
habc_sharperbound uses 6.92/(xN - 6.66) where the paper's Proposition 6.6(vi)
states 6.92/(x - 12); the script certifies the sign and magnitude of that
deviation at the campaign points.

Exit 0 iff all checks pass. /usr/bin/python3 with mpmath; runtime < 120 s.
"""
import sys
from mpmath import iv, mp, mpf, floor as mpfloor

iv.dps = 40
mp.dps = 40

FAIL = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAIL.append(name)

def IV(a, b=None):
    return iv.mpf([a, a if b is None else b])

HEAD = 4000  # head length for the (23) sum enclosure

# ---------------- Transcription T1 (paper-direct, head-first) ----------------
def T1(x, y, t):
    x, y, t = IV(x), IV(y), IV(t)
    fourpi = 4 * iv.pi
    xq = x / fourpi
    N = int(mpfloor(mpf(iv.sqrt(xq + t/16).a)))
    Nv = IV(N)
    g = iv.exp(IV('0.02') * y) * xq ** (-y/2)                        # (20)
    res = (1+y)/2 + (t/4)*iv.log(xq) \
        - t * pos(1 - 3*y + 4*y*(1+y)/x**2) / (2*x**2)               # (21)
    kap = t*y / (2*(x - 6))                                          # (22)
    # (23): summand s_n = (1 + g N^kap n^y) b_n / n^res * (exp(u_n) - 1)
    pref = g * Nv**kap
    head = IV(0)
    for n in range(1, HEAD+1):
        nv = IV(n)
        bn = iv.exp((t/4) * iv.log(nv)**2)
        un = ((t**2/16) * iv.log(xq/nv**2)**2 + IV('0.626')) / (x - IV('6.66'))
        head += (1 + pref * nv**y) * bn / nv**res * (iv.exp(un) - 1)
    # tail over n in (HEAD, N]: summand is bounded by max of its values at the
    # endpoints times the count, using monotone factors:
    #   b_n/n^res = n^{(t/4)log n - res} has exponent increasing in n, so the
    #   factor is bounded by max at n=HEAD+1 and n=N (convexity in log n);
    #   (1 + pref n^y) <= (1 + pref N^y);  u_n <= u at n=1 (log^2 max).
    def term_core(n):
        nv = IV(n)
        return iv.exp((t/4)*iv.log(nv)**2) / nv**res
    u1 = ((t**2/16) * iv.log(xq)**2 + IV('0.626')) / (x - IV('6.66'))
    core_max = iv.mpf([0, max(mpf(term_core(HEAD+1).b), mpf(term_core(N).b))])
    tail_hi = IV(N - HEAD) * (1 + pref * Nv**y) * core_max * (iv.exp(u1) - 1)
    e23 = iv.mpf([mpf(head.a), mpf((head + tail_hi).b)])
    T1.head, T1.tail = head, tail_hi
    ec0 = xq ** (-(1+y)/4) * iv.exp(-(t/16)*iv.log(xq)**2
        + IV('1.24') * (3**y + 3**(-y)) / (Nv - IV('0.125'))
        + (3*iv.sqrt(iv.log(xq)**2 + (iv.pi/2)**2) + IV('10.44')) / (x - 12))  # (24)
    return N, g, res, kap, e23, ec0

def pos(u):
    # interval positive part
    return iv.mpf([max(mpf(u.a), 0), max(mpf(u.b), 0)])

# ---------------- Transcription T2 (log-space, tail-first) ----------------
def T2(x, y, t):
    X, Y, T = IV(x), IV(y), IV(t)
    LQ = iv.log(X) - iv.log(4) - iv.log(iv.pi)      # log(x/4pi)
    XQ = iv.exp(LQ)
    N = int(mpfloor(mpf(iv.sqrt(XQ + T/16).a)))
    g = iv.exp(IV('0.02')*Y - (Y/2)*LQ)                              # (20) in log space
    corr = 1 - 3*Y + 4*Y*(1+Y)*iv.exp(-2*iv.log(X))
    corr = iv.mpf([max(mpf(corr.a), 0), max(mpf(corr.b), 0)])
    res = (1+Y)/2 + (T/4)*LQ - T*corr*iv.exp(-2*iv.log(X))/2         # (21)
    kap = T*Y/2 * iv.exp(-iv.log(X - 6))                             # (22)
    lpref = iv.log(g) + kap*iv.log(IV(N))
    total = IV(0)
    for n in range(HEAD, 0, -1):                     # tail-first summation
        ln = iv.log(IV(n))
        lcore = (T/4)*ln**2 - res*ln
        lu = iv.log((T**2/16)*(LQ - 2*ln)**2 + IV('0.626')) - iv.log(X - IV('6.66'))
        u = iv.exp(lu)
        total += (1 + iv.exp(lpref + Y*ln)) * iv.exp(lcore) * (iv.exp(u) - 1)
    # independent tail derivation: exponent phi(n) = (t/4)log^2 n - res log n is
    # convex in log n => core <= max(endpoint values); count (N-HEAD) terms.
    def lcore_at(n):
        ln = iv.log(IV(n))
        return (T/4)*ln**2 - res*ln
    cmax = max(mpf(iv.exp(lcore_at(HEAD+1)).b), mpf(iv.exp(lcore_at(N)).b))
    u_max = iv.exp(iv.log((T**2/16)*LQ**2 + IV('0.626')) - iv.log(X - IV('6.66')))
    tail_hi = IV(N - HEAD) * (1 + iv.exp(lpref + Y*iv.log(IV(N)))) \
              * iv.mpf([0, cmax]) * (iv.exp(u_max) - 1)
    e23 = iv.mpf([mpf(total.a), mpf((total + tail_hi).b)])
    labs = iv.sqrt(LQ**2 + (iv.pi/2)**2)
    ec0 = iv.exp(-(1+Y)/4*LQ - (T/16)*LQ**2
        + IV('1.24')*(iv.exp(Y*iv.log(IV(3))) + iv.exp(-Y*iv.log(IV(3))))/(IV(N) - IV('0.125'))
        + (3*labs + IV('10.44'))/(X - 12))                           # (24)
    return N, g, res, kap, e23, ec0

# ---------------- the 5 campaign points ----------------
PTS = [
    ("0.20-row barrier corner", '5000000194858', '0.16733', '0.186'),
    ("0.20-row slab top",       '5000000194858', '1.0',     '0.01'),
    ("campaign interior",       '5500000000000', '0.2',     '0.15'),
    ("0.197-site (0.1809 row)", '6000000185827', '0.1809',  '0.1809'),
    ("0.197-site tuned params", '6000000185827', '0.19748', '0.1775'),
]

def overlap(a, b):
    return mpf(a.a) <= mpf(b.b) and mpf(b.a) <= mpf(a.b)

def end_agree(a, b, tol):
    """Endpoint-wise relative agreement of two enclosures of the same quantity.
    (The (23) enclosure is intrinsically wide - crude tail bound vs small head -
    so union relwidth would be dominated by enclosure width, not disagreement;
    the discriminating statistic is each endpoint pair separately.)"""
    lo_ok = abs(mpf(a.a) - mpf(b.a)) <= mpf(tol) * max(abs(mpf(a.a)), abs(mpf(b.a)), mpf('1e-300'))
    hi_ok = abs(mpf(a.b) - mpf(b.b)) <= mpf(tol) * max(abs(mpf(a.b)), abs(mpf(b.b)), mpf('1e-300'))
    return lo_ok and hi_ok

def trunc(v, d=12):
    s = mp.nstr(mpf(v), d+3)
    return s  # display only; comparisons are interval-based

for name, xs, ys, ts in PTS:
    N1, g1, r1, k1, e231, ec01 = T1(xs, ys, ts)
    N2, g2, r2, k2, e232, ec02 = T2(xs, ys, ts)
    check(f"[{name}] N agree ({N1})", N1 == N2)
    for lbl, a, b, tol in (("(20) gamma", g1, g2, '1e-12'), ("(21) Re s_*", r1, r2, '1e-12'),
                            ("(22) kappa", k1, k2, '1e-12'), ("(23) eA+eB", e231, e232, '1e-6'),
                            ("(24) eC0", ec01, ec02, '1e-6')):
        ok = overlap(a, b) and end_agree(a, b, tol)
        check(f"[{name}] {lbl} T1xT2 overlap+endpoints agree to {tol}", ok)
    print(f"   N={N1}  gamma<= {trunc(g1.b)}  Re s_*>= {trunc(r1.a)}  kappa<= {trunc(k1.b)}")
    print(f"   eA+eB <= {trunc(e231.b)}   eC0 <= {trunc(ec01.b)}   total <= {trunc((e231+ec01).b)}")
    # sanity: error total far below the campaign |f_t| floors (0.03 threshold)
    check(f"[{name}] eA+eB+eC0 upper end < 1e-3", mpf((e231 + ec01).b) < mpf('1e-3'))

# ---------------- repo-formula mismatch flag ----------------
# paper Prop (vi) factor: 6.92/(x-12); repo habc_sharperbound: 6.92/(xN-6.66).
# certify: repo denominator strictly larger => repo term strictly SMALLER, i.e.
# the repo bound is NOT a verbatim transcription of the paper (flagged), though
# numerically negligible at campaign x (relative deviation < 2e-12 certified).
x = IV('5000000194858')
paper_term = IV('6.92') / (x - 12)
repo_term = IV('6.92') / (x - IV('6.66'))
check("FLAG repo 6.92/(x-6.66) < paper 6.92/(x-12) (strict, certified)",
      mpf(repo_term.b) < mpf(paper_term.a))
rel = (paper_term - repo_term) / paper_term
check("FLAG mismatch magnitude relative < 2e-12 at campaign x", mpf(rel.b) < mpf('2e-12'))

print()
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
print("ALL CHECKS PASSED (error_terms_audit package)")
sys.exit(0)
