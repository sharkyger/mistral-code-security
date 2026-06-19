# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Pre-stable releases use `v0.x.y` per the fleet versioning rule.

## [Unreleased]

## [0.1.0] - 2026-06-19

First tagged release of the Mistral-side CVE gate.

### Added

- npm install gating via PMG ([safedep/pmg](https://github.com/safedep/pmg),
  Apache 2.0). Documented as a declared external dependency; runtime PATH
  check fails closed when PMG is not installed. See README for install
  instructions. Phase 2 (separate): mistral-vibe config allowlist entry
  that routes npm operations through this gate.
- `pmg_npm_gate.py` helper module with `is_pmg_available()` and
  `run_npm_via_pmg(args)`, plus offline test coverage in
  `tests/test_pmg_npm_gate.py`.
- CI workflow (`.github/workflows/ci.yml`): pytest matrix on Python
  3.10/3.11/3.12 + shellcheck on the hooks and installer. The repo's own
  tests now run on every push/PR (previously local-only).
- `--allow-unknown-age` flag to opt out of the fail-closed freshness hold.

### Security

- **Freshness hold now fails CLOSED on unverifiable age** (pip/npm). Previously
  `check_min_age` returned "no hold" when a package's age could not be
  determined (registry timestamp missing or lookup failed), waving it through —
  the freshness defense exists precisely for versions too new for the CVE DBs,
  exactly when the timestamp is most likely unfetchable. An unknown age is now
  HELD unless `--allow-unknown-age` is passed. Aligns with the fleet
  fail-closed rule; regression tests added.

### Fixed

- `datetime.UTC` → `datetime.timezone.utc` in the release-age path. `datetime.UTC`
  only exists on Python 3.11+, so the freshness-hold age computation raised an
  uncaught `AttributeError` on Python 3.10.
- Corrected the security-advisory contact URL in `.github/ISSUE_TEMPLATE/config.yml`
  (pointed at a non-existent `mistral-code-security` repo).
- `hooks/pii-redaction-gate.sh`: removed an ERE negative-lookahead `(?!...)` that
  POSIX `grep -E` never supported (so it never matched as intended); added a
  Bash 3.2 empty-array guard under `set -u`.
- `hooks/gitleaks-pre-write.sh`: byte-faithful `printf` instead of `echo`;
  empty-path fallback so `basename` never yields `.`.
- `hooks/secret-leak-detector.sh`: removed a dead variable.
- `agents/security-{red,blue}-team.md`: corrected references to non-existent
  script paths.

[Unreleased]: https://github.com/sharkyger/mistral-code-cve-gate/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sharkyger/mistral-code-cve-gate/releases/tag/v0.1.0
