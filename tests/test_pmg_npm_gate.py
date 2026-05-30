"""Tests for PMG-backed npm gating."""
import shutil

import pytest

import pmg_npm_gate
from pmg_npm_gate import is_pmg_available, run_npm_via_pmg


def test_is_pmg_available_returns_false_when_missing(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    assert is_pmg_available() is False


def test_is_pmg_available_returns_true_when_present(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/local/bin/pmg")
    assert is_pmg_available() is True


def test_run_npm_via_pmg_raises_when_pmg_missing(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="PMG.*required"):
        run_npm_via_pmg(["install", "express"])


def test_run_npm_via_pmg_invokes_pmg_subprocess(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/local/bin/pmg")
    captured: dict = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs

        class R:
            returncode = 0

        return R()

    monkeypatch.setattr(pmg_npm_gate.subprocess, "run", fake_run)
    rc = run_npm_via_pmg(["install", "express"])
    assert rc == 0
    assert captured["args"] == ["pmg", "npm", "install", "express"]
    assert captured["kwargs"].get("check") is False


def test_run_npm_via_pmg_propagates_nonzero_exit_code(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/local/bin/pmg")

    def fake_run(args, **kwargs):
        class R:
            returncode = 42

        return R()

    monkeypatch.setattr(pmg_npm_gate.subprocess, "run", fake_run)
    assert run_npm_via_pmg(["install", "bogus"]) == 42
