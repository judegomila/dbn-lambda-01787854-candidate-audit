# Dockerfile — pinned reproduction environment for the three FLINT/Arb
# verifier packages of this bundle (see REPRODUCE_FLINT.md).
#
# Matches the toolchain of the recorded Linux re-runs of 2026-06-13
# (Ubuntu 24.04 "noble": gcc, libflint-dev 3.0.1 = FLINT 3 with Arb
# merged, python3 + numpy 1.26.4 + mpmath, PARI/GP).
#
# Build (from the bundle root):
#   docker build -t dbn21a-flint .
# Run everything (manifest + all pure-Python verifiers + the three
# FLINT/Arb packages live):
#   docker run --rm -v "$PWD":/bundle -w /bundle dbn21a-flint bash check_bundle.sh
# Or a single package:
#   docker run --rm -v "$PWD":/bundle -w /bundle dbn21a-flint \
#     bash -c '( cd certificates/certified1965/grid_full && bash verify.sh )'
FROM ubuntu:24.04

# Pin the distro package set; 24.04 ships libflint-dev 3.0.1 and
# python3-numpy 1.26.4 (the exact pair of the recorded re-runs).
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        libflint-dev \
        libgmp-dev \
        libmpfr-dev \
        python3 \
        python3-numpy \
        python3-mpmath \
        python3-sympy \
        pari-gp \
        coreutils \
    && rm -rf /var/lib/apt/lists/*

# The verifiers invoke /usr/bin/python3 explicitly; nothing else needed.
CMD ["bash"]
