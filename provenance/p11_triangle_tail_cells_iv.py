#!/usr/bin/env python3
"""Rigorous interval cell reduction for the P11 Triangle Dini tail gate.

For n > K and fixed N, write R=n/N, L=log n, q=N^2-t/16 and

  a_N = -.5 log(1-t/(16N^2)),
  h = L + gamma'/gamma = .02 + log R + a_N.

After factoring the positive b_t(n), for the active divisor set
S={d|gcd(n,2310): R<=d},

  C0 = sum_{d in S} mu(d) r_d,
  Cy = sum_{d in S} mu(d) r_d d^{-y},
  Dy = sum_{d in S} mu(d) r_d d^{-y} (h-log d),
  r_d = exp((t/4)(sum_{p|d}log(p)^2+log(d)^2-2Llog d)),
  G = gamma n^y = exp(y h).

Then B=b_t(n)C0, u=gamma A=b_t(n)G Cy and
u'=b_t(n)G Dy.  Thus the branch-free tail condition

  |u'| <= .5 log(n)(|B|+|u|)

is equivalent to

  G|Dy| <= .5 L (|C0|+G|Cy|).                         (*)

The script enumerates all 32 gcd patterns and every activation sector in
R, then adaptively subdivides outward-rounded (N,R,y) boxes until (*) is
proved.  Integer/divisibility constraints are deliberately relaxed, so a
pass proves a superset of the required discrete domain.
"""

import argparse
import heapq
import math
from dataclasses import dataclass
from fractions import Fraction as F

from mpmath import iv, mp


PRIMES = (2, 3, 5, 7, 11)
D = math.prod(PRIMES)
DIVS = tuple(
    sorted(
        math.prod(
            PRIMES[i] for i in range(len(PRIMES)) if mask & (1 << i)
        )
        for mask in range(1 << len(PRIMES))
    )
)


def ivq(q):
    return iv.mpf(q.numerator) / q.denominator


def lo(x):
    return mp.mpf(x.a)


def hi(x):
    return mp.mpf(x.b)


def abs_lo(x):
    a, b = lo(x), hi(x)
    if a <= 0 <= b:
        return mp.mpf(0)
    return min(abs(a), abs(b))


def abs_hi(x):
    return max(abs(lo(x)), abs(hi(x)))


@dataclass(frozen=True)
class Cell:
    gcdpat: int
    active: tuple
    nlo: F
    nhi: F
    rlo: F
    rhi: F
    ylo: F
    yhi: F
    depth: int = 0


def midpoint_geom(a, b):
    # Exact rational near the geometric midpoint; mediant in log is not
    # rational, so use sqrt(float) only to CHOOSE an interior rational split.
    # Soundness does not depend on the choice because both closed children
    # cover the parent exactly.
    m = math.sqrt(float(a) * float(b))
    den = 10**12
    q = F(int(m * den), den)
    if not a < q < b:
        q = (a + b) / 2
    return q


def midpoint_arith(a, b):
    return (a + b) / 2


class Verifier:
    def __init__(self, tlo, thi, cutoff, prec):
        iv.prec = prec
        mp.prec = prec
        self.tlo = tlo
        self.thi = thi
        tlo_iv = ivq(tlo)
        thi_iv = ivq(thi)
        self.t = iv.mpf([tlo_iv.a, thi_iv.b])
        self.cutoff = cutoff
        self.log_cut = mp.log(cutoff + 1)
        self.logp = {p: iv.log(p) for p in PRIMES}
        self.logd = {d: iv.log(d) if d > 1 else iv.mpf(0) for d in DIVS}
        self.sumlogp2 = {}
        self.sign = {}
        for d in DIVS:
            z = iv.mpf(0)
            omega = 0
            for p in PRIMES:
                if d % p == 0:
                    z += self.logp[p] ** 2
                    omega += 1
            self.sumlogp2[d] = z
            self.sign[d] = -1 if omega & 1 else 1

    def eval_cell(self, c):
        N = iv.mpf([ivq(c.nlo).a, ivq(c.nhi).b])
        R = iv.mpf([ivq(c.rlo).a, ivq(c.rhi).b])
        y = iv.mpf([ivq(c.ylo).a, ivq(c.yhi).b])

        logN = iv.log(N)
        logR = iv.log(R)
        rawL = logN + logR
        Llo = max(self.log_cut, lo(rawL))
        Lhi = hi(rawL)
        if Lhi < self.log_cut:
            return True, mp.mpf(0), "empty"
        L = iv.mpf([Llo, Lhi])

        aN = -iv.log(1 - self.t / (16 * N * N)) / 2
        h = ivq(F(1, 50)) + logR + aN
        G = iv.exp(y * h)

        C0 = iv.mpf(0)
        Cy = iv.mpf(0)
        Dy = iv.mpf(0)
        for d in c.active:
            ld = self.logd[d]
            exponent = (
                self.t
                / 4
                * (self.sumlogp2[d] + ld * ld - 2 * L * ld)
            )
            rd = iv.exp(exponent)
            dy = iv.exp(-y * ld)
            signed = self.sign[d] * rd
            C0 += signed
            Cy += signed * dy
            Dy += signed * dy * (h - ld)

        lhs_hi = hi(G) * abs_hi(Dy)
        rhs_lo = (
            mp.mpf("0.5")
            * Llo
            * (abs_lo(C0) + lo(G) * abs_lo(Cy))
        )
        if rhs_lo <= 0:
            return False, mp.inf, "zero-denominator enclosure"
        ratio = lhs_hi / rhs_lo
        return ratio < 1, ratio, ""

    def split(self, c):
        wn = math.log(float(c.nhi / c.nlo))
        wr = math.log(float(c.rhi / c.rlo))
        wy = float(c.yhi - c.ylo)
        # Balance dimensions empirically: y widths around .005 and log widths
        # around .005 generally make the cancellation enclosures sharp.
        scores = (wn, wr, 2.0 * wy)
        which = max(range(3), key=lambda i: scores[i])
        if which == 0 and c.nlo < c.nhi:
            m = midpoint_geom(c.nlo, c.nhi)
            return (
                Cell(c.gcdpat, c.active, c.nlo, m, c.rlo, c.rhi,
                     c.ylo, c.yhi, c.depth + 1),
                Cell(c.gcdpat, c.active, m, c.nhi, c.rlo, c.rhi,
                     c.ylo, c.yhi, c.depth + 1),
            )
        if which == 1 and c.rlo < c.rhi:
            m = midpoint_geom(c.rlo, c.rhi)
            return (
                Cell(c.gcdpat, c.active, c.nlo, c.nhi, c.rlo, m,
                     c.ylo, c.yhi, c.depth + 1),
                Cell(c.gcdpat, c.active, c.nlo, c.nhi, m, c.rhi,
                     c.ylo, c.yhi, c.depth + 1),
            )
        if c.ylo < c.yhi:
            m = midpoint_arith(c.ylo, c.yhi)
            return (
                Cell(c.gcdpat, c.active, c.nlo, c.nhi, c.rlo, c.rhi,
                     c.ylo, m, c.depth + 1),
                Cell(c.gcdpat, c.active, c.nlo, c.nhi, c.rlo, c.rhi,
                     m, c.yhi, c.depth + 1),
            )
        # Fallback to any nondegenerate dimension.
        if c.nlo < c.nhi:
            m = midpoint_arith(c.nlo, c.nhi)
            return (
                Cell(c.gcdpat, c.active, c.nlo, m, c.rlo, c.rhi,
                     c.ylo, c.yhi, c.depth + 1),
                Cell(c.gcdpat, c.active, m, c.nhi, c.rlo, c.rhi,
                     c.ylo, c.yhi, c.depth + 1),
            )
        if c.rlo < c.rhi:
            m = midpoint_arith(c.rlo, c.rhi)
            return (
                Cell(c.gcdpat, c.active, c.nlo, c.nhi, c.rlo, m,
                     c.ylo, c.yhi, c.depth + 1),
                Cell(c.gcdpat, c.active, c.nlo, c.nhi, m, c.rhi,
                     c.ylo, c.yhi, c.depth + 1),
            )
        raise RuntimeError("cannot split failed point cell")


def initial_cells(nlo, nhi, ylo, yhi, cutoff):
    rmin = F(cutoff + 1, nhi)
    cells = []
    for g in DIVS:
        gd = tuple(d for d in DIVS if g % d == 0)
        previous = rmin
        for threshold in gd:
            upper = F(threshold)
            if upper < rmin:
                continue
            lower = max(previous, rmin)
            if lower <= upper:
                # On the open sector (previous divisor, threshold], exactly
                # these divisors are active.  Closed overlap at the lower
                # endpoint is harmless: the adjacent sector is also checked.
                active = tuple(d for d in gd if d >= threshold)
                cells.append(
                    Cell(g, active, F(nlo), F(nhi), lower, upper, ylo, yhi)
                )
            previous = upper
    return cells


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nlo", type=int, required=True)
    p.add_argument("--nhi", type=int, required=True)
    p.add_argument("--tlo-num", type=int, required=True)
    p.add_argument("--tlo-den", type=int, required=True)
    p.add_argument("--thi-num", type=int, required=True)
    p.add_argument("--thi-den", type=int, required=True)
    p.add_argument("--ylo-num", type=int, required=True)
    p.add_argument("--ylo-den", type=int, required=True)
    p.add_argument("--yhi-num", type=int, required=True)
    p.add_argument("--yhi-den", type=int, required=True)
    p.add_argument("--cutoff", type=int, default=6000)
    p.add_argument("--prec", type=int, default=180)
    p.add_argument("--max-depth", type=int, default=32)
    p.add_argument("--max-cells", type=int, default=2000000)
    a = p.parse_args()

    tlo = F(a.tlo_num, a.tlo_den)
    thi = F(a.thi_num, a.thi_den)
    ylo = F(a.ylo_num, a.ylo_den)
    yhi = F(a.yhi_num, a.yhi_den)
    verifier = Verifier(tlo, thi, a.cutoff, a.prec)

    pending = initial_cells(a.nlo, a.nhi, ylo, yhi, a.cutoff)
    checked = 0
    passed = 0
    split_count = 0
    max_ratio = mp.mpf(0)
    max_ratio_cell = None
    max_depth_seen = 0

    while pending:
        c = pending.pop()
        checked += 1
        if checked > a.max_cells:
            raise SystemExit("FAIL max-cells exceeded")
        ok, ratio, note = verifier.eval_cell(c)
        max_depth_seen = max(max_depth_seen, c.depth)
        if ok:
            passed += 1
            if ratio > max_ratio:
                max_ratio = ratio
                max_ratio_cell = c
            continue
        if c.depth >= a.max_depth:
            print("FAILED CELL", c)
            print("ratio", ratio, note)
            raise SystemExit(1)
        c1, c2 = verifier.split(c)
        pending.append(c1)
        pending.append(c2)
        split_count += 1
        if checked % 10000 == 0:
            print(
                "PROGRESS",
                checked,
                "pending",
                len(pending),
                "passed",
                passed,
                "splits",
                split_count,
                "max_ratio",
                max_ratio,
                flush=True,
            )

    print("RESULT ALL PASS")
    print("initial_cells", len(initial_cells(
        a.nlo, a.nhi, ylo, yhi, a.cutoff)))
    print("checked", checked)
    print("passed_leaves", passed)
    print("splits", split_count)
    print("max_depth", max_depth_seen)
    print("max_ratio_upper", max_ratio)
    print("max_ratio_cell", max_ratio_cell)


if __name__ == "__main__":
    main()
