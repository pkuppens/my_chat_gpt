#!/bin/bash
# cleanup-github-actions.sh
# Cleans up obsolete GitHub Actions workflow runs
#
# Targets:
# 1. Runs that required approval but are now obsolete (queued/waiting, old)
# 2. Runs for branches that no longer exist
# 3. Superseded runs (keeps only most recent completed per workflow+branch)
#
# Usage:
#   ./cleanup-github-actions.sh                    # Dry-run (show what would be cleaned)
#   ./cleanup-github-actions.sh --execute          # Execute cleanup
#   ./cleanup-github-actions.sh --help             # Show help
#
# Based on: babblr/scripts/cleanup-merged-branches.sh
# Requires: gh CLI with workflow scope (gh auth refresh -s workflow)

set -e

DRY_RUN=true
STALE_DAYS=7  # Runs queued/waiting older than this are considered obsolete

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[OK]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_help() {
    cat << EOF
GitHub Actions Workflow Run Cleanup

Cleans up:
1. Obsolete approval runs - queued/waiting runs older than ${STALE_DAYS} days
2. Runs for branches that no longer exist
3. Superseded runs - keeps only most recent completed per workflow+branch

Usage:
    $0                    # Dry-run
    $0 --execute          # Execute cleanup
    $0 --help             # This help

Requirements:
- gh CLI installed and authenticated (in PATH)
- Workflow scope: gh auth refresh -s workflow
- On Windows: run from Git Bash or a terminal where 'gh' works
EOF
    exit 0
}

for arg in "$@"; do
    case $arg in
        --execute) DRY_RUN=false ;;
        --help|-h) show_help ;;
        *) print_error "Unknown argument: $arg"; exit 1 ;;
    esac
done

if [ "$DRY_RUN" = true ]; then
    print_warning "DRY-RUN MODE - No changes will be made"
    print_info "Run with --execute to perform cleanup"
    echo ""
fi

command -v gh >/dev/null 2>&1 || { print_error "gh CLI required (ensure it is in PATH). Install: https://cli.github.com/"; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { print_error "Not in a git repository"; exit 1; }
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || { print_error "python3 or python required"; exit 1; })

REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
print_info "Repository: $REPO"
echo ""

# Fetch latest refs for accurate branch check
print_info "Fetching latest refs..."
git fetch origin --prune 2>/dev/null || true

TEMP_RUNS="cleanup_actions_runs_$$.json"
gh run list --limit 1000 --json databaseId,status,conclusion,workflowName,headBranch,createdAt > "$TEMP_RUNS"

# Existing branches (local + remote, normalized)
EXISTING_BRANCHES=$(git branch -a | sed 's/remotes\/origin\///' | sed 's/^[* ]*//' | grep -v "HEAD" | sort -u)

# ============================================================================
# STEP 1: Obsolete approval runs (queued/waiting, old)
# ============================================================================
print_info "STEP 1: Checking for obsolete queued/waiting runs (older than ${STALE_DAYS} days)..."

STALE_CUTOFF=$($PYTHON -c "from datetime import datetime, timedelta; print((datetime.utcnow() - timedelta(days=${STALE_DAYS})).strftime('%Y-%m-%dT%H:%M:%SZ'))")

OBSOLETE_APPROVAL_IDS=$($PYTHON << PYEOF
import json
from datetime import datetime

with open("$TEMP_RUNS") as f:
    data = json.load(f)

cutoff = "$STALE_CUTOFF"
stale = []
for r in data:
    if r['status'] in ('queued', 'pending', 'waiting'):
        if r.get('createdAt', '') < cutoff:
            stale.append(str(r['databaseId']))
print('\n'.join(stale))
PYEOF
)

OBSOLETE_COUNT=0
OBSOLETE_DELETED=0

for run_id in $OBSOLETE_APPROVAL_IDS; do
    [ -z "$run_id" ] && continue
    OBSOLETE_COUNT=$((OBSOLETE_COUNT + 1))
    if [ "$DRY_RUN" = false ]; then
        print_info "Deleting obsolete run $run_id"
        if echo "y" | gh run delete "$run_id" 2>/dev/null; then
            OBSOLETE_DELETED=$((OBSOLETE_DELETED + 1))
        else
            print_warning "Failed to delete run $run_id (need: gh auth refresh -s workflow)"
        fi
    else
        print_warning "Would delete obsolete run $run_id"
    fi
done

[ $OBSOLETE_COUNT -eq 0 ] && print_success "No obsolete approval runs" || print_warning "Found $OBSOLETE_COUNT obsolete run(s)"
echo ""

# ============================================================================
# STEP 2: Runs for deleted branches
# ============================================================================
print_info "STEP 2: Checking runs for deleted branches..."

WORKFLOW_BRANCHES=$($PYTHON -c "
import json
with open('$TEMP_RUNS') as f:
    data = json.load(f)
seen = set()
for r in data:
    b = r.get('headBranch', '')
    if b and b not in seen:
        seen.add(b)
        print(b)
")

DELETED_BRANCH_RUNS=0
DELETED_BRANCH_SUCCESS=0

while IFS= read -r branch; do
    [ -z "$branch" ] && continue
    # Skip PR refs - handled by superseded cleanup
    case "$branch" in refs/pull/*) continue ;; esac
    # Check if branch exists
    if ! echo "$EXISTING_BRANCHES" | grep -qx "$branch"; then
        RUN_IDS=$(gh run list --branch "$branch" --limit 1000 --json databaseId --jq '.[].databaseId')
        if [ -n "$RUN_IDS" ]; then
            for run_id in $RUN_IDS; do
                DELETED_BRANCH_RUNS=$((DELETED_BRANCH_RUNS + 1))
                if [ "$DRY_RUN" = false ]; then
                    print_info "Deleting run $run_id (branch '$branch' deleted)"
                    if echo "y" | gh run delete "$run_id" 2>/dev/null; then
                        DELETED_BRANCH_SUCCESS=$((DELETED_BRANCH_SUCCESS + 1))
                    fi
                else
                    print_warning "Would delete run $run_id (branch '$branch' deleted)"
                fi
            done
        fi
    fi
done <<< "$WORKFLOW_BRANCHES"

[ $DELETED_BRANCH_RUNS -eq 0 ] && print_success "No runs for deleted branches" || print_warning "Found $DELETED_BRANCH_RUNS run(s) for deleted branches"
echo ""

# ============================================================================
# STEP 3: Superseded runs (keep only most recent completed per workflow+branch)
# ============================================================================
print_info "STEP 3: Checking superseded runs (keep most recent completed per workflow+branch)..."

KEEP_RUNS=$($PYTHON << PYEOF
import json
from collections import defaultdict

with open("$TEMP_RUNS") as f:
    data = json.load(f)

groups = defaultdict(list)
for r in data:
    key = r['workflowName'] + '|' + r['headBranch']
    groups[key].append(r)

keep = []
for runs in groups.values():
    completed = [r for r in runs if r['status'] == 'completed']
    if completed:
        completed.sort(key=lambda x: x['createdAt'], reverse=True)
        keep.append(str(completed[0]['databaseId']))
print('\n'.join(keep))
PYEOF
)

ALL_IDS=$($PYTHON -c "import json; f=open('$TEMP_RUNS'); d=json.load(f); print('\n'.join(str(r['databaseId']) for r in d))")
SUPERSEDED_COUNT=0
SUPERSEDED_DELETED=0

for run_id in $ALL_IDS; do
    [ -z "$run_id" ] && continue
    echo "$KEEP_RUNS" | grep -qx "$run_id" && continue
    SUPERSEDED_COUNT=$((SUPERSEDED_COUNT + 1))
    if [ "$DRY_RUN" = false ]; then
        RUN_INFO=$($PYTHON -c "
import json
f=open('$TEMP_RUNS')
for r in json.load(f):
    if r['databaseId']==$run_id:
        print(r['workflowName']+' ['+(r.get('conclusion') or r['status'])+'] on '+r['headBranch'])
        break
" 2>/dev/null)
        print_info "Deleting superseded $run_id: $RUN_INFO"
        if echo "y" | gh run delete "$run_id" 2>/dev/null; then
            SUPERSEDED_DELETED=$((SUPERSEDED_DELETED + 1))
        fi
    fi
done

[ $SUPERSEDED_COUNT -eq 0 ] && print_success "No superseded runs" || print_warning "Found $SUPERSEDED_COUNT superseded run(s)"
echo ""

rm -f "$TEMP_RUNS"

# ============================================================================
# SUMMARY
# ============================================================================
echo "========================================"
print_success "CLEANUP SUMMARY"
echo "========================================"
TOTAL=$((OBSOLETE_COUNT + DELETED_BRANCH_RUNS + SUPERSEDED_COUNT))
if [ "$DRY_RUN" = true ]; then
    echo "Would clean: $TOTAL runs (obsolete: $OBSOLETE_COUNT, deleted-branch: $DELETED_BRANCH_RUNS, superseded: $SUPERSEDED_COUNT)"
    echo ""
    print_info "Run with --execute to perform: $0 --execute"
else
    DELETED=$((OBSOLETE_DELETED + DELETED_BRANCH_SUCCESS + SUPERSEDED_DELETED))
    echo "Deleted: $DELETED of $TOTAL runs"
fi
echo ""
