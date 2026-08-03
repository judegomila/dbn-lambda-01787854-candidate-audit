# Archived evidence for the `0.1782354` lower-time candidate

Status: unreviewed computer-assisted proof candidate; not an established
theorem.

This directory archives the successful local evidence for

\[
t_0=1607/10000,
\qquad y_0^2=87677/2500000,
\qquad
t_0+y_0^2/2=891177/5000000=0.1782354.
\]

## Contents

- `p*.log.gz`: all 3,359,013 finite rows from \(N=690988\) through
  \(N=4050000\), with the P13/P11/P7/P5/P23 schedule.
- `direct_singletons_01782354.log.gz`: 22 independent non-amortized family
  and shard seam rows.
- `triangle_y_dini_256.log`: complete five-leg height-transfer replay.
- `tail_01782354_arb_*.log`: 256-, 512-bit and sanitized P1113 tail runs.
- `normalizer_*.log`, `native_binding_01782354.log`, and
  `window_freeze_01782354.log`: supporting analytic/source-binding checks.
- `assembly_01782354.log`: the successful integrated assembly.
- `REPLAY_METADATA.txt`: pinned image, producer hash, exact parameters and
  wall-clock provenance for the complete finite replay.
- `REPLAY_SHA256SUMS`: hashes of the original uncompressed finite outputs.
- `SOURCE_SHA256SUMS`: hashes of every lower-time source and runner.
- `SHA256SUMS`: hashes of the archived evidence files themselves.

The compressed rows are parsed directly by
`verifiers/verify_finite_01782354.py`. The complete archived-evidence check is

```text
python3 verifiers/verify_finite_01782354.py \
  certificates/lower_time_01782354
python3 verifiers/verify_direct_singletons_01782354.py \
  certificates/lower_time_01782354/direct_singletons_01782354.log.gz \
  certificates/lower_time_01782354
python3 verifiers/verify_assembly_01782354.py \
  certificates/lower_time_01782354 \
  certificates/lower_time_01782354/direct_singletons_01782354.log.gz
```

Fresh regeneration uses the scripts listed in
`CANDIDATE_PARAMETERS_01782354.md`. The pre-existing sealed `0.1787854`
source and certificates remain separate and unchanged.
