"""
Integration tests for GitHub issue retriever functionality.

These tests interact with the actual GitHub API and require valid credentials.
They are marked with @pytest.mark.integration and are skipped by default in regular test runs.

This module tests the IssueRetriever class against the actual GitHub API to verify that:
1. All expected functions are available in the external github library
2. Function calls with various parameters are accepted without runtime exceptions
3. The API responds with valid data structures

The tests focus on successful function calls rather than specific results, since the actual
number of issues and their content will vary over time.
"""

from datetime import datetime, timedelta, timezone

import pytest

from my_chat_gpt_utils.github_utils import IssueRetriever, get_github_client


@pytest.fixture
def github_repository():
    """Get a real GitHub repository for integration testing."""
    client = get_github_client(test_mode=True)
    # Use PyGithub repository which is guaranteed to have issues
    return client.get_repo("PyGithub/PyGithub")


@pytest.mark.integration
def test_get_recent_issues_basic(github_repository):
    """Test basic issue retrieval with default parameters."""
    retriever = IssueRetriever(github_repository)
    issues = retriever.get_recent_issues()
    assert isinstance(issues, list)  # Verify we get a list back


@pytest.mark.integration
def test_get_recent_issues_with_state(github_repository):
    """Test issue retrieval with different state filters."""
    retriever = IssueRetriever(github_repository)

    # Test with different states
    for state in ["open", "closed", "all"]:
        issues = retriever.get_recent_issues(state=state)
        assert isinstance(issues, list)


@pytest.mark.integration
def test_get_recent_issues_with_time_window(github_repository):
    """Test issue retrieval with different time windows."""
    retriever = IssueRetriever(github_repository)

    # Test with different time windows
    for days in [7, 30, 90, 365]:
        issues = retriever.get_recent_issues(days=days)
        assert isinstance(issues, list)

        # Verify issues are within the time window
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        for issue in issues:
            assert issue.created_at >= cutoff_date


@pytest.mark.integration
def test_get_recent_issues_empty_repository(github_repository):
    """Test issue retrieval from a repository with no recent issues."""
    retriever = IssueRetriever(github_repository)

    # Use a very short time window to likely get no issues
    issues = retriever.get_recent_issues(days=1)
    assert isinstance(issues, list)
    assert len(issues) >= 0  # Should not raise an exception even if empty


@pytest.mark.integration
def test_get_recent_issues_large_time_window(github_repository):
    """Test issue retrieval with a large time window."""
    retriever = IssueRetriever(github_repository)

    # Test with a large time window (1 year)
    issues = retriever.get_recent_issues(days=365)
    assert isinstance(issues, list)
    # Don't assert on length since it depends on repository activity
