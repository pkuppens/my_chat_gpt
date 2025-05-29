# GitHub Workflow Best Practices

This document outlines best practices and workflow steps for working with GitHub repositories.

## Basic Workflow Steps

### 1. Branch Management

- Always create a new branch for each feature/fix
- Use descriptive branch names: `feature/description` or `fix/description`
- Keep branches up to date with main
- Delete branches after merging

### 2. Making Changes

- Make small, focused commits
- Test changes locally before committing
- Run pre-commit hooks and tests
- Keep changes atomic and self-contained

### 3. Staging Changes

```bash
# Check status
git status

# Add specific files
git add <file>

# Add all changes (including new files)
git add .

# Remove files from staging
git reset <file>
```

**Note**:

- `git add .` stages all changes in the current directory and subdirectories, including:
  - Modified files
  - New files
  - Deleted files
- Use `git status` to verify what will be staged
- Be careful with `git add .` in large repositories - it may stage unwanted files
- Consider using `git add -p` for interactive staging of specific changes

### 4. Pre-commit Hook Workflow

- Stage all files first: `git add .`
- Run pre-commit hooks: `pre-commit run --all-files`
- If auto-fixes are applied:

  ```bash
  # Stage the auto-fixed files
  git add .

  # Run hooks again to ensure all issues are fixed
  pre-commit run --all-files
  ```

- If hooks fail without auto-fixes, fix issues manually and repeat
- Only proceed to commit after all hooks pass

### 5. Committing Changes

1. **Stage Changes**:

   ```bash
   git add .
   ```

2. **Commit with Message**:

   ```bash
   git commit -m "type(scope): description"
   ```

   - Use conventional commit types (feat, fix, docs, style, refactor, test, chore)
   - Include scope if relevant (e.g., github, openai, utils)
   - Write clear, concise descriptions

3. **Verify Commit**:
   ```bash
   git log -1
   ```

### 6. Pushing Changes to Main

1. **Ensure Clean State**:

   ```bash
   git status
   ```

   - Should show "nothing to commit, working tree clean"

2. **Push to Main**:

   ```bash
   git push origin main
   ```

3. **Verify Push**:
   - Check GitHub repository for latest commit
   - Verify changes are reflected in the main branch
   - Check GitHub Actions status if applicable

### 7. Pull Requests

- Create PRs early for feedback
- Keep PRs focused and small
- Update PR description as changes are made
- Request reviews from relevant team members
- Address review comments promptly
- Squash commits when merging

## Pre-commit Hooks

### Common Issues and Solutions

1. **Trailing Whitespace**

   - Remove trailing spaces at line ends
   - Use editor settings to trim trailing whitespace
   - Run `git diff --check` before committing

2. **Line Length**

   - Keep lines under 132 characters (ruff default)
   - Use line breaks for long strings
   - Break long function calls into multiple lines

3. **Test Failures**

   - Run tests locally before committing
   - Fix failing tests before pushing
   - Update tests when changing functionality

4. **Code Style**
   - Follow PEP 8 guidelines
   - Use ruff for code formatting and linting

### Running Pre-commit Hooks Manually

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Run hooks on staged files
pre-commit run

# Run specific hook
pre-commit run <hook-id>
```

### Auto-fix Workflow

1. **Initial Setup**

   ```bash
   # Install pre-commit hooks
   pre-commit install

   # Configure auto-fix behavior (in .pre-commit-config.yaml)
   repos:
   - repo: ...
     hooks:
     - id: ...
       args: [--fix, --auto-fix]  # Enable auto-fixing where supported
   ```

2. **Usage**

   ```bash
   # Stage all files first
   git add .

   # Run hooks with auto-fix
   pre-commit run --all-files

   # Stage fixed files
   git add .

   # Verify all issues are fixed
   pre-commit run --all-files
   ```

3. **Troubleshooting**
   - If hooks fail after auto-fix, manual intervention needed
   - Check hook output for specific issues
   - Fix remaining issues manually
   - Re-run hooks until all pass

## Common Commands

```bash
# Update local repository
git fetch origin
git pull origin main

# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout <branch>

# View changes
git diff
git diff --staged

# View commit history
git log
git log --oneline
git log --graph

# Clean up
git clean -fd  # Remove untracked files and directories
git reset --hard  # Reset to last commit (use with caution)
```

## Best Practices

1. **Commit Messages**

   - Be specific and descriptive
   - Explain what changed and why
   - Reference issues when relevant
   - Keep first line under 100 characters
   - Use present tense ("Add feature" not "Added feature")

2. **Code Review**

   - Review your own code before pushing
   - Address all review comments
   - Keep PRs focused and small
   - Update documentation as needed

3. **Branch Management**

   - Keep main branch clean and stable
   - Use feature branches for development
   - Delete merged branches
   - Keep branches up to date

4. **Security**
   - Never commit sensitive data
   - Use environment variables for secrets
   - Review file permissions
   - Use .gitignore appropriately

## Troubleshooting

1. **Pre-commit Hook Failures**

   - Check hook output for specific issues
   - Fix issues locally before committing
   - Update hooks if needed
   - Document common issues and solutions

2. **Merge Conflicts**

   - Resolve conflicts locally
   - Use git status to identify conflicts
   - Choose correct version or combine changes
   - Test after resolving conflicts

3. **Lost Changes**
   - Use git reflog to find lost commits
   - Create backups before major changes
   - Use git stash for temporary storage
   - Document recovery procedures
