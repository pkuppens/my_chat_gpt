"""
Test module for analyze_issue module from my_chat_gpt_utils package.
This module contains unit tests for the LLMIssueAnalyzer class.
"""

import json
import unittest
from typing import Dict, Any, Optional
from unittest.mock import patch, MagicMock

from my_chat_gpt_utils.analyze_issue import LLMIssueAnalyzer, IssueAnalysis
from my_chat_gpt_utils.openai_utils import OpenAIConfig


class TestAnalyzeIssue(unittest.TestCase):
    """
    Test class for LLMIssueAnalyzer.
    Tests the analyze_issue method with mocked dependencies.
    """

    @patch("my_chat_gpt_utils.analyze_issue.openai.chat.completions.create")
    def test_analyze_issue(self, mock_openai_create: MagicMock) -> None:
        """
        Test the analyze_issue method of LLMIssueAnalyzer.

        This test verifies that:
        1. The OpenAI API is called with correct parameters
        2. Response is properly processed
        3. Analysis object is returned with correct attributes

        Args:
            mock_openai_create: Mock for the OpenAI API call

        Raises:
            AssertionError: If any of the test assertions fail
        """
        # Setup the mock response from OpenAI API
        expected_analysis: Dict[str, str] = {"issue_type": "Bug", "priority": "High", "complexity": "Moderate"}

        # Create a structured mock response that matches OpenAI's API structure
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps(expected_analysis)))]
        mock_openai_create.return_value = mock_response

        # Create test configuration with defined parameters
        config = OpenAIConfig(api_key="test_key", model="test_model", max_tokens=100, temperature=0.5)

        # Initialize the analyzer with the configuration
        analyzer = LLMIssueAnalyzer(config)

        # Define test issue data
        issue_data: Dict[str, Any] = {
            "repo_owner": "test_owner",
            "repo_name": "test_repo",
            "issue_number": 1,
            "issue_title": "Test Issue",
            "issue_body": "This is a test issue.",
        }

        # Execute the method under test
        analysis: IssueAnalysis = analyzer.analyze_issue(issue_data)

        # Verify OpenAI API was called with correct parameters
        mock_openai_create.assert_called_once()
        call_args = mock_openai_create.call_args[1]

        # Verify the model parameter was passed correctly
        self.assertEqual(call_args.get("model"), "test_model")

        # Verify presence of messages in the API call
        self.assertIn("messages", call_args)

        # Verify the correct format of the messages parameter
        messages = call_args.get("messages", [])
        self.assertTrue(len(messages) > 0)

        # Verify temperature and max_tokens parameters
        self.assertEqual(call_args.get("temperature"), 0.5)
        self.assertEqual(call_args.get("max_tokens"), 100)

        # Verify the analysis results match expected values
        self.assertEqual(analysis.issue_type, expected_analysis["issue_type"])
        self.assertEqual(analysis.priority, expected_analysis["priority"])
        self.assertEqual(analysis.complexity, expected_analysis["complexity"])


if __name__ == "__main__":
    unittest.main()
