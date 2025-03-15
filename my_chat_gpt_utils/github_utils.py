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

from dataclasses import dataclass
import datetime
import json
import os
from typing import List, Dict, Any, Optional, Tuple
import requests

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from github import Github, Repository

from my_chat_gpt_utils.logger import logger

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

    def get_recent_issues(self, days_back: int = 30, state: Optional[str] = None) -> List[IssueContext]:
        """
        Retrieve recent issues from the repository.

        Args:
            days_back (int, optional): Number of days to look back. Defaults to 30.
            state (str, optional): Filter by issue state (open/closed). Defaults to None.

        Returns:
            List[IssueContext]: List of recent issues in the repository.
        """
        cutoff_date = datetime.now() - datetime.timedelta(days=days_back)
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
    ) -> List[Tuple[IssueContext, float]]:
        """
        Compute similarities between a target issue and existing issues.

        Args:
            target_issue (IssueContext): The issue to compare against others.
            existing_issues (List[IssueContext]): List of issues to compare.
            threshold (float, optional): Minimum similarity score. Defaults to 0.8.

        Returns:
            List[Tuple[IssueContext, float]]: Similar issues with their similarity scores.
        """

        def prepare_text(issue: IssueContext) -> str:
            return f"{issue.title}\n{issue.body or ''}"

        issue_texts = [prepare_text(issue) for issue in existing_issues]
        target_text = prepare_text(target_issue)

        # Add target text and compute similarities
        all_texts = issue_texts + [target_text]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]

        # Filter and return similar issues
        return [(existing_issues[i], similarities[i]) for i in range(len(similarities)) if similarities[i] >= threshold]


class GithubClientFactory:
    """
    Factory class for creating GitHub API clients and retrieving repository context.
    """

    @classmethod
    def create_client(cls) -> Github:
        """
        Creates a GitHub client using environment-based authentication.

        Returns:
            Github: Authenticated GitHub client instance.

        Raises:
            ValueError: If GitHub token is not found in environment.
        """
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        return get_github_client(github_token)

    @classmethod
    def get_repository(cls, client: Github) -> Repository.Repository:
        """
        Retrieves the GitHub repository from environment configuration.

        Args:
            client (Github): Authenticated GitHub client.

        Returns:
            Repository.Repository: The specified GitHub repository.

        Raises:
            ValueError: If repository name is not found in environment.
        """
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            raise ValueError("GITHUB_REPOSITORY not found in environment variables")
        return get_repository(client, repo_name)


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
