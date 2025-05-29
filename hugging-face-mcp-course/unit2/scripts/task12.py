#!/usr/bin/env python3
"""
Verification script for Task 1.2: TextBlob Setup
Checks TextBlob installation and functionality.
"""

import importlib.util
import sys

import nltk
from textblob import TextBlob


def check_nltk_data() -> bool:
    """Check if required NLTK data is downloaded."""
    try:
        # Check if punkt is downloaded
        nltk.data.find("tokenizers/punkt")
        # Check if brown corpus is downloaded
        nltk.data.find("corpora/brown")
        return True
    except LookupError:
        return False


def test_sentiment_analysis() -> bool:
    """Test TextBlob sentiment analysis with a known example."""
    try:
        text = "I love this course!"
        blob = TextBlob(text)
        sentiment = blob.sentiment

        # Check if sentiment values are within expected ranges
        if not (-1 <= sentiment.polarity <= 1):
            return False
        if not (0 <= sentiment.subjectivity <= 1):
            return False

        # Print the results for verification
        print(f"Test text: '{text}'")
        print(f"Polarity: {sentiment.polarity:.2f} (should be positive)")
        print(f"Subjectivity: {sentiment.subjectivity:.2f}")

        return True
    except Exception as e:
        print(f"Error testing sentiment analysis: {e}")
        return False


def main():
    """Run Task 1.2 verification checks."""
    print("🔍 Verifying Task 1.2: TextBlob Setup")
    print("=" * 50)

    # Check if TextBlob is installed
    if importlib.util.find_spec("textblob") is not None:
        print("✅ TextBlob is installed")
    else:
        print("❌ TextBlob is not installed")
        print("   Please run: uv add textblob")
        return 1

    # Check NLTK data
    if check_nltk_data():
        print("✅ Required NLTK data is downloaded")
    else:
        print("❌ Required NLTK data is missing")
        print("   Please run: uv run python -c \"import nltk; nltk.download('punkt'); nltk.download('brown')\"")
        return 1

    # Test sentiment analysis
    print("\nTesting sentiment analysis functionality...")
    if test_sentiment_analysis():
        print("✅ Sentiment analysis is working correctly")
    else:
        print("❌ Sentiment analysis test failed")
        return 1

    print("\n✨ Task 1.2 verification complete!")
    print("TextBlob is properly installed and configured.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
