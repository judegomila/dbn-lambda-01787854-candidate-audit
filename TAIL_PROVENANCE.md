# Tail verifier provenance

The target tail files are not independent new engines.  They are the deposited
Mosaic Intelligence second-line engine for the 0.1875/0.1891 assemblies plus
one explicitly delimited target block.

The pristine source is:

```text
vendor/deposited/assembly1875_1891_secondline.py
SHA-256 3cdbf8a43d4bd490d817253a3e848be5082e2e4de98c5b046078d816e450ee8a
```

The two target variants change only:

1. the file header identifying the audit patch;
2. interval precision (`160` or `256`);
3. `MHEAD_MAX`, from `50000` to `153814`;
4. the block between `BEGIN/END AUDIT PATCH TRI178785400SAFE`.

Run:

```sh
python3 verifiers/verify_tail_patch_provenance.py
```

The script reverses exactly those transformations and requires byte-for-byte
identity with the deposited source.  This establishes source lineage; it does
not replace mathematical review of the generic `run_band` tail argument.
