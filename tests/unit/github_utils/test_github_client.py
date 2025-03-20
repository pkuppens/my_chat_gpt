"""
Unit tests for GitHub client functionality.

This module tests the GitHub client factory and related functionality, focusing on:
1. Business Logic:
   - Client creation with proper authentication
   - Repository access and validation
   - Environment-specific behavior (local vs CI/CD)
   - Error handling for invalid credentials

2. Edge Cases:
   - Missing environment variables
   - Invalid tokens
   - Network failures
   - Repository access issues
   - Test mode vs production mode differences

The tests ensure that the GitHub client provides the necessary functionality
for the application while handling various error conditions appropriately.
"""

import os
from unittest.mock import patch

import pytest
from github import GithubException

from my_chat_gpt_utils.github_utils import GithubClientFactory


def detect_test_environment():
    """Detect the current test environment."""
    if os.getenv("GITHUB_ACTIONS"):
        return "github_actions"
    elif os.getenv("CI"):
        return "ci"
    else:
        return "local"


@pytest.fixture(scope="session")
def test_environment():
    """Configure test environment based on context."""
    env_type = detect_test_environment()
    if env_type == "local":
        # Load .env file for local development
        from dotenv import load_dotenv

        load_dotenv()
    return env_type


@pytest.fixture
def github_client(test_environment):
    """Create a GitHub client with appropriate configuration."""
    if test_environment in ["github_actions", "ci"]:
        # Use environment variables in CI/CD
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            pytest.skip("GITHUB_TOKEN not available in CI environment")
    else:
        # Use .env file in local development
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            pytest.skip("GITHUB_TOKEN not available in local environment")

    return GithubClientFactory.create_client()


def test_github_client_authentication():
    """Test GitHub client authentication and basic functionality."""
    # Test with valid token
    with patch("my_chat_gpt_utils.github_utils.Github") as mock_github:
        mock_github.return_value.get_user.return_value = "test_user"
        with patch.dict(os.environ, {"GITHUB_TOKEN": "valid-token"}, clear=True):
            client = GithubClientFactory.create_client()
            assert client is not None
            assert client.get_user() == "test_user"

    # Test with invalid token
    with patch("my_chat_gpt_utils.github_utils.Github") as mock_github:
        mock_github.return_value.get_user.side_effect = GithubException(401, {"message": "Bad credentials"})
        with patch.dict(os.environ, {"GITHUB_TOKEN": "invalid-token"}, clear=True):
            with pytest.raises(ValueError, match="Invalid or expired GITHUB_TOKEN"):
                GithubClientFactory.create_client()


def test_github_client_environment_handling():
    """Test GitHub client behavior in different environments."""
    # Test local environment
    with patch.dict(os.environ, {"GITHUB_TOKEN": "local-token"}, clear=True):
        client = GithubClientFactory.create_client()
        assert client is not None

    # Test CI environment
    with patch.dict(os.environ, {"GITHUB_TOKEN": "ci-token", "CI": "true"}, clear=True):
        client = GithubClientFactory.create_client()
        assert client is not None

    # Test GitHub Actions environment
    with patch.dict(os.environ, {"GITHUB_TOKEN": "actions-token", "GITHUB_ACTIONS": "true"}, clear=True):
        client = GithubClientFactory.create_client()
        assert client is not None


def test_github_client_repository_access():
    """Test repository access and validation."""
    # Test with valid repository
    with patch("my_chat_gpt_utils.github_utils.Github") as mock_github:
        mock_repo = mock_github.return_value.get_repo.return_value
        mock_repo.get_issues.return_value = []

        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GITHUB_TOKEN": "test-token"}, clear=True):
            client = GithubClientFactory.create_client()
            repo = GithubClientFactory.get_repository(client)
            assert repo is not None
            assert hasattr(repo, "get_issues")

    # Test with invalid repository
    with patch("my_chat_gpt_utils.github_utils.Github") as mock_github:
        mock_github.return_value.get_repo.side_effect = GithubException(404, {"message": "Not Found"})
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/invalid-repo", "GITHUB_TOKEN": "test-token"}, clear=True):
            with pytest.raises(GithubException):
                client = GithubClientFactory.create_client()
                GithubClientFactory.get_repository(client)


def test_github_client_test_mode():
    """Test GitHub client in test mode."""
    with patch.dict(os.environ, {}, clear=True):
        client = GithubClientFactory.create_client(test_mode=True)
        assert client is not None


def test_github_client_error_handling():
    """Test error handling in GitHub client operations."""
    # Test missing token
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GITHUB_TOKEN environment variable is required"):
            GithubClientFactory.create_client()

    # Test network failure
    with patch("my_chat_gpt_utils.github_utils.Github") as mock_github:
        mock_github.side_effect = Exception("Network error")
        with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}, clear=True):
            with pytest.raises(Exception, match="Network error"):
                GithubClientFactory.create_client()
