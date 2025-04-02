"""
Shared test configuration and fixtures.

This module provides shared test utilities, mock classes, and fixtures that can be used
across different test modules.
"""

import json
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

from my_chat_gpt_utils.openai_utils import OpenAIConfig

# Import project_root to configure Python path


class MockOpenAI:
    """Mock class for OpenAI API interactions."""

    def __init__(self, expected_response: Dict[str, Any]):
        """
        Initialize the mock OpenAI client.

        Args:
        ----
            expected_response: Dictionary containing the expected API response.

        """
        self.expected_response = expected_response

    def create(self, **kwargs):
        """
        Create a mock OpenAI API response.

        Args:
        ----
            **kwargs: Arbitrary keyword arguments that would be passed to the real API.

        Returns:
        -------
            MagicMock: A mock response object with the expected content.

        """
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps(self.expected_response)))]
        return mock_response


class MockGitHub:
    """Mock class for GitHub API interactions."""

    def __init__(self):
        """Initialize the mock GitHub client with empty lists for labels and comments."""
        self.labels = []
        self.comments = []

    def ensure_labels_exist(self, owner: str, repo: str, labels: list) -> list:
        """
        Ensure the specified labels exist in the repository.

        Args:
        ----
            owner: Repository owner.
            repo: Repository name.
            labels: List of labels to ensure exist.

        Returns:
        -------
            list: The list of labels that were added.

        """
        self.labels.extend(labels)
        return labels

    def add_labels_to_issue(self, owner: str, repo: str, issue_number: int, labels: list) -> bool:
        """
        Add labels to a GitHub issue.

        Args:
        ----
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number to add labels to.
            labels: List of labels to add.

        Returns:
        -------
            bool: True if labels were added successfully.

        """
        self.labels.extend(labels)
        return True

    def append_response_to_issue(self, client, repo_name: str, issue_data: Dict[str, Any], comment: str) -> bool:
        """
        Append a response as a comment to a GitHub issue.

        Args:
        ----
            client: GitHub client instance.
            repo_name: Name of the repository.
            issue_data: Dictionary containing issue information.
            comment: Comment text to append.

        Returns:
        -------
            bool: True if comment was added successfully.

        """
        self.comments.append(comment)
        return True


@pytest.fixture
def mock_openai():
    """
    Create a mock OpenAI client fixture.

    Returns
    -------
        MockOpenAI: A configured mock OpenAI client.

    """
    expected_response = {
        "issue_type": "Bug Fix",
        "priority": "High",
        "summary": "Test summary",
        "analysis": "Test analysis",
    }
    return MockOpenAI(expected_response)


@pytest.fixture
def mock_github():
    """
    Create a mock GitHub client fixture.

    Returns
    -------
        MockGitHub: A configured mock GitHub client.

    """
    return MockGitHub()


@pytest.fixture
def mock_issue_data():
    """
    Create mock issue data fixture.

    Returns
    -------
        dict: Dictionary containing mock issue data.

    """
    return {
        "repo_owner": "test_owner",
        "repo_name": "test_repo",
        "issue_number": 1,
        "issue_title": "Test Issue",
        "issue_body": "Test issue body",
    }


@pytest.fixture
def mock_openai_config():
    """
    Create a mock OpenAI configuration fixture.

    Returns
    -------
        OpenAIConfig: A configured mock OpenAI configuration.

    """
    return OpenAIConfig(
        api_key="test-key",
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=0.7,
    )
