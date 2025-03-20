"""
Shared test configuration and fixtures.

This module provides shared test utilities, mock classes, and fixtures that can be used
across different test modules.
"""

import json
import os
import sys
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from my_chat_gpt_utils.openai_utils import OpenAIConfig


class MockOpenAI:
    """Mock class for OpenAI API interactions."""

    def __init__(self, expected_response: Dict[str, Any]):
        self.expected_response = expected_response

    def create(self, **kwargs):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps(self.expected_response)))]
        return mock_response


class MockGitHub:
    """Mock class for GitHub API interactions."""

    def __init__(self):
        self.labels = []
        self.comments = []

    def ensure_labels_exist(self, owner: str, repo: str, labels: list) -> list:
        self.labels.extend(labels)
        return labels

    def add_labels_to_issue(self, owner: str, repo: str, issue_number: int, labels: list) -> bool:
        self.labels.extend(labels)
        return True

    def append_response_to_issue(self, client, repo_name: str, issue_data: Dict[str, Any], comment: str) -> bool:
        self.comments.append(comment)
        return True


@pytest.fixture
def mock_openai():
    """Fixture providing a mock OpenAI API client."""
    return MockOpenAI(
        {
            "issue_type": "Bug Fix",
            "priority": "High",
            "complexity": "Moderate",
            "review_feedback": "Test feedback",
            "next_steps": ["Step 1", "Step 2"],
        }
    )


@pytest.fixture
def mock_github():
    """Fixture providing a mock GitHub API client."""
    return MockGitHub()


@pytest.fixture
def mock_issue_data():
    """Fixture providing sample issue data."""
    return {
        "repo_owner": "test-owner",
        "repo_name": "test-repo",
        "issue_number": 123,
        "title": "Test Issue",
        "body": "Test body",
    }


@pytest.fixture
def mock_openai_config():
    """Fixture providing OpenAI configuration."""
    return OpenAIConfig(api_key="test-key", model="test-model", max_tokens=100, temperature=0.5)
