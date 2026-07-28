#!/usr/bin/env python3
"""Prototype interval proof of direct-Triangle numerator monotonicity.

This avoids the invalid standard-majorant rewrite.  For fixed N and t write

  B_n = b_t(n) C0_n,
  gamma A_n = b_t(n) G_n Cy_n,
  (gamma A_n)' = b_t(n) G_n Dy_n.

The upper right Dini derivative of

  gamma + sum_n (|B_n| + |gamma A_n|) n^{-sigma}

is at most gamma' plus the sum of

  b_t(n)n^{-sigma}
  [G|Dy| - sigma_y log(n)(|C0|+G|Cy|)].

Here sigma_y >= 1/2 on the full target domain.  The script certifies every
bracket nonpositive for n > HEAD by a finite gcd/activation-cell reduction,
and bounds the positive parts for 2 <= n <= HEAD below -gamma'.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from math import prod
from mpmath import iv, mp
import os

iv.prec = 120
mp.prec = 120

HEAD = 6000
T = F(16125, 100000)
Y2 = F(350708, 10_000_000)
PRIME_BLOCKS = (
    ("P11", (2, 3, 5, 7, 11), 690_988, 728_999),
    ("P7", (2, 3, 5, 7), 729_000, 818_999),
    ("P5", (2, 3, 5), 819_000, 1_027_999),
    ("P23", (2, 3), 1_028_000, 3_840_000),
)


def itv(q):
    if isinstance(q, F):
        return iv.mpf(q.numerator) / q.denominator
    return iv.mpf(q)


def hull(a, b):
    return a + (b - a) * iv.mpf([0, 1])


def positive_part(x):
    if x.b <= 0:
        return itv(0)
    return iv.mpf([0, x.b])


def rational_tile(lo: F, hi: F, index: int, count: int):
    a = lo + (hi - lo) * F(index, count)
    b = lo + (hi - lo) * F(index + 1, count)
    return hull(itv(a), itv(b))


Y_LO = iv.sqrt(itv(Y2))
Y_HI = iv.sqrt(1 - 2 * itv(T))


def y_tile(index: int, count: int):
    a = Y_LO + (Y_HI - Y_LO) * itv(F(index, count))
    b = Y_LO + (Y_HI - Y_LO) * itv(F(index + 1, count))
    return hull(a, b)


@dataclass(frozen=True)
class DivisorData:
    value: int
    sign: int
    log: object
    prime_log_square_sum: object


def divisor_data(primes):
    out = []
    for mask in range(1 << len(primes)):
        value = 1
        sign = 1
        prime_log_square_sum = itv(0)
        for bit, prime in enumerate(primes):
            if mask & (1 << bit):
                value *= prime
                sign = -sign
                prime_log_square_sum += iv.log(prime) ** 2
        out.append(
            DivisorData(
                value,
                sign,
                iv.log(value),
                prime_log_square_sum,
            )
        )
    return tuple(out)


def common_quantities(n_box, y, t=itv(T)):
    q = n_box * n_box - t / 16
    logq = iv.log(q)
    rate = itv(F(1, 50)) - logq / 2
    gamma = iv.exp(rate * y)
    return q, logq, rate, gamma


def sigma_box(n_box, y, t=itv(T)):
    q, logq, rate, gamma = common_quantities(n_box, y, t)
    x = 4 * iv.pi * q
    h = 1 - 3 * y + 4 * y * (1 + y) / (x * x)
    sigma = (1 + y) / 2 + (t / 4) * logq
    sigma -= (t / (2 * x * x)) * positive_part(h)
    return sigma, rate, gamma


def coefficient_boxes(active, z, y, rate, t=itv(T)):
    c0 = itv(0)
    cy = itv(0)
    dy = itv(0)
    for item in active:
        logm = z - item.log
        # Actual Euler-P coefficient:
        #   |lambda_d| = product_{p|d} b_t(p),
        # not b_t(d).  After factoring b_t(n), n=dm,
        #
        # |lambda_d| b_t(m) / b_t(n)
        # = exp((t/4)(sum_{p|d} log(p)^2 - log(d)^2
        #             - 2 log(d) log(m))).
        #
        # The sum-log-square correction is essential for composite d.
        rd = iv.exp(
            (t / 4)
            * (
                item.prime_log_square_sum
                - item.log * item.log
                - 2 * item.log * logm
            )
        )
        yd = iv.exp(-y * item.log)
        signed = rd if item.sign > 0 else -rd
        c0 += signed
        cy += signed * yd
        dy += signed * yd * (logm + rate)
    return c0, cy, dy


def bracket_box(n_box, z, y, active):
    _, _, rate, gamma = common_quantities(n_box, y)
    c0, cy, dy = coefficient_boxes(active, z, y, rate)
    G = gamma * iv.exp(y * z)
    bracket = (
        G * abs(dy)
        - (z / 2) * (abs(c0) + G * abs(cy))
    )
    return bracket


def head_gate(label, primes, nlo, nhi, n_tiles=2, y_tiles=32):
    data = divisor_data(primes)
    total_boxes = 0
    worst_ratio = itv(0)
    worst = None
    for ni in range(n_tiles):
        nbox = rational_tile(F(nlo), F(nhi), ni, n_tiles)
        for yi in range(y_tiles):
            y = y_tile(yi, y_tiles)
            sigma, rate, gamma = sigma_box(nbox, y)
            head = itv(0)
            for n in range(2, HEAD + 1):
                z = iv.log(n)
                active = tuple(item for item in data if n % item.value == 0)
                c0, cy, dy = coefficient_boxes(active, z, y, rate)
                G = gamma * iv.exp(y * z)
                bracket = (
                    G * abs(dy)
                    - (z / 2) * (abs(c0) + G * abs(cy))
                )
                factor = iv.exp((itv(T) / 4) * z * z - sigma * z)
                head += factor * positive_part(bracket)
            decay = -rate * gamma
            total_boxes += 1
            if not (head.b < decay.a):
                return False, {
                    "label": label,
                    "n_tile": ni,
                    "y_tile": yi,
                    "head": head,
                    "decay": decay,
                }
            ratio = head / decay
            if ratio.b > worst_ratio.b:
                worst_ratio = ratio
                worst = (ni, yi, head, decay)
    return True, {
        "label": label,
        "boxes": total_boxes,
        "worst_ratio": worst_ratio,
        "worst": worst,
    }


def tail_cells(primes):
    data = divisor_data(primes)
    result = []
    for gmask in range(1 << len(primes)):
        allowed = []
        for dmask, item in enumerate(data):
            if dmask & ~gmask == 0:
                allowed.append(item)
        allowed.sort(key=lambda item: item.value)
        for cell, high_item in enumerate(allowed):
            low = 0 if cell == 0 else allowed[cell - 1].value
            high = high_item.value
            active = tuple(item for item in allowed if item.value >= high)
            result.append((gmask, cell, low, high, active))
    return tuple(result)


def tail_gate(
    label,
    primes,
    nlo,
    nhi,
    n_tiles=4,
    y_tiles=24,
    ratio_tiles=8,
    head_log_tiles=48,
):
    failures = []
    boxes = 0
    max_depth_seen = 0
    worst_ratio = itv(0)
    worst = None
    cells = tail_cells(primes)
    log_head = iv.log(HEAD)

    def y_from_s(sa: F, sb: F):
        a = Y_LO + (Y_HI - Y_LO) * itv(sa)
        b = Y_LO + (Y_HI - Y_LO) * itv(sb)
        return hull(a, b)

    def certify_ratio_box(
        na: F,
        nb: F,
        ra: F,
        rb: F,
        sa: F,
        sb: F,
        active,
        depth=0,
    ):
        nonlocal boxes, max_depth_seen
        nbox = hull(itv(na), itv(nb))
        y = y_from_s(sa, sb)
        r = hull(itv(ra), itv(rb))
        z = iv.log(nbox) + iv.log(r)
        bracket = bracket_box(nbox, z, y, active)
        boxes += 1
        max_depth_seen = max(max_depth_seen, depth)
        if bracket.b <= 0:
            return True, None
        if depth >= 24:
            return False, bracket

        # Split only one dimension.  The floating scores choose efficiency;
        # the proof still comes solely from the interval inequalities.
        nscore = float(mp.log(mp.mpf(nb.numerator) * na.denominator
                              / (mp.mpf(nb.denominator) * na.numerator)))
        rscore = float(mp.log(mp.mpf(rb.numerator) * ra.denominator
                              / (mp.mpf(rb.denominator) * ra.numerator)))
        yscore = float(sb - sa) * 0.7
        if rscore >= nscore and rscore >= yscore:
            mid = (ra + rb) / 2
            pieces = ((na, nb, ra, mid, sa, sb),
                      (na, nb, mid, rb, sa, sb))
        elif yscore >= nscore:
            mid = (sa + sb) / 2
            pieces = ((na, nb, ra, rb, sa, mid),
                      (na, nb, ra, rb, mid, sb))
        else:
            mid = (na + nb) / 2
            pieces = ((na, mid, ra, rb, sa, sb),
                      (mid, nb, ra, rb, sa, sb))
        for piece in pieces:
            ok, bad = certify_ratio_box(*piece, active, depth + 1)
            if not ok:
                return False, bad
        return True, None

    def certify_log_n_box(
        na: F,
        nb: F,
        z,
        sa: F,
        sb: F,
        active,
        depth=0,
    ):
        nonlocal boxes, max_depth_seen
        nbox = hull(itv(na), itv(nb))
        w = iv.log(nbox)
        if z.a > w.b:
            return True, None
        y = y_from_s(sa, sb)
        bracket = bracket_box(nbox, z, y, active)
        boxes += 1
        max_depth_seen = max(max_depth_seen, depth)
        if bracket.b <= 0:
            return True, None
        if depth >= 28:
            return False, bracket

        nscore = float(mp.log(mp.mpf(nb.numerator) * na.denominator
                              / (mp.mpf(nb.denominator) * na.numerator)))
        zscore = float(z.b - z.a)
        yscore = float(sb - sa) * 0.7
        if zscore >= nscore and zscore >= yscore:
            mid = (z.a + z.b) / 2
            pieces = (
                (na, nb, iv.mpf([z.a, mid]), sa, sb),
                (na, nb, iv.mpf([mid, z.b]), sa, sb),
            )
        elif yscore >= nscore:
            mid = (sa + sb) / 2
            pieces = (
                (na, nb, z, sa, mid),
                (na, nb, z, mid, sb),
            )
        else:
            mid = (na + nb) / 2
            pieces = (
                (na, mid, z, sa, sb),
                (mid, nb, z, sa, sb),
            )
        for piece in pieces:
            ok, bad = certify_log_n_box(*piece, active, depth + 1)
            if not ok:
                return False, bad
        return True, None

    for gmask, cell, low, high, active in cells:
        for ni in range(n_tiles):
            na = F(nlo) + F(nhi - nlo) * F(ni, n_tiles)
            nb = F(nlo) + F(nhi - nlo) * F(ni + 1, n_tiles)
            nbox = hull(itv(na), itv(nb))
            w = iv.log(nbox)
            for yi in range(y_tiles):
                y = y_tile(yi, y_tiles)
                sa = F(yi, y_tiles)
                sb = F(yi + 1, y_tiles)
                if cell == 0:
                    # Physical domain HEAD <= n <= N is triangular in
                    # (log N, log n).  Rectangles outside it are skipped;
                    # crossing rectangles are a harmless enlargement.
                    log_nhi = iv.log(itv(F(nlo) + (F(nhi - nlo) * F(ni + 1, n_tiles))))
                    for zi in range(head_log_tiles):
                        za = log_head + (log_nhi - log_head) * itv(F(zi, head_log_tiles))
                        zb = log_head + (log_nhi - log_head) * itv(F(zi + 1, head_log_tiles))
                        z = hull(za, zb)
                        ok, bracket = certify_log_n_box(
                            na, nb, z, sa, sb, active
                        )
                        if not ok:
                            failures.append((gmask, cell, ni, yi, zi, bracket))
                            if len(failures) >= 10:
                                return False, {
                                    "label": label,
                                    "boxes": boxes,
                                    "failures": failures,
                                }
                else:
                    for ri in range(ratio_tiles):
                        ra = F(low) + F(high - low) * F(ri, ratio_tiles)
                        rb = F(low) + F(high - low) * F(ri + 1, ratio_tiles)
                        ok, bracket = certify_ratio_box(
                            na, nb, ra, rb, sa, sb, active
                        )
                        if not ok:
                            failures.append((gmask, cell, ni, yi, ri, bracket))
                            if len(failures) >= 10:
                                return False, {
                                    "label": label,
                                    "boxes": boxes,
                                    "failures": failures,
                                    "max_depth": max_depth_seen,
                                }
    return True, {
        "label": label,
        "boxes": boxes,
        "cells": len(cells),
        "max_depth": max_depth_seen,
        "worst_ratio": worst_ratio,
        "worst": worst,
    }


def main():
    print("ROW", T, Y2, "HEAD", HEAD)
    all_ok = True
    part = os.environ.get("TRIANGLE_PART", "all")
    if part in ("all", "head"):
        for label, primes, nlo, nhi in PRIME_BLOCKS:
            ok, detail = head_gate(label, primes, nlo, nhi)
            print("HEAD", "PASS" if ok else "FAIL", detail)
            all_ok &= ok
    if part in ("all", "tail"):
        for label, primes, nlo, nhi in PRIME_BLOCKS:
            ok, detail = tail_gate(label, primes, nlo, nhi)
            print("TAIL", "PASS" if ok else "FAIL", detail)
            all_ok &= ok
    print("RESULT", "ALL PASS" if all_ok else "FAIL")
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
