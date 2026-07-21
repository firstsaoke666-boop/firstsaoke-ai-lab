# Security Policy

## Supported versions

Security updates are provided for the latest version on the repository's
default branch. Older commits, branches, and unpublished development snapshots
are not supported unless maintainers explicitly state otherwise.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Report it privately
through GitHub's private vulnerability reporting feature for this repository.
Include the affected component, reproduction steps, potential impact, and any
known mitigations. Maintainers will acknowledge the report and coordinate
disclosure after assessing and correcting the issue.

If private vulnerability reporting is unavailable, contact a repository owner
through a trusted private channel and provide only enough information to
establish a secure reporting path.

## Secret handling

- Never commit `.env` files, API keys, access tokens, passwords, credentials,
  private keys, or production configuration.
- Use environment variables or an approved secret manager at runtime.
- Keep local secrets in ignored files and provide sanitized `.env.example`
  templates when configuration documentation is needed.
- Never place secrets in tests, fixtures, logs, documentation, issue reports,
  pull requests, or screenshots.
- Revoke and rotate any credential immediately if it may have been exposed.
