#!/usr/bin/env python3
"""Prove that each candidate tail file is the deposited engine plus one patch."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = ROOT / "vendor" / "deposited" / "assembly1875_1891_secondline.py"
TARGETS = (
    (ROOT / "verifiers" / "verify_tail_1787854_160.py", 160),
    (ROOT / "verifiers" / "verify_tail_1787854_256.py", 256),
)

HEADER = (
    "# AUDIT PATCH TRI178785400SAFE: pristine deposited engine plus the one\n"
    "# delimited parameter block below; no engine formulas changed.\n"
)
BEGIN = (
    "\n# =====================================================================\n"
    "# BEGIN AUDIT PATCH TRI178785400SAFE\n"
)
END = (
    "# END AUDIT PATCH TRI178785400SAFE\n"
    "# =====================================================================\n"
)


def restore_deposited_source(path: Path, precision: int) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("#!/usr/bin/env /usr/bin/python3\n" + HEADER):
        raise AssertionError(f"{path.name}: missing exact audit header")

    text = text.replace(HEADER, "", 1)
    precision_block = f"iv.prec = {precision}\nmp.prec = {precision}\n"
    if text.count(precision_block) != 1:
        raise AssertionError(f"{path.name}: unexpected precision block")
    text = text.replace(
        precision_block,
        "iv.prec = 160\nmp.prec = 160\n",
        1,
    )

    if text.count("MHEAD_MAX = 153814") != 1:
        raise AssertionError(f"{path.name}: unexpected MHEAD_MAX patch")
    text = text.replace("MHEAD_MAX = 153814", "MHEAD_MAX = 50000", 1)

    start = text.find(BEGIN)
    if start < 0:
        raise AssertionError(f"{path.name}: patch begin marker missing")
    finish = text.find(END, start)
    if finish < 0:
        raise AssertionError(f"{path.name}: patch end marker missing")
    finish += len(END)
    text = text[:start] + text[finish:]
    return text


base = BASE_PATH.read_text(encoding="utf-8")
for target, precision in TARGETS:
    restored = restore_deposited_source(target, precision)
    if restored != base:
        raise AssertionError(
            f"{target.name}: changes exist outside the declared audit patch"
        )
    print(
        f"[PASS] {target.name}: deposited engine + "
        f"precision={precision}, MHEAD_MAX=153814, TRI178785400SAFE block"
    )

print("RESULT: TAIL PATCH PROVENANCE PASS")
