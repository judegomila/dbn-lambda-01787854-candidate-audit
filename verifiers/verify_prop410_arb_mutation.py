#!/usr/bin/env python3
"""Prove the Prop 4.10 Arb certificate chain rejects mutated evidence.

Every mutation below is applied to a temporary copy of the sealed
transcripts, source tree, or checker state, and the strict parser
verifiers/verify_prop410_arb_logs.py must refuse it.  This tests the
checker, not the mathematics: a verifier that accepts everything
certifies nothing.  Nothing here touches the sealed tree.

The final group also proves there is no silent fallback to the derived
mpmath cross-check: with the Arb evidence absent, verification fails
even though independent/prop410/prop410_proof.py is present and passes,
and the assembly's P17 wiring is pinned textually.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PARSER = ROOT / "verifiers" / "verify_prop410_arb_logs.py"
LOGS = ROOT / "logs"

mutations = 0
escaped = 0


def load_checker():
    """Load the strict parser as a fresh module without running its CLI."""

    spec = importlib.util.spec_from_file_location("_prop410_logs", PARSER)
    module = importlib.util.module_from_spec(spec)
    src = PARSER.read_text(encoding="utf-8")
    src = src[: src.index('if __name__ == "__main__":')]
    exec(compile(src, str(PARSER), "exec"), module.__dict__)
    return module


def expect_caught(label: str, run) -> None:
    global mutations, escaped
    mutations += 1
    module = load_checker()
    try:
        run(module)
    except Exception as exc:  # noqa: BLE001 - any refusal is a catch
        print(f"[CAUGHT] {label} ({type(exc).__name__})")
        return
    escaped += 1
    print(
        f"[ESCAPED] {label}  <-- the checker accepted bad evidence",
        file=sys.stderr,
    )


def mutated_log_dir(tmp: Path, mutate) -> Path:
    """Copy both sealed transcripts into tmp and apply `mutate` to them."""

    log_dir = tmp / "logs"
    log_dir.mkdir()
    for bits in (256, 512):
        name = f"prop410_arb_{bits}.log"
        text = (LOGS / name).read_text(encoding="utf-8")
        (log_dir / name).write_text(mutate(text, bits), encoding="utf-8")
    return log_dir


def run_with_mutated_logs(label: str, mutate) -> None:
    def run(module) -> None:
        with tempfile.TemporaryDirectory() as name:
            module.main(mutated_log_dir(Path(name), mutate))

    expect_caught(label, run)


def run_with_missing_log(label: str, bits_to_remove: int) -> None:
    def run(module) -> None:
        with tempfile.TemporaryDirectory() as name:
            log_dir = mutated_log_dir(Path(name), lambda text, bits: text)
            (log_dir / f"prop410_arb_{bits_to_remove}.log").unlink()
            module.main(log_dir)

    expect_caught(label, run)


def fake_root(tmp: Path) -> Path:
    """A minimal repository copy carrying the files the parser binds."""

    root = tmp / "repo"
    (root / "verifiers").mkdir(parents=True)
    shutil.copy(
        ROOT / "verifiers" / "verify_prop410_arb.c",
        root / "verifiers" / "verify_prop410_arb.c",
    )
    shutil.copy(ROOT / "PROOF_NOTE.md", root / "PROOF_NOTE.md")
    return root


def main() -> int:
    print("--- transcript mutations the parser must reject")
    run_with_missing_log("256-bit precision run removed", 256)
    run_with_missing_log("512-bit precision run removed", 512)
    run_with_mutated_logs(
        "altered t-box endpoint in the parameter block",
        lambda text, bits: text.replace(
            "PARAM tbox_hi = 161250001/1000000000",
            "PARAM tbox_hi = 161250002/1000000000",
        ),
    )
    run_with_mutated_logs(
        "altered N0 in the domain banner",
        lambda text, bits: text.replace("N0=690988", "N0=690989"),
    )
    run_with_mutated_logs(
        "missing domain/sign gate line",
        lambda text, bits: text.replace(
            "[PASS] gate kappa_domain: 0 < kappa < 1\n", ""
        ),
    )
    run_with_mutated_logs(
        "duplicated decisive result record",
        lambda text, bits: text.replace(
            "Emax upper point = ",
            "Emax upper point = [1e-9 +/- 0]\nEmax upper point = ",
        ),
    )
    run_with_mutated_logs(
        "duplicated terminal success line",
        lambda text, bits: text
        + "RESULT: ALL ARB PROP410 CHECKS PASS\n",
    )
    run_with_mutated_logs(
        "explicit failure marker",
        lambda text, bits: text.replace("[PASS] gate", "[FAIL] gate", 1),
    )
    run_with_mutated_logs(
        "nonzero failure count",
        lambda text, bits: text.replace(
            "TOTAL CHECKS: 31; FAILURES: 0",
            "TOTAL CHECKS: 31; FAILURES: 1",
        ),
    )
    run_with_mutated_logs(
        "nonfinite Emax ball",
        lambda text, bits: re.sub(
            r"^Emax upper point = .*$",
            "Emax upper point = nan",
            text,
            flags=re.MULTILINE,
        ),
    )
    run_with_mutated_logs(
        "insufficient precision in the banner",
        lambda text, bits: text.replace(
            f"precision={bits},", "precision=255,"
        ),
    )
    run_with_mutated_logs(
        "Emax endpoint above the stated bound",
        lambda text, bits: re.sub(
            r"^Emax upper point = .*$",
            "Emax upper point = [2.4e-7 +/- 1e-30]",
            text,
            flags=re.MULTILINE,
        ),
    )
    run_with_mutated_logs(
        "unexpected extra parameter record",
        lambda text, bits: text.replace(
            "PARAM m0 = 2000\n",
            "PARAM m0 = 2000\nPARAM extra = 1/2\n",
        ),
    )
    run_with_mutated_logs(
        "too-small stated Emax threshold in the parameter block",
        lambda text, bits: text.replace(
            "PARAM stated_Emax = 233494905212337849/10^24",
            "PARAM stated_Emax = 133494905212337849/10^24",
        ),
    )

    print("--- source and document binding mutations")

    def remove_program(module) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = fake_root(Path(name))
            (root / "verifiers" / "verify_prop410_arb.c").unlink()
            module.ROOT = root
            module.check_bindings()

    expect_caught("Arb program removed", remove_program)

    def alter_source_tbox(module) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = fake_root(Path(name))
            source = root / "verifiers" / "verify_prop410_arb.c"
            source.write_text(
                source.read_text(encoding="utf-8").replace(
                    "set_q(thi, 161250001, 1000000000UL);",
                    "set_q(thi, 161250002, 1000000000UL);",
                ),
                encoding="utf-8",
            )
            module.ROOT = root
            module.check_bindings()

    expect_caught("t-box endpoint altered in the Arb source", alter_source_tbox)

    def alter_source_n0(module) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = fake_root(Path(name))
            source = root / "verifiers" / "verify_prop410_arb.c"
            source.write_text(
                source.read_text(encoding="utf-8").replace(
                    "#define N0 690988UL", "#define N0 690989UL"
                ),
                encoding="utf-8",
            )
            module.ROOT = root
            module.check_bindings()

    expect_caught("N0 altered in the Arb source", alter_source_n0)

    def strip_backend_note(module) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = fake_root(Path(name))
            note = root / "PROOF_NOTE.md"
            note.write_text(
                note.read_text(encoding="utf-8").replace(
                    "same-backend replay", "independent implementation"
                ),
                encoding="utf-8",
            )
            module.ROOT = root
            module.check_bindings()

    expect_caught(
        "PROOF_NOTE.md reclassifies the mpmath copy as independent",
        strip_backend_note,
    )

    print("--- no fallback to the mpmath result when Arb evidence is absent")

    def no_fallback(module) -> None:
        assert (ROOT / "independent" / "prop410" / "prop410_proof.py").is_file()
        with tempfile.TemporaryDirectory() as name:
            empty = Path(name) / "logs"
            empty.mkdir()
            module.main(empty)

    expect_caught(
        "empty evidence directory despite a passing mpmath program",
        no_fallback,
    )

    assembly = (ROOT / "verifiers" / "verify_assembly_1787854.py").read_text(
        encoding="utf-8"
    )
    wired = (
        "verifiers/verify_prop410_arb_logs.py" in assembly
        and "RESULT: SEALED ARB PROP410 CERTIFICATES PASS" in assembly
        and re.search(r"p17,\s*\n\s*a3,", assembly) is not None
    )
    mutations_note = "[CAUGHT]" if wired else "[ESCAPED]"
    global escaped
    if not wired:
        escaped += 1
    print(
        f"{mutations_note} assembly P17 wiring pins the Arb parser inside "
        "hypothesis (ii)"
    )

    print(f"TOTAL MUTATIONS APPLIED: {mutations + 1}")
    if escaped:
        print(
            f"RESULT: PROP410 ARB MUTATION RESISTANCE FAIL ({escaped} escaped)",
            file=sys.stderr,
        )
        return 1
    print("RESULT: PROP410 ARB MUTATION RESISTANCE PASS")
    print(
        "STATUS: every mutation was rejected; this tests the checker, "
        "not the mathematics."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
