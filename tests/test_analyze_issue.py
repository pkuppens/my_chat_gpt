import unittest
from unittest.mock import patch, MagicMock
from my_chat_gpt_utils.analyze_issue import LLMIssueAnalyzer
from my_chat_gpt_utils.openai_utils import OpenAIConfig

class TestAnalyzeIssue(unittest.TestCase):

    @patch('my_chat_gpt_utils.analyze_issue.get_github_issue')
    @patch('my_chat_gpt_utils.analyze_issue.append_response_to_issue')
    @patch('my_chat_gpt_utils.analyze_issue.openai.chat.completions.create')
    def test_analyze_issue(self, mock_openai_create, mock_append_response_to_issue, mock_get_github_issue):
        mock_response = MagicMock()
        mock_response.choices[0].message.content.strip.return_value = '{"issue_type": "Bug", "priority": "High", "complexity": "Moderate"}'
        mock_openai_create.return_value = mock_response

        mock_issue = MagicMock()
        mock_get_github_issue.return_value = mock_issue

        config = OpenAIConfig(api_key="test_key", model="test_model", max_tokens=100, temperature=0.5)
        analyzer = LLMIssueAnalyzer(config)

        issue_data = {
            "repo_owner": "test_owner",
            "repo_name": "test_repo",
            "issue_number": 1,
            "issue_title": "Test Issue",
            "issue_body": "This is a test issue."
        }

        analysis = analyzer.analyze_issue(issue_data)

        mock_get_github_issue.assert_called_once_with(issue_data["repo_owner"], issue_data["repo_name"], issue_data)
        mock_append_response_to_issue.assert_called_once_with(mock_issue, issue_data["repo_name"], issue_data, mock_response.choices[0].message.content.strip())
        self.assertEqual(analysis.issue_type, "Bug")
        self.assertEqual(analysis.priority, "High")
        self.assertEqual(analysis.complexity, "Moderate")

if __name__ == '__main__':
    unittest.main()
