import os
import requests
from github import Github

# Constants for tags, priority levels, and issue types
ISSUE_TYPES = ["Epic", "Change Request", "Bug Fix", "Task", "Question"]
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

def get_github_client(token: str) -> Github:
    """Get an authenticated GitHub client."""
    return Github(token)

def get_repository(client: Github, repo_name: str):
    """Get a repository object."""
    return client.get_repo(repo_name)

def get_issues(repo, state: str = "open"):
    """Get issues from the repository."""
    return repo.get_issues(state=state)

def create_issue(repo, title: str, body: str, labels: list = None):
    """Create a new issue in the repository."""
    return repo.create_issue(title=title, body=body, labels=labels)

def edit_issue(issue, title: str = None, body: str = None, state: str = None, labels: list = None):
    """Edit an existing issue."""
    if title:
        issue.edit(title=title)
    if body:
        issue.edit(body=body)
    if state:
        issue.edit(state=state)
    if labels:
        issue.edit(labels=labels)

def add_comment(issue, comment: str):
    """Add a comment to an issue."""
    return issue.create_comment(comment)
