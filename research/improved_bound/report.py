"""Report writing for the improved-bound lane.

Two properties are enforced here rather than left to discipline, because
both have already cost this repository real work:

1.  Every report opens with the exact invocation that produced it.
    ``independent/prop43/prop43_proof.c`` is sealed but cannot be re-run:
    it takes twelve positional arguments, seven of which appear nowhere in
    the nine stored sweep outputs, so about three hours of certified
    compute is unreproducible from the tree.  A program whose invocation
    is not recorded is reproducible only in principle.

2.  The output directory is redirectable.  The sealed review container
    mounts the repository read-only, so a hardcoded ``runs/`` path makes a
    program unrunnable under the seal.  ``prop410_proof.py`` had to be
    modified during promotion for exactly this reason; doing it here means
    promotion needs no modification at all.

Neither property affects the arithmetic.  A report is a transcript, never
evidence: the certified values and the exit status stand on their own.
"""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import sys


HERE = Path(__file__).resolve().parent

#: Printed by every entry point.  Anything under ``research/`` is outside
#: the sealed review surface; see REVIEW_SCOPE.md.
STATUS = (
    "STATUS: UNSEALED RESEARCH ONLY; no improved Lambda bound certified."
)

#: Redirects the report directory.  Set by a promoted verifier when the
#: repository is mounted read-only.
OUTPUT_DIR_ENV = "IMPROVED_BOUND_OUTPUT_DIR"


def invocation_line(argv: list[str] | None = None) -> str:
    """Return the exact command line, quoted so it can be pasted back."""

    parts = list(sys.argv if argv is None else argv)
    return "INVOCATION: " + " ".join(shlex.quote(part) for part in parts)


def output_dir() -> Path:
    """Return the report directory, honouring the redirect."""

    override = os.environ.get(OUTPUT_DIR_ENV)
    return Path(override) if override else HERE / "runs"


def write_report(
    name: str,
    lines: list[str],
    argv: list[str] | None = None,
) -> Path:
    """Write ``name`` with the invocation as its first line.

    Returns the path written.  Callers should print the same body to
    stdout: a reader must never have to open a file to see a result.
    """

    body = "\n".join([invocation_line(argv), ""] + list(lines) + [STATUS, ""])
    directory = output_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(body, encoding="utf-8")
    return path
