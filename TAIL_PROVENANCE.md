# Tail verifier provenance

The target tail proof has two implementation lines.

The primary line is the standalone FLINT/Arb verifier
`verifiers/verify_tail_arb.c`, accompanied by `TAIL_LEMMA.md`.  It reads no
cached numerical input, rebuilds all 153,814 exact convolution coefficients,
uses exact rational candidate parameters, covers every \(N\ge3{,}840{,}000\)
and the full required \(y\)-range, and refuses precision below 256 bits.
The sealed 256- and 512-bit logs are parsed fail-closed by
`verifiers/verify_tail_arb_logs.py`.

Run a fresh primary replay with:

```sh
./scripts/run_tail_arb.sh replay/tail_arb
```

The older Python interval files are supplementary regression and provenance
checks.  They are the deposited Mosaic Intelligence second-line engine for
the 0.1875/0.1891 assemblies plus one explicitly delimited target block and
the conservative \(10.44\to10.50\) effective-error substitution. They are not
the sole logical support for the target tail.

The pristine source is:

```text
vendor/deposited/assembly1875_1891_secondline.py
SHA-256 3cdbf8a43d4bd490d817253a3e848be5082e2e4de98c5b046078d816e450ee8a
```

The two target variants change only:

1. the file header identifying the audit patch;
2. interval precision (`160` or `256`);
3. `MHEAD_MAX`, from `50000` to `153814`;
4. the single exact-rational error constant from `1044/100` to `1050/100`;
5. the block between `BEGIN/END AUDIT PATCH TRI178785400SAFE`.

Run:

```sh
python3 verifiers/verify_tail_patch_provenance.py
```

The script reverses exactly those transformations and requires byte-for-byte
identity with the deposited source.  This establishes the supplementary
line's source lineage; it does not replace mathematical review of either the
standalone Arb theorem or the generic `run_band` argument.
