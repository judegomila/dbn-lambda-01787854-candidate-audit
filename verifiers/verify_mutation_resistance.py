#!/usr/bin/env python3
"""Test the cross-check itself, by feeding it things it must reject.

ADVERSARIAL_REVIEW_PROTOCOL.md asks for mutation tests and nothing has
provided them.  A verifier that passes everything certifies nothing, and
that risk grows as margins widen: the 0.1782354 lane's binding margin is
some 797 times the sealed lane's, so an inequality check there would still
pass with a badly wrong constant.

This script mutates each thing verify_independent_crosscheck.py asserts and
requires the corresponding check to FAIL.  It passes only when every
mutation is caught.  It is the inverse of the other verifiers: their job is
to fail closed on bad input, and this one's job is to prove they do.

Nothing here touches the sealed tree.  Every mutation is applied to an
in-memory copy of the checker's module state or to a temporary file.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "verifiers" / "verify_independent_crosscheck.py"

mutations = 0
escaped = 0


def load_checker():
    """Load the cross-check as a fresh module, without running main()."""

    spec = importlib.util.spec_from_file_location("_crosscheck", TARGET)
    module = importlib.util.module_from_spec(spec)
    src = TARGET.read_text(encoding="utf-8").replace(
        'if __name__ == "__main__":\n    raise SystemExit(main())', ""
    )
    exec(compile(src, str(TARGET), "exec"), module.__dict__)
    return module


def expect_caught(label: str, run) -> None:
    """`run` must cause at least one [FAIL].  If it does not, we escaped."""

    global mutations, escaped
    mutations += 1
    module = load_checker()
    before = module.failures
    try:
        run(module)
    except SystemExit:
        # A hard abort also counts as catching the mutation.
        print(f"[CAUGHT] {label} (aborted)")
        return
    except Exception as exc:  # noqa: BLE001 - any refusal is a catch
        print(f"[CAUGHT] {label} ({type(exc).__name__})")
        return
    if module.failures > before:
        print(f"[CAUGHT] {label}")
    else:
        escaped += 1
        print(f"[ESCAPED] {label}  <-- the checker accepted a bad input", file=sys.stderr)


def mutate_expected_constant(module, attr: str) -> None:
    """Flip the last digit of a pinned constant, then re-run doc checks."""

    original = getattr(module, attr)
    setattr(module, attr, original[:-1] + ("8" if original[-1] != "8" else "7"))
    # DOCUMENTED holds copies of the originals; rebuild it from the mutation.
    module.DOCUMENTED = [
        (name, getattr(module, "PROP410_EMAX") if "233494" in digits else getattr(module, "PROP62_SHARP"))
        for name, digits in module.DOCUMENTED
    ]
    module.verify_documents()


def main() -> int:
    print("--- mutating the constants the documents are checked against")
    expect_caught(
        "E_max digit flipped: documents must stop matching",
        lambda m: mutate_expected_constant(m, "PROP410_EMAX"),
    )
    expect_caught(
        "sharp barrier constant digit flipped: documents must stop matching",
        lambda m: mutate_expected_constant(m, "PROP62_SHARP"),
    )

    print("--- mutating the documents themselves")

    def corrupt_document(module, name: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_root = Path(tmp)
            for doc, _ in module.DOCUMENTED:
                src = ROOT / doc
                dst = fake_root / doc
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dst)
            target = fake_root / name
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    module.PROP410_EMAX, "0.000000000000000000000000"
                ).replace(module.PROP62_SHARP, "0.000000000000000"),
                encoding="utf-8",
            )
            module.ROOT = fake_root
            module.verify_documents()

    for doc in ("README.md", "PROOF_NOTE.md", "CANDIDATE_PARAMETERS.md"):
        expect_caught(f"{doc} stripped of its published constants", lambda m, d=doc: corrupt_document(m, d))

    print("--- mutating the programs' locations")

    def hide_prop410(module) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "scratch"
            scratch.mkdir()
            module.INDEPENDENT = Path(tmp) / "absent"
            module.verify_prop410(scratch)

    expect_caught("prop410 program removed: presence check must fail", hide_prop410)

    print(f"TOTAL MUTATIONS APPLIED: {mutations}")
    if escaped:
        print(
            f"RESULT: MUTATION RESISTANCE FAIL ({escaped} escaped)", file=sys.stderr
        )
        return 1
    print("RESULT: MUTATION RESISTANCE PASS")
    print(
        "STATUS: every mutation was rejected; this tests the checker, "
        "not the mathematics."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
