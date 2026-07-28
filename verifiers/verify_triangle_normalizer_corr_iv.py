#!/usr/bin/env python3
"""Interval gates for native modmoll/correction y-monotonicity.

Row:
  t = 129/800, y0^2 = 87677/2500000,
  N = 690988..3840000 on four Euler-prime legs.

The proof is analytic except for its worst-corner gates:

* sigma(y2)-sigma(y1) >= (y2-y1)/2, so
  M(y)=sum |lambda_d|d^{-sigma(y)} is decreasing.
* Every positive correction summand has upper logarithmic y-rate

    Xi(N,y) = g(N) + .5 log N + k(N) log N + 1/y,

  where g=1/50-.5log(N^2-t/16) and
  k=t/[2(4pi(N^2-t/16)-6)].

  Xi is decreasing in N and y; the script encloses Xi(N0,y0)<0.
"""

import argparse
import math
from fractions import Fraction as F

from mpmath import iv, mp


T = F(129, 800)
Y2 = F(87677, 2500000)
N0 = 690988
N1 = 3840000
LEGS = (
    ("P11", (2, 3, 5, 7, 11), 690988, 728999),
    ("P7", (2, 3, 5, 7), 729000, 818999),
    ("P5", (2, 3, 5), 819000, 1027999),
    ("P23", (2, 3), 1028000, 3840000),
)


def itv(q):
    if isinstance(q, F):
        return iv.mpf(q.numerator) / q.denominator
    return iv.mpf(q)


def hull(a, b):
    return iv.mpf([a.a, b.b])


def positive_part(x):
    return iv.mpf([max(mp.mpf(0), mp.mpf(x.a)),
                   max(mp.mpf(0), mp.mpf(x.b))])


def check(name, condition, detail=""):
    print("PASS" if condition else "FAIL", name, detail)
    if not condition:
        raise SystemExit(1)


def divisors(primes):
    out = []
    for mask in range(1 << len(primes)):
        d = 1
        lam_abs = itv(1)
        for bit, p in enumerate(primes):
            if mask & (1 << bit):
                d *= p
                lp = iv.log(p)
                lam_abs *= iv.exp(itv(T) * lp * lp / 4)
        out.append((d, lam_abs))
    return tuple(out)


def sigma_box(nlo, nhi, ylo, yhi):
    N = iv.mpf([nlo, nhi])
    y = hull(ylo, yhi)
    t = itv(T)
    q = N * N - t / 16
    x = 4 * iv.pi * q
    h = 1 - 3 * y + 4 * y * (1 + y) / (x * x)
    return (
        (1 + y) / 2
        + (t / 4) * iv.log(q)
        - (t / (2 * x * x)) * positive_part(h)
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prec", type=int, default=180)
    a = p.parse_args()
    iv.prec = a.prec
    mp.prec = a.prec

    t = itv(T)
    y0 = iv.sqrt(itv(Y2))
    ymax = iv.sqrt(1 - 2 * t)
    ybox = hull(y0, ymax)
    n0 = itv(N0)
    q0 = n0 * n0 - t / 16
    x0 = 4 * iv.pi * q0
    lnN0 = iv.log(n0)

    # h_y<0 makes the positive-part correction nonincreasing, whence
    # sigma(y2)-sigma(y1) >= (y2-y1)/2 even across the kink.
    hprime = -3 + 4 * (1 + 2 * ybox) / (x0 * x0)
    check(
        "S1 h_y<0 on full N/y domain; sigma slope >=1/2",
        hprime.b < 0,
        "hprime=" + str(hprime),
    )

    g0 = itv(F(1, 50)) - iv.log(q0) / 2
    k0 = t / (2 * (x0 - 6))
    Xi0 = g0 + lnN0 / 2 + k0 * lnN0 + 1 / y0
    check(
        "C1 worst-corner correction log-rate Xi(N0,y0)<0",
        Xi0.b < 0,
        "Xi=" + str(Xi0),
    )

    # d/dN [g(N)+.5 log N]
    aa = t / 16
    first_derivative = -(n0 * n0 + aa) / (
        2 * n0 * (n0 * n0 - aa)
    )
    check(
        "C2 d_N[g+.5logN]<0",
        first_derivative.b < 0,
        "upper=" + str(first_derivative.b),
    )

    # k log N has derivative with the sign of
    # (x-6)/N - 8 pi N log N.
    klog_numerator = (x0 - 6) / n0 - 8 * iv.pi * n0 * lnN0
    check(
        "C3 d_N[k(N)logN]<0",
        klog_numerator.b < 0,
        "upper=" + str(klog_numerator.b),
    )
    check(
        "C4 logN0>1/2 (closed-form monotonicity premise)",
        lnN0.a > itv(F(1, 2)).b,
        "logN0=" + str(lnN0),
    )

    # Each nonempty Euler prime family has a strictly decreasing native
    # normalizer.  The interval calculation is only a sign witness; the
    # proof is M'=-sigma' sum_{d>1}|lambda_d|log(d)d^{-sigma}<0.
    for label, primes, nlo, nhi in LEGS:
        sig = sigma_box(nlo, nhi, y0, ymax)
        positive_sum = itv(0)
        M = itv(0)
        for d, lam_abs in divisors(primes):
            mass = lam_abs * iv.exp(-sig * iv.log(d))
            M += mass
            if d > 1:
                positive_sum += mass * iv.log(d)
        derivative_upper = -positive_sum / 2
        check(
            f"M-{label} M>=1 and D^+M<0 on leg",
            M.a >= 1 and derivative_upper.b < 0,
            "M=" + str(M) + " derivative_upper=" + str(derivative_upper),
        )

    print(
        "ATOM u/(1-exp(-u)) <= 1+u for u>0 follows from "
        "1+u<=exp(u); after u=k*y*log(m), correction term rate "
        "<=g+1/y+k*log(N)+.5*log(N)."
    )
    print("RESULT ALL PASS precision", a.prec)


if __name__ == "__main__":
    main()
