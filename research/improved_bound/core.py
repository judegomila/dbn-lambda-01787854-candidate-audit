"""The improved-bound reduction.

PROVENANCE AND MODIFICATIONS
----------------------------
TODO before this lane is promoted: state what this is derived from, and
what was removed or changed relative to that ancestor.  Follow the
headers of ``independent/prop43/prop43_proof.c`` and
``independent/prop410/prop410_proof.py``, which name their ancestor in
the candidate repository and enumerate the dead code they dropped.

WHAT THIS COMPUTES
------------------
TODO: the statement, as it will appear as a numbered proposition in the
manuscript.  Write the proposition before the code, not after: the point
of the block is that the program is the proof of a stated claim, not that
a stated claim is a description of the program.

CRITERIA THIS LANE MUST MEET BEFORE PROMOTION
---------------------------------------------
These are the standards the existing promoted programs satisfy.  A lane
that misses any of them is research, not evidence.

* Reads no stored certificates.  Every input is an exact rational or
  integer literal in the source.  If a value comes from a log, the
  program is checking a cache, not recomputing.
* Exact or outward-rounded interval arithmetic throughout.  No float
  enters a certified comparison.  ``exact.py`` in the sibling lane shows
  the pattern for rational square-root bounds.
* Fail-closed.  Any unproved branch, any uncertified row, any failed
  gate aborts non-zero.  Never downgrade a failure to a warning.
* Deterministic.  The same invocation produces byte-identical output.
* Records its invocation.  ``report.write_report`` does this; use it.
"""

from __future__ import annotations

from fractions import Fraction as F


# The currently certified bound, for comparison.  Any claim this lane
# makes must be checked against it explicitly: an "improvement" that is
# not strictly smaller is a bug, and one that is smaller is the whole
# point and must be stated as such.
CERTIFIED_BOUND = F(893927, 5000000)  # 0.1787854


class ReductionError(RuntimeError):
    """A fail-closed error.  Never caught to produce a softer result."""


def certified_bound() -> F:
    """Return the bound this repository currently certifies."""

    return CERTIFIED_BOUND


def improved_bound() -> F:
    """Return the bound this lane establishes, as an exact rational.

    TODO: implement.  Must raise ReductionError rather than return a
    value it cannot certify.
    """

    raise ReductionError("improved_bound() is not implemented yet")


def compare_to_certified(candidate: F) -> dict[str, object]:
    """Position a candidate bound against the certified one, exactly."""

    if not isinstance(candidate, F):
        raise ReductionError(f"bound must be an exact Fraction, got {type(candidate)!r}")
    return {
        "candidate": candidate,
        "certified": CERTIFIED_BOUND,
        "strictly_better": candidate < CERTIFIED_BOUND,
        "margin": CERTIFIED_BOUND - candidate,
    }
