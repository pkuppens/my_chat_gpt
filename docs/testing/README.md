# Testing Documentation

This directory contains documentation related to testing practices and tools used in the project.

## Contents

1. [Code Coverage](./CODECOV.md)
   - Coverage reporting strategy
   - Local and CI coverage analysis
   - Best practices

## Testing Overview

The project uses:
- pytest for test execution
- pytest-cov for coverage reporting
- GitHub Actions for CI/CD
- Coverage reports available as workflow artifacts

## GitHub Token in Tests

Some tests can use a real GitHub token for authentication if available:

1. **Local Development**:
   - Set `GITHUB_TOKEN` in your `.env` file
   - Token is used only for authentication
   - No actual modifications are made to GitHub
   - Tests fall back to mocks if token is not available

2. **CI Environment**:
   - GitHub Actions provides `GITHUB_TOKEN` automatically
   - Token has read-only access by default
   - Safe for running tests

3. **Safety Measures**:
   - All modifying operations (creating labels, posting comments) are mocked
   - Only authentication uses the real token
   - Tests work without a token (using mocks)
   - No sensitive operations are performed

## Quick Links

- [GitHub Actions Workflow](../../.github/workflows/test.yml)
- [Test Directory](../../tests/)
- [pytest Configuration](../../pytest.ini)
