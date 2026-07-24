# Companion wider-margin baseline

## Purpose

This repository is the primary private-review candidate for

\[
\Lambda\le0.1787854.
\]

The separate private repository
[`judegomila/dbn-lambda-01858207-candidate-audit`](https://github.com/judegomila/dbn-lambda-01858207-candidate-audit/tree/e9cc86b9c4eb6e9d87a76116b1067843dc34d4f4)
is retained as a wider-margin fallback and companion robustness cross-check at
\(\Lambda\le0.1858207\).

Neither package is an established theorem. Both remain unreviewed
computer-assisted proof candidates.

## Logical relationship

Numerically,

\[
0.1858207-0.1787854=0.0070353>0.
\]

If the \(0.1787854\) candidate is correct, then the weaker
\(0.1858207\) inequality follows automatically. The converse does not hold.
The companion repository is not a premise in the proof assembled here.

The two packages should therefore be reviewed as follows:

1. test the \(0.1787854\) package as the primary claimed improvement;
2. use the \(0.1858207\) package to detect shared or divergent implementation
   errors and to isolate failures caused by the tighter parameters;
3. if the primary package fails, report the failure explicitly and assess the
   companion package separately;
4. never present a passing companion replay as evidence that a failed primary
   obligation is valid.

## Quantitative comparison

| item | primary \(0.1787854\) | companion \(0.1858207\) |
|---|---:|---:|
| finite rows | \(3,149,013\) | \(2,054,013\) |
| finite cutoff | \(N=3,840,000\) | \(N=2,745,000\) |
| final finite margin | \(\ge5.57871094787\times10^{-7}\) | \(\ge0.001082791723\) |
| tail post-error margin | \(>0.0001735209373337\) | \(\ge0.0221132941\) |
| barrier time top | \(129/800=0.16125\) | \(1809/10000=0.1809\) |
| barrier height floor | \(0.1809\) | \(0.165\) |
| closed time prisms | \(883\) | \(1,087\) |
| minimum recorded prism residual | \(>0.5198498946138725\) | \(>0.616277355322\) |

The companion's larger margins and larger local barrier box make it a useful
control. The primary package nevertheless proposes the stronger final upper
bound.

## Independent evidence roles

The primary package contributes:

- a sealed full regeneration of all \(3,149,013\) finite rows;
- direct singleton checks across every finite-family and shard seam;
- separate Python and FLINT/Arb tail implementations;
- 256- and 512-bit Arb tail certificates;
- complete Linux/GCC/FLINT 3.0.1 and macOS/Clang/FLINT 3.6.0 barrier replays.

The companion package contributes:

- a separately structured C/zlib/libm/MPFR verification layer;
- a different finite cutoff and tail partition with much larger slack;
- an artifact-identical 126-bit Arb stored-sums regeneration;
- mutation tests for its W1 evidence and parser paths; and
- a wider local W1 zero-free certificate.

These are valuable cross-checks, but some analytic ideas and upstream inputs
are shared. Agreement is not clean-room proof of correctness.

## Review disposition

The \(0.1787854\) repository should be sent to the external mathematician as
the primary target. The \(0.1858207\) repository should be provided as a
companion control after the reviewer understands that:

- it proves a weaker proposed conclusion;
- it does not repair a mathematical gap in the primary package;
- its larger margins can help distinguish analytic from numerical failures;
- both packages still require independent theorem-to-code review.
