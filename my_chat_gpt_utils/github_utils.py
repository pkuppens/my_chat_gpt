"""
GitHub Issue Management Utility

This module provides functionality for working with GitHub issues programmatically.
It includes helper functions for connecting to GitHub, accessing repositories,
and performing common issue operations such as creating, retrieving, editing,
and commenting on issues.

Dependencies:
    - PyGithub

Usage:
    Import this module to interact with GitHub issues using the provided functions.
    You will need a valid GitHub access token to authenticate requests.

Example:
    client = get_github_client("your-github-token")
    repo = get_repository(client, "username/repository")
    issues = get_issues(repo)
"""

from typing import List, Dict, Any
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


def get_github_issue(client: Github, repo_name: str, issue_data: Dict[str, Any]):
    """Convert a dictionary to a GitHub issue object."""
    repo = get_repository(client, repo_name)
    return repo.get_issue(number=issue_data["issue_number"])


def append_response_to_issue(client: Github, repo_name: str, issue_data: Dict[str, Any], response: str):
    """Append the complete response to the issue comments."""
    issue = get_github_issue(client, repo_name, issue_data)
    comment = f"## OpenAI API Response\n\n{response}"
    return add_comment(issue, comment)


class GitHubLabelManager:
    """
    Manages GitHub issue labels, ensuring required labels exist and are applied.
    """

    def __init__(self, github_token: str):
        """
        Initialize the label manager.

        Args:
            github_token (str): GitHub authentication token.
        """
        self.github_token = github_token
        self.headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}

    def ensure_labels_exist(self, repo_owner: str, repo_name: str, labels: List[str], color: str = "6f42c1") -> None:
        """
        Ensure specified labels exist in the repository.

        Args:
            repo_owner (str): GitHub repository owner.
            repo_name (str): GitHub repository name.
            labels (List[str]): Labels to ensure exist.
            color (str, optional): Default color for new labels.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/labels"

        # Get existing labels
        response = requests.get(url, headers=self.headers)
        existing_labels = [label["name"] for label in response.json()]

        # Create missing labels
        for label in labels:
            if label not in existing_labels:
                label_data = {"name": label, "color": color}
                requests.post(url, headers=self.headers, json=label_data)

    def add_labels_to_issue(self, repo_owner: str, repo_name: str, issue_number: int, labels: List[str]) -> bool:
        """
        Add labels to a specific GitHub issue.

        Args:
            repo_owner (str): GitHub repository owner.
            repo_name (str): GitHub repository name.
            issue_number (int): Issue number to label.
            labels (List[str]): Labels to add.

        Returns:
            bool: True if labels were successfully added, False otherwise.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
        response = requests.post(url, headers=self.headers, json={"labels": labels})
        return response.status_code == 200
