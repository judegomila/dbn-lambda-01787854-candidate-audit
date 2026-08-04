# Canonical invocations for `prop43_proof.c`

This closes the reproducibility gap recorded in `independent/README.md`.
The seven arguments described there as unrecorded were never lost: they are
in `scripts/run_full_sweep.sh`, which is sealed and has always been on
`main`. Only the *mapping* was missing.

## Interface

```
prop43_proof Nstart Nend tlo_num thi_num t_den y2num y2den mtype prec K hw mode [stride]
```

## Parameters fixed for every shard

| argument | value | source |
|---|---|---|
| `tlo_num thi_num t_den` | `161250000 161250001 1000000000` | `run_later` in `run_full_sweep.sh`; equals `t0 = 129/800` |
| `y2num y2den` | `350708 10000000` | same; equals `y0^2 = 87677/2500000` |
| `mode` | `t` | same |
| `stride` | omitted (defaults to 1) | every stored summary records `stride 1` |

The `run_exact` band uses the equivalent coarser triple
`16125 16125 100000` for the same `t0`.

## The canonical schedule

Exactly as `scripts/run_full_sweep.sh` invokes it. Mollifier bands are named
by their largest prime.

### P11 band — `mtype 6 prec 220 K 14 hw 0.005`

```
prop43_proof 690988  690988  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 690989  690990  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 690991  690995  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 690996  691010  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 691011  691050  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 691051  691150  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 691151  691500  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 691501  693000  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 693001  697000  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 697001  707000  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 707001  718000  16125 16125 100000 350708 10000000 6 220 14 0.005 t
prop43_proof 718001  728999  16125 16125 100000 350708 10000000 6 220 14 0.005 t
```

`N = 690988` is the binding row: it attains `T_min = 791366e-12`.

### P7 band — `mtype 5 prec 200 K 14 hw 0.005`

```
prop43_proof 729000  818999  161250000 161250001 1000000000 350708 10000000 5 200 14 0.005 t
```

### P5 band — `mtype 4 prec 200 K 14 hw 0.005`

```
prop43_proof 819000  1027999 161250000 161250001 1000000000 350708 10000000 4 200 14 0.005 t
```

### P23 band — `mtype 3`, precision and half-width vary by range

```
prop43_proof 1028000 1030000 161250000 161250001 1000000000 350708 10000000 3 240 16 0.00025 t
prop43_proof 1030001 1050000 161250000 161250001 1000000000 350708 10000000 3 240 16 0.00025 t
prop43_proof 1050001 1100000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.002   t
prop43_proof 1100001 1300000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.01    t
prop43_proof 1300001 1700000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.01    t
prop43_proof 1700001 2200000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.01    t
prop43_proof 2200001 2800000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.01    t
prop43_proof 2800001 3300000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.01    t
prop43_proof 3300001 3840000 161250000 161250001 1000000000 350708 10000000 3 220 14 0.01    t
```

The first two ranges need `prec 240 K 16 hw 0.00025`; that tightening is
load-bearing, not decorative. Do not widen it without re-certifying.

## Relation to the nine stored sweeps

`dan-reworking/code/prop43/runs/` holds nine runs. Eight map onto bands
above exactly:

| stored run | range | mtype | canonical band |
|---|---|---|---|
| `p11` | 690988–728999 | 6 | the whole P11 band, merged |
| `p7` | 729000–818999 | 5 | P7, identical |
| `p5` | 819000–1027999 | 4 | P5, identical |
| `p23_s1`–`s6` | 1028000–3840000 | 3 | the nine P23 shards, re-sharded into six equal parts of 468,667 |

**The one thing still not recoverable** is which `prec K hw` triple the
author used inside each `p23_s*` shard. His shards straddle boundaries where
the canonical schedule changes precision — `s1` spans `1028000–1496666`,
crossing both the `240/16/0.00025` and `220/14/0.002` ranges — so a single
triple was used for each, and no artifact records which.

That does not matter for reproducibility. **The canonical schedule above is
the authoritative one**, and it is what a replay should execute. The stored
runs are corroboration produced under a different sharding, not the
specification.

## Cost

Roughly 3 hours single-threaded across all bands. The nine stored summaries
record 13–22 minutes per shard on eight cores. Any replay job should shard
the P23 band and run the bands concurrently, as `run_full_sweep.sh` does with
`p11_pid`, `p7_pid`, `p235_pid` and `p23_pid`.
