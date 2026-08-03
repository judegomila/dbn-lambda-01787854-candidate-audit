"""Unsealed research tools for dynamic de Bruijn--Newman barriers.

Nothing in this package is part of the sealed proof surface.  In particular,
successful output from these tools is not a certificate of a new bound.
"""

from .core import (
    CANDIDATE,
    ERROR_MAX,
    TAIL_MARGIN_LOWER,
    CriterionRow,
)

__all__ = [
    "CANDIDATE",
    "ERROR_MAX",
    "TAIL_MARGIN_LOWER",
    "CriterionRow",
]
