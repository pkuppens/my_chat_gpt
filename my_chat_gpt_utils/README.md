# Utils and GitHub Components

This document provides an overview of the utils and GitHub components, including what is needed for workflows.

## `utils/github_utils.py`

This file contains shared GitHub functionality for accessing the repository, querying issues, adding new ones, editing issues, and adding comments. It also includes constants for tags, priority levels, and issue types.

### Functions

- `get_github_client(token: str) -> Github`: Get an authenticated GitHub client.
- `get_repository(client: Github, repo_name: str)`: Get a repository object.
- `get_issues(repo, state: str = "open")`: Get issues from the repository.
- `create_issue(repo, title: str, body: str, labels: list = None)`: Create a new issue in the repository.
- `edit_issue(issue, title: str = None, body: str = None, state: str = None, labels: list = None)`: Edit an existing issue.
- `add_comment(issue, comment: str)`: Add a comment to an issue.

### Constants

- `ISSUE_TYPES`: List of issue types.
- `PRIORITY_LEVELS`: List of priority levels.

## Workflows

### `.github/scripts/analyze_issue.py`

This script analyzes GitHub issues using an LLM and updates the issue with labels and comments based on the analysis. It uses the shared GitHub functionality and constants from `utils/github_utils.py`.

### `.github/scripts/identify_duplicates_v2.py`

This script identifies duplicate issues in the repository and comments on the newly created issue with links to potential duplicates. It uses the shared GitHub functionality and constants from `utils/github_utils.py`.

### Example Workflow Configuration

To use these scripts in your GitHub workflows, you can create a workflow file in the `.github/workflows` directory. Here is an example configuration for analyzing issues:

```yaml
name: Issue Analyzer
on:
  issues:
    types: [opened, edited]

jobs:
  analyze-issue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Set PYTHONPATH
        run: echo "PYTHONPATH=$PYTHONPATH:$(pwd)" >> $GITHUB_ENV
      - name: Install dependencies
        run: pip install openai pyyaml requests PyGithub pytest scikit-learn
      - name: Run issue analyzer
        env:
          LLM_PROVIDER: openai
          LLM_MODEL: gpt-4o-mini
          MAX_TOKENS: 4096
          TEMPERATURE: 0.1
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PYTHONUNBUFFERED: "1"
        run: python -u .github/scripts/analyze_issue.py
```

This configuration sets up a GitHub Action that runs the `analyze_issue.py` script whenever an issue is opened or edited.
