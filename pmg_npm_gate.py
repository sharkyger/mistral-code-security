"""npm install gating via PMG (Package Manager Guard, safedep/pmg).

Integration model A: PMG is a declared external dependency. At runtime
we check for the `pmg` binary on PATH. If present, callers can route
npm operations through `pmg npm <args>`. If absent, ``run_npm_via_pmg``
fails closed with a clear error directing the operator to the install
command (see README).

Why PMG: it adds malware + cooldown checks on top of the CVE checks
this repo already runs via ``dependency_security_check.py``. Apache 2.0,
free tier with no API key. Phase 2 (separate PR) will wire mistral-vibe
to route bare ``npm install`` through this gate.

This module has no CLI entry-point yet — the cve-gate hook surface is
shell-hook driven (see ``hooks/dependency-security-gate.sh``). Wiring
will land in Phase 2 once the CLI router exists. Stdlib only.
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Sequence

PMG_INSTALL_HINT = (
    "PMG (Package Manager Guard) is required for npm gating.\n"
    "Install with: npm i -g @safedep/pmg\n"
    "Docs: https://github.com/safedep/pmg"
)


def is_pmg_available() -> bool:
    """Return True iff `pmg` is on PATH."""
    return shutil.which("pmg") is not None


def run_npm_via_pmg(npm_args: Sequence[str]) -> int:
    """Forward ``npm <args>`` through ``pmg npm <args>``.

    Fails closed with :class:`RuntimeError` if PMG is missing. Returns
    the subprocess exit code on success.
    """
    if not is_pmg_available():
        raise RuntimeError(PMG_INSTALL_HINT)
    return subprocess.run(
        ["pmg", "npm", *npm_args], check=False
    ).returncode
