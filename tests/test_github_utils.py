"""
Test suite for GitHub utility functions.

This module contains unit tests for the GitHub-related utility functions
in my_chat_gpt_utils.github_utils, including issue retrieval and response
appending functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

from my_chat_gpt_utils.github_utils import append_response_to_issue, get_github_issue


class TestGitHubUtils(unittest.TestCase):
    """Test cases for GitHub utility functions."""

    @patch("my_chat_gpt_utils.github_utils.get_repository")
    @patch("my_chat_gpt_utils.github_utils.Github")
    def test_get_github_issue(self, MockGithub, mock_get_repository):
        """
        Test the get_github_issue function.

        This test verifies that the function correctly retrieves an issue
        from a GitHub repository using the provided client and issue data.
        """
        mock_client = MockGithub.return_value
        mock_repo = mock_get_repository.return_value
        mock_issue = MagicMock()
        mock_repo.get_issue.return_value = mock_issue

        issue_data = {
            "repo_owner": "test_owner",
            "repo_name": "test_repo",
            "issue_number": 1,
        }

        issue = get_github_issue(mock_client, issue_data["repo_name"], issue_data)
        mock_get_repository.assert_called_once_with(mock_client, issue_data["repo_name"])
        mock_repo.get_issue.assert_called_once_with(number=issue_data["issue_number"])
        self.assertEqual(issue, mock_issue)

    @patch("my_chat_gpt_utils.github_utils.get_github_issue")
    @patch("my_chat_gpt_utils.github_utils.add_comment")
    def test_append_response_to_issue(self, mock_add_comment, mock_get_github_issue):
        """
        Test the append_response_to_issue function.

        This test verifies that the function correctly appends a response
        as a comment to a GitHub issue using the provided client and issue data.
        """
        mock_issue = MagicMock()
        mock_get_github_issue.return_value = mock_issue

        client = MagicMock()
        repo_name = "test_repo"
        issue_data = {
            "repo_owner": "test_owner",
            "repo_name": repo_name,
            "issue_number": 1,
        }
        response = "Test response"

        append_response_to_issue(client, repo_name, issue_data, response)
        mock_get_github_issue.assert_called_once_with(client, repo_name, issue_data)
        mock_add_comment.assert_called_once_with(mock_issue, f"## OpenAI API Response\n\n{response}")


if __name__ == "__main__":
    unittest.main()
