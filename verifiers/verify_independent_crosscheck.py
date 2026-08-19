#!/usr/bin/env python3
"""Run the recomputation programs and bind their output to the package.

The programs under independent/ are self-contained recomputations of
quantities the candidate also derives by its own route.  They read no
stored certificates: each one calculates from exact rational inputs and
prints a certified upper bound.  prop62 is an independently written
implementation.  prop410 is a same-backend replay: it shares mpmath.iv
and a line-for-line identical effective_error_budget() with
verifiers/verify_finite_and_binding.py, so its agreement binds the
published digits to a reproducible calculation without supplying
cross-backend independence.  The authoritative Proposition 4.10
certification is the FLINT/Arb lane parsed by
verifiers/verify_prop410_arb_logs.py (assembly prerequisite P17).

This verifier closes a specific gap.  The sharp constants

    E_max = 0.000000233494905212337849        (Proposition 4.10)
    0.000356523011600040                      (Proposition 6.2)

are stated in README.md, PROOF_NOTE.md, MAXIMUM_CHECKS.md,
CANDIDATE_PARAMETERS.md and BARRIER_CERTIFICATE.md, but the sealed
verifiers only ever machine-checked weaker bounds around them:
verify_finite_and_binding.py gates on error_max < 234/10**9, and
barrier/src/verify_uniform_error_01787854.c gates on the loose 0.00125
allowance.  Nothing recomputed the displayed digits themselves.  Here
each program is executed and its certified value is compared, as an
exact decimal string, against the digits the documents publish.

Scope.  A pass means the two implementations agree and that the
published digits are the ones a fresh computation produces.  It is not
a proof of either proposition and does not upgrade the candidate's
review status.

prop43_proof.c is deliberately not run here.  It is a nine-shard sweep
costing roughly three hours; it has its own workflow job.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
INDEPENDENT = ROOT / "independent"

# The digits the package publishes, and where it publishes them.  A
# mismatch means either a program changed or a document drifted.
PROP410_EMAX = "0.000000233494905212337849"
PROP62_SHARP = "0.000356523011600040"
PROP62_LOOSE = "0.00125"

DOCUMENTED = [
    ("CANDIDATE_PARAMETERS.md", PROP410_EMAX),
    ("PROOF_NOTE.md", PROP410_EMAX),
    ("README.md", PROP410_EMAX),
    ("MAXIMUM_CHECKS.md", PROP410_EMAX),
    ("BARRIER_CERTIFICATE.md", PROP62_SHARP),
    ("CANDIDATE_PARAMETERS.md", PROP62_SHARP),
    ("PROOF_NOTE.md", PROP62_SHARP),
    ("README.md", PROP62_SHARP),
]

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


def run(command: list[str], scratch: Path, env: dict[str, str] | None = None) -> str:
    """Run a program to completion and return its stdout."""

    merged = dict(os.environ)
    merged.pop("PYTHONOPTIMIZE", None)
    merged.pop("PYTHONPATH", None)
    merged.pop("PYTHONHOME", None)
    merged["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        merged.update(env)
    completed = subprocess.run(
        command,
        cwd=scratch,
        env=merged,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        print(completed.stdout, file=sys.stderr)
        print(completed.stderr, file=sys.stderr)
        raise SystemExit(
            f"SEAL-ADJACENT FAILURE: {command[0]} exited {completed.returncode}"
        )
    return completed.stdout


def verify_prop410(scratch: Path) -> None:
    """Proposition 4.10 budget: same-backend mpmath replay (corroboration)."""

    program = INDEPENDENT / "prop410" / "prop410_proof.py"
    check("prop410 program is present", program.is_file())

    out = run(
        [sys.executable, str(program)],
        scratch,
        {"PROP410_OUTPUT_DIR": str(scratch / "prop410")},
    )

    check("prop410 reports its own PASS", "RESULT PASS:" in out)
    check(
        f"prop410 recomputes E_max = {PROP410_EMAX}",
        f"E_max = {PROP410_EMAX}" in out,
    )
    check(
        "prop410 certifies the summed budget at the published digits",
        re.search(
            r"e_A\+e_B\+e_C0\s*<=\s*" + re.escape(PROP410_EMAX), out
        )
        is not None,
    )


def verify_prop62(scratch: Path) -> None:
    """Proposition 6.2: the uniform error bound on the barrier box."""

    program = INDEPENDENT / "prop62" / "prop62_proof.c"
    check("prop62 program is present", program.is_file())

    if shutil.which("gcc") is None:
        raise SystemExit("SEAL-ADJACENT FAILURE: gcc is required for prop62")

    binary = scratch / "prop62_proof"
    # Match the flags run_container_review.sh already uses for the
    # package's own Arb sources.  Imposing stricter flags here would let
    # an unrelated warning fail the seal.
    run(
        ["gcc", "-O2", str(program), "-o", str(binary), "-lflint", "-lm"],
        scratch,
    )
    check("prop62 compiles under the sealed toolchain", binary.is_file())

    out = run([str(binary)], scratch)

    check("prop62 reports its own PASS", "PASS" in out and "FAIL" not in out)
    check(
        f"prop62 certifies the sharp constant {PROP62_SHARP}",
        PROP62_SHARP in out,
    )


def verify_documents() -> None:
    """The published digits must be the ones the programs produce."""

    for name, digits in DOCUMENTED:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        check(f"{name} publishes {digits}", digits in text)

    barrier = (ROOT / "BARRIER_CERTIFICATE.md").read_text(encoding="utf-8")
    check(
        "the sharp constant is still recorded below the loose allowance",
        f"{PROP62_SHARP}<{PROP62_LOOSE}" in barrier.replace(" ", ""),
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="independent-crosscheck.") as name:
        scratch = Path(name)
        # Cheapest and most fragile-to-drift first, so a document edit is
        # reported even on a host missing the Arb toolchain.
        verify_documents()
        verify_prop410(scratch)
        verify_prop62(scratch)

    print(f"TOTAL CHECKS RUN: {checks}")
    if failures:
        print(f"RESULT: INDEPENDENT CROSS-CHECK FAIL ({failures})", file=sys.stderr)
        return 1
    print("RESULT: INDEPENDENT CROSS-CHECK PASS")
    print(
        "STATUS: agreement on published constants (prop62 cross-written, "
        "prop410 same-backend replay); not a proof of either proposition."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
