# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Pre-stable releases use `v0.x.y` per the fleet versioning rule.

## [Unreleased]

### Added

- npm install gating via PMG ([safedep/pmg](https://github.com/safedep/pmg),
  Apache 2.0). Documented as a declared external dependency; runtime PATH
  check fails closed when PMG is not installed. See README for install
  instructions. Phase 2 (separate): mistral-vibe config allowlist entry
  that routes npm operations through this gate.
- `pmg_npm_gate.py` helper module with `is_pmg_available()` and
  `run_npm_via_pmg(args)`.
- Offline test coverage in `tests/test_pmg_npm_gate.py`.
