"""
Execute GitHub issue LLM analysis.

This script analyzes GitHub issues using a Language Model (LLM) to:
1. Classify issue type and priority
2. Assess complexity
3. Provide review feedback
4. Suggest next steps

The script can run in three modes:
1. GitHub Actions mode (default): Uses GITHUB_EVENT_PATH to get issue data
2. Local test mode (--test): Uses mock data for testing
3. Local issue mode (--issue): Analyzes a specific GitHub issue number

Required Environment Variables:
    - OPENAI_API_KEY: Your OpenAI API key
    - GITHUB_TOKEN: Your GitHub personal access token
    - GITHUB_REPOSITORY: Repository in format "owner/repo" (only for non-test mode)

Optional Environment Variables:
    - LLM_MODEL: OpenAI model to use (default: gpt-4)
    - MAX_TOKENS: Maximum tokens for LLM response (default: 4096)
    - TEMPERATURE: LLM temperature setting (default: 0.1)

Example Usage:
    # Run in test mode
    python analyze_issue.py --test

    # Analyze a specific issue
    python analyze_issue.py --issue 123

    # Run in GitHub Actions mode
    python analyze_issue.py
"""

# ruff: noqa: E402
import os
import sys
from pathlib import Path

# Add repository root to Python path
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Now we can import other modules
import argparse
import json
import logging
from typing import Any, Dict

from dotenv import load_dotenv

from my_chat_gpt_utils.analyze_issue import process_issue_analysis
from my_chat_gpt_utils.openai_utils import OpenAIConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Load environment variables from .env file if it exists
env_file = os.path.join(Path(__file__).resolve().parents[2], '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)


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


def get_test_issue_data() -> Dict[str, Any]:
    """Get test issue data for local development."""
    return {
        "repo_owner": "test_owner",
        "repo_name": "test_repo",
        "issue_number": 1,
        "issue_title": "Test Issue",
        "issue_body": "This is a test issue",
    }


def get_openai_config() -> OpenAIConfig:
    """Get OpenAI configuration from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )
    if api_key == "your_openai_api_key_here":
        raise ValueError(
            "Please replace 'your_openai_api_key_here' in .env with your actual OpenAI API key"
        )

    return OpenAIConfig(
        api_key=api_key,
        model=os.getenv("LLM_MODEL", "gpt-4"),
        temperature=float(os.getenv("TEMPERATURE", "0.1")),
        max_tokens=int(os.getenv("MAX_TOKENS", "4096")),
    )


def get_github_repo_info() -> tuple[str, str]:
    """Get GitHub repository owner and name from environment variables."""
    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo:
        raise ValueError(
            "GITHUB_REPOSITORY environment variable is required. "
            "Please set it in your .env file or environment."
        )

    try:
        owner, name = repo.split("/")
        return owner, name
    except ValueError:
        raise ValueError(
            f"Invalid GITHUB_REPOSITORY format: {repo}. "
            "Expected format: 'owner/repo'"
        )


def validate_github_token() -> None:
    """Validate that GitHub token is set and not the default value."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError(
            "GITHUB_TOKEN environment variable is required. "
            "Please set it in your .env file or environment."
        )
    if token == "your_github_token_here":
        raise ValueError(
            "Please replace 'your_github_token_here' in .env with your actual GitHub token"
        )


def main() -> None:
    """Execute the GitHub issue LLM analysis workflow."""
    parser = argparse.ArgumentParser(
        description="Analyze GitHub issues using LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--test", action="store_true", help="Run in test mode with mock data")
    parser.add_argument("--issue", type=int, help="GitHub issue number to analyze")
    args = parser.parse_args()

    try:
        logging.info("Starting issue analysis")

        # Validate GitHub token except in test mode
        if not args.test:
            validate_github_token()

        # Get issue data based on mode
        if args.test:
            issue_data = get_test_issue_data()
        elif args.issue:
            # TODO: Implement GitHub API call to get issue data
            raise NotImplementedError("GitHub API integration not implemented yet")
        else:
            event = validate_github_event()
            repo_owner, repo_name = get_github_repo_info()
            issue_data = {
                "repo_owner": repo_owner,
                "repo_name": repo_name,
                "issue_number": event["issue"]["number"],
                "issue_title": event["issue"]["title"],
                "issue_body": event["issue"]["body"] or "",
            }

        # Get OpenAI configuration
        openai_config = get_openai_config()

        # Process the issue
        analysis_result = process_issue_analysis(issue_data, openai_config, test_mode=args.test)

        logging.info("Completed issue analysis")
        print(json.dumps(analysis_result, indent=2))

    except ValueError as e:
        logging.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except NotImplementedError as e:
        logging.error(f"Not implemented: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error during execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
