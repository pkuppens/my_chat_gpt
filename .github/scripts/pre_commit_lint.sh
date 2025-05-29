#!/bin/bash

# Pre-commit script to run linting and formatting
# This script uses ruff for both linting and formatting (replaces black and flake8)
# It exits with a non-zero status if linting fails
# Use --no-verify to bypass the lint check

# Run ruff for linting
echo "Running ruff linting..."
ruff check .
LINT_EXIT_CODE=$?

# Run ruff for formatting check
echo "Running ruff formatting check..."
ruff format --check .
FORMAT_EXIT_CODE=$?

# Check the exit status of the linting and formatting commands
if [ $LINT_EXIT_CODE -ne 0 ] || [ $FORMAT_EXIT_CODE -ne 0 ]; then
  echo "Linting or formatting failed. Please fix the issues before committing."
  echo "To fix formatting issues automatically, run: ruff format ."
  echo "To fix linting issues automatically, run: ruff check --fix ."
  exit 1
fi

echo "Linting and formatting passed. Proceeding with commit."
exit 0
