#!/bin/bash

# Pre-commit script to run linting
# This script uses black and flake8 for linting
# It exits with a non-zero status if linting fails
# Use --no-verify to bypass the lint check

# Run black for code formatting
black .

# Run flake8 for linting
flake8

# Check the exit status of the linting commands
if [ $? -ne 0 ]; then
  echo "Linting failed. Please fix the issues before committing."
  exit 1
fi

echo "Linting passed. Proceeding with commit."
exit 0
