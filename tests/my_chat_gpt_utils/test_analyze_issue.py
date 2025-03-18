"""
Test module for analyze_issue module from my_chat_gpt_utils package.

This module tests the functionality for analyzing GitHub issues using LLMs. The analysis includes:
1. Classifying issues by type (Bug, Feature, etc.)
2. Assessing issue complexity
3. Determining priority levels
4. Generating review feedback and next steps
5. Managing GitHub labels and comments

The tests cover both direct API interactions and GitHub workflow integration.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict
from unittest.mock import MagicMock, mock_open, patch

import pytest

from my_chat_gpt_utils.analyze_issue import (IssueAnalysis, LLMIssueAnalyzer,
                                             create_analysis_comment,
                                             get_issue_data,
                                             get_issue_specific_labels,
                                             get_required_labels,
                                             process_issue_analysis)
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
def mock_issue_analysis():
    """Fixture providing a sample issue analysis result."""
    return IssueAnalysis(
        issue_type="Bug Fix",
        priority="High",
        complexity="Moderate",
        review_feedback="Test feedback",
        next_steps=["Step 1", "Step 2"],
    )


@pytest.fixture
def mock_issue_data():
    """Fixture providing sample issue data."""
    return {"repo_owner": "test-owner", "repo_name": "test-repo", "issue_number": 123, "title": "Test Issue", "body": "Test body"}


@pytest.fixture
def mock_openai_config():
    """Fixture providing OpenAI configuration."""
    return OpenAIConfig(api_key="test-key", model="test-model", max_tokens=100, temperature=0.5)


def test_analyze_issue(mock_openai, mock_issue_data, mock_openai_config):
    """Test the core issue analysis functionality."""
    with patch("my_chat_gpt_utils.analyze_issue.openai.chat.completions.create", side_effect=mock_openai.create):
        analyzer = LLMIssueAnalyzer(mock_openai_config)
        analysis = analyzer.analyze_issue(mock_issue_data)

        assert analysis.issue_type == "Bug Fix"
        assert analysis.priority == "High"
        assert analysis.complexity == "Moderate"
        assert analysis.review_feedback == "Test feedback"
        assert analysis.next_steps == ["Step 1", "Step 2"]


def test_get_required_labels():
    """Test retrieval of required GitHub labels."""
    labels = get_required_labels()
    assert "Type: Bug Fix" in labels
    assert "Priority: High" in labels
    assert "Complexity: Simple" in labels


def test_get_issue_specific_labels(mock_issue_analysis):
    """Test generation of issue-specific labels."""
    labels = get_issue_specific_labels(mock_issue_analysis)
    assert labels == ["Type: Bug Fix", "Priority: High", "Complexity: Moderate"]


def test_create_analysis_comment(mock_issue_analysis):
    """Test creation of analysis comment."""
    comment = create_analysis_comment(mock_issue_analysis)
    assert "**Type:** Bug Fix" in comment
    assert "**Priority:** High" in comment
    assert "**Complexity:** Moderate" in comment
    assert "Test feedback" in comment
    assert "Step 1" in comment
    assert "Step 2" in comment


def test_process_issue_analysis(mock_openai, mock_github, mock_issue_data, mock_openai_config):
    """Test the complete issue analysis process including GitHub interactions."""
    with patch("my_chat_gpt_utils.analyze_issue.openai.chat.completions.create", side_effect=mock_openai.create), patch(
        "my_chat_gpt_utils.analyze_issue.GitHubLabelManager", return_value=mock_github
    ), patch("my_chat_gpt_utils.analyze_issue.append_response_to_issue", side_effect=mock_github.append_response_to_issue):

        result = process_issue_analysis(mock_issue_data, mock_openai_config)

        assert result.issue_type == "Bug Fix"
        assert result.priority == "High"
        assert result.complexity == "Moderate"
        assert len(mock_github.labels) > 0
        assert len(mock_github.comments) == 1


def test_get_issue_data_with_provided_data(mock_issue_data):
    """Test getting issue data when provided directly."""
    result = get_issue_data(mock_issue_data)
    assert result == mock_issue_data


def test_get_issue_data_from_env():
    """Test getting issue data from environment variable."""
    test_data = {"title": "Test Issue", "body": "Test body"}
    with patch.dict("os.environ", {"ISSUE_DATA": json.dumps(test_data)}):
        result = get_issue_data()
        assert result == test_data


def test_get_issue_data_from_event_file():
    """Test getting issue data from GitHub event file."""
    test_data = {"title": "Test Issue", "body": "Test body"}
    event_data = {"issue": test_data}
    with patch.dict("os.environ", {"GITHUB_EVENT_PATH": "test_event.json"}):
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(event_data))):
                result = get_issue_data()
                assert result == test_data


def test_get_issue_data_no_data():
    """Test getting issue data when no data is available."""
    with patch.dict("os.environ", {}, clear=True):
        result = get_issue_data()
        assert result == {}


def test_get_issue_data_invalid_json():
    """Test handling of invalid JSON in environment variable."""
    with patch.dict("os.environ", {"ISSUE_DATA": "invalid json"}):
        result = get_issue_data()
        assert result == {}


def test_get_issue_data_invalid_event_file():
    """Test handling of invalid event file."""
    with patch.dict("os.environ", {"GITHUB_EVENT_PATH": "test_event.json"}):
        with patch("builtins.open", mock_open(read_data="invalid json")):
            result = get_issue_data()
            assert result == {}
