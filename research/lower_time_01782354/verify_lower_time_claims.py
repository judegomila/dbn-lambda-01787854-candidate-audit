#!/usr/bin/env python3
"""Independently re-check the 0.1782354 lower-time extension's own claims.

This is a *research* check, not evidence.  It re-derives, in exact rational
arithmetic, every numeric claim the extension documents make about their
parameters, and re-verifies the archived certificate corpus against its own
manifest.  What it does NOT do is validate the mathematics of the finite,
tail or barrier computations: those live in the archived logs and were
produced outside this repository's sealed container (see ASSESSMENT.md).

A pass here means the extension's stated parameter arithmetic is exact and
its archive transported intact.  Nothing more.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
CERTS = HERE / "certificates"

# Parameters of the current sealed candidate, for comparison.
T0_SEALED = F(129, 800)
LAMBDA_SEALED = F(893927, 5000000)

# Parameters the extension proposes.
T0_NEW = F(1607, 10000)
Y0SQ = F(87677, 2500000)
LAMBDA_NEW = F(891177, 5000000)

STATUS = (
    "STATUS: UNSEALED RESEARCH ONLY; the 0.1782354 extension is not "
    "certified by this repository."
)

checks = 0
failures = 0


def check(label: str, condition: bool) -> None:
    global checks, failures
    checks += 1
    if condition:
        print(f"[PASS] {label}")
    else:
        failures += 1
        print(f"[FAIL] {label}", file=sys.stderr)


def check_parameter_arithmetic() -> None:
    """Every displayed rational in the extension documents."""

    check(
        "sealed bound is t0 + y0^2/2 at the sealed time",
        T0_SEALED + Y0SQ / 2 == LAMBDA_SEALED,
    )
    check(
        "proposed bound is t0 + y0^2/2 at the lowered time",
        T0_NEW + Y0SQ / 2 == LAMBDA_NEW,
    )
    check(
        "stated improvement 11/20000 is exact",
        LAMBDA_SEALED - LAMBDA_NEW == F(11, 20000),
    )
    check("stated 1 - 2*t0 = 3393/5000", 1 - 2 * T0_NEW == F(3393, 5000))
    check(
        "stated y0^2 + 2*t0 = 891177/2500000",
        Y0SQ + 2 * T0_NEW == F(891177, 2500000),
    )

    # Domain of the Polymath criterion, Theorem 1.2.
    check("criterion domain: 0 < t0 < 1/2", F(0) < T0_NEW < F(1, 2))
    check("criterion domain: 0 < y0^2 < 1 - 2*t0", F(0) < Y0SQ < 1 - 2 * T0_NEW)
    check("canopy top square below one: y0^2 + 2*t0 < 1", Y0SQ + 2 * T0_NEW < 1)

    # The reuse argument for the barrier transcript: the new curved barrier
    # is a subset of the certified one precisely because the time is lower.
    check(
        "lowered time lies strictly inside the certified t-range",
        T0_NEW < T0_SEALED,
    )
    check(
        "proposed bound is strictly better than the sealed one",
        LAMBDA_NEW < LAMBDA_SEALED,
    )


def check_archive_integrity() -> None:
    """The archived corpus must still match the manifest it shipped with."""

    manifest = CERTS / "SHA256SUMS"
    check("archive manifest is present", manifest.is_file())
    if not manifest.is_file():
        return

    listed = 0
    mismatched: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, _, name = line.partition("  ")
        target = CERTS / name.lstrip("./")
        if not target.is_file():
            mismatched.append(f"{name} (missing)")
            continue
        listed += 1
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            mismatched.append(name)

    check(f"all {listed} archived files match their recorded digests", not mismatched)
    if mismatched:
        for name in mismatched[:10]:
            print(f"       {name}", file=sys.stderr)


def check_assembly_transcript() -> None:
    """The archived assembly must actually reach its stated conclusion."""

    log = CERTS / "assembly_01782354.log"
    check("archived assembly transcript is present", log.is_file())
    if not log.is_file():
        return
    text = log.read_text(encoding="utf-8", errors="replace")
    check(
        "assembly transcript reports its own PASS",
        "RESULT: LOWER-TIME UNCONDITIONAL CANDIDATE ASSEMBLY PASS" in text,
    )
    check(
        "assembly transcript concludes at the proposed bound",
        "Lambda <= 891177/5000000 = 0.1782354" in text,
    )
    check(
        "assembly transcript retains its unreviewed-status line",
        "not an established theorem" in text,
    )
    check("assembly transcript contains no FAIL line", "[FAIL]" not in text)


def check_provenance_caveats() -> None:
    """Record, as checks, the two provenance facts ASSESSMENT.md relies on.

    These are deliberately asserted rather than described: if a future
    re-import silently fixes them, this file should start failing so the
    assessment gets revisited rather than quietly going stale.
    """

    meta = CERTS / "REPLAY_METADATA.txt"
    check("replay metadata is present", meta.is_file())
    if not meta.is_file():
        return
    text = meta.read_text(encoding="utf-8")
    check(
        "KNOWN CAVEAT still present: replay came from a dirty tree",
        "repository_dirty=true" in text,
    )
    check(
        "KNOWN CAVEAT still present: replay used the unpinned dbn21a-flint image",
        "container_image=dbn21a-flint" in text,
    )


def main() -> int:
    check_parameter_arithmetic()
    check_archive_integrity()
    check_assembly_transcript()
    check_provenance_caveats()
    print(f"TOTAL CHECKS RUN: {checks}")
    if failures:
        print(f"RESULT: LOWER-TIME CLAIM CHECK FAIL ({failures})", file=sys.stderr)
        return 1
    print("RESULT: LOWER-TIME PARAMETER AND ARCHIVE CHECK PASS")
    print(STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
