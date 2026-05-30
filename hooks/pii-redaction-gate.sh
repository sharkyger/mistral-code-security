#!/usr/bin/env bash
# UserPromptSubmit hook — blocks prompts containing PII before the model sees them.
# Claude Code's UserPromptSubmit can only BLOCK (exit 2), not silently redact.
# The user must re-submit without PII.
set -euo pipefail
INPUT="$(cat)"
PROMPT="$(echo "$INPUT" | jq -r '.prompt // empty')"
if [[ -z "$PROMPT" ]]; then
  exit 0
fi
# Whitelisted emails — user's own known addresses (not PII leaks)
WHITELIST=(
  # Add your own email addresses here
  # "your-email@example.com"
)
# Strip whitelisted emails before scanning.
# Guard against empty array under set -u — on Bash 3.2 (macOS default),
# "${arr[@]}" on an empty array raises unbound variable.
SANITIZED="$PROMPT"
for addr in ${WHITELIST[@]+"${WHITELIST[@]}"}; do
  SANITIZED="${SANITIZED//$addr/WHITELISTED}"
done
FINDINGS=""
# Email addresses (after whitelist removal, ignoring @example.com test data).
# POSIX ERE doesn't support Perl lookahead, so we extract candidates and
# filter the @example.com / WHITELISTED ones out explicitly.
REMAINING=$(echo "$SANITIZED" | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | grep -v '@example\.com' | grep -v 'WHITELISTED' || true)
if [[ -n "$REMAINING" ]]; then
  FINDINGS="${FINDINGS}Email address detected. "
fi
# Credit card numbers (13-19 digits with optional separators)
if echo "$PROMPT" | grep -qE '\b[0-9]{4}[-[:space:]]?[0-9]{4}[-[:space:]]?[0-9]{4}[-[:space:]]?[0-9]{1,7}\b'; then
  FINDINGS="${FINDINGS}Credit card number detected. "
fi
# SSN (US format)
if echo "$PROMPT" | grep -qE '\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b'; then
  FINDINGS="${FINDINGS}SSN detected. "
fi
# IBAN (2 uppercase letters + 2 digits + 4-30 alphanumeric)
if echo "$PROMPT" | grep -qE '\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4,30}\b'; then
  FINDINGS="${FINDINGS}IBAN detected. "
fi
# German phone numbers — DISABLED due to high false positive rate with dates, zip codes, etc.
# Uncomment and tune if needed:
# if echo "$PROMPT" | grep -qE '\b(\+49|0049|0)[1-9][0-9]{1,4}[-[:space:]/]?[0-9]{3,8}\b'; then
#   FINDINGS="${FINDINGS}German phone number detected. "
# fi
if [[ -n "$FINDINGS" ]]; then
  echo "BLOCKED: PII detected in your prompt: ${FINDINGS}" >&2
  echo "Remove personal data before submitting. Store PII in .env or Notion, not in prompts." >&2
  exit 2
fi
exit 0
