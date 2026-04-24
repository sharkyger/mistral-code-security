# Mistral Code Security

**Supply chain security for Mistral AI coding tools.** Every pip install, npm install, and brew install your AI coding assistant runs gets checked against 3 vulnerability databases before execution.

> Your AI assistant installs packages on your machine. Nobody is checking what is in them. Until now.

## Why Mistral Users Should Care

Mistral positions itself as the EU-first AI provider. If you chose Mistral for data sovereignty and compliance, your security posture should match. Every unvetted package install is a compliance risk.

This project adds the safety net that is missing from every AI coding tool on the market.

## What This Does

When your AI coding tool tries to install a package, this system:

1. **Intercepts** the install command (pip, npm, composer, cargo, go, gem, brew)
2. **Queries 3 databases** for known vulnerabilities:
   - [NIST NVD](https://nvd.nist.gov/) - US government vulnerability database
   - [OSV.dev](https://osv.dev/) - Google open source vulnerability database
   - [GitHub Advisory Database](https://github.com/advisories) - GitHub security advisories
3. **Blocks** the install if vulnerabilities are found
4. **Allows** it through if clean

No API keys required. All three databases are free and public. Zero dependencies (Python stdlib only).

## Quick Start

### For Mistral with Claude Code / Codestral

If you use Mistral models through Claude Code, Codestral, or any tool with hook support:

```bash
git clone https://github.com/sharkyger/mistral-code-security.git
cd mistral-code-security
bash install.sh
```

### For any AI coding tool

The scanner works standalone. Integrate it into any workflow:

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
| `settings-template.json` | Ready-to-use settings with all hooks wired up |
| `install.sh` | One-command installer |

## EU Compliance Angle

If you are in a regulated industry (finance, healthcare, government), unvetted dependencies are an audit finding waiting to happen:

- **NIS2 Directive** requires supply chain risk management
- **DORA** (Digital Operational Resilience Act) mandates ICT risk management for financial entities
- **GDPR** Article 32 requires appropriate technical measures, including secure development practices

This tool provides an auditable record of every package check (JSON output on stdout).

## Related

- [claude-code-security](https://github.com/sharkyger/claude-code-security) - Same protection optimized for Anthropic Claude Code
- [homebrew-safe-upgrade](https://github.com/sharkyger/homebrew-safe-upgrade) - Same scanner integrated into Homebrew upgrades

## License

MIT
