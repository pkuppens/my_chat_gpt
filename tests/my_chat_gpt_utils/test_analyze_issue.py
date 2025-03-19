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

# Test comment for IDE pre-commit hooks
import json
import os
from datetime import datetime
from typing import Any, Dict
from unittest.mock import MagicMock, mock_open, patch

import pytest

from my_chat_gpt_utils.analyze_issue import (
    IssueAnalysis,
    LLMIssueAnalyzer,
    create_analysis_comment,
    get_issue_data,
    get_issue_specific_labels,
    get_required_labels,
    process_issue_analysis,
    setup_openai_config,
)
from my_chat_gpt_utils.openai_utils import (
    DEFAULT_LLM_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    OpenAIConfig,
)


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Automatically mock OpenAI client for all tests."""
    with patch("openai.OpenAI") as mock_client:
        mock_client.return_value = MagicMock()
        yield mock_client


class MockOpenAI:
    """
    Mock class for OpenAI API interactions.

    This is a practical example of how to mock an external API client. Here's how it works:

    1. When we create a mock, we tell it what response to return:
       mock = MockOpenAI({"issue_type": "Bug Fix", "priority": "High"})

    2. The mock mimics the real OpenAI client's structure:
       Real client: client.chat.completions.create(...)
       Our mock:   mock.chat.completions.create(...)

    3. When the code calls create(), our mock returns a fake response that looks like:
       {
           "choices": [
               {
                   "message": {
                       "content": '{"issue_type": "Bug Fix", "priority": "High"}'
                   }
               }
           ]
       }

    This lets us test our code without making real API calls. For example:
    >>> mock = MockOpenAI({"issue_type": "Bug Fix"})
    >>> analyzer = LLMIssueAnalyzer(config)
    >>> analyzer.client = mock  # Use our mock instead of real client
    >>> result = analyzer.analyze_issue(data)  # This uses our mock, not real API
    >>> assert result.issue_type == "Bug Fix"  # Test passes!
    """

    def __init__(self, expected_response: Dict[str, Any]):
        """
        Create a mock that will return the given response.

        Args:
            expected_response: The data we want our mock to return.
                             This should match what our code expects.
        """
        self.expected_response = expected_response

        # Create the nested structure that matches OpenAI's client
        self.chat = MagicMock()
        self.chat.completions = MagicMock()

        # Tell the mock what to return when create() is called
        self.chat.completions.create = MagicMock(return_value=self._create_mock_response())

    def _create_mock_response(self):
        """
        Create a fake response that looks like what OpenAI would return.

        The real OpenAI API returns responses in this format:
        {
            "choices": [
                {
                    "message": {
                        "content": "JSON string here"
                    }
                }
            ]
        }

        We create a similar structure using MagicMock objects:
        - mock_response.choices[0].message.content = "our JSON string"
        """
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps(self.expected_response)))]
        return mock_response


class MockGitHub:
    """
    Mock class for GitHub API interactions.

    This mock simulates GitHub's API by:
    1. Storing actions (like adding labels or comments) in memory
    2. Providing methods that match GitHub's API structure
    3. Allowing us to check what actions were performed

    Example usage:
    >>> mock_github = MockGitHub()
    >>> mock_github.add_labels_to_issue("owner", "repo", 123, ["bug", "high"])
    >>> mock_github.labels  # Check what labels were added
    ['bug', 'high']

    The mock tracks:
    - Labels: What labels were created and added to issues
    - Comments: What comments were posted to issues

    This lets us verify that our code:
    1. Creates the right labels
    2. Adds labels to issues
    3. Posts comments with the right content
    """

    def __init__(self):
        """Initialize empty lists to track labels and comments."""
        self.labels = []  # Track all labels that were created or added
        self.comments = []  # Track all comments that were posted

    def ensure_labels_exist(self, owner: str, repo: str, labels: list) -> list:
        """
        Simulate creating labels in a GitHub repository.

        Args:
            owner: Repository owner (not used in mock)
            repo: Repository name (not used in mock)
            labels: List of labels to create

        Returns:
            list: The labels that were created
        """
        self.labels.extend(labels)  # Track the labels
        return labels

    def add_labels_to_issue(self, owner: str, repo: str, issue_number: int, labels: list) -> bool:
        """
        Simulate adding labels to a GitHub issue.

        Args:
            owner: Repository owner (not used in mock)
            repo: Repository name (not used in mock)
            issue_number: Issue number (not used in mock)
            labels: List of labels to add

        Returns:
            bool: Always True in mock
        """
        self.labels.extend(labels)  # Track the labels
        return True

    def append_response_to_issue(self, client, repo_name: str, issue_data: Dict[str, Any], comment: str) -> bool:
        """
        Simulate posting a comment to a GitHub issue.

        Args:
            client: GitHub client (not used in mock)
            repo_name: Repository name (not used in mock)
            issue_data: Issue data (not used in mock)
            comment: The comment text to post

        Returns:
            bool: Always True in mock
        """
        self.comments.append(comment)  # Track the comment
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
    """
    Test the core issue analysis functionality.

    This test shows how to use our mock in practice:
    1. Create an analyzer with test config
    2. Replace its client with our mock
    3. Call analyze_issue() - it will use our mock instead of real API
    4. Check that we got the expected results

    The mock_openai fixture provides a mock configured to return:
    {
        "issue_type": "Bug Fix",
        "priority": "High",
        "complexity": "Moderate",
        "review_feedback": "Test feedback",
        "next_steps": ["Step 1", "Step 2"]
    }
    """
    analyzer = LLMIssueAnalyzer(mock_openai_config)
    analyzer.client = mock_openai  # Use mock instead of real client
    analysis = analyzer.analyze_issue(mock_issue_data)

    # Verify we got the expected results from our mock
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
    """
    Test the complete issue analysis process including GitHub interactions.

    This test will use a real GitHub token if available (from environment), falling back to mocks if not.
    No actual modifications are made to any GitHub issues during the test.

    The test verifies:
    1. The right labels would be created (but aren't actually created)
    2. The right comment would be posted (but isn't actually posted)
    3. The analysis results are correct
    """
    # Create analyzer with mock OpenAI client
    analyzer = LLMIssueAnalyzer(mock_openai_config)
    analyzer.client = mock_openai

    # Try to get actual GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    if github_token:
        # Use real GitHub client for validation, but mock the actual operations
        with patch("my_chat_gpt_utils.analyze_issue.GitHubLabelManager", return_value=mock_github), patch(
            "my_chat_gpt_utils.analyze_issue.append_response_to_issue", side_effect=mock_github.append_response_to_issue
        ), patch("my_chat_gpt_utils.analyze_issue.LLMIssueAnalyzer", return_value=analyzer):

            result = process_issue_analysis(mock_issue_data, mock_openai_config)
    else:
        # Fallback to complete mocking if no token available
        mock_github_client = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_github_client.get_user.return_value = mock_user
        # Mock the login property to avoid authentication check
        mock_user.login = "test-user"

        with patch("my_chat_gpt_utils.analyze_issue.GitHubLabelManager", return_value=mock_github), patch(
            "my_chat_gpt_utils.analyze_issue.append_response_to_issue", side_effect=mock_github.append_response_to_issue
        ), patch("my_chat_gpt_utils.github_utils.GithubClientFactory.get_github_token", return_value="mock-token"), patch(
            "my_chat_gpt_utils.analyze_issue.LLMIssueAnalyzer", return_value=analyzer
        ), patch(
            "github.Github", return_value=mock_github_client
        ):

            result = process_issue_analysis(mock_issue_data, mock_openai_config)

    # Verify analysis results
    assert result.issue_type == "Bug Fix"
    assert result.priority == "High"
    assert result.complexity == "Moderate"

    # Verify GitHub interactions (these operations are always mocked)
    assert len(mock_github.labels) > 0  # Labels were created
    assert len(mock_github.comments) == 1  # Comment was posted


def test_get_issue_data_with_provided_data(mock_issue_data):
    """Test getting issue data when provided directly."""
    result = get_issue_data(mock_issue_data)
    assert result == mock_issue_data


def test_get_issue_data_from_env():
    """Test getting issue data from environment variable."""
    test_data = {"title": "Test Issue", "body": "Test Body"}
    with patch.dict("os.environ", {"ISSUE_DATA": json.dumps(test_data)}):
        result = get_issue_data()
        assert result == test_data


def test_get_issue_data_from_event_file():
    """Test getting issue data from event file."""
    test_data = {"issue": {"title": "Test Issue", "body": "Test Body"}}
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        with patch.dict("os.environ", {"GITHUB_EVENT_PATH": "test_path"}):
            result = get_issue_data()
            assert result == test_data["issue"]


def test_get_issue_data_event_file_error():
    """Test handling of event file reading error."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=IOError("File error")):
        with patch.dict("os.environ", {"GITHUB_EVENT_PATH": "test_path"}):
            result = get_issue_data()
            assert result == {}


def test_get_issue_data_empty_env():
    """Test getting issue data with empty environment."""
    with patch.dict("os.environ", {}, clear=True):
        result = get_issue_data()
        assert result == {}


def test_get_issue_data_provided_data():
    """Test getting issue data from provided data."""
    test_data = {"title": "Test Issue", "body": "Test Body"}
    result = get_issue_data(test_data)
    assert result == test_data


def test_get_issue_data_invalid_json():
    """Test handling of invalid JSON in environment variable."""
    with patch.dict("os.environ", {"ISSUE_DATA": "invalid json"}):
        result = get_issue_data()
        assert result == {}


def test_setup_openai_config_success():
    """Test successful OpenAI configuration setup."""
    with patch.dict(
        "os.environ", {"OPENAI_API_KEY": "test-key", "LLM_MODEL": "test-model", "MAX_TOKENS": "100", "TEMPERATURE": "0.5"}
    ), patch("my_chat_gpt_utils.analyze_issue.OpenAIVersionChecker.check_library_version", return_value=True), patch(
        "my_chat_gpt_utils.analyze_issue.OpenAIValidator.validate_api_key", return_value=True
    ):

        config = setup_openai_config()
        assert config.api_key == "test-key"
        assert config.model == "test-model"
        assert config.max_tokens == 100
        assert config.temperature == 0.5


def test_setup_openai_config_invalid_version():
    """Test OpenAI configuration setup with invalid library version."""
    with patch.dict(
        "os.environ", {"OPENAI_API_KEY": "test-key", "LLM_MODEL": "test-model", "MAX_TOKENS": "100", "TEMPERATURE": "0.5"}
    ), patch("my_chat_gpt_utils.analyze_issue.OpenAIVersionChecker.check_library_version", return_value=False):

        with pytest.raises(RuntimeError, match="Incompatible OpenAI library version"):
            setup_openai_config()


def test_setup_openai_config_invalid_api_key():
    """Test OpenAI configuration setup with invalid API key."""
    with patch.dict(
        "os.environ", {"OPENAI_API_KEY": "test-key", "LLM_MODEL": "test-model", "MAX_TOKENS": "100", "TEMPERATURE": "0.5"}
    ), patch("my_chat_gpt_utils.analyze_issue.OpenAIVersionChecker.check_library_version", return_value=True), patch(
        "my_chat_gpt_utils.analyze_issue.OpenAIValidator.validate_api_key", return_value=False
    ):

        with pytest.raises(ValueError, match="Invalid OpenAI API key"):
            setup_openai_config()


def test_setup_openai_config_default_values():
    """Test OpenAI configuration setup with default values."""
    with patch.dict("os.environ", {}, clear=True), patch(
        "my_chat_gpt_utils.analyze_issue.OpenAIVersionChecker.check_library_version", return_value=True
    ), patch("my_chat_gpt_utils.analyze_issue.OpenAIValidator.validate_api_key", return_value=True):

        config = setup_openai_config()
        assert config.api_key == ""
        assert config.model == DEFAULT_LLM_MODEL
        assert config.max_tokens == DEFAULT_MAX_TOKENS
        assert config.temperature == DEFAULT_TEMPERATURE


def test_analyze_issue_error_handling(mock_issue_data, mock_openai_config):
    """Test error handling in analyze_issue method."""
    analyzer = LLMIssueAnalyzer(mock_openai_config)
    mock_client = MagicMock()
    mock_client.chat = MagicMock()
    mock_client.chat.completions = MagicMock()
    mock_client.chat.completions.create = MagicMock(side_effect=Exception("API Error"))
    analyzer.client = mock_client
    with pytest.raises(Exception) as exc_info:
        analyzer.analyze_issue(mock_issue_data)
    assert "API Error" in str(exc_info.value)
