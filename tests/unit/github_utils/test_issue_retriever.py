"""
Unit tests for GitHub issue retriever functionality.

This module tests the IssueRetriever class and related functionality.
All external dependencies are mocked to ensure reliable testing.
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from my_chat_gpt_utils.github_utils import IssueContext, IssueRetriever


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    return MagicMock()


@pytest.fixture
def mock_now():
    """Create a mock datetime.now()."""
    return datetime(2024, 3, 19, 12, 0, 0)


@pytest.fixture
def mock_issues():
    """Fixture providing mock GitHub issues."""
    mock_issue1 = MagicMock()
    mock_issue1.number = 1
    mock_issue1.title = "Test Issue 1"
    mock_issue1.body = "Test Body 1"
    mock_issue1.state = "open"
    mock_issue1.created_at = datetime.now() - timedelta(days=1)
    mock_issue1.html_url = "https://github.com/test/repo/issues/1"

    mock_issue2 = MagicMock()
    mock_issue2.number = 2
    mock_issue2.title = "Test Issue 2"
    mock_issue2.body = "Test Body 2"
    mock_issue2.state = "closed"
    mock_issue2.created_at = datetime.now() - timedelta(days=31)
    mock_issue2.html_url = "https://github.com/test/repo/issues/2"

    return [mock_issue1, mock_issue2]


def test_get_recent_issues(mock_repository, mock_now):
    """Test retrieving recent issues."""
    retriever = IssueRetriever(mock_repository)
    mock_issues = [
        MagicMock(created_at=mock_now - timedelta(days=5)),
        MagicMock(created_at=mock_now - timedelta(days=15)),
        MagicMock(created_at=mock_now - timedelta(days=25)),
    ]
    mock_repository.get_issues.return_value = mock_issues

    with patch("my_chat_gpt_utils.github_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        issues = retriever.get_recent_issues(days_back=30)
        assert len(issues) == 3
        mock_repository.get_issues.assert_called_once_with(state="open")


def test_get_recent_issues_with_state(mock_repository, mock_now):
    """Test retrieving recent issues with specific state."""
    retriever = IssueRetriever(mock_repository)
    mock_issues = [MagicMock(created_at=mock_now - timedelta(days=5)), MagicMock(created_at=mock_now - timedelta(days=15))]
    mock_repository.get_issues.return_value = mock_issues

    with patch("my_chat_gpt_utils.github_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        issues = retriever.get_recent_issues(days_back=30, state="closed")
        assert len(issues) == 2
        mock_repository.get_issues.assert_called_once_with(state="closed")


def test_get_recent_issues_empty(mock_repository, mock_now):
    """Test retrieving recent issues when none exist."""
    retriever = IssueRetriever(mock_repository)
    mock_repository.get_issues.return_value = []

    with patch("my_chat_gpt_utils.github_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        issues = retriever.get_recent_issues(days_back=30)
        assert len(issues) == 0
        mock_repository.get_issues.assert_called_once_with(state="open")


def test_get_recent_issues_all_old(mock_repository, mock_now):
    """Test retrieving recent issues when all are too old."""
    retriever = IssueRetriever(mock_repository)
    mock_issues = [MagicMock(created_at=mock_now - timedelta(days=35)), MagicMock(created_at=mock_now - timedelta(days=40))]
    mock_repository.get_issues.return_value = mock_issues

    with patch("my_chat_gpt_utils.github_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        issues = retriever.get_recent_issues(days_back=30)
        assert len(issues) == 0
        mock_repository.get_issues.assert_called_once_with(state="open")
