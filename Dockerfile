# Standalone review environment for the 0.1787854 candidate.
# The base is the exact linux/amd64 child manifest selected from Ubuntu's
# 24.04 index on 2026-07-23.  Do not replace it with the multi-architecture
# index: Noble arm64 resolves through ports.ubuntu.com, which is not covered
# by Ubuntu's dated archive snapshot service.
FROM ubuntu:24.04@sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf

# Freeze package resolution to the signed Ubuntu archive as it existed when
# this review package was prepared.  The minimal Ubuntu image has no CA bundle,
# so the first transaction relies on APT's archive signatures and package
# hashes while bootstrapping ca-certificates; all later HTTPS is authenticated.
RUN sed -i '/^Signed-By:/a Snapshot: 20260723T000000Z' \
        /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 \
        -o APT::Update::Error-Mode=any \
        -o Acquire::https::Verify-Peer=false \
        --snapshot 20260723T000000Z update \
    && DEBIAN_FRONTEND=noninteractive apt-get \
        -o Acquire::Retries=5 \
        -o Acquire::https::Verify-Peer=false \
        --snapshot 20260723T000000Z install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -o Acquire::Retries=5 \
        -o APT::Update::Error-Mode=any \
        --snapshot 20260723T000000Z update \
    && DEBIAN_FRONTEND=noninteractive apt-get \
        -o Acquire::Retries=5 \
        --snapshot 20260723T000000Z install -y --no-install-recommends \
        coreutils \
        diffutils \
        gcc \
        gzip \
        libc6-dev \
        libflint-dev \
        libgmp-dev \
        libmpfr-dev \
        pari-gp \
        python3 \
        python3-mpmath \
        python3-sympy \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/review-requirements.txt
RUN python3 -m venv /opt/dbn-review \
    && /opt/dbn-review/bin/pip install --no-cache-dir --require-hashes \
       -r /tmp/review-requirements.txt

ENV PATH="/opt/dbn-review/bin:${PATH}" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0
LABEL org.opencontainers.image.title="DBN Lambda 0.1787854 review environment" \
      org.opencontainers.image.description="Pinned linux/amd64 verifier toolchain using the Ubuntu archive snapshot 20260723T000000Z" \
      org.opencontainers.image.source="https://github.com/judegomila/dbn-lambda-01787854-candidate-audit" \
      org.opencontainers.image.base.digest="sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf" \
      org.opencontainers.image.dbn.ubuntu-snapshot="20260723T000000Z" \
      org.opencontainers.image.dbn.platform="linux/amd64"
WORKDIR /work

CMD ["./scripts/run_container_review.sh"]
