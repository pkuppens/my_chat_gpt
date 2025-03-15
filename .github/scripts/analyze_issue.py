import os
import logging
from datetime import datetime

from my_chat_gpt_utils.analyze_issue import LLMIssueAnalyzer

from my_chat_gpt_utils.github_utils import (
    GitHubEventProcessor,
    GitHubLabelManager,
    ISSUE_TYPES,
    PRIORITY_LEVELS,
)
from my_chat_gpt_utils.openai_utils import (
    OpenAIConfig,
    OpenAIVersionChecker,
    OpenAIValidator,
    DEFAULT_LLM_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
)
from my_chat_gpt_utils.logger import logger

# Which of these work? Actually, all of them, with the PYTHONUNBUFFERED option on.
logging.info("Logging the start of the issue analysis...")
logger.info("Logger the start of the issue analysis...")
print("Printing the start of the issue analysis...")


def main():
    """
    Main execution function for GitHub issue LLM analysis.
    """
    # Validate OpenAI library and API key
    if not OpenAIVersionChecker.check_library_version():
        raise RuntimeError("Incompatible OpenAI library version")

    # Setup configurations
    openai_config = OpenAIConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=os.environ.get("LLM_MODEL", DEFAULT_LLM_MODEL),
        max_tokens=int(os.environ.get("MAX_TOKENS", DEFAULT_MAX_TOKENS)),
        temperature=float(os.environ.get("TEMPERATURE", DEFAULT_TEMPERATURE)),
    )

    # Validate OpenAI API key
    if not OpenAIValidator.validate_api_key(openai_config.api_key):
        raise ValueError("Invalid OpenAI API key")

    # Retrieve issue data using GitHubEventProcessor from previous script
    try:
        event = GitHubEventProcessor.parse_issue_event()
        issue_data = {
            "repo_owner": event.get("repository", {}).get("owner", {}).get("login"),
            "repo_name": event.get("repository", {}).get("name"),
            "issue_number": event.get("issue", {}).get("number"),
            "issue_title": event.get("issue", {}).get("title"),
            "issue_body": event.get("issue", {}).get("body") or "",
        }

        # Analyze issue
        llm_analyzer = LLMIssueAnalyzer(openai_config)
        analysis = llm_analyzer.analyze_issue(issue_data)

        # Prepare labels
        label_manager = GitHubLabelManager(os.environ.get("GITHUB_TOKEN", ""))

        # Ensure all potential labels exist
        all_labels = [
            *[f"Type: {issue_type}" for issue_type in ISSUE_TYPES],
            *[f"Priority: {priority}" for priority in PRIORITY_LEVELS],
            "Complexity: Simple",
            "Complexity: Moderate",
            "Complexity: Complex",
        ]
        label_manager.ensure_labels_exist(issue_data["repo_owner"], issue_data["repo_name"], all_labels)

        # Add specific labels for this issue
        specific_labels = [f"Type: {analysis.issue_type}", f"Priority: {analysis.priority}", f"Complexity: {analysis.complexity}"]
        label_manager.add_labels_to_issue(
            issue_data["repo_owner"], issue_data["repo_name"], issue_data["issue_number"], specific_labels
        )

        # Add comment with analysis details
        comment = f"""
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

        # Optional: Add comment to issue
        logger.info(f"Analysis complete for issue #{issue_data['issue_number']}")
        logger.info(f"Analysis result: {analysis}")
        logger.info(f"Comment added to issue: {comment}")
        # You would implement this similar to previous script's add_comment_to_issue method

    except Exception as e:
        logger.error(f"Issue analysis failed: {e}")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        raise
