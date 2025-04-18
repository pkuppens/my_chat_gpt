"""
Analyze GitHub issues using Language Models.

The module provides functionality for:
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
from typing import Any, Dict, List, Optional, Union

import openai
from openai import APIError, RateLimitError
from openai import AuthenticationError as OpenAIAuthenticationError

from my_chat_gpt_utils.exceptions import (
    OpenAIAuthenticationError as CustomOpenAIAuthenticationError,
)
from my_chat_gpt_utils.exceptions import (
    ProblemCauseSolution,
)
from my_chat_gpt_utils.github_utils import (
    ISSUE_TYPES,
    PRIORITY_LEVELS,
    GitHubLabelManager,
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

    Attributes
    ----------
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
    """Analyzes GitHub issues using a Language Model."""

    def __init__(self, config: OpenAIConfig):
        """
        Initialize the analyzer with OpenAI configuration.

        Args:
        ----
            config (OpenAIConfig): Configuration for OpenAI API.

        """
        self.config = config
        self.client = openai.OpenAI(api_key=config.api_key)

    def analyze_issue(self, issue_data: Dict[str, Any]) -> IssueAnalysis:
        """
        Analyze a GitHub issue using OpenAI's API.

        Args:
        ----
            issue_data (Dict[str, Any]): Issue data to analyze.

        Returns:
        -------
            IssueAnalysis: Analysis results.

        Raises:
        ------
            ProblemCauseSolution: For various issues with clear problem-cause-solution descriptions
            OpenAIAuthenticationError: If OpenAI API key is invalid or expired
            ValueError: If the response format is invalid
            json.JSONDecodeError: If the response content is not valid JSON

        """
        # Prepare the prompt
        try:
            system_prompt, user_prompt = load_analyze_issue_prompt(
                {
                    "issue_title": issue_data.get("title", issue_data.get("issue_title", "")),
                    "issue_body": issue_data.get("body", issue_data.get("issue_body", "")),
                },
            )
        except Exception as e:
            raise ProblemCauseSolution(
                problem="Failed to prepare analysis prompt",
                cause=f"Error loading or formatting prompt templates: {str(e)}",
                solution="Check if prompt template files exist and contain valid placeholders",
                original_exception=e,
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
                raise ProblemCauseSolution(
                    problem="Invalid OpenAI API response",
                    cause="Response missing 'choices' array",
                    solution="Check if the OpenAI API endpoint is correct and returning expected format",
                )

            if not hasattr(response.choices[0], "message"):
                raise ProblemCauseSolution(
                    problem="Invalid OpenAI API response",
                    cause="Response missing 'message' in first choice",
                    solution="Check if the OpenAI API endpoint is correct and returning expected format",
                )

            if not hasattr(response.choices[0].message, "content"):
                raise ProblemCauseSolution(
                    problem="Invalid OpenAI API response",
                    cause="Response missing 'content' in message",
                    solution="Check if the OpenAI API endpoint is correct and returning expected format",
                )

            # Get and validate content
            content = response.choices[0].message.content
            if not isinstance(content, (str, bytes, bytearray)):
                raise ProblemCauseSolution(
                    problem="Invalid OpenAI API response content",
                    cause=f"Unexpected content type: {type(content)}",
                    solution="Check if the OpenAI API endpoint is returning text content as expected",
                )

            # Parse response
            try:
                analysis_dict = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenAI response as JSON: {content}")
                raise ProblemCauseSolution(
                    problem="Invalid OpenAI API response format",
                    cause="Response content is not valid JSON",
                    solution="Check if the system prompt is correctly instructing the model to return JSON",
                    original_exception=e,
                )

            # Validate required fields
            required_fields = ["issue_type", "priority", "complexity"]
            missing_fields = [field for field in required_fields if field not in analysis_dict]
            if missing_fields:
                raise ProblemCauseSolution(
                    problem="Incomplete analysis results",
                    cause=f"Missing required fields in analysis: {', '.join(missing_fields)}",
                    solution="Check if the system prompt correctly specifies all required fields",
                )

            return IssueAnalysis(
                issue_type=analysis_dict["issue_type"],
                priority=analysis_dict["priority"],
                complexity=analysis_dict["complexity"],
                review_feedback=analysis_dict.get("review_feedback", ""),
                next_steps=analysis_dict.get("next_steps", []),
            )

        except OpenAIAuthenticationError as e:
            raise CustomOpenAIAuthenticationError(
                original_exception=e,
                problem="OpenAI API authentication failed",
                cause="Invalid or expired API key",
                solution="Check your OpenAI API key and ensure it is correctly set in the environment",
            )
        except RateLimitError as e:
            raise ProblemCauseSolution(
                problem="OpenAI API rate limit exceeded",
                cause="Too many requests in a short time period",
                solution="Wait before retrying or upgrade your OpenAI API plan for higher rate limits",
                original_exception=e,
            )
        except APIError as e:
            raise ProblemCauseSolution(
                problem="OpenAI API error",
                cause=f"API request failed: {str(e)}",
                solution="Check OpenAI service status and try again later",
                original_exception=e,
            )
        except Exception as e:
            logger.error(f"Failed to analyze issue: {e}")
            raise ProblemCauseSolution(
                problem="Issue analysis failed",
                cause=f"Unexpected error during analysis: {str(e)}",
                solution="Check the logs for more details and try again",
                original_exception=e,
            )


def setup_openai_config() -> OpenAIConfig:
    """
    Set up and validate OpenAI configuration.

    Returns
    -------
        OpenAIConfig: Validated OpenAI configuration.

    Raises
    ------
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

    Returns
    -------
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
    ----
        analysis (IssueAnalysis): Issue analysis results.

    Returns:
    -------
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
    ----
        analysis (IssueAnalysis): Issue analysis results.

    Returns:
    -------
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
{chr(10).join(f"- {step}" for step in analysis.next_steps)}

---
*Analyzed automatically at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""


def process_issue_analysis(
    issue_data: Dict[str, Any],
    openai_config: Union[Dict[str, Any], OpenAIConfig],
    test_mode: bool = False,
) -> Dict[str, Any]:
    """
    Process issue analysis with OpenAI and GitHub integration.

    Args:
    ----
        issue_data (Dict[str, Any]): Issue data dictionary
        openai_config (Union[Dict[str, Any], OpenAIConfig]): OpenAI configuration
        test_mode (bool): If True, run in test mode

    Returns:
    -------
        Dict[str, Any]: Analysis results

    """
    if isinstance(openai_config, dict):
        openai_config = OpenAIConfig(**openai_config)

    github_client = get_github_client(test_mode=test_mode)
    label_manager = GitHubLabelManager(
        github_client.get_user().login if github_client else get_github_client(test_mode=test_mode).get_user().login,
    )

    # Create analyzer and analyze issue
    analyzer = LLMIssueAnalyzer(openai_config)
    analysis = analyzer.analyze_issue(issue_data)

    # Create label manager and ensure required labels exist
    label_manager.ensure_labels_exist(issue_data["repo_owner"], issue_data["repo_name"], get_required_labels())

    # Add specific labels for this issue
    issue_labels = get_issue_specific_labels(analysis)
    label_manager.add_labels_to_issue(
        issue_data["repo_owner"],
        issue_data["repo_name"],
        issue_data["issue_number"],
        issue_labels,
    )

    # Create and post comment
    comment = create_analysis_comment(analysis)
    full_repo_name = f"{issue_data['repo_owner']}/{issue_data['repo_name']}"
    append_response_to_issue(github_client or get_github_client(), full_repo_name, issue_data, comment)

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
