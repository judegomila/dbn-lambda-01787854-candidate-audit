#!/usr/bin/env python3
"""Verify the complete OCI archive attached to the reviewer release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile


DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
BLOB_NAME_RE = re.compile(r"blobs/sha256/([0-9a-f]{64})\Z")
MAX_JSON_SIZE = 1024 * 1024
ALLOWED_DIRECTORY_NAMES = {"blobs", "blobs/sha256"}
EXPECTED_LABELS = {
    "org.opencontainers.image.base.digest": (
        "sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf"
    ),
    "org.opencontainers.image.dbn.ubuntu-snapshot": "20260723T000000Z",
    "org.opencontainers.image.dbn.platform": "linux/amd64",
    "org.opencontainers.image.source": (
        "https://github.com/judegomila/dbn-lambda-01787854-candidate-audit"
    ),
}


def digest_hex(digest: str) -> str:
    if not DIGEST_RE.fullmatch(digest):
        raise ValueError(f"invalid sha256 descriptor: {digest!r}")
    return digest.split(":", 1)[1]


def descriptor(payload: object, name: str) -> tuple[str, int]:
    if not isinstance(payload, dict):
        raise ValueError(f"{name} descriptor is not an object")
    digest = payload.get("digest")
    size = payload.get("size")
    if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
        raise ValueError(f"{name} has an invalid digest")
    if not isinstance(size, int) or size < 0:
        raise ValueError(f"{name} has an invalid size")
    return digest, size


def read_member(
    archive: tarfile.TarFile, members: dict[str, tarfile.TarInfo], name: str
) -> bytes:
    member = members.get(name)
    if member is None or not member.isfile():
        raise ValueError(f"missing regular archive member: {name}")
    if member.size > MAX_JSON_SIZE:
        raise ValueError(f"JSON member is unexpectedly large: {name}")
    stream = archive.extractfile(member)
    if stream is None:
        raise ValueError(f"cannot read archive member: {name}")
    return stream.read()


def json_member(
    archive: tarfile.TarFile, members: dict[str, tarfile.TarInfo], name: str
) -> object:
    return json.loads(read_member(archive, members, name))


def verify_blob(
    archive: tarfile.TarFile, member: tarfile.TarInfo, expected_hex: str
) -> None:
    stream = archive.extractfile(member)
    if stream is None:
        raise ValueError(f"cannot read blob: {member.name}")
    hasher = hashlib.sha256()
    while True:
        chunk = stream.read(1024 * 1024)
        if not chunk:
            break
        hasher.update(chunk)
    if hasher.hexdigest() != expected_hex:
        raise ValueError(
            f"blob digest mismatch: {member.name} hashes to {hasher.hexdigest()}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the DBN reviewer OCI archive and its exact image identity."
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("--manifest-digest", required=True)
    parser.add_argument("--config-digest", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_hex = digest_hex(args.manifest_digest)
    config_hex = digest_hex(args.config_digest)

    with tarfile.open(args.archive, "r:*") as archive:
        members: dict[str, tarfile.TarInfo] = {}
        blob_members: dict[str, tarfile.TarInfo] = {}
        canonical_members: set[str] = set()
        for member in archive:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"unsafe archive path: {member.name}")
            if member.name in members:
                raise ValueError(f"duplicate archive member: {member.name}")
            if not (member.isfile() or member.isdir()):
                raise ValueError(f"unsupported archive member type: {member.name}")
            canonical_name = member.name.rstrip("/")
            if canonical_name in canonical_members:
                raise ValueError(
                    f"duplicate canonical archive member: {member.name}"
                )
            canonical_members.add(canonical_name)
            if member.isdir():
                if canonical_name not in ALLOWED_DIRECTORY_NAMES:
                    raise ValueError(
                        f"unexpected archive directory: {member.name}"
                    )
            elif (
                member.name not in {"oci-layout", "index.json"}
                and BLOB_NAME_RE.fullmatch(member.name) is None
            ):
                raise ValueError(
                    f"unexpected regular archive member: {member.name}"
                )
            members[member.name] = member
            match = BLOB_NAME_RE.fullmatch(member.name)
            if match:
                if not member.isfile():
                    raise ValueError(f"blob is not a regular file: {member.name}")
                blob_members[match.group(1)] = member

        if not blob_members:
            raise ValueError("archive contains no OCI blobs")

        layout = json_member(archive, members, "oci-layout")
        if layout != {"imageLayoutVersion": "1.0.0"}:
            raise ValueError("invalid oci-layout")
        index = json_member(archive, members, "index.json")
        if not isinstance(index, dict) or index.get("schemaVersion") != 2:
            raise ValueError("invalid OCI index")
        manifests = index.get("manifests")
        if not isinstance(manifests, list) or len(manifests) != 1:
            raise ValueError("OCI index must contain exactly one image manifest")
        indexed_digest, indexed_size = descriptor(manifests[0], "index manifest")
        if indexed_digest != args.manifest_digest:
            raise ValueError(
                f"manifest digest mismatch: expected {args.manifest_digest}, "
                f"index records {indexed_digest}"
            )

        manifest_member = blob_members.get(manifest_hex)
        if manifest_member is None:
            raise ValueError("manifest blob is missing")
        if manifest_member.size != indexed_size:
            raise ValueError("manifest descriptor size does not match blob size")
        verify_blob(archive, manifest_member, manifest_hex)
        manifest = json.loads(read_member(archive, members, manifest_member.name))
        if not isinstance(manifest, dict) or manifest.get("schemaVersion") != 2:
            raise ValueError("invalid image manifest")

        recorded_config, config_size = descriptor(
            manifest.get("config"), "config"
        )
        if recorded_config != args.config_digest:
            raise ValueError(
                f"config digest mismatch: expected {args.config_digest}, "
                f"manifest records {recorded_config}"
            )
        config_member = blob_members.get(config_hex)
        if config_member is None or config_member.size != config_size:
            raise ValueError("config blob is missing or has the wrong size")

        layers = manifest.get("layers")
        if not isinstance(layers, list) or not layers:
            raise ValueError("image manifest has no layers")
        layer_digests: list[str] = []
        for index_number, layer in enumerate(layers):
            layer_digest, layer_size = descriptor(
                layer, f"layer[{index_number}]"
            )
            layer_hex = digest_hex(layer_digest)
            layer_member = blob_members.get(layer_hex)
            if layer_member is None or layer_member.size != layer_size:
                raise ValueError(
                    f"layer blob is missing or has the wrong size: {layer_digest}"
                )
            layer_digests.append(layer_digest)
        if len(set(layer_digests)) != len(layer_digests):
            raise ValueError("image manifest repeats a layer digest")
        expected_blob_hexes = {
            manifest_hex,
            config_hex,
            *(digest_hex(digest) for digest in layer_digests),
        }
        actual_blob_hexes = set(blob_members)
        if actual_blob_hexes != expected_blob_hexes:
            extras = sorted(actual_blob_hexes - expected_blob_hexes)
            missing = sorted(expected_blob_hexes - actual_blob_hexes)
            details: list[str] = []
            if extras:
                details.append("unreferenced blobs: " + ", ".join(extras))
            if missing:
                details.append("missing referenced blobs: " + ", ".join(missing))
            raise ValueError("; ".join(details))
        for blob_hex, member in blob_members.items():
            if blob_hex != manifest_hex:
                verify_blob(archive, member, blob_hex)

        config = json.loads(read_member(archive, members, config_member.name))
        if not isinstance(config, dict):
            raise ValueError("image config is not an object")
        if config.get("os") != "linux" or config.get("architecture") != "amd64":
            raise ValueError(
                f"wrong image platform: {config.get('os')}/{config.get('architecture')}"
            )
        runtime_config = config.get("config")
        labels = (
            runtime_config.get("Labels")
            if isinstance(runtime_config, dict)
            else None
        )
        if not isinstance(labels, dict):
            raise ValueError("image config has no label object")
        for key, expected in EXPECTED_LABELS.items():
            actual = labels.get(key)
            if actual != expected:
                raise ValueError(
                    f"wrong image label {key}: expected {expected!r}, got {actual!r}"
                )

        rootfs = config.get("rootfs")
        diff_ids = rootfs.get("diff_ids") if isinstance(rootfs, dict) else None
        if not isinstance(diff_ids, list) or len(diff_ids) != len(layers):
            raise ValueError("config rootfs diff-id count does not match layer count")

    print(f"manifest_digest={args.manifest_digest}")
    print(f"config_digest={args.config_digest}")
    print(f"layer_count={len(layer_digests)}")
    print(f"verified_blob_count={len(blob_members)}")
    print("platform=linux/amd64")
    print("RESULT: COMPLETE OCI IMAGE ARCHIVE VERIFIED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
