# Pre-commit Configuration

This document describes the pre-commit hooks configuration and usage in this project.

## Current Setup

We use pre-commit hooks to ensure code quality and consistency. The hooks run automatically before each commit.

### Active Hooks

#### Code Formatting & Style
- `trailing-whitespace`: Removes trailing whitespace
- `end-of-file-fixer`: Ensures files end with a single newline
- `black`: Python code formatter
- `isort`: Python import sorter (configured to be compatible with black)
- `flake8`: Python linter with docstring checking

#### Code Quality
- `check-ast`: Validates Python syntax
- `check-yaml`: Validates YAML files
- `check-json`: Validates JSON files
- `check-merge-conflict`: Checks for merge conflict markers

#### Security
- `check-added-large-files`: Prevents large files from being committed
- `detect-private-key`: Prevents committing private keys

#### Testing
- `pytest`: Runs the test suite before each commit

## Setup Instructions

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the git hooks:
   ```bash
   pre-commit install
   ```

3. (Optional) Run against all files:
   ```bash
   pre-commit run --all-files
   ```

## Hook Execution

- Most hooks run in the `pre-commit` stage
- Hooks like `trailing-whitespace` and `end-of-file-fixer` will automatically fix issues
- The pytest hook ensures all tests pass before allowing commits

## Troubleshooting

If you need to bypass pre-commit hooks temporarily:
```bash
git commit -m "Your message" --no-verify
```

Common issues:
1. **Whitespace or EOL issues**: Let the hooks fix them automatically
2. **Failed tests**: Fix the failing tests before committing
3. **Black/isort conflicts**: The hooks are configured to work together with compatible settings

## Configuration

The configuration is in `.pre-commit-config.yaml`. Key features:
- Black and isort are configured to work together
- Flake8 includes docstring checking
- Pytest runs as a local hook
- File formatting hooks run automatically

For more information, visit the [pre-commit documentation](https://pre-commit.com/).
