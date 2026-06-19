# Product Requirements Document — mistral-code-cve-gate

> Last updated: 2026-05-30 — SKELETON draft (pending Sharky's review of TODOs)
> Third-party tool. Not affiliated with Mistral.

## Mission

Pre-install CVE gate for Mistral-powered AI coding tools (Mistral Codestral, Le Chat). Intercepts every `pip install`, `npm install`, `composer install`, `cargo`, `go get`, `gem install`, and `brew install` the AI assistant suggests; queries 3 vulnerability databases (NIST NVD + OSV.dev + GitHub Advisory) for the target version (including the transitive tree); blocks the install if known unpatched vulnerabilities are found. The gate fires **before** any install script executes.

## Why it exists / problem

Mistral-powered AI coding tools can install packages on the user's behalf, but they don't check whether those packages have known security issues. Users who chose Mistral specifically for **EU data sovereignty** should have a pre-install pipeline that matches — `claude-code-cve-gate` covers the Anthropic path; this repo covers the Mistral path. Same gate logic, same scanner, parallel hook surface.

## Scope (in)

- **PreToolUse Bash hook** wired for Mistral Codestral / Le Chat hook conventions, intercepting `pip|npm|composer|cargo|go|gem|brew install` (7 ecosystems).
- **Full transitive tree resolution** via the package manager's own dry-run mode for pip / npm / composer / gem.
- **Multi-source vulnerability query:** NIST NVD + OSV.dev + GitHub Advisory (deduplicated, version-aware).
- **3-day freshness hold** (pip + npm); overridable via `SAFE_INSTALL_MIN_AGE`.
- **Fail-closed mode** via `STRICT_FAIL_CLOSED=1`; default = best-effort allow.
- **Zero runtime deps** (Python stdlib only); no API keys required.
- **Shared `SAFE_INSTALL_MIN_AGE`** with `claude-code-cve-gate` (one config covers both).
- **npm gating via PMG** ([safedep/pmg](https://github.com/safedep/pmg), Apache 2.0) — layered on top of the 3-DB CVE scanner to add malware detection + configurable cooldown. Integration model: declared external dependency + runtime PATH check, fail-closed. Helper module `pmg_npm_gate.py` exposes `run_npm_via_pmg(args)`. Phase 2 (separate PR): wire `~/.vibe/config.toml` so bare `npm install` from mistral-vibe routes through this gate automatically.

## Non-goals (out)

Same as [`claude-code-cve-gate/docs/PRD.md`](https://github.com/sharkyger/claude-code-cve-gate/blob/main/docs/PRD.md) — pre-install only, no SBOM / SARIF / IDE-CI as primary surface, no auto-remediation, no telemetry, no CVE-aware freshness-hold auto-bypass (that lives in `homebrew-safe-upgrade`).

Additionally:
- **No Claude / Anthropic hook surface.** That's `claude-code-cve-gate`'s job — same scanner, different host.

## Quality bar

- **3-layer code review** on every PR ([[fleet-code-review-standard]]).
- **Signed releases.**
- **No public security issues** ([[feedback_security_repos_no_public_issues]]).
- **Python static-analysis floor:** Bandit + Mypy moderate strict (pattern from `composer-cve-gate` #24). <TODO: confirm landed here — currently not.>
- **Shared scanner sync:** `dependency_security_check.py` is fleet-shared lineage with the cve-gate trilogy — stay in sync with the canonical version in `composer-cve-gate`. Pending sync items are tracked internally.

## Retirement / self-archive criteria

Retired when **both**:
1. Mistral Code / Le Chat ships native, default-on pre-install vulnerability gating across all 7 ecosystems with equivalent multi-source query + freshness hold; AND
2. That native gate operates **pre-script-execution**.

If only one ships, this repo keeps the uncovered half. If Mistral and Anthropic converge on a shared hook protocol (or a generalized "AI-tool install gate" emerges), evaluate consolidating with `claude-code-cve-gate`.

## Architecture

Mirrors `claude-code-cve-gate`'s architecture — PreToolUse Bash hook + Python scanner (`dependency_security_check.py`, stdlib-only). Hook configuration differs to match Mistral's host conventions; scanner is shared lineage with the cve-gate trilogy.

## References

- **Sibling:** [`claude-code-cve-gate`](https://github.com/sharkyger/claude-code-cve-gate) — same gate, Claude hook surface.
- **CLI counterparts:** [`composer-cve-gate`](https://github.com/sharkyger/composer-cve-gate), [`pip-cve-gate`](https://github.com/sharkyger/pip-cve-gate), [`homebrew-safe-upgrade`](https://github.com/sharkyger/homebrew-safe-upgrade).
- **Fleet context:** `project_safe_install_fleet_design` memory; `docs/roadmaps/safe-install-fleet.md` in agency-system.
- **Rename history:** `project_security_repos_rename` memory (mistral-code-security → mistral-code-cve-gate, 2026-05-17).

## Status

Current state: **no tags yet** → tag as **v0.1.0** (pre-stable) on the next release per [[feedback_oss_versioning_rule]]. Promotion to v1.0.0 gated on the quality floor (static-analysis + scanner sync + `.coderabbit.yaml`).

## Change log for this document

| Date | Author | Change |
|---|---|---|
| 2026-05-29 | claude (skeleton) | Initial draft from README + memory + convention template. |
| 2026-05-30 | claude | Added npm-gating-via-PMG scope bullet; Phase 2 mistral-vibe wiring noted as follow-up. |
