# Lower-time `0.1782354` proof-gap audit

Status: completion record for a locally archived, unreviewed
computer-assisted proof candidate. It is not an established theorem. The
early probes below motivated the final schedule; the completed evidence is
archived under `certificates/lower_time_01782354/`.

## Exact target

Keep

\[
X=6000000185827,\qquad y_0^2=\frac{87677}{2500000},
\]

and lower the time to

\[
t_0=\frac{1607}{10000}=0.16070.
\]

Then

\[
t_0+\frac{y_0^2}{2}
=\frac{891177}{5000000}=0.1782354,
\]

\[
1-2t_0=\frac{3393}{5000}=0.6786,
\qquad
y_0^2+2t_0=\frac{891177}{2500000}=0.3564708.
\]

The improvement from the current row is exactly

\[
\frac{893927-891177}{5000000}=\frac{11}{20000}=0.00055.
\]

## Certificates that are reusable unchanged

1. **Verified zeta height and sign map.**  The values of \(X\) and \(y_0\)
   are unchanged, so the Platt--Trudgian height comparison and the
   \(H_0\)-to-zeta symmetry/sign map are unchanged.
2. **The closed barrier transcript.**  It certifies the stronger rectangle
   \([X,X+1]+i[0.1809,1]\) for every
   \(0\leq t\leq129/800\).  Since \(1607/10000<129/800\), the new curved
   barrier is a subset.  Its horizontal width is unchanged, the barrier-floor
   margin remains \(234599/10^8\), and the new canopy top square is
   \(891177/2500000<1\).  The existing two 883-prism transcripts and their
   parser can therefore be cited as a stronger premise; they should not be
   regenerated merely to end at the smaller time.
3. **The native Triangle algebra.**  The convolution identity in
   `NATIVE_BINDING.md` is parameter-independent.  Its application still
   requires new positive producer rows and a new effective-error bound.

## Certificates that are not reusable

Every stored finite row has a time header beginning at \(0.16125\), so none
contains \(0.16070\).  The old finite logs, direct singleton logs, Dini logs,
normalizer/correction logs, tail logs, window-freeze specialization and final
assembly must therefore be rerun or parameterized.

An in-memory specialization of the existing finite error calculation to

\[
I_t=[160700000/10^9,160700001/10^9]
\]

passed all twelve analytic gates and gave the directed upper values

\[
e_A+e_B\leq2.069160539017\times10^{-12},
\]

\[
e_{C,0}\leq2.39369958707357123\times10^{-7},
\quad
E_{\max}\leq2.39372027867896139\times10^{-7}.
\]

The correction logarithmic-rate gate remained strictly negative, with upper
endpoint \(-1.363112154757640694\).  These are probes, not archived
certificates.

An in-memory specialization of the exact/interval window-freeze audit to the
seed schedule through \(N_*=4050000\) passed all 30 mathematical gates.  Its
directed site margins were

\[
x_*-x_{690988}>5377393.987424462185,
\qquad
x_{690989}-x_*>11989041.175095784575.
\]

The final parameterized window/source-binding verifier passes 46/46 gates
and is consumed by the integrated assembly.

## Exploratory finite schedule

The old switch rows do not survive the lower time.  Direct singleton probes
gave:

| family and row | exploratory result |
|---|---:|
| P13 at \(690988\) | \(L\geq0.000670513304\) |
| P11 at \(729000\) | \(L\geq0.004925221524\) |
| P7 at \(729000\) | `UNCERT` |
| P7 at \(775000\) | \(L\geq0.007453700913\) |
| P5 at \(819000\) | `UNCERT` |
| P5 at \(850000\) | \(L\geq0.000444786684\) |
| P23 at \(1028000\) | `UNCERT` |
| P23 at \(1075000\) | \(L\geq0.002584962181\) |
| P23 at \(3840000\) | \(L\geq0.295275065797\) |

A reasonable seed schedule for the full sweep is therefore

\[
\begin{array}{c|c}
690988\ldots728999 & P13\\
729000\ldots774999 & P11\\
775000\ldots849999 & P7\\
850000\ldots1074999 & P5\\
1075000\ldots N_* & P23.
\end{array}
\]

The singleton values do not certify the intervening rows.  Every row must be
produced fail-closed, and naive-versus-amortized comparisons are required at
all shard endpoints and family joints.  The P13 Dini theorem must retain the
prime cross term \(\sum_{p\mid d}\log^2p\); the normalizer proof must also add
the P13 factor.  All height-transfer checks must use the enlarged top
\(\sqrt{3393/5000}\).

## Fixed P1113 tail

The old tail certificate cannot be reused: its time interval does not contain
the new row, and the new final-height top is larger.  Exact decimal brackets
for the new top are

\[
\left(\frac{8237718}{10^7}\right)^2
<\frac{3393}{5000}
\leq
\left(\frac{8237719}{10^7}\right)^2.
\]

Using the existing fixed P1113 stencil and \(M=153814\), a 256-bit interval
probe gave:

| tail cutoff | directed \(D\) upper | directed flow-error lower | result |
|---:|---:|---:|---|
| \(3840000\) | \(1.0243833114\) | negative | fails |
| \(4020000\) | \(1.0001499344\) | negative | fails |
| \(4030000\) | \(0.9988498352\) | \(0.0007150482\) | all gates pass |
| \(4050000\) | \(0.9962636244\) | \(0.0023232968\) | all gates pass |

Increasing the convolution head at \(N_*=3840000\) can make the numerical
contraction smaller than one, but it does **not** repair the proof: for heads
\(200000,250000,300000\), the required sigma-2 endpoint-cap gate still fails.
The clean route is to extend the finite P23 lane.  A conservative choice
\(N_*=4050000\) adds 210,000 rows and gives substantially more tail slack
than the near-threshold \(4030000\) option.

`verifiers/verify_tail_01782354_arb.c` now supplies the separate primary
FLINT/Arb specialization, including exact hull checks, and
`scripts/run_tail_01782354_arb.sh` replays it at 256 and 512 bits.  A local
hardened replay also passed ASan/UBSan. Its logs are archived, the standalone
instantiation is `TAIL_LEMMA_01782354.md`, and the finite sweep overlaps on
the complete window \(N=N_*\). An additional independent non-Arb interval
implementation remains desirable as review redundancy, but it is not a
premise of the present assembly.

## Proof-grade completion checklist

- [x] Seal a full P13/P11/P7/P5/P23 finite sweep at the new time box through
      the selected \(N_*\), with no gaps, duplicates, `UNCERT` rows or
      nonpositive lower endpoints.
- [x] Audit the P13 recurrence, shifted-support partition and activation
      updates; compare naive and amortized values at every shard seam.
- [x] Run the six-prime direct Dini verifier and all later legs at multiple
      precisions on the actual schedule and enlarged height interval.
- [x] Extend and rerun the native normalizer/correction monotonicity verifier.
- [x] Seal the new P1113 tail and prove overlap on the complete \(N_*\) window.
- [x] Parameterize the window-freeze/site verifier at \(t_0=1607/10000\) and
      the new finite/tail cutoff.  The large site margins should persist, but
      the old parameter-specific output is not a substitute.
- [x] Write a new fail-closed assembly which checks the exact rational target,
      invokes the unchanged stronger barrier certificate, and consumes only
      the new finite, height-transfer and tail artifacts.
- [x] Update hashes, provenance, replay metadata and exposition only after all
      load-bearing logs are sealed.

Remaining external work is adversarial review, an independent implementation
of the new tail specialization, and eventual publication/peer verification.
