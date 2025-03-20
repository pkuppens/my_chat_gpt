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

import datetime
import json
import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import MagicMock

import requests
from dotenv import load_dotenv
from github import Github, GithubException, Repository
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from my_chat_gpt_utils.logger import logger


def get_github_client(test_mode: bool = False) -> Github:
    """Get a GitHub client instance.

    Args:
        test_mode (bool): If True, skip repository validation.

    Returns:
        Github: GitHub client instance
    """
    client = GithubClientFactory.create_client(test_mode=test_mode)

    if not test_mode:
        GithubClientFactory.get_repository(client)  # Validate repository access

    return client


__all__ = [
    "get_github_client",
    "get_repository",
    "get_issues",
    "create_issue",
    "edit_issue",
    "add_comment",
    "get_github_issue",
    "append_response_to_issue",
    "ISSUE_TYPES",
    "PRIORITY_LEVELS",
    "IssueContext",
    "IssueRetriever",
    "IssueSimilarityAnalyzer",
    "GithubClientFactory",
    "GitHubEventProcessor",
    "GitHubLabelManager",
    "IssueDataProvider",
]

# Constants for tags, priority levels, and issue types
ISSUE_TYPES = ["Epic", "Change Request", "Bug Fix", "Task", "Question"]
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]


@dataclass
class IssueContext:
    """
    Represents the context and metadata of a GitHub issue.

    Attributes:
        number (int): The unique issue number.
        title (str): The title of the issue.
        body (str): The body/description of the issue.
        state (str): Current state of the issue (open/closed).
        created_at (datetime): Timestamp when the issue was created.
        url (str): HTML URL of the issue.
    """

    number: int
    title: str
    body: Optional[str]
    state: str
    created_at: datetime
    url: str


class IssueRetriever:
    """
    Service for retrieving and filtering GitHub issues.
    """

    def __init__(self, repository: Repository.Repository):
        """
        Initialize the issue retriever with a specific repository.

        Args:
            repository (Repository.Repository): The GitHub repository to query.
        """
        self.repository = repository

    def get_recent_issues(self, days_back: int = 30, state: str = "open") -> List[IssueContext]:
        """
        Retrieve recent issues from the repository.

        Args:
            days_back (int, optional): Number of days to look back. Defaults to 30.
            state (str, optional): Filter by issue state (open/closed). Defaults to None.

        Returns:
            List[IssueContext]: List of recent issues in the repository.
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        issues = get_issues(self.repository, state=state)

        return [
            IssueContext(
                number=issue.number,
                title=issue.title,
                body=issue.body,
                state=issue.state,
                created_at=issue.created_at,
                url=issue.html_url,
            )
            for issue in issues
            if issue.created_at >= cutoff_date
        ]


class IssueSimilarityAnalyzer:
    """
    Performs similarity analysis on GitHub issues using TF-IDF and cosine similarity.
    """

    def __init__(self, vectorizer: Optional[TfidfVectorizer] = None):
        """
        Initialize the similarity analyzer.

        Args:
            vectorizer (Optional[TfidfVectorizer]): Custom vectorizer. Uses default if not provided.
        """
        self.vectorizer = vectorizer or TfidfVectorizer(stop_words="english")

    def compute_similarities(
        self, target_issue: IssueContext, existing_issues: List[IssueContext], threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        Compute similarities between a target issue and existing issues.

        Args:
            target_issue (IssueContext): The issue to compare against others.
            existing_issues (List[IssueContext]): List of issues to compare.
            threshold (float, optional): Minimum similarity score. Defaults to 0.8.

        Returns:
            List[Dict[str, Any]]: Similar issues with their similarity scores.
        """
        if not existing_issues:
            return []

        # Combine target and existing issues for vectorization
        all_texts = [self._get_issue_text(issue) for issue in [target_issue] + existing_issues]

        # Fit and transform all texts
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)

        # Compute similarities between target and existing issues
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

        # Filter and format results
        similar_issues = []
        for i, score in enumerate(similarities):
            if score >= threshold:
                similar_issues.append({"issue": existing_issues[i], "similarity": float(score)})

        return similar_issues

    def _get_issue_text(self, issue: IssueContext) -> str:
        """Get combined text from issue title and body."""
        text = issue.title or ""
        if issue.body:
            text += " " + issue.body
        return text


class GithubClientFactory:
    """Factory class for creating GitHub clients."""

    @staticmethod
    def get_github_token() -> str:
        """Get GitHub token from environment variables or .env file."""
        # Try environment variables first
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token

        # Try .env file
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token

        raise ValueError("GITHUB_TOKEN not found in environment variables")

    @staticmethod
    def create_client(token: Optional[str] = None, test_mode: bool = False) -> Github:
        """Create a GitHub client with the given token."""
        if test_mode:
            mock_client = MagicMock()
            mock_client.get_user.return_value.login = "test-user"
            return mock_client

        if not token:
            token = GithubClientFactory.get_github_token()

        try:
            client = Github(token)
            # Validate token by checking user login
            client.get_user().login
            return client
        except GithubException as e:
            logger.error(f"Failed to create GitHub client with provided token: {e}")
            raise ValueError("Invalid or expired GITHUB_TOKEN or unable to connect to GitHub") from e

    @staticmethod
    def get_repository(client: Github) -> Repository:
        """Get repository from environment variables."""
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            raise ValueError("GITHUB_REPOSITORY not found in environment variables")
        return client.get_repo(repo_name)


class GitHubEventProcessor:
    """
    Processes GitHub webhook events for issue-related actions.

    TODO: Move to GithubUtils module.
    """

    @staticmethod
    def parse_issue_event() -> Dict[str, Any]:
        """
        Parse the GitHub Actions event file.

        Returns:
            Dict[str, Any]: Parsed GitHub event data.

        Raises:
            ValueError: If event cannot be processed.
        """
        event_path = os.getenv("GITHUB_EVENT_PATH")
        if not event_path:
            raise ValueError("Not running in GitHub Actions environment")

        try:
            with open(event_path, "r", encoding="utf-8") as f:
                event = json.load(f)

            if "issue" not in event:
                raise ValueError("Event does not contain issue data")

            return event
        except Exception as e:
            logger.error("Event processing error: %s", e)
            raise

    @classmethod
    def extract_issue_context(cls, event: Dict[str, Any]) -> IssueContext:
        """
        Extract IssueContext from a GitHub event.

        Args:
            event (Dict[str, Any]): Parsed GitHub event.

        Returns:
            IssueContext: Extracted issue context.
        """
        issue_data = event["issue"]
        return IssueContext(
            number=issue_data["number"],
            title=issue_data["title"],
            body=issue_data.get("body"),
            state=issue_data["state"],
            created_at=datetime.fromisoformat(issue_data["created_at"].replace("Z", "+00:00")),
            url=issue_data["html_url"],
        )


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


class IssueDataProvider:
    """
    Provides flexible issue data retrieval from various sources.
    """

    @staticmethod
    def from_github_event() -> Dict[str, Any]:
        """
        Get issue data from GitHub event.

        Returns:
            Dict[str, Any]: Issue data from GitHub event.

        Raises:
            ValueError: If event cannot be processed.
        """
        event = GitHubEventProcessor.parse_issue_event()
        return {
            "repo_owner": event.get("repository", {}).get("owner", {}).get("login"),
            "repo_name": event.get("repository", {}).get("name"),
            "issue_number": event.get("issue", {}).get("number"),
            "issue_title": event.get("issue", {}).get("title"),
            "issue_body": event.get("issue", {}).get("body") or "",
        }

    @staticmethod
    def from_issue_number(client: Github, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Get issue data from issue number.

        Args:
            client (Github): GitHub client.
            repo_name (str): Repository name.
            issue_number (int): Issue number.

        Returns:
            Dict[str, Any]: Issue data.
        """
        repo = get_repository(client, repo_name)
        issue = repo.get_issue(number=issue_number)
        return {
            "repo_owner": repo.owner.login,
            "repo_name": repo_name,
            "issue_number": issue_number,
            "issue_title": issue.title,
            "issue_body": issue.body or "",
        }

    @staticmethod
    def from_latest_issue(client: Github, repo_name: str) -> Dict[str, Any]:
        """
        Get data from the latest issue in the repository.

        Args:
            client (Github): GitHub client.
            repo_name (str): Repository name.

        Returns:
            Dict[str, Any]: Issue data.
        """
        repo = get_repository(client, repo_name)
        issues = repo.get_issues(state="open", sort="created", direction="desc")
        latest_issue = issues.get_page(0)[0] if issues.totalCount > 0 else None

        if not latest_issue:
            raise ValueError("No open issues found in the repository")

        return {
            "repo_owner": repo.owner.login,
            "repo_name": repo_name,
            "issue_number": latest_issue.number,
            "issue_title": latest_issue.title,
            "issue_body": latest_issue.body or "",
        }
