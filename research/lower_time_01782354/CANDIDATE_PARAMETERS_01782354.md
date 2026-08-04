# Exploratory lower-time candidate parameters

Status: complete local fail-closed assembly pass; unreviewed computer-assisted
proof candidate, not an established theorem.

## Headline

\[
t_0=\frac{1607}{10000}=0.16070,
\qquad
y_0^2=\frac{87677}{2500000}=0.0350708,
\]

\[
\boxed{
\Lambda\leq t_0+\frac{y_0^2}{2}
=\frac{891177}{5000000}
=0.1782354.
}
\]

This is exactly \(11/20000=0.00055\) below the repository's previous
`0.1787854` candidate.

The final-height and barrier-canopy squares are

\[
1-2t_0=\frac{3393}{5000}=0.6786,
\qquad
y_0^2+2t_0=\frac{891177}{2500000}=0.3564708.
\]

The site and verified-height inputs are unchanged:

\[
X=6000000185827,qquad
T_{\rm PT}=3000175332800.
\]

## Finite schedule

The complete fail-closed replay covers 3,359,013 consecutive rows:

| Family | Primes | Rows | Stored minimum |
|---|---|---:|---:|
| P13 | 2,3,5,7,11,13 | 690988–728999 | `0.000670513304@690988` |
| P11 | 2,3,5,7,11 | 729000–774999 | `0.004925245406@729000` |
| P7 | 2,3,5,7 | 775000–849999 | `0.007453723667@775000` |
| P5 | 2,3,5 | 850000–1074999 | `0.000444808402@850000` |
| P23 | 2,3 | 1075000–4050000 | `0.002584981890@1075000` |

There are no gaps, overlaps or `UNCERT` rows. The global stored finite floor
is the P5 switch row. The independently recomputed effective-error ceiling is

\[
E_{\max}
\leq0.000000239372027867896139,
\]

leaving the normalized binding margin

\[
0.000444569029972132\ldots>0.
\]

Twenty-two direct non-amortized singleton rows dominate every family/shard
seam, and all eleven shard starts reproduce their amortized rows exactly.

## Height transfer and tail

The five-leg upper-Dini verifier covers the complete interval

\[
y_0\leq y\leq\sqrt{3393/5000}.
\]

At 256 bits its strict worst ratio is the P13 cell

\[
0.9999999980092249<1.
\]

The native normalizer/correction verifier passes at 180 and 256 bits. The
window-freeze audit passes all 46 mathematical and source-binding checks.

The fixed P1113 tail starts at \(N_*=4{,}050{,}000\). At 512 bits,

\[
D_{\rm ub}=0.996263624349153199188926591862\ldots
\]

and its post-error margin is

\[
0.00232329680607003070087534456632\ldots>0.
\]

## Barrier inheritance

The existing dual 883-prism certificates prove zero-freeness on the stronger
closed slab

\[
[X,X+1]\times[0.1809,1]\times[0,0.16125].
\]

Since \(t_0=0.16070<0.16125\) and the new curved canopy is smaller, the
required barrier is a strict subset. Both archived platform transcripts pass
unchanged.

## Replay entry points

```text
./scripts/run_finite_01782354.sh FRESH_OUTPUT_DIRECTORY
./scripts/run_direct_singletons_01782354.sh FRESH_OUTPUT_DIRECTORY FINITE_OUTPUT_DIRECTORY
./scripts/run_triangle_y_dini_p13.sh 256
RUN_SANITIZERS=1 ./scripts/run_tail_01782354_arb.sh FRESH_OUTPUT_DIRECTORY
python3 verifiers/verify_assembly_01782354.py FINITE_OUTPUT_DIRECTORY DIRECT_LOG
```

Archived local evidence and hashes are under
`certificates/lower_time_01782354/`.

The moving-real-rung idea is documented separately in
`MOVING_REAL_RUNG_BARRIER.md`; it is not used in this numerical bound.
