# Contributing to Agent Memory Hub

We welcome contributions! Please follow these guidelines to ensure a smooth process.

## Development Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Pull Request Process

1. Create a new branch for your feature or fix.
2. Ensure all tests pass.
3. Add new tests for any new functionality.
4. Ensure 80% minimum code coverage.
5. Update documentation if necessary.
6. Submit a PR with a clear description of changes.

## Coding Standards

- Use strict type hints.
- Write docstrings for all public methods.
- Run `ruff check .` before submitting.
- Avoid hardcoding any credentials.
