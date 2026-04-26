# Mistral Code Security

Security-first wrapper for the package installs Mistral-powered AI coding tools run on your behalf. 
Every `pip install`, `npm install`, and `brew install` your AI coding assistant suggests gets checked against 3 vulnerability databases before it touches your system, so you never blindly pull in a known CVE.

## Why

Mistral-powered coding tools can install packages for you, but they don't check whether those packages have known security issues. 
Most of the time that's fine. 
Sometimes it isn't.

This adds a security gate at the hook level: 
it intercepts every install your AI assistant tries to run, 
queries three public vulnerability databases, 
checks whether the *target version* is actually affected, 
and only lets the install proceed if it comes back clean. 
Packages with known vulnerabilities are blocked and listed separately.

If you chose Mistral for EU data sovereignty, your install pipeline should match. 
This closes that gap.

## What This Does

When your AI coding tool tries to install a package, this system:

1. **Intercepts** the install command (pip, npm, composer, cargo, go, gem, brew)
2. **Queries 3 databases** for known vulnerabilities:
   - [NIST NVD](https://nvd.nist.gov/) - US government vulnerability database
   - [OSV.dev](https://osv.dev/) - Google open source vulnerability database
   - [GitHub Advisory Database](https://github.com/advisories) - GitHub security advisories
3. **Blocks** the install if vulnerabilities are found
4. **Allows** it through if clean

No API keys required. 
All three databases are free and public. 
Zero dependencies (Python stdlib only).

## How This Compares

Every other security tool for AI coding assistants scans what is already installed. 
This one blocks the bad package before it ever reaches your machine.

| Tool | What it does | Gap |
|------|-------------|-----|
| mcp-scan (Stytch) | Audits installed MCP server configs | Post-install audit only |
| AgentSeal | Scans MCP configs for prompt injection | Config audit, not install blocking |
| AgentAuditKit | 77-rule scanner with SARIF output | CI/CD integration, not real-time |
| Endor Labs | Dependency vetting for AI code | Enterprise SaaS, not open source |

**Our approach:** 
Real-time interception at the moment the AI agent suggests `pip install` / `npm install`. 
Three databases checked, decision made, install blocked or allowed — before anything touches your system.

## Quick Start

### For Mistral with Claude Code / Codestral

If you use Mistral models through Claude Code, Codestral, or any tool with hook support:

```bash
git clone https://github.com/sharkyger/mistral-code-security.git
cd mistral-code-security
bash install.sh
```

### For any AI coding tool

The scanner works standalone. 

Integrate it into any workflow:

```bash
# Check before installing
python3 dependency_security_check.py pip some-package 1.2.3

# Use in CI/CD
python3 dependency_security_check.py npm express 4.17.1 2>/dev/null | jq .status
```

## What is Included

| File | What it does |
|------|-------------|
| `dependency_security_check.py` | 3-database vulnerability scanner (standalone, zero deps) |
| `hooks/dependency-security-gate.sh` | Blocks installs until CVE-clean |
| `hooks/block-dangerous-bash.sh` | Blocks rm -rf, eval injection, env dumping |
| `hooks/block-dangerous-git.sh` | Blocks force push, hook skipping, destructive operations |
| `hooks/secret-leak-detector.sh` | Detects API keys, AWS creds, JWTs, passwords in written files |
| `hooks/protect-sensitive-files.sh` | Blocks reading .env, credentials/, SSH keys |
| `hooks/gitleaks-pre-write.sh` | Scans content with gitleaks before Write — blocks secrets before they reach disk |
| `hooks/pii-redaction-gate.sh` | Blocks PII (emails, credit cards, IBAN) in prompts before the model sees them |
| `agents/security-red-team.md` | Offensive security agent — OWASP, supply chain, prompt injection testing |
| `agents/security-blue-team.md` | Defensive security agent — validates hooks, posture, compliance |
| `settings-template.json` | Ready-to-use settings with all hooks wired up |
| `install.sh` | One-command installer |

## EU Compliance Angle

If you are in a regulated industry (finance, healthcare, government), unvetted dependencies are an audit finding waiting to happen:

- **NIS2 Directive** requires supply chain risk management
- **DORA** (Digital Operational Resilience Act) mandates ICT risk management for financial entities
- **GDPR** Article 32 requires appropriate technical measures, including secure development practices

This tool provides an auditable record of every package check (JSON output on stdout).

## Red Team / Blue Team Agents

This repo includes two security agent definitions:

**Red Team** (`agents/security-red-team.md`) — Offensive. 

Probes your code for:
- OWASP Top 10 vulnerabilities
- Supply chain risks (unpinned deps, typosquatting)
- Secrets in code and git history (via gitleaks)
- Prompt injection in AI tool configs
- Insecure file permissions

**Blue Team** (`agents/security-blue-team.md`) — Defensive. 

Validates that:
- All security hooks are installed and wired
- Gitignore covers sensitive files
- Credential files have proper permissions (600)
- Dependencies are free of known CVEs
- Tool settings aren't overly permissive
- NIS2/DORA/GDPR compliance checkpoints are met

Copy them to `.claude/agents/` (or equivalent) and invoke for on-demand security assessments.

## Prerequisites

- **gitleaks** (required for `gitleaks-pre-write.sh`): `brew install gitleaks`
  (or `brew safe-install gitleaks` if you have [homebrew-safe-upgrade](https://github.com/sharkyger/homebrew-safe-upgrade) installed — gates the install through 3 CVE databases first)
- **jq** (required for all hooks): usually pre-installed on macOS

## Related

- [claude-code-security](https://github.com/sharkyger/claude-code-security) - Same protection optimized for Anthropic Claude Code
- [homebrew-safe-upgrade](https://github.com/sharkyger/homebrew-safe-upgrade) - Same scanner integrated into Homebrew upgrades

## License

MIT
