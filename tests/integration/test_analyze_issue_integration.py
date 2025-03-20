"""
Integration tests for analyze_issue module from my_chat_gpt_utils package.

This module contains integration tests that:
1. Use real GitHub clients when appropriate (with proper test tokens)
2. Test actual API interactions
3. Run in a controlled environment with test repositories

These tests are separate from unit tests to:
1. Allow running unit tests without GitHub access
2. Prevent accidental modifications to real repositories
3. Make it clear which tests require external services

These tests interact with the actual GitHub API and require valid credentials.
They are marked with @pytest.mark.integration and are skipped by default in regular test runs.
"""

import os
from unittest.mock import patch

import pytest

from my_chat_gpt_utils.analyze_issue import process_issue_analysis
from my_chat_gpt_utils.openai_utils import OpenAIConfig

# Skip all tests if required environment variables are not set
pytestmark = pytest.mark.skipif(
    not all(
        [
            os.getenv("GITHUB_TOKEN"),
            os.getenv("GITHUB_REPOSITORY"),
            os.getenv("OPENAI_API_KEY"),
        ]
    ),
    reason="Required environment variables not set",
)


@pytest.fixture
def test_issue_data():
    """Fixture providing test issue data for integration tests."""
    return {
        "repo_owner": os.getenv("GITHUB_REPOSITORY").split("/")[0],
        "repo_name": os.getenv("GITHUB_REPOSITORY").split("/")[1],
        "issue_number": 1,  # Use a test issue number
        "issue_title": "Test Integration Issue",
        "issue_body": "This is a test issue for integration testing.",
    }


@pytest.fixture
def test_openai_config():
    """Fixture providing OpenAI configuration for integration tests."""
    return OpenAIConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",  # Use a faster model for testing
        temperature=0.7,
        max_tokens=500,
    )


@pytest.mark.integration
def test_process_issue_analysis_integration(test_issue_data, test_openai_config):
    """
    Integration test for the complete issue analysis process.

    This test:
    1. Uses real GitHub client with test token
    2. Makes actual API calls to OpenAI
    3. Creates real labels and comments on a test issue

    Requirements:
    1. GITHUB_TOKEN with appropriate permissions
    2. GITHUB_REPOSITORY pointing to a test repository
    3. OPENAI_API_KEY for API access
    """
    result = process_issue_analysis(test_issue_data, test_openai_config, test_mode=True)

    # Verify analysis results
    assert result.issue_type in ["Bug Fix", "Feature", "Task", "Question"]
    assert result.priority in ["Critical", "High", "Medium", "Low"]
    assert result.complexity in ["Simple", "Moderate", "Complex"]
    assert isinstance(result.review_feedback, str)
    assert isinstance(result.next_steps, list)
