# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability, please report it responsibly.

### How to report

Please email `security@example.com` with the subject "Vulnerability Report - agent-memory-hub".
Do **NOT** open a public issue on GitHub for security vulnerabilities.

### What to include

- Description of the vulnerability.
- Steps to reproduce.
- Potential impact.

### Response Timeline

- We will acknowledge receipt within 48 hours.
- We will provide a timeline for the fix within 1 week.

## Security Best Practices for Users

- Always pin your dependencies.
- Rotate service account keys regularly or use Workload Identity.
- Enable `region_restricted=True` for sensitive workloads.
