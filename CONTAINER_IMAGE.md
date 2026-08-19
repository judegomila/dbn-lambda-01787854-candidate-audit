# Canonical review container

## Build inputs

The root `Dockerfile` defines the canonical Linux review environment. It pins:

- the exact Ubuntu 24.04 linux/amd64 child-manifest digest;
- the Ubuntu archive snapshot timestamp;
- the native package set; and
- the SHA-256-locked Python requirements.

The architecture is deliberately fixed to `linux/amd64`. Reviewers on another
host architecture should use Docker's emulation rather than silently resolving
packages from a different Ubuntu archive.

The build retries transient archive downloads up to five times, but treats any
incomplete package-index update as fatal. It never falls back to a live mirror
or a different snapshot date. GitHub Actions also retains the complete
container-build transcript when acquisition fails before proof replay begins.

## Local build

```sh
docker build --platform linux/amd64 \
  -t dbn-lambda-01787854-review .
```

The repository's replay scripts reject an image whose recorded snapshot,
architecture, or reviewed build-input identity does not match the sealed
release.

## Published verified review image

The release-tag workflow in `.github/workflows/publish-verified-image.yml`
builds one image, runs the stored/critical replay and the complete
3,149,013-row replay against that exact local image, and only then publishes
it to:

```text
ghcr.io/judegomila/dbn-lambda-01787854-review
```

OCI image bytes include builder-created metadata, so two correct builds need
not have the same registry digest. The release contract therefore uses only
the digest produced by the tag workflow's single tested build. That exact
`image@sha256:...` reference is written to `REVIEW_IMAGE.txt` in the workflow
artifact and attached to the immutable GitHub release. GitHub's release
attestation binds the review tag, commit, PDF, seal, and digest record.

The GHCR container package has its own visibility setting, independent of
the repository's: while it remains access-controlled, pulling it requires
the authenticated flow below, and the complete offline image archive
attached to the release provides the same bytes without registry access.
Keyless public-transparency-log signing was deferred while the repository
was private and can now be adopted; the release contract meanwhile binds
the image by its recorded digest. No signing key or repository secret is
required.

## Complete offline image archive

The v3 release also carries
`dbn-lambda-01787854-review-v3.oci.tar`, a complete OCI archive containing
the exact registry manifest, config, and every referenced layer.  It is not a
thin Docker export.  `RELEASE_MANIFEST.json` records the expected manifest
and config digests.  Verify the archive before loading it:

```sh
python3 scripts/verify_release_image_archive.py \
  dbn-lambda-01787854-review-v3.oci.tar \
  --manifest-digest sha256:MANIFEST_DIGEST \
  --config-digest sha256:CONFIG_DIGEST
docker load --input dbn-lambda-01787854-review-v3.oci.tar
```

The verifier hashes the manifest, config, and every layer; rejects missing,
duplicate, extra, or unreferenced archive members; checks all descriptor
sizes; and enforces the linux/amd64 platform and pinned release labels.  Once
loaded, the image can be run offline by its config digest
`sha256:CONFIG_DIGEST` with the same read-only, no-network invocation below.

`scripts/fetch_release_image_oci.py` independently reconstructs this archive
from the exact GHCR digest.  It reads a GitHub token only from
standard input, strips registry authorization on cross-host redirects, checks
each downloaded descriptor, and never stores the token in the archive.

While the GHCR package is access-controlled, an authorized reviewer can
authenticate to the registry and pull the recorded immutable digest. The
GitHub token used for `docker login` must have `read:packages` access:

```sh
gh release download review-01787854-v3 --pattern REVIEW_IMAGE.txt --clobber
gh release verify review-01787854-v3
gh release verify-asset review-01787854-v3 REVIEW_IMAGE.txt
gh auth refresh -h github.com -s read:packages
review_docker_config=$(mktemp -d)
review_docker_host=$(docker context inspect --format '{{.Endpoints.docker.Host}}')
cleanup_review_registry() {
  DOCKER_HOST="$review_docker_host" \
    docker --config "$review_docker_config" logout ghcr.io >/dev/null 2>&1 || true
  rm -rf -- "$review_docker_config"
}
trap cleanup_review_registry EXIT INT TERM
gh auth token | DOCKER_HOST="$review_docker_host" \
  docker --config "$review_docker_config" login \
  ghcr.io -u GITHUB_USERNAME --password-stdin
DOCKER_HOST="$review_docker_host" \
docker --config "$review_docker_config" pull \
  ghcr.io/judegomila/dbn-lambda-01787854-review@sha256:DIGEST
mkdir -p replay/published-image-review
DOCKER_HOST="$review_docker_host" docker run \
  --rm --platform linux/amd64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --tmpfs /tmp:rw,exec,nosuid,size=4g \
  -e REVIEW_OUTPUT=/review-output/evidence \
  -v "$PWD:/work:ro" \
  -v "$PWD/replay/published-image-review:/review-output" \
  -w /work \
  ghcr.io/judegomila/dbn-lambda-01787854-review@sha256:DIGEST
cleanup_review_registry
trap - EXIT INT TERM
```

Replace `DIGEST` only with the `image_digest` value from the verified release
asset.  The temporary Docker configuration isolates the short-lived registry
credential from the reviewer's normal Docker configuration, and the trap
removes it on normal exit, error, or interruption.

A tag is only a convenient name. The SHA-256 digest is the immutable image
identity used for review, and the release asset records which exact image
passed both replay lanes.
