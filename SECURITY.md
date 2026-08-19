# Security and review policy

## Scope

This repository is a referee package, not an application or service.
The supported review target is the exact commit identified by the current
review tag. Other commits, copied files, or locally modified trees are outside
the release claim.

## Reporting

Report suspected credential exposure, malicious artifacts, unsafe execution,
or proof-certificate tampering privately to the repository owner via
GitHub's private vulnerability reporting for this repository (or, failing
that, a direct channel to the owner) before any public disclosure, so a
correction or advisory can accompany the report. Mathematical errors are
not security issues: raise those openly as issues or referee findings.

## Execution boundary

- `./verify.sh` is the stored, fail-closed entry point.
- Fresh native replay should run in the documented container with networking
  disabled, a read-only repository mount, and a fresh output directory.
- The vendored historical native executable is retained only as sealed
  provenance and is not executed by the review entry points.
- No workflow requires repository secrets, deploy keys, or writable checkout
  credentials.
- Pull-request workflows must not receive secrets or persistent repository
  credentials.

## Integrity boundary

`SHA256SUMS` binds every stable regular file except the manifest itself.
Symlinks, special files, unlisted files, missing files, and common build or
editor debris cause seal verification to fail. Git commit and tag identities
bind the manifest to the reviewed snapshot.

The container base image, Ubuntu package snapshot, and Python wheels are
versioned inputs. Reviewers should record the resulting container identity
and installed native package versions in their replay transcript.

## Expected secret posture

The repository is designed to contain no API keys, access tokens, passwords,
private keys, or credential-bearing URLs. Introducing a secret as a build
argument, workflow secret, committed file, generated PDF field, archive
member, or test fixture is prohibited.

## Trust boundary

The remaining software trust includes Git, Docker, the pinned Ubuntu archive
snapshot, GCC, Python, FLINT/Arb, GMP, MPFR, ReportLab, the operating system,
and GitHub's storage and Actions infrastructure. Independent mathematical
review and independent recomputation are still required; see
`ADVERSARIAL_REVIEW_PROTOCOL.md`.
