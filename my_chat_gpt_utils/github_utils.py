"""Utilities for interacting with GitHub API and processing GitHub issues."""

import datetime
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, TypeVar, cast

import requests
from github import Github
from github.GithubException import BadCredentialsException, GithubException, RateLimitExceededException
from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from my_chat_gpt_utils.exceptions import GithubAuthenticationError, ProblemCauseSolution

T = TypeVar("T")


def safe_get(obj: Optional[Dict[str, Any]], key: str, default: T) -> T:
    """Safely get a value from a dictionary with a default value."""
    if obj is None:
        return default
    return obj.get(key, default)


def get_github_client(test_mode: bool = False) -> Github:
    """
    Get a GitHub client instance.

    Args:
    ----
        test_mode (bool): If True, skip repository validation.

    Returns:
    -------
        Github: GitHub client instance

    Raises:
    ------
        GithubAuthenticationError: If GitHub token is invalid or expired
        ProblemCauseSolution: For other GitHub API related issues

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

    def __init__(self, repository: Any):
        """Initialize the issue retriever with a GitHub repository."""
        self.repository = repository

    def get_recent_issues(self, state: str = "all", days_back: int = 30) -> List[Any]:
        """
        Retrieve recent issues from the repository.

        Args:
        ----
            state (str): Issue state to filter by (open/closed/all)
            days_back (int): Number of days to look back

        Returns:
        -------
            List[Any]: List of issues created within the specified time window

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
        self, current_issue: Any, comparable_issues: List[Any], threshold: Optional[float] = None
    ) -> List[Tuple[Any, float]]:
        """
        Compute similarity scores between current issue and comparable issues.

        Args:
        ----
            current_issue (Any): The issue to compare against.
            comparable_issues (List[Any]): List of issues to compare with.
            threshold (Optional[float]): Override the default similarity threshold.

        Returns:
        -------
            List[Tuple[Any, float]]: List of (issue, similarity) tuples for issues above threshold.

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
            GithubAuthenticationError: If GitHub token is invalid or expired
            ProblemCauseSolution: For other GitHub API related issues

        """
        if not token:
            token = os.getenv("GITHUB_TOKEN")
        if not token and not test_mode:
            raise ProblemCauseSolution(
                problem="GitHub token not found",
                cause="GITHUB_TOKEN environment variable is not set",
                solution="Set the GITHUB_TOKEN environment variable with a valid GitHub token",
            )

        client = Github(token or "test_token")
        if not test_mode:
            try:
                client.get_user()  # Validate token by making an API call
            except RateLimitExceededException as e:
                raise ProblemCauseSolution(
                    problem="GitHub API rate limit exceeded",
                    cause="Too many requests in a short time period",
                    solution="Wait before retrying or authenticate to increase rate limits",
                    original_exception=e,
                )
            except BadCredentialsException as e:
                raise GithubAuthenticationError(
                    original_exception=e,
                    problem="GitHub API authentication failed",
                    cause="Invalid or expired GitHub token",
                    solution="Check your GitHub token and ensure it has the required permissions",
                )
            except GithubException as e:
                if e.status == 401:
                    raise GithubAuthenticationError(
                        original_exception=e,
                        problem="GitHub API authentication failed",
                        cause="Invalid or expired GitHub token",
                        solution="Check your GitHub token and ensure it has the required permissions",
                    )
                elif e.status == 403:
                    # Token exists but doesn't have user permissions
                    # This is expected for GITHUB_TOKEN in GitHub Actions
                    logging.warning(
                        "GitHub token does not have user permissions. "
                        "This is normal for GITHUB_TOKEN in GitHub Actions. "
                        "Some features may be limited."
                    )
                else:
                    raise ProblemCauseSolution(
                        problem=f"GitHub API request failed with status {e.status}",
                        cause="Unexpected GitHub API error",
                        solution="Check the GitHub API documentation for more information about this error",
                        original_exception=e,
                    )
            except Exception as e:
                raise ProblemCauseSolution(
                    problem="Failed to validate GitHub token",
                    cause=f"Unexpected error: {str(e)}",
                    solution="Check your network connection and try again",
                    original_exception=e,
                )
        return client

    @staticmethod
    def get_repository(client: Github) -> Repository:
        """
        Get the repository context from environment variables.

        Args:
        ----
            client (Github): GitHub client instance.

        Returns:
        -------
            Repository: GitHub repository instance.

        Raises:
        ------
            ProblemCauseSolution: If repository information is missing or invalid
            GithubAuthenticationError: If GitHub token is invalid or expired

        """
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            raise ProblemCauseSolution(
                problem="Repository information not found",
                cause="GITHUB_REPOSITORY environment variable is not set",
                solution="Set the GITHUB_REPOSITORY environment variable in format 'owner/repo'",
            )
        try:
            repo = client.get_repo(repo_name)
            return cast(Repository, repo)
        except BadCredentialsException as e:
            raise GithubAuthenticationError(
                original_exception=e,
                problem="GitHub API authentication failed",
                cause="Invalid or expired GitHub token",
                solution="Check your GitHub token and ensure it has the required permissions",
            )
        except RateLimitExceededException as e:
            raise ProblemCauseSolution(
                problem="GitHub API rate limit exceeded",
                cause="Too many requests in a short time period",
                solution="Wait before retrying or authenticate to increase rate limits",
                original_exception=e,
            )
        except GithubException as e:
            if e.status == 404:
                raise ProblemCauseSolution(
                    problem="Repository not found",
                    cause=f"Repository '{repo_name}' does not exist or is not accessible",
                    solution="Check if the repository exists and if your token has access to it",
                    original_exception=e,
                )
            elif e.status == 403:
                raise ProblemCauseSolution(
                    problem="Access to repository denied",
                    cause="Insufficient permissions to access the repository",
                    solution="Ensure your GitHub token has the required repository access permissions",
                    original_exception=e,
                )
            else:
                raise ProblemCauseSolution(
                    problem=f"Failed to access repository with status {e.status}",
                    cause="Unexpected GitHub API error",
                    solution="Check the GitHub API documentation for more information about this error",
                    original_exception=e,
                )


class GitHubEventProcessor:
    """Processes GitHub webhook events for issue-related actions."""

    @staticmethod
    def parse_issue_event() -> Dict[str, Any]:
        """Parse and validate the GitHub issue event."""
        event_path = os.getenv("GITHUB_EVENT_PATH")
        if not event_path:
            raise ProblemCauseSolution(
                problem="GitHub event path not found",
                cause="GITHUB_EVENT_PATH environment variable is not set",
                solution="Ensure this script is running in a GitHub Actions workflow",
            )

        try:
            with open(event_path, "r") as f:
                event = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ProblemCauseSolution(
                problem="Failed to parse GitHub event file",
                cause=f"Error reading or parsing event file: {str(e)}",
                solution="Check if the event file exists and contains valid JSON",
                original_exception=e,
            )

        if "issue" not in event:
            raise ProblemCauseSolution(
                problem="Invalid GitHub event type",
                cause="Event does not contain issue data",
                solution="Ensure this action is triggered by an issue event",
            )

        return event

    @staticmethod
    def extract_issue_context(event: Dict[str, Any]) -> Dict[str, Any]:
        """Extract issue context from the event data."""
        issue_data = event["issue"]
        required_fields = ["number", "title", "body"]
        missing_fields = [field for field in required_fields if field not in issue_data]
        if missing_fields:
            raise ProblemCauseSolution(
                problem="Missing required issue fields",
                cause=f"Event data is missing fields: {', '.join(missing_fields)}",
                solution="Ensure the GitHub event contains all required issue fields",
            )

        return issue_data


def get_repository(client: Any, repo_name: str):
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


def get_github_issue(client: Any, repo_name: str, issue_data: Dict[str, Any]):
    """Convert a dictionary to a GitHub issue object."""
    repo = get_repository(client, repo_name)
    return repo.get_issue(number=issue_data["issue_number"])


def append_response_to_issue(client: Any, repo_name: str, issue_data: Dict[str, Any], response: str):
    """Append the complete response to the issue comments."""
    issue = get_github_issue(client, repo_name, issue_data)
    comment = f"## OpenAI API Response\n\n{response}"
    return add_comment(issue, comment)


class GitHubLabelManager:
    """Class to manage GitHub issue labels."""

    def __init__(self, github_token: str):
        """
        Initialize GitHubLabelManager.

        Args:
        ----
            github_token (str): GitHub authentication token

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
            repo_owner (str): GitHub repository owner
            repo_name (str): GitHub repository name
            labels (List[str]): Labels to ensure exist
            color (str, optional): Default color for new labels

        Raises:
        ------
            ProblemCauseSolution: If label operations fail

        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/labels"

        try:
            # Get existing labels
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            existing_labels = [label["name"] for label in response.json()]

            # Create missing labels
            for label in labels:
                if label not in existing_labels:
                    label_data = {"name": label, "color": color}
                    response = requests.post(url, headers=self.headers, json=label_data)
                    response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if response.status_code == 403:
                raise ProblemCauseSolution(
                    problem="Failed to manage repository labels",
                    cause="Insufficient permissions to manage labels",
                    solution="Ensure your GitHub token has 'repo' scope permissions",
                    original_exception=e,
                )
            else:
                raise ProblemCauseSolution(
                    problem="Failed to manage repository labels",
                    cause=f"GitHub API request failed with status {response.status_code}",
                    solution="Check the GitHub API documentation for more information about this error",
                    original_exception=e,
                )

    def add_labels_to_issue(self, repo_owner: str, repo_name: str, issue_number: int, labels: List[str]) -> bool:
        """
        Add labels to a GitHub issue.

        Args:
        ----
            repo_owner (str): Owner of the repository
            repo_name (str): Name of the repository
            issue_number (int): Issue number
            labels (List[str]): List of labels to add

        Returns:
        -------
            bool: True if labels were added successfully, False otherwise

        Raises:
        ------
            ProblemCauseSolution: If there is an error adding labels

        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
        response = None

        try:
            response = requests.post(url, headers=self.headers, json={"labels": labels})
            # Check status code first
            if response.status_code == 404:
                raise ProblemCauseSolution(
                    problem="Failed to add labels to issue",
                    cause="Issue or repository not found",
                    solution="Check if the repository and issue exist and you have access to them",
                    original_exception=None,
                )
            elif response.status_code == 403:
                raise ProblemCauseSolution(
                    problem="Failed to add labels to issue",
                    cause="Insufficient permissions",
                    solution="Ensure your GitHub token has write access to the repository",
                    original_exception=None,
                )

            # Then raise for other status codes
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            if not isinstance(e, requests.exceptions.HTTPError):  # Only handle non-HTTP errors here
                raise ProblemCauseSolution(
                    problem="Failed to add labels to issue",
                    cause=f"GitHub API error: {str(e)}",
                    solution="Check the GitHub API documentation for more information",
                    original_exception=e,
                )
            raise  # Re-raise HTTP errors to be caught by the outer exception handler
        except Exception as e:
            raise ProblemCauseSolution(
                problem="Failed to add labels to issue",
                cause=f"Unexpected error: {str(e)}",
                solution="Check your network connection and try again",
                original_exception=e,
            )


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
            ProblemCauseSolution: If event cannot be processed.

        """
        event = GitHubEventProcessor.parse_issue_event()
        repo_data = safe_get(event, "repository", {})
        owner_data = safe_get(repo_data, "owner", {})
        issue_data = safe_get(event, "issue", {})

        return {
            "repo_owner": safe_get(owner_data, "login", ""),
            "repo_name": safe_get(repo_data, "name", ""),
            "issue_number": safe_get(issue_data, "number", 0),
            "issue_title": safe_get(issue_data, "title", ""),
            "issue_body": safe_get(issue_data, "body", "") or "",
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

        Raises:
        ------
            ProblemCauseSolution: If issue cannot be retrieved

        """
        try:
            repo = client.get_repo(repo_name)
            repo = cast(Repository, repo)
            issue = repo.get_issue(number=issue_number)
            issue = cast(Issue, issue)
            owner = cast(NamedUser, repo.owner)

            return {
                "repo_owner": owner.login,
                "repo_name": repo_name,
                "issue_number": issue_number,
                "issue_title": issue.title or "",
                "issue_body": issue.body or "",
            }
        except GithubException as e:
            if e.status == 404:
                raise ProblemCauseSolution(
                    problem="Issue not found",
                    cause=f"Issue #{issue_number} does not exist in repository '{repo_name}'",
                    solution="Check if the issue number is correct and if your token has access to it",
                    original_exception=e,
                )
            else:
                raise ProblemCauseSolution(
                    problem="Failed to retrieve issue",
                    cause=f"GitHub API request failed with status {e.status}",
                    solution="Check the GitHub API documentation for more information about this error",
                    original_exception=e,
                )

    @staticmethod
    def from_latest_issue(client: Any, repo_name: str) -> Dict[str, Any]:
        """
        Get data from the latest issue in the repository.

        Args:
        ----
            client (Any): GitHub client.
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
