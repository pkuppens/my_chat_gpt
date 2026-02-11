# Scripts Directory

This directory contains utility scripts for repository maintenance and automation.

## Repository Cleanup Scripts

### cleanup-merged-branches.sh

Cleans up branches that have been merged into the main branch, both locally and on the remote repository.

**Features:**
- Deletes local branches that have been merged
- Deletes remote branches that have been merged  
- Protects important branches (main, master, develop, staging, production, release/*, hotfix/*)
- Works both locally and in GitHub Actions
- Dry-run mode by default (safe to test)

**Usage:**
```bash
# Dry-run (shows what would be deleted)
./scripts/cleanup-merged-branches.sh

# Execute cleanup
./scripts/cleanup-merged-branches.sh --execute

# Only clean local branches
./scripts/cleanup-merged-branches.sh --execute --local-only

# Only clean remote branches  
./scripts/cleanup-merged-branches.sh --execute --remote-only

# Show help
./scripts/cleanup-merged-branches.sh --help
```

**Requirements:**
- git installed
- Write permissions for remote branch deletion
- For remote deletion: either git credentials or gh CLI authenticated

### cleanup-github-actions.sh

Cleans up obsolete GitHub Actions workflow runs to keep the Actions history manageable.

**What it cleans:**
1. **Obsolete approval runs** - queued/waiting runs older than 7 days
2. **Runs for deleted branches** - workflow runs for branches that no longer exist
3. **Superseded runs** - keeps only the most recent completed run per workflow+branch, plus any failed runs newer than the last successful run (for debugging)

**Features:**
- Keeps failed workflow runs for debugging (if they haven't been superseded by a successful run)
- Dry-run mode by default (safe to test)
- Works both locally and in GitHub Actions

**Usage:**
```bash
# Dry-run (shows what would be deleted)
./scripts/cleanup-github-actions.sh

# Execute cleanup
./scripts/cleanup-github-actions.sh --execute

# Show help
./scripts/cleanup-github-actions.sh --help
```

**Requirements:**
- gh CLI installed and authenticated
- Workflow scope: `gh auth refresh -s workflow`

## Automated Cleanup

The cleanup scripts are automatically run by the GitHub Actions workflow `.github/workflows/cleanup.yml` after successful merges to the main branch.

**Workflow behavior:**
- Triggers automatically after pushes to main
- Can be manually triggered via workflow_dispatch
- Runs both branch cleanup and workflow run cleanup
- Only runs after CI/CD passes
- Requires `contents: write` and `actions: write` permissions

## Local Development

To test the cleanup scripts locally before they run automatically:

1. **Test branch cleanup:**
   ```bash
   # Dry-run to see what would be deleted
   ./scripts/cleanup-merged-branches.sh
   
   # Actually delete merged branches
   ./scripts/cleanup-merged-branches.sh --execute
   ```

2. **Test workflow cleanup:**
   ```bash
   # Authenticate gh CLI with workflow scope
   gh auth refresh -s workflow
   
   # Dry-run to see what would be deleted
   ./scripts/cleanup-github-actions.sh
   
   # Actually delete old workflow runs
   ./scripts/cleanup-github-actions.sh --execute
   ```

## Safety Features

Both scripts include multiple safety features:

1. **Dry-run by default** - No changes are made unless `--execute` is specified
2. **Protected branches** - Important branches are never deleted
3. **Failed run preservation** - Failed workflow runs are kept for debugging
4. **Clear logging** - All actions are logged with colored output for visibility
5. **Error handling** - Scripts continue even if individual operations fail

## Troubleshooting

### Branch cleanup fails with permission errors

For remote branch deletion, you need:
- Git credentials configured, OR
- GitHub CLI authenticated: `gh auth login`

### Workflow cleanup fails with "Need workflow scope"

Run: `gh auth refresh -s workflow` to grant the necessary permissions.

### Script shows "Not in a git repository"

Make sure you run the scripts from within the repository directory.

## Other Scripts

### collect_langchain_articles.py

Utility script for collecting LangChain articles. See the script itself for usage details.

