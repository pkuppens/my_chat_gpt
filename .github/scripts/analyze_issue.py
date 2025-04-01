"""
Execute GitHub issue LLM analysis.

This script:
1. Retrieves issue data from GitHub
2. Analyzes the issue using LLM
3. Adds appropriate labels and comments
"""

import json
import logging
import os
import sys
from typing import Any, Dict

from my_chat_gpt_utils.analyze_issue import analyze_issue


def validate_github_event() -> Dict[str, Any]:
    """Validate that the GitHub event is an issue event and return the event data."""
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        raise ValueError("This script should be run within a GitHub Action")

    try:
        with open(event_path, "r") as f:
            event = json.load(f)
    except Exception as e:
        raise ValueError(f"Error reading event file: {e}")

    if "issue" not in event:
        raise ValueError("This action only works with issue events")

    required_fields = ["title", "body", "number"]
    missing_fields = [field for field in required_fields if field not in event["issue"]]
    if missing_fields:
        raise ValueError(f"Missing required issue fields: {', '.join(missing_fields)}")

    return event


def main() -> None:
    """Execute the GitHub issue LLM analysis workflow."""
    try:
        logging.info("Starting issue analysis")
        event = validate_github_event()
        analysis_result = analyze_issue(
            event["issue"]["number"],
            event["issue"]["title"],
            event["issue"]["body"] or "",
        )
        logging.info("Completed issue analysis")
        print(json.dumps(analysis_result, indent=2))

    except Exception as e:
        logging.error(f"Error during execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
