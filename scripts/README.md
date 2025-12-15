# Pre-commit Testing

This directory contains scripts to validate code quality before committing.

## Pre-commit Test Script

Run the comprehensive validation script before pushing code:

```bash
python scripts/pre_commit_test.py
```

This script runs:

1. **Linting** - Ruff code quality checks
2. **Security Audit** - pip-audit for vulnerable dependencies
3. **Security Scan** - Bandit for code security issues
4. **Test Suite** - All pytest tests
5. **Coverage Check** - Ensures minimum 70% code coverage
6. **Build Validation** - Verifies package builds successfully

## Quick Test

For a faster check during development:

```bash
# Run tests only
pytest tests/ -v

# Run linting only
ruff check .

# Run with coverage
pytest --cov=agent_memory_hub
```

## CI/CD Integration

The same checks run automatically in GitHub Actions on every push to `main` or pull request.
