# Proposition 4.10 Arb verifier provenance

## What this lane certifies and why it exists

Proposition 4.10 (the uniform effective-approximation error budget on the
finite region) was previously machine-checked by two Python programs —
`verifiers/verify_finite_and_binding.py` and
`independent/prop410/prop410_proof.py` — that share one numerical backend
(`mpmath.iv` at 220 bits) and a line-for-line identical
`effective_error_budget()`.  The second program was therefore a
same-backend replay, and exact rational comparison of its returned
endpoints was conditional on `mpmath.iv` correctly outward-rounding its
transcendental interval operations.  That trust gap is closed here.

The authoritative implementation is now the standalone FLINT/Arb program
`verifiers/verify_prop410_arb.c`.  It reads no stored certificate,
requires its working precision as an explicit argument, refuses precision
below 256 bits, constructs every constant from exact integers or
rationals, uses rigorous Arb enclosures for every transcendental
operation, emits all exact parameters and every domain/sign gate, and
makes each decisive comparison by subtracting the exact rational bound
and requiring the entire resulting ball to be strictly on the winning
side.  Directed endpoints are converted to exact dyadic points before
entering monotone majorants, per the program header.

The `mpmath.iv` path is retained as non-authoritative same-backend
corroboration.

## Certified results

At both 256 and 512 bits, in the pinned review container:

```text
e_A+e_B  <= 2.05702368866622e-12  < 206/10^14
e_C0     <= 2.33492848188649183e-7 = stated bound (certified strictly below)
E_max    <= 2.33494905212337849e-7 = stated bound (certified strictly below)
E_max    <  234/10^9               (coarse load-bearing budget)
T_min-E_max >= 5.5787109478766215e-7 > 557/10^9 > 0
```

The published constants were not changed: the Arb calculation certifies
the previously displayed sharp decimals directly.

## Sealed artifacts

```text
verifiers/verify_prop410_arb.c
SHA-256 0d40f9b8137f83fcfd7c6546e333d23acac052fa7ca3822f4d7d3075c62e66d8

logs/prop410_arb_256.log
SHA-256 995651e49112928472d6511a191d727783b0abdf77c20f2f6c32ec814986b244

logs/prop410_arb_512.log
SHA-256 3945dee56684fb1ebc6866c67b09b5850d315fd191b65e594f1430ee52076edb
```

The strict parser is `verifiers/verify_prop410_arb_logs.py`; it runs as
prerequisite P17 of `verifiers/verify_assembly_1787854.py` and directly
in `verify.sh`.  `verifiers/verify_prop410_arb_mutation.py` proves the
parser rejects twenty distinct evidence mutations, including removal of
either precision run and any fallback to the `mpmath` result.

## Authoritative run environment

The sealed transcripts were produced inside the pinned review container
(root `Dockerfile`; Ubuntu 24.04 linux/amd64, archive snapshot
`20260723T000000Z`), image config digest

```text
sha256:8665570eadc48f3b884b4bb038f492ec9d130cdd466c9deb16f6795878da72c5
```

with the container toolchain

```text
gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
libflint-dev 3.0.1-3.1build1
```

invoked as

```sh
docker run --rm --platform linux/amd64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --tmpfs /tmp:rw,exec,nosuid,size=1g \
  -v "$PWD:/work:ro" \
  -v "$PWD/replay/prop410-container:/review-output" \
  -w /work dbn-lambda-01787854-review \
  ./scripts/run_prop410_arb.sh /review-output/evidence
```

at repository baseline commit
`034a37acce703e128e63e2f36520b0c8af6c1c76` plus this lane's changes; the
source hash above is the binding identity of the compiled program.  The
runner compiles with `-O2 -std=c17 -Wall -Wextra -Werror -pedantic`, runs
256 and 512 bits, rejects 255 bits and a missing precision argument, and
parses the fresh transcripts strictly.

A macOS arm64 corroboration run (Apple clang, Homebrew FLINT 3.6.0)
produced byte-identical 256- and 512-bit transcripts, so the certified
digits agree across two operating systems, two compilers, two FLINT
major versions, and two working precisions.

## Replay

```sh
./scripts/run_prop410_arb.sh replay/prop410_arb
```

The output directory must not already exist.  `RUN_SANITIZERS=1` adds an
address/undefined-sanitizer build and run at 256 bits.
