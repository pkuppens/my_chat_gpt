"""
Unit tests for GitHub issue similarity analyzer functionality.

This module tests the IssueSimilarityAnalyzer class and related functionality.
All external dependencies are mocked to ensure reliable testing.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer

from my_chat_gpt_utils.github_utils import IssueContext, IssueSimilarityAnalyzer


@pytest.fixture
def mock_issues():
    """Create mock issues for testing."""
    issues = []
    for i in range(3):
        issue = MagicMock()
        issue.title = f"Test Issue {i}"
        issue.body = f"Test body {i}"
        issues.append(issue)
    return issues


@pytest.fixture
def mock_vectorizer():
    """Create mock TF-IDF vectorizer."""
    vectorizer = MagicMock(spec=TfidfVectorizer)
    # Create a mock matrix with shape (3, 4) for 3 documents and 4 features
    mock_matrix = np.array([[0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.4, 0.5], [0.3, 0.4, 0.5, 0.6]])
    vectorizer.fit_transform.return_value = mock_matrix
    return vectorizer


def test_compute_similarities(mock_issues, mock_vectorizer):
    """Test computing similarities between issues."""
    analyzer = IssueSimilarityAnalyzer()
    target_issue = mock_issues[0]
    existing_issues = mock_issues[1:]

    with patch("my_chat_gpt_utils.github_utils.TfidfVectorizer", return_value=mock_vectorizer), patch(
        "my_chat_gpt_utils.github_utils.cosine_similarity"
    ) as mock_cosine:
        mock_cosine.return_value = np.array([[0.85, 0.75]])
        similarities = analyzer.compute_similarities(target_issue, existing_issues, threshold=0.8)
        assert len(similarities) == 1
        assert similarities[0]["issue"] == mock_issues[1]
        assert similarities[0]["similarity"] == 0.85


def test_compute_similarities_below_threshold(mock_issues, mock_vectorizer):
    """Test computing similarities with high threshold."""
    analyzer = IssueSimilarityAnalyzer()
    target_issue = mock_issues[0]
    existing_issues = mock_issues[1:]

    with patch("my_chat_gpt_utils.github_utils.TfidfVectorizer", return_value=mock_vectorizer), patch(
        "my_chat_gpt_utils.github_utils.cosine_similarity"
    ) as mock_cosine:
        mock_cosine.return_value = np.array([[0.75, 0.65]])
        similarities = analyzer.compute_similarities(target_issue, existing_issues, threshold=0.8)
        assert len(similarities) == 0


def test_compute_similarities_empty_existing(mock_issues, mock_vectorizer):
    """Test computing similarities with no existing issues."""
    analyzer = IssueSimilarityAnalyzer()
    target_issue = mock_issues[0]
    existing_issues = []

    similarities = analyzer.compute_similarities(target_issue, existing_issues)
    assert len(similarities) == 0


def test_compute_similarities_no_body(mock_issues, mock_vectorizer):
    """Test computing similarities with issues that have no body."""
    analyzer = IssueSimilarityAnalyzer()
    target_issue = MagicMock()
    target_issue.title = "Test Issue"
    target_issue.body = None
    existing_issues = mock_issues[1:]

    with patch("my_chat_gpt_utils.github_utils.TfidfVectorizer", return_value=mock_vectorizer), patch(
        "my_chat_gpt_utils.github_utils.cosine_similarity"
    ) as mock_cosine:
        mock_cosine.return_value = np.array([[0.85, 0.75]])
        similarities = analyzer.compute_similarities(target_issue, existing_issues)
        assert len(similarities) == 1
        assert similarities[0]["issue"] == mock_issues[1]
        assert similarities[0]["similarity"] == 0.85
