---
name: check-security-review
description: Audit code for security vulnerabilities, injection risks, hardcoded secrets, and proper input validation.
---

Gather the code to audit:

```bash
git diff main..HEAD 2>/dev/null || git diff master..HEAD
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
git status
```

If $ARGUMENTS is provided, also read that specific file or directory.

Perform a security audit covering:

## Injection
- SQL injection, command injection, LDAP injection
- Template injection, path traversal

## Authentication & Authorization
- Missing auth checks, broken access control
- Insecure session handling, JWT misuse

## Secrets & Data Exposure
- Hardcoded credentials, API keys, tokens in code
- Sensitive data logged or exposed in error messages
- PII without encryption at rest or in transit

## Input Validation
- Missing or bypassable validation on user input
- Unsafe deserialization, type confusion

## Dependencies
- Outdated packages with known CVEs (check package.json / requirements.txt / go.mod if present)

## Format each finding as:
`🔴 [OWASP category] file:line — risk — remediation`

End with a risk summary: Critical / High / Medium / Low findings count and top recommendation.
