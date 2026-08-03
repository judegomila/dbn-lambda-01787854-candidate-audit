#!/usr/bin/env python3
"""Write or verify the exact stable-file SHA-256 inventory.

The stable tree is the repository tree after excluding only:

* repository-local transient roots: .git, .venv, replay, and tmp;
* unsealed content roots: dan-reworking and research (see below);
* Python cache directories named __pycache__; and
* SHA256SUMS itself (a manifest cannot contain its own digest).

Everything else is part of the seal.  In check mode, an unlisted regular
file, a missing listed file, a malformed/duplicate entry, a hash mismatch,
or any symlink/special file in the stable tree is fatal.

Known stray editor/build products (.DS_Store, *.pyc, *.pyo, *.pyd, *.o, and
*.out) are forbidden outside the excluded roots.  They are not silently
omitted and cannot accidentally become part of a release seal.

An excluded root is not descended into at all, so none of the checks above
apply anywhere inside it: such a subtree may contain symlinks, special
files, stray build products, and files absent from SHA256SUMS.

The transient roots hold generated or ephemeral state.  The unsealed
content roots are different in kind: they hold durable content, kept out
of the seal so that active work can iterate without resealing the audited
artifact on every rebuild.  Nothing under them is attested by SHA256SUMS
or by verify.sh, and they are outside the reviewed surface.

* dan-reworking is the referee's in-progress workspace.
* research is the exploratory lane: work that is deliberately not part of
  the candidate and is not evidence for it.

Neither is a place to park material that the candidate relies on.  When a
program under either root becomes load-bearing it must be promoted into
the sealed tree, as independent/ records for the recomputation programs.
See REVIEW_SCOPE.md for scope and THIRD_PARTY.md for third-party material
these roots carry.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_NAME = "SHA256SUMS"
TRANSIENT_ROOTS = {".git", ".venv", "replay", "tmp"}
UNSEALED_CONTENT_ROOTS = {"dan-reworking", "research"}
EXCLUDED_ROOTS = TRANSIENT_ROOTS | UNSEALED_CONTENT_ROOTS
EXCLUDED_DIR_NAMES = {"__pycache__"}
FORBIDDEN_FILE_NAMES = {".DS_Store"}
FORBIDDEN_FILE_SUFFIXES = {".o", ".out", ".pyc", ".pyd", ".pyo"}
HEX_DIGITS = frozenset("0123456789abcdef")


class SealError(RuntimeError):
    """A fail-closed seal validation error."""


def relative_display(parts: tuple[str, ...]) -> str:
    return "./" + PurePosixPath(*parts).as_posix()


def stable_files() -> dict[str, Path]:
    """Return the exact stable inventory, rejecting links and special files."""

    found: dict[str, Path] = {}

    def visit(directory: Path, parts: tuple[str, ...]) -> None:
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise SealError(f"cannot scan {relative_display(parts)}: {exc}") from exc

        for entry in entries:
            child_parts = parts + (entry.name,)
            display = relative_display(child_parts)
            if "\n" in entry.name or "\r" in entry.name:
                raise SealError(f"newline forbidden in stable path: {display!r}")
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as exc:
                raise SealError(f"cannot stat {display}: {exc}") from exc

            if stat.S_ISLNK(mode):
                raise SealError(f"symlink forbidden in stable tree: {display}")

            if not parts and entry.name in EXCLUDED_ROOTS:
                if stat.S_ISDIR(mode):
                    continue
                # In a git worktree or submodule checkout, .git is a
                # regular file holding a gitdir: pointer rather than a
                # directory.  Its contents are outside the seal in either
                # form, so accepting the file form costs no coverage and
                # lets a reviewer check the seal from a worktree.  A
                # symlink is still refused above.  Every other excluded
                # root must be a real directory: replacing one with a
                # file would hide content that belongs in the tree.
                if entry.name == ".git" and stat.S_ISREG(mode):
                    continue
                raise SealError(f"excluded root is not a directory: {display}")
            if stat.S_ISDIR(mode) and entry.name in EXCLUDED_DIR_NAMES:
                continue
            if stat.S_ISDIR(mode):
                visit(Path(entry.path), child_parts)
                continue
            if not stat.S_ISREG(mode):
                raise SealError(f"special file forbidden in stable tree: {display}")
            if not parts and entry.name == MANIFEST_NAME:
                continue
            if (
                entry.name in FORBIDDEN_FILE_NAMES
                or Path(entry.name).suffix in FORBIDDEN_FILE_SUFFIXES
            ):
                raise SealError(
                    f"stray editor/build artifact forbidden in stable tree: {display}"
                )
            found[display] = Path(entry.path)

    visit(ROOT, ())
    return found


def digest_regular_file(path: Path, display: str) -> str:
    """Hash one regular file without following a last-component symlink."""

    flags = os.O_RDONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise SealError(f"cannot open {display}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise SealError(f"not a regular file while hashing: {display}")
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1024 * 1024)
            if not block:
                break
            hasher.update(block)
        after = os.fstat(descriptor)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise SealError(f"file changed while hashing: {display}")
        return hasher.hexdigest()
    finally:
        os.close(descriptor)


def build_manifest(inventory: dict[str, Path]) -> str:
    lines = [
        f"{digest_regular_file(inventory[name], name)}  {name}\n"
        for name in sorted(inventory)
    ]
    return "".join(lines)


def parse_manifest(path: Path) -> dict[str, str]:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError as exc:
        raise SealError(f"missing {MANIFEST_NAME}") from exc
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise SealError(f"{MANIFEST_NAME} must be a regular, non-symlink file")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SealError(f"cannot read {MANIFEST_NAME}: {exc}") from exc
    if not raw.endswith(b"\n"):
        raise SealError(f"{MANIFEST_NAME} must end with a newline")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise SealError(f"{MANIFEST_NAME} is not ASCII") from exc

    parsed: dict[str, str] = {}
    previous = ""
    for line_number, line in enumerate(text.splitlines(), 1):
        if len(line) < 68 or line[64:68] != "  ./":
            raise SealError(f"{MANIFEST_NAME}:{line_number}: malformed entry")
        digest = line[:64]
        name = line[66:]
        if any(character not in HEX_DIGITS for character in digest):
            raise SealError(f"{MANIFEST_NAME}:{line_number}: invalid SHA-256")
        pure = PurePosixPath(name[2:])
        if (
            not name.startswith("./")
            or pure.is_absolute()
            or not pure.parts
            or any(part in {"", ".", ".."} for part in pure.parts)
            or pure.as_posix() != name[2:]
        ):
            raise SealError(f"{MANIFEST_NAME}:{line_number}: noncanonical path")
        if name in parsed:
            raise SealError(f"{MANIFEST_NAME}:{line_number}: duplicate {name}")
        if previous and name <= previous:
            raise SealError(
                f"{MANIFEST_NAME}:{line_number}: entries are not strictly sorted"
            )
        parsed[name] = digest
        previous = name
    if not parsed:
        raise SealError(f"{MANIFEST_NAME} is empty")
    return parsed


def check() -> None:
    inventory = stable_files()
    expected = parse_manifest(ROOT / MANIFEST_NAME)
    actual_names = set(inventory)
    expected_names = set(expected)
    extras = sorted(actual_names - expected_names)
    missing = sorted(expected_names - actual_names)
    if extras or missing:
        details: list[str] = []
        if extras:
            details.append("unsealed extra files: " + ", ".join(extras))
        if missing:
            details.append("missing sealed files: " + ", ".join(missing))
        raise SealError("; ".join(details))

    mismatches = [
        name
        for name in sorted(expected)
        if digest_regular_file(inventory[name], name) != expected[name]
    ]
    if mismatches:
        raise SealError("SHA-256 mismatch: " + ", ".join(mismatches))
    print(f"RESULT: SHA-256 SEAL PASS ({len(expected)} stable files)")


def write() -> None:
    manifest = build_manifest(stable_files())
    transient = ROOT / "tmp"
    transient.mkdir(mode=0o700, exist_ok=True)
    if transient.is_symlink() or not transient.is_dir():
        raise SealError("./tmp must be a real directory")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix="SHA256SUMS.", dir=transient
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "w", encoding="ascii", newline="\n") as stream:
            stream.write(manifest)
            stream.flush()
            os.fsync(stream.fileno())
        target = ROOT / MANIFEST_NAME
        if os.path.lexists(target) and target.is_symlink():
            raise SealError(f"{MANIFEST_NAME} must not be a symlink")
        os.replace(temporary, target)
    finally:
        if os.path.lexists(temporary):
            temporary.unlink()
    print(f"RESULT: WROTE SHA-256 SEAL ({manifest.count(chr(10))} stable files)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.check:
            check()
        else:
            write()
    except (OSError, SealError) as exc:
        print(f"SEAL FAILURE: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
