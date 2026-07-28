#!/usr/bin/env python3
"""Fetch one exact private GHCR image into a complete OCI archive.

The GitHub token is read from standard input and is never written to disk.
Every registry object is checked against its sha256 descriptor before the
archive is created.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tarfile
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
)


DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
IMAGE_RE = re.compile(
    r"ghcr\.io/(?P<repository>[a-z0-9_.-]+/[a-z0-9_.-]+)"
    r"@(?P<digest>sha256:[0-9a-f]{64})\Z"
)
MANIFEST_ACCEPT = ", ".join(
    (
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    )
)
USER_AGENT = "dbn-lambda-01787854-release-fetch/1"


class SafeRedirectHandler(HTTPRedirectHandler):
    """Do not forward a registry bearer token to a blob CDN."""

    def redirect_request(self, request, fp, code, message, headers, new_url):
        redirected = super().redirect_request(
            request, fp, code, message, headers, new_url
        )
        if redirected is None:
            return None
        old_parts = urlsplit(request.full_url)
        new_parts = urlsplit(new_url)
        if new_parts.scheme.lower() != "https":
            raise ValueError(f"refusing non-HTTPS redirect to {new_url}")
        old_host = old_parts.netloc
        new_host = new_parts.netloc
        if old_host != new_host:
            redirected.remove_header("Authorization")
        return redirected


OPENER = build_opener(SafeRedirectHandler())


def digest_hex(digest: str) -> str:
    if not DIGEST_RE.fullmatch(digest):
        raise ValueError(f"invalid sha256 descriptor: {digest!r}")
    return digest.split(":", 1)[1]


def request_bytes(url: str, headers: dict[str, str]) -> tuple[bytes, str]:
    request = Request(url, headers={**headers, "User-Agent": USER_AGENT})
    with OPENER.open(request, timeout=60) as response:
        return response.read(), response.headers.get_content_type()


def bearer_token(repository: str, username: str, github_token: str) -> str:
    query = urlencode(
        {
            "service": "ghcr.io",
            "scope": f"repository:{repository}:pull",
        }
    )
    basic = base64.b64encode(
        f"{username}:{github_token}".encode("utf-8")
    ).decode("ascii")
    raw, _ = request_bytes(
        f"https://ghcr.io/token?{query}",
        {"Authorization": f"Basic {basic}", "Accept": "application/json"},
    )
    payload = json.loads(raw)
    token = payload.get("token") or payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise ValueError("GHCR token response did not contain a bearer token")
    return token


def verify_payload(payload: bytes, digest: str, expected_size: int | None) -> None:
    actual = hashlib.sha256(payload).hexdigest()
    if actual != digest_hex(digest):
        raise ValueError(f"digest mismatch for {digest}: got sha256:{actual}")
    if expected_size is not None and len(payload) != expected_size:
        raise ValueError(
            f"size mismatch for {digest}: expected {expected_size}, got {len(payload)}"
        )


def download_blob(
    url: str,
    bearer: str,
    digest: str,
    expected_size: int,
    destination: Path,
) -> None:
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {bearer}",
            "Accept": "application/octet-stream",
            "User-Agent": USER_AGENT,
        },
    )
    hasher = hashlib.sha256()
    size = 0
    with OPENER.open(request, timeout=60) as response, destination.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            size += len(chunk)
            out.write(chunk)
    if hasher.hexdigest() != digest_hex(digest):
        raise ValueError(
            f"digest mismatch for {digest}: got sha256:{hasher.hexdigest()}"
        )
    if size != expected_size:
        raise ValueError(
            f"size mismatch for {digest}: expected {expected_size}, got {size}"
        )


def descriptor(payload: object, name: str) -> tuple[str, int, str]:
    if not isinstance(payload, dict):
        raise ValueError(f"{name} descriptor is not an object")
    digest = payload.get("digest")
    size = payload.get("size")
    media_type = payload.get("mediaType")
    if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
        raise ValueError(f"{name} has an invalid digest")
    if not isinstance(size, int) or size < 0:
        raise ValueError(f"{name} has an invalid size")
    if not isinstance(media_type, str) or not media_type:
        raise ValueError(f"{name} has an invalid media type")
    return digest, size, media_type


def add_bytes(archive: tarfile.TarFile, name: str, payload: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(payload)
    info.mode = 0o644
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    info.mtime = 0
    import io

    archive.addfile(info, io.BytesIO(payload))


def add_file(archive: tarfile.TarFile, name: str, path: Path) -> None:
    info = tarfile.TarInfo(name)
    info.size = path.stat().st_size
    info.mode = 0o644
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    info.mtime = 0
    with path.open("rb") as stream:
        archive.addfile(info, stream)


def canonical_json(payload: object) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch one digest-pinned private GHCR image as a complete OCI tar."
    )
    parser.add_argument(
        "image",
        help="exact image reference, ghcr.io/OWNER/NAME@sha256:DIGEST",
    )
    parser.add_argument("output", type=Path, help="new OCI archive path")
    parser.add_argument("--username", required=True, help="GitHub login")
    parser.add_argument(
        "--token-stdin",
        action="store_true",
        help="required safety flag: read the GitHub token from standard input",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    match = IMAGE_RE.fullmatch(args.image)
    if match is None:
        raise ValueError("image must be an exact lowercase ghcr.io digest reference")
    if not args.token_stdin:
        raise ValueError("--token-stdin is required; tokens are never accepted as arguments")
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    if not args.output.parent.is_dir():
        raise FileNotFoundError(f"output directory does not exist: {args.output.parent}")

    github_token = sys.stdin.readline().strip()
    if not github_token:
        raise ValueError("standard input did not contain a GitHub token")

    repository = match.group("repository")
    manifest_digest = match.group("digest")
    bearer = bearer_token(repository, args.username, github_token)
    github_token = ""

    manifest_url = (
        f"https://ghcr.io/v2/{repository}/manifests/{manifest_digest}"
    )
    manifest_raw, manifest_type = request_bytes(
        manifest_url,
        {
            "Authorization": f"Bearer {bearer}",
            "Accept": MANIFEST_ACCEPT,
        },
    )
    verify_payload(manifest_raw, manifest_digest, None)
    manifest = json.loads(manifest_raw)
    if manifest.get("schemaVersion") != 2:
        raise ValueError("image manifest schemaVersion is not 2")

    config_digest, config_size, _ = descriptor(
        manifest.get("config"), "config"
    )
    layers = manifest.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("image manifest has no layers")
    descriptors = [descriptor(layer, f"layer[{index}]") for index, layer in enumerate(layers)]
    all_descriptors = [(config_digest, config_size)] + [
        (digest, size) for digest, size, _ in descriptors
    ]
    if len({digest for digest, _ in all_descriptors}) != len(all_descriptors):
        raise ValueError("image manifest repeats a config or layer digest")

    output_tmp = args.output.with_name(args.output.name + ".partial")
    if output_tmp.exists():
        raise FileExistsError(f"refusing to overwrite {output_tmp}")

    try:
        with tempfile.TemporaryDirectory(
            prefix="dbn-oci-", dir=str(args.output.parent)
        ) as temp_name:
            temp = Path(temp_name)
            manifest_path = temp / digest_hex(manifest_digest)
            manifest_path.write_bytes(manifest_raw)
            blob_paths: dict[str, Path] = {manifest_digest: manifest_path}
            for digest, size in all_descriptors:
                path = temp / digest_hex(digest)
                download_blob(
                    f"https://ghcr.io/v2/{repository}/blobs/{digest}",
                    bearer,
                    digest,
                    size,
                    path,
                )
                blob_paths[digest] = path

            index = {
                "schemaVersion": 2,
                "mediaType": "application/vnd.oci.image.index.v1+json",
                "manifests": [
                    {
                        "mediaType": manifest.get("mediaType") or manifest_type,
                        "digest": manifest_digest,
                        "size": len(manifest_raw),
                        "annotations": {
                            "org.opencontainers.image.ref.name": manifest_digest
                        },
                    }
                ],
            }
            with tarfile.open(output_tmp, "w", format=tarfile.PAX_FORMAT) as archive:
                add_bytes(
                    archive,
                    "oci-layout",
                    canonical_json({"imageLayoutVersion": "1.0.0"}),
                )
                add_bytes(archive, "index.json", canonical_json(index))
                for digest in [manifest_digest] + [
                    item[0] for item in all_descriptors
                ]:
                    add_file(
                        archive,
                        f"blobs/sha256/{digest_hex(digest)}",
                        blob_paths[digest],
                    )
        os.replace(output_tmp, args.output)
    finally:
        if output_tmp.exists():
            output_tmp.unlink()

    print(f"image_digest={manifest_digest}")
    print(f"config_digest={config_digest}")
    print(f"layer_count={len(descriptors)}")
    print(f"archive={args.output}")
    print("RESULT: COMPLETE OCI IMAGE ARCHIVE CREATED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
