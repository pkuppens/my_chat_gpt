"""
Unit tests for GitHub issue similarity analyzer functionality.

This module tests the IssueSimilarityAnalyzer class which uses TF-IDF and cosine similarity
to identify similar GitHub issues. The tests focus on realistic scenarios where:

1. Two issues about the same topic (e.g., API-related) should have high similarity (>0.6)
2. Two issues about different topics (e.g., API vs UI) should have low similarity
3. Edge cases like issues with no body should still work correctly

The tests use real TF-IDF vectorization to ensure the similarity detection works as expected
in real-world scenarios, rather than just testing the mathematical correctness.
"""

from unittest.mock import MagicMock

import pytest

from my_chat_gpt_utils.github_utils import IssueSimilarityAnalyzer


@pytest.fixture
def realistic_issues():
    """Create realistic test issues with different topics and content."""
    issues = []

    # API-related issues
    api_issue1 = MagicMock()
    api_issue1.title = "Add rate limiting to REST API endpoints"
    api_issue1.body = (
        "We need to implement rate limiting for our REST API to prevent abuse. Should use token bucket algorithm."
    )
    issues.append(api_issue1)

    api_issue2 = MagicMock()
    api_issue2.title = "Implement rate limiting for API"
    api_issue2.body = "Add rate limiting to protect our API endpoints from abuse. Consider using token bucket."
    issues.append(api_issue2)

    # UI-related issue
    ui_issue = MagicMock()
    ui_issue.title = "Fix button alignment in mobile view"
    ui_issue.body = "The submit button is misaligned on mobile devices. Need to adjust CSS for better responsiveness."
    issues.append(ui_issue)

    # Issue with no body
    no_body_issue = MagicMock()
    no_body_issue.title = "Add rate limiting to REST API endpoints"
    no_body_issue.body = None
    issues.append(no_body_issue)

    return issues


def test_similar_issues_have_high_similarity(realistic_issues):
    """Test that issues about the same topic have high similarity scores."""
    analyzer = IssueSimilarityAnalyzer(similarity_threshold=0.6)
    target_issue = realistic_issues[0]  # First API issue
    existing_issues = [realistic_issues[1]]  # Second API issue

    similarities = analyzer.compute_similarities(target_issue, existing_issues)
    assert len(similarities) == 1
    assert similarities[0][1] > 0.6  # High similarity for similar issues


def test_different_topics_have_low_similarity(realistic_issues):
    """Test that issues about different topics have low similarity scores."""
    analyzer = IssueSimilarityAnalyzer(similarity_threshold=0.6)
    target_issue = realistic_issues[0]  # API issue
    existing_issues = [realistic_issues[2]]  # UI issue

    similarities = analyzer.compute_similarities(target_issue, existing_issues)
    assert len(similarities) == 0  # No issues should be above threshold


def test_issue_with_no_body(realistic_issues):
    """Test that similarity can be computed for issues without a body."""
    analyzer = IssueSimilarityAnalyzer(similarity_threshold=0.6)
    target_issue = realistic_issues[3]  # Issue with no body
    existing_issues = [realistic_issues[0]]  # API issue

    similarities = analyzer.compute_similarities(target_issue, existing_issues)
    assert len(similarities) == 1
    assert similarities[0][1] > 0.6  # High similarity based on title only


def test_empty_existing_issues():
    """Test handling of empty existing issues list."""
    analyzer = IssueSimilarityAnalyzer(similarity_threshold=0.6)
    target_issue = MagicMock()
    target_issue.title = "Test Issue"
    target_issue.body = "Test body"
    existing_issues = []

    similarities = analyzer.compute_similarities(target_issue, existing_issues)
    assert len(similarities) == 0
