"""
Unit tests for GitHub issue retriever functionality.

This module tests the IssueRetriever class which is responsible for retrieving and filtering
GitHub issues based on their age and state. The tests focus on real-world scenarios where:

1. We need to find recent issues (within last 30 days) to analyze
2. We need to filter issues by their state (open/closed) to focus on relevant ones
3. We need to handle edge cases like no recent issues or all issues being too old

The tests verify that the retriever correctly:
- Filters out issues older than the specified time window
- Respects the issue state filter (open/closed/all)
- Returns an empty list when no issues match the criteria
- Handles repository access and API responses correctly

This ensures we only process relevant issues and don't waste resources on old or irrelevant ones.
"""

import datetime
from unittest.mock import MagicMock

import pytest

from my_chat_gpt_utils.github_utils import IssueRetriever


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    return MagicMock()


def create_mock_issue(days_old: int) -> MagicMock:
    """Create a mock issue with a proper datetime for created_at."""
    issue = MagicMock()
    issue.created_at = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_old)
    return issue


def test_get_recent_issues(mock_repository):
    """Test retrieving recent issues."""
    retriever = IssueRetriever(mock_repository)

    # Create mock issues with proper datetime objects
    mock_issues = [
        create_mock_issue(days)
        for days in [5, 15, 25]  # All within 30 days
    ]
    mock_repository.get_issues.return_value = mock_issues

    issues = retriever.get_recent_issues(days_back=30)
    assert len(issues) == 3  # All issues are within 30 days


def test_get_recent_issues_with_state(mock_repository):
    """Test retrieving recent issues with specific state."""
    retriever = IssueRetriever(mock_repository)

    # Create mock issues with proper datetime objects
    mock_issues = [
        create_mock_issue(days)
        for days in [5, 15]  # All within 30 days
    ]
    mock_repository.get_issues.return_value = mock_issues

    issues = retriever.get_recent_issues(days_back=30, state="closed")
    assert len(issues) == 2  # Both issues are within 30 days

    # Verify that get_issues was called with both state and since parameters
    call_args = mock_repository.get_issues.call_args[1]
    assert call_args["state"] == "closed"
    assert "since" in call_args
    assert isinstance(call_args["since"], datetime.datetime)


def test_get_recent_issues_empty(mock_repository):
    """Test retrieving recent issues when none exist."""
    retriever = IssueRetriever(mock_repository)
    mock_repository.get_issues.return_value = []

    issues = retriever.get_recent_issues(days_back=30)
    assert len(issues) == 0


def test_get_recent_issues_all_old(mock_repository):
    """Test retrieving recent issues when all are too old."""
    retriever = IssueRetriever(mock_repository)

    # Create mock issues with proper datetime objects
    mock_issues = [
        create_mock_issue(days)
        for days in [35, 40]  # All older than 30 days
    ]
    mock_repository.get_issues.return_value = mock_issues

    issues = retriever.get_recent_issues(days_back=30)
    assert len(issues) == 0  # No issues within 30 days
