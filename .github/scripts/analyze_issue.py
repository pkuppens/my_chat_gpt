"""
GitHub Action script for analyzing issues using LLM.

This script is triggered by GitHub Actions to analyze new or updated issues.
It uses the analyze_issue module to perform the analysis and update the issue
with labels and comments.
"""

import logging

from my_chat_gpt_utils.analyze_issue import (
    get_issue_data,
    process_issue_analysis,
    setup_openai_config,
)
from my_chat_gpt_utils.logger import logger

# Needs the PYTHONUNBUFFERED option on to log in the github actions
logging.info("Logging the start of the issue analysis...")


def main():
    """
    Main execution function for GitHub issue LLM analysis.
    """
    try:
        # Setup OpenAI configuration
        openai_config = setup_openai_config()

        # Get issue data from appropriate source
        issue_data = get_issue_data()

        # Process the issue analysis
        process_issue_analysis(issue_data, openai_config)

    except Exception as e:
        logger.error(f"Issue analysis failed: {e}")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        raise
