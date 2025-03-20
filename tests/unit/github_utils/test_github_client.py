"""
Unit tests for GitHub client functionality.

This module tests the GitHub client factory and related functionality.
Tests focus on business logic and required functionality rather than implementation details.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from github import Github, GithubException

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

    return GithubClientFactory.create_client(token)


def test_github_client_required_functionality(github_client):
    """Test that the GitHub client provides required functionality."""
    # Test basic GitHub operations
    assert hasattr(github_client, "get_user")
    assert hasattr(github_client, "get_repo")

    # Test user access
    user = github_client.get_user()
    assert user is not None
    assert hasattr(user, "login")

    # Test repository access with a known repository
    repo_name = os.getenv("GITHUB_REPOSITORY")
    if repo_name:
        repo = github_client.get_repo(repo_name)
        assert repo is not None
        assert hasattr(repo, "get_issues")


def test_github_client_error_handling():
    """Test GitHub client error handling."""
    # Test invalid token
    with patch("my_chat_gpt_utils.github_utils.Github") as mock_github:
        mock_github.return_value.get_user.side_effect = GithubException(401, {"message": "Bad credentials"})
        with pytest.raises(ValueError, match="Invalid or expired GITHUB_TOKEN or unable to connect to GitHub"):
            GithubClientFactory.create_client("invalid-token")

    # Test missing token
    with patch.dict(os.environ, {}, clear=True), patch("my_chat_gpt_utils.github_utils.load_dotenv", return_value=None):
        with pytest.raises(ValueError, match="GITHUB_TOKEN not found in environment variables"):
            GithubClientFactory.create_client()


def test_github_client_test_mode():
    """Test GitHub client in test mode."""
    client = GithubClientFactory.create_client(test_mode=True)

    # Verify required functionality is available
    assert hasattr(client, "get_user")
    assert hasattr(client, "get_repo")

    # Test basic operations
    user = client.get_user()
    assert user is not None
    assert hasattr(user, "login")

    # Test repository access in test mode
    repo = client.get_repo("owner/repo")
    assert repo is not None
    assert hasattr(repo, "get_issues")


def test_repository_access(github_client):
    """Test repository access functionality."""
    # Test with valid repository from environment
    repo_name = os.getenv("GITHUB_REPOSITORY")
    if repo_name:
        repo = GithubClientFactory.get_repository(github_client)
        assert repo is not None
        assert hasattr(repo, "get_issues")

    # Test with invalid repository
    with pytest.raises(ValueError, match="GITHUB_REPOSITORY not found in environment variables"):
        with patch.dict(os.environ, {}, clear=True):
            GithubClientFactory.get_repository(github_client)
