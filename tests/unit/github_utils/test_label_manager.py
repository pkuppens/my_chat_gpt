"""
Unit tests for GitHub label manager functionality.

This module tests the GitHubLabelManager class and related functionality.
All external dependencies are mocked to ensure reliable testing.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from my_chat_gpt_utils.github_utils import GitHubLabelManager


@pytest.fixture
def label_manager():
    """Fixture providing a GitHub label manager instance."""
    return GitHubLabelManager("test-token")


@pytest.fixture
def mock_response():
    """Fixture providing a mock requests response."""
    mock = MagicMock(spec=requests.Response)
    mock.status_code = 200
    return mock


def test_ensure_labels_exist_new_labels(label_manager, mock_response):
    """Test creating new labels when they don't exist."""
    mock_response.json.return_value = [{"name": "existing-label"}]
    with (
        patch("requests.get", return_value=mock_response),
        patch("requests.post", return_value=mock_response),
    ):
        labels = ["new-label-1", "new-label-2"]
        label_manager.ensure_labels_exist("owner", "repo", labels)

        # Verify POST request was made for each new label
        assert requests.post.call_count == 2
        for label in labels:
            requests.post.assert_any_call(
                "https://api.github.com/repos/owner/repo/labels",
                headers={
                    "Authorization": "token test-token",
                    "Accept": "application/vnd.github.v3+json",
                },
                json={"name": label, "color": "6f42c1"},
            )


def test_ensure_labels_exist_existing_labels(label_manager, mock_response):
    """Test handling existing labels."""
    mock_response.json.return_value = [{"name": "existing-label"}]
    with (
        patch("requests.get", return_value=mock_response),
        patch("requests.post", return_value=mock_response),
    ):
        labels = ["existing-label", "new-label"]
        label_manager.ensure_labels_exist("owner", "repo", labels)

        # Verify POST request was only made for the new label
        assert requests.post.call_count == 1
        requests.post.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/labels",
            headers={
                "Authorization": "token test-token",
                "Accept": "application/vnd.github.v3+json",
            },
            json={"name": "new-label", "color": "6f42c1"},
        )


def test_ensure_labels_exist_custom_color(label_manager, mock_response):
    """Test creating labels with custom color."""
    mock_response.json.return_value = []
    with (
        patch("requests.get", return_value=mock_response),
        patch("requests.post", return_value=mock_response),
    ):
        labels = ["test-label"]
        label_manager.ensure_labels_exist("owner", "repo", labels, color="ff0000")

        requests.post.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/labels",
            headers={
                "Authorization": "token test-token",
                "Accept": "application/vnd.github.v3+json",
            },
            json={"name": "test-label", "color": "ff0000"},
        )


def test_add_labels_to_issue_success(label_manager, mock_response):
    """Test successfully adding labels to an issue."""
    with patch("requests.post", return_value=mock_response):
        result = label_manager.add_labels_to_issue("owner", "repo", 123, ["label1", "label2"])
        assert result is True

        requests.post.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/issues/123/labels",
            headers={
                "Authorization": "token test-token",
                "Accept": "application/vnd.github.v3+json",
            },
            json={"labels": ["label1", "label2"]},
        )


def test_add_labels_to_issue_failure(label_manager):
    """Test handling failure when adding labels."""
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    with patch("requests.post", return_value=mock_response):
        result = label_manager.add_labels_to_issue("owner", "repo", 123, ["label1"])
        assert result is False


def test_add_labels_to_issue_empty_labels(label_manager, mock_response):
    """Test adding empty list of labels."""
    with patch("requests.post", return_value=mock_response):
        result = label_manager.add_labels_to_issue("owner", "repo", 123, [])
        assert result is True

        requests.post.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/issues/123/labels",
            headers={
                "Authorization": "token test-token",
                "Accept": "application/vnd.github.v3+json",
            },
            json={"labels": []},
        )
