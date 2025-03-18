"""
This module provides functionality for analyzing GitHub issues using LLMs.

It includes:
1. Issue analysis using OpenAI's API
2. Label management
3. Comment generation
4. Environment-based issue data retrieval
"""

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import openai

from my_chat_gpt_utils.github_utils import (
    ISSUE_TYPES,
    PRIORITY_LEVELS,
    GitHubEventProcessor,
    GitHubLabelManager,
    IssueDataProvider,
    append_response_to_issue,
    get_github_client,
)
from my_chat_gpt_utils.logger import logger
from my_chat_gpt_utils.openai_utils import (
    DEFAULT_LLM_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    OpenAIConfig,
    OpenAIValidator,
    OpenAIVersionChecker,
)
from my_chat_gpt_utils.prompts import load_analyze_issue_prompt


@dataclass
class IssueAnalysis:
    """
    Represents the analysis results of a GitHub issue.

    Attributes:
        issue_type (str): Type of the issue (e.g., Bug, Feature).
        priority (str): Priority level of the issue.
        complexity (str): Complexity assessment of the issue.
        review_feedback (str): Detailed feedback from the review.
        next_steps (List[str]): Suggested next steps.
    """

    issue_type: str
    priority: str
    complexity: str
    review_feedback: str
    next_steps: List[str]


class LLMIssueAnalyzer:
    """
    Analyzes GitHub issues using a Language Model.
    """

    def __init__(self, config: OpenAIConfig):
        """
        Initialize the analyzer with OpenAI configuration.

        Args:
            config (OpenAIConfig): Configuration for OpenAI API.
        """
        self.config = config
        self.client = openai.OpenAI(api_key=config.api_key)

    def analyze_issue(self, issue_data: Dict[str, Any]) -> IssueAnalysis:
        """
        Analyze a GitHub issue using OpenAI's API.

        Args:
            issue_data (Dict[str, Any]): Issue data to analyze.

        Returns:
            IssueAnalysis: Analysis results.

        Raises:
            ValueError: If the response format is invalid.
            json.JSONDecodeError: If the response content is not valid JSON.
            Exception: For other API or processing errors.
        """
        # Prepare the prompt
        system_prompt, user_prompt = load_analyze_issue_prompt(
            {
                "issue_title": issue_data.get("title", issue_data.get("issue_title", "")),
                "issue_body": issue_data.get("body", issue_data.get("issue_body", "")),
            }
        )

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            # Validate response structure
            if not hasattr(response, "choices") or not response.choices:
                raise ValueError("OpenAI response missing 'choices' array")

            if not hasattr(response.choices[0], "message"):
                raise ValueError("OpenAI response missing 'message' in first choice")

            if not hasattr(response.choices[0].message, "content"):
                raise ValueError("OpenAI response missing 'content' in message")

            # Get and validate content
            content = response.choices[0].message.content
            if not isinstance(content, (str, bytes, bytearray)):
                raise ValueError(f"Invalid content type: {type(content)}. Expected str, bytes, or bytearray.")

            # Parse response
            try:
                analysis_dict = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenAI response as JSON: {content}")
                raise

            # Validate required fields
            required_fields = ["issue_type", "priority", "complexity"]
            missing_fields = [field for field in required_fields if field not in analysis_dict]
            if missing_fields:
                raise ValueError(f"Analysis missing required fields: {missing_fields}")

            return IssueAnalysis(
                issue_type=analysis_dict["issue_type"],
                priority=analysis_dict["priority"],
                complexity=analysis_dict["complexity"],
                review_feedback=analysis_dict.get("review_feedback", ""),
                next_steps=analysis_dict.get("next_steps", []),
            )

        except Exception as e:
            logger.error(f"Failed to analyze issue: {e}")
            raise


def setup_openai_config() -> OpenAIConfig:
    """
    Set up and validate OpenAI configuration.

    Returns:
        OpenAIConfig: Validated OpenAI configuration.

    Raises:
        RuntimeError: If OpenAI library version is incompatible.
        ValueError: If OpenAI API key is invalid.
    """
    if not OpenAIVersionChecker.check_library_version():
        raise RuntimeError("Incompatible OpenAI library version")

    config = OpenAIConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=os.environ.get("LLM_MODEL", DEFAULT_LLM_MODEL),
        max_tokens=int(os.environ.get("MAX_TOKENS", DEFAULT_MAX_TOKENS)),
        temperature=float(os.environ.get("TEMPERATURE", DEFAULT_TEMPERATURE)),
    )

    if not OpenAIValidator.validate_api_key(config.api_key):
        raise ValueError("Invalid OpenAI API key")

    return config


def get_required_labels() -> List[str]:
    """
    Get list of all required labels for issues.

    Returns:
        List[str]: List of required labels.
    """
    return [
        *[f"Type: {issue_type}" for issue_type in ISSUE_TYPES],
        *[f"Priority: {priority}" for priority in PRIORITY_LEVELS],
        "Complexity: Simple",
        "Complexity: Moderate",
        "Complexity: Complex",
    ]


def get_issue_specific_labels(analysis: IssueAnalysis) -> List[str]:
    """
    Get labels specific to an issue based on its analysis.

    Args:
        analysis (IssueAnalysis): Issue analysis results.

    Returns:
        List[str]: List of specific labels for the issue.
    """
    return [
        f"Type: {analysis.issue_type}",
        f"Priority: {analysis.priority}",
        f"Complexity: {analysis.complexity}",
    ]


def create_analysis_comment(analysis: IssueAnalysis) -> str:
    """
    Create a formatted comment with analysis details.

    Args:
        analysis (IssueAnalysis): Issue analysis results.

    Returns:
        str: Formatted comment text.
    """
    return f"""
## Issue Analysis

**Type:** {analysis.issue_type}
**Priority:** {analysis.priority}
**Complexity:** {analysis.complexity}

### Review Summary
{analysis.review_feedback}

### Suggested Next Steps
{chr(10).join(f'- {step}' for step in analysis.next_steps)}

---
*Analyzed automatically at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""


def process_issue_analysis(issue_data: Dict[str, Any], openai_config: Dict[str, Any]) -> IssueAnalysis:
    """
    Process a GitHub issue by analyzing it and adding appropriate labels and comments.

    Args:
        issue_data (Dict[str, Any]): Issue data including repository and issue details.
        openai_config (Dict[str, Any]): OpenAI configuration.

    Returns:
        IssueAnalysis: The analysis result.
    """
    llm_analyzer = LLMIssueAnalyzer(openai_config)
    analysis = llm_analyzer.analyze_issue(issue_data)

    # Prepare labels
    label_manager = GitHubLabelManager(os.environ.get("GITHUB_TOKEN", ""))

    # Ensure all potential labels exist
    label_manager.ensure_labels_exist(issue_data["repo_owner"], issue_data["repo_name"], get_required_labels())

    # Add specific labels for this issue
    label_manager.add_labels_to_issue(
        issue_data["repo_owner"], issue_data["repo_name"], issue_data["issue_number"], get_issue_specific_labels(analysis)
    )

    # Add comment with analysis details
    comment = create_analysis_comment(analysis)
    append_response_to_issue(get_github_client(), issue_data["repo_name"], issue_data, comment)

    logger.info(f"Analysis complete for issue #{issue_data['issue_number']}")
    logger.info(f"Analysis result: {analysis}")
    logger.info(f"Comment added to issue: {comment}")

    return analysis


def get_issue_data(issue_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get issue data from environment or provided data."""
    if issue_data is not None:
        return issue_data

    # Try to get data from environment
    issue_data = os.getenv("ISSUE_DATA")
    if issue_data:
        try:
            return json.loads(issue_data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse ISSUE_DATA: {e}")
            return {}

    # Try to get data from event file
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and os.path.exists(event_path):
        try:
            with open(event_path, "r", encoding="utf-8") as f:
                event_data = json.load(f)
                return event_data.get("issue", {})
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Failed to read event file: {e}")
            return {}

    return {}
