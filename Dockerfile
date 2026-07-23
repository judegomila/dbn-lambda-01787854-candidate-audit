# Standalone review environment for the 0.1787854 candidate.
# The base image digest is the Ubuntu 24.04 multi-architecture manifest used
# when this review package was prepared on 2026-07-23.
FROM ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
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

ENV PATH="/opt/dbn-review/bin:${PATH}"
WORKDIR /work

CMD ["./scripts/run_container_review.sh"]
