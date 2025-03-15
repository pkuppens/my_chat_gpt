"""
This script identifies duplicate GitHub issues using TF-IDF and cosine similarity.

Modules:
    typing: Provides type hints for function signatures.
    dataclasses: Provides a decorator and functions for creating data classes.
    os: Provides a way of using operating system dependent functionality.
    json: Provides functions for parsing JSON.
    sys: Provides access to some variables used or maintained by the interpreter.
    datetime: Supplies classes for manipulating dates and times.
    github: Provides access to the GitHub API.
    sklearn.feature_extraction.text: Provides TF-IDF vectorizer for text feature extraction.
    sklearn.metrics.pairwise: Provides cosine similarity metric.
    my_chat_gpt_utils.logger: Custom logger for logging messages.
    my_chat_gpt_utils.github_utils: Custom utilities for GitHub operations.

Classes:
    IssueContext: Represents the context and metadata of a GitHub issue.
    GithubClientFactory: Factory class for creating GitHub API clients and retrieving repository context.
    IssueRetriever: Service for retrieving and filtering GitHub issues.
    IssueSimilarityAnalyzer: Performs similarity analysis on GitHub issues using TF-IDF and cosine similarity.
    GitHubEventProcessor: Processes GitHub webhook events for issue-related actions.

Functions:
    main: Main execution function for GitHub issue similarity detection.
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

from my_chat_gpt_utils.logger import logger
from my_chat_gpt_utils.github_utils import (
    GitHubEventProcessor,
    GithubClientFactory,
    get_issues,
)


def main():
    """
    Main execution function for GitHub issue similarity detection.
    """
    # Setup GitHub client and repository
    github_client = GithubClientFactory.create_client()
    repository = GithubClientFactory.get_repository(github_client)

    # Process event and extract issue context
    event = GitHubEventProcessor.parse_issue_event()
    current_issue = GitHubEventProcessor.extract_issue_context(event)

    # Retrieve recent issues
    issue_retriever = IssueRetriever(repository)
    recent_issues = issue_retriever.get_recent_issues(state="all")

    # Filter out current issue from recent issues
    comparable_issues = [issue for issue in recent_issues if issue.number != current_issue.number]

    # Analyze similarities
    similarity_analyzer = IssueSimilarityAnalyzer()
    similar_issues = similarity_analyzer.compute_similarities(current_issue, comparable_issues)

    # Optional: log or process similar issues
    for issue, similarity in similar_issues:
        logger.info(f"Similar Issue: #{issue.number} " f"(Similarity: {similarity:.2%}, URL: {issue.url})")


if __name__ == "__main__":
    main()
