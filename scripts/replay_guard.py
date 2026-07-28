#!/usr/bin/env python3
"""Create fresh replay roots and validate regular evidence files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path, PurePath
import stat
import sys


class GuardError(RuntimeError):
    pass


def within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def reject_repo_component_links(raw: Path, root: Path) -> None:
    try:
        relative = raw.relative_to(root)
    except ValueError:
        return
    cursor = root
    for component in relative.parts[:-1]:
        cursor /= component
        if os.path.lexists(cursor) and cursor.is_symlink():
            raise GuardError(f"repository output path crosses symlink: {cursor}")


def prepare(root_text: str, output_text: str) -> None:
    root_raw = Path(os.path.abspath(os.path.expanduser(root_text)))
    if root_raw.is_symlink():
        raise GuardError("repository root must not be a symlink")
    root = root_raw.resolve(strict=True)
    if not root.is_dir():
        raise GuardError("repository root is not a directory")
    if not output_text:
        raise GuardError("empty output path")

    raw = Path(os.path.abspath(os.path.expanduser(output_text)))
    reject_repo_component_links(raw, root_raw)
    if os.path.lexists(raw):
        kind = "symlink" if raw.is_symlink() else "existing path"
        raise GuardError(f"fresh output required; refusing {kind}: {raw}")
    output = raw.resolve(strict=False)
    filesystem_root = Path(output.anchor)
    if output == filesystem_root:
        raise GuardError("refusing filesystem root as replay output")
    if output == root or within(root, output):
        raise GuardError("refusing repository root or its ancestor as replay output")
    if within(output, root) and not within(output, root / "replay"):
        raise GuardError(
            "output inside repository must be below the transient replay/ directory"
        )
    if os.path.lexists(output):
        kind = "symlink" if output.is_symlink() else "existing path"
        raise GuardError(f"fresh output required; refusing {kind}: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir(mode=0o700)
    mode = output.lstat().st_mode
    if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
        raise GuardError(f"failed to create a real output directory: {output}")
    print(output)


def require_files(root_text: str, names: list[str]) -> None:
    root_raw = Path(root_text)
    if root_raw.is_symlink():
        raise GuardError(f"evidence root is a symlink: {root_raw}")
    root = root_raw.resolve(strict=True)
    if not root.is_dir():
        raise GuardError(f"evidence root is not a directory: {root}")
    if not names:
        raise GuardError("no evidence paths supplied")
    for name in names:
        pure = PurePath(name)
        if (
            pure.is_absolute()
            or not pure.parts
            or any(part in {"", ".", ".."} for part in pure.parts)
            or str(pure) != name
        ):
            raise GuardError(f"noncanonical evidence path: {name}")
        path = root
        mode = 0
        for part in pure.parts:
            path /= part
            try:
                mode = path.lstat().st_mode
            except FileNotFoundError as exc:
                raise GuardError(f"missing evidence file: {name}") from exc
            if stat.S_ISLNK(mode):
                raise GuardError(f"evidence path crosses symlink: {name}")
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise GuardError(f"evidence is not a regular non-symlink file: {name}")
        if path.stat().st_size == 0:
            raise GuardError(f"empty evidence file: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("root")
    prepare_parser.add_argument("output")
    require_parser = subparsers.add_parser("require")
    require_parser.add_argument("root")
    require_parser.add_argument("names", nargs="+")
    arguments = parser.parse_args()
    try:
        if arguments.command == "prepare":
            prepare(arguments.root, arguments.output)
        else:
            require_files(arguments.root, arguments.names)
    except (GuardError, OSError) as exc:
        print(f"REPLAY GUARD FAILURE: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
