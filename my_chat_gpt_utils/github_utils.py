"""Utilities for interacting with GitHub API and processing GitHub issues."""

import datetime
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests
from github import Github, Issue, Repository
from github.GithubException import GithubException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_github_client(test_mode: bool = False) -> Github:
    """
    Get a GitHub client instance.

    Args:
    ----
        test_mode (bool): If True, skip repository validation.

    Returns:
    -------
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

    Attributes
    ----------
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
    created_at: datetime.datetime
    url: str


class IssueRetriever:
    """Service for retrieving and filtering GitHub issues."""

    def __init__(self, repository: Repository):
        """Initialize the issue retriever with a GitHub repository."""
        self.repository = repository

    def get_recent_issues(self, state: str = "all", days_back: int = 30) -> List[Issue]:
        """
        Retrieve recent issues from the repository.

        Args:
        ----
            state (str): Issue state to filter by (open/closed/all)
            days_back (int): Number of days to look back

        Returns:
        -------
            List[Issue]: List of issues created within the specified time window

        """
        since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)
        # Get issues from GitHub API with since parameter
        issues = self.repository.get_issues(state=state, since=since)
        # Double-check the date filter since GitHub API's since parameter isn't always reliable
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)
        return [issue for issue in issues if issue.created_at >= cutoff_date]


class IssueSimilarityAnalyzer:
    """Performs similarity analysis on GitHub issues using TF-IDF and cosine similarity."""

    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize the analyzer with TF-IDF vectorizer.

        Args:
        ----
            similarity_threshold (float): Minimum similarity score to consider issues similar.
                                       Defaults to 0.8 for longer issues, but can be lower for testing.

        """
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.similarity_threshold = similarity_threshold

    def compute_similarities(
        self, current_issue: Issue, comparable_issues: List[Issue], threshold: Optional[float] = None
    ) -> List[Tuple[Issue, float]]:
        """
        Compute similarity scores between current issue and comparable issues.

        Args:
        ----
            current_issue (Issue): The issue to compare against.
            comparable_issues (List[Issue]): List of issues to compare with.
            threshold (Optional[float]): Override the default similarity threshold.

        Returns:
        -------
            List[Tuple[Issue, float]]: List of (issue, similarity) tuples for issues above threshold.

        """
        if not comparable_issues:
            return []

        current_text = f"{current_issue.title}\n{current_issue.body or ''}"
        comparable_texts = [f"{issue.title}\n{issue.body or ''}" for issue in comparable_issues]

        all_texts = comparable_texts + [current_text]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]

        # Use provided threshold or fall back to default
        threshold_to_use = threshold if threshold is not None else self.similarity_threshold
        # Filter issues above threshold
        return [(issue, score) for issue, score in zip(comparable_issues, similarities) if score >= threshold_to_use]


class GithubClientFactory:
    """Factory class for creating GitHub API clients and retrieving repository context."""

    @staticmethod
    def create_client(token: Optional[str] = None, test_mode: bool = False) -> Github:
        """
        Create a GitHub client using environment variables.

        Args:
        ----
            token (Optional[str]): GitHub API token. If not provided, will use GITHUB_TOKEN env var.
            test_mode (bool): If True, skip repository validation.

        Returns:
        -------
            Github: GitHub client instance

        Raises:
        ------
            ValueError: If token is missing or invalid

        """
        if not token:
            token = os.getenv("GITHUB_TOKEN")
        if not token and not test_mode:
            raise ValueError("GITHUB_TOKEN environment variable is required")

        client = Github(token or "test_token")
        if not test_mode:
            try:
                client.get_user()  # Validate token by making an API call
            except GithubException as e:
                if e.status == 401:
                    raise ValueError("Invalid or expired GITHUB_TOKEN")
                raise
        return client

    @staticmethod
    def get_repository(client: Github) -> Repository:
        """Get the repository context from environment variables."""
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            raise ValueError("GITHUB_REPOSITORY environment variable is required")
        return client.get_repo(repo_name)


class GitHubEventProcessor:
    """Processes GitHub webhook events for issue-related actions."""

    @staticmethod
    def parse_issue_event() -> Dict[str, Any]:
        """Parse and validate the GitHub issue event."""
        event_path = os.getenv("GITHUB_EVENT_PATH")
        if not event_path:
            raise ValueError("GITHUB_EVENT_PATH environment variable is required")

        with open(event_path, "r") as f:
            event = json.load(f)

        if "issue" not in event:
            raise ValueError("Event does not contain issue data")

        return event

    @staticmethod
    def extract_issue_context(event: Dict[str, Any]) -> Issue:
        """Extract issue context from the event data."""
        issue_data = event["issue"]
        required_fields = ["number", "title", "body"]
        missing_fields = [field for field in required_fields if field not in issue_data]
        if missing_fields:
            raise ValueError(f"Missing required issue fields: {', '.join(missing_fields)}")

        return issue_data


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
    """Manages GitHub issue labels, ensuring required labels exist and are applied."""

    def __init__(self, github_token: str):
        """
        Initialize the label manager.

        Args:
        ----
            github_token (str): GitHub authentication token.

        """
        self.github_token = github_token
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def ensure_labels_exist(self, repo_owner: str, repo_name: str, labels: List[str], color: str = "6f42c1") -> None:
        """
        Ensure specified labels exist in the repository.

        Args:
        ----
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
        ----
            repo_owner (str): GitHub repository owner.
            repo_name (str): GitHub repository name.
            issue_number (int): Issue number to label.
            labels (List[str]): Labels to add.

        Returns:
        -------
            bool: True if labels were successfully added, False otherwise.

        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
        response = requests.post(url, headers=self.headers, json={"labels": labels})
        return response.status_code == 200


class IssueDataProvider:
    """Provides flexible issue data retrieval from various sources."""

    @staticmethod
    def from_github_event() -> Dict[str, Any]:
        """
        Get issue data from GitHub event.

        Returns
        -------
            Dict[str, Any]: Issue data from GitHub event.

        Raises
        ------
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
        ----
            client (Github): GitHub client.
            repo_name (str): Repository name.
            issue_number (int): Issue number.

        Returns:
        -------
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
        ----
            client (Github): GitHub client.
            repo_name (str): Repository name.

        Returns:
        -------
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
