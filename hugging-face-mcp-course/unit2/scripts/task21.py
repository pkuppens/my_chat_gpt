#!/usr/bin/env python3
"""
Verification script for Task 2.1: Basic Sentiment Analysis Server
Checks the server implementation and functionality.
"""

import importlib.util
import sys
from pathlib import Path


def check_server_file() -> bool:
    """Check if unit2.py exists and has required components."""
    server_path = Path("hugging-face-mcp-course/unit2/unit2.py")
    if not server_path.exists():
        print("❌ Server file not found at:", server_path)
        return False

    # Check if file contains required components
    with open(server_path, "r") as f:
        content = f.read()

    required_components = [
        "import gradio as gr",
        "from textblob import TextBlob",
        "def sentiment_analysis",
        "gr.Interface",
        "demo.launch(mcp_server=True)",
    ]

    missing = [comp for comp in required_components if comp not in content]
    if missing:
        print("❌ Server file is missing required components:")
        for comp in missing:
            print(f"   - {comp}")
        return False

    return True


def test_sentiment_function() -> bool:
    """Test the sentiment_analysis function directly."""
    try:
        # Import the function from unit2.py
        spec = importlib.util.spec_from_file_location("unit2", "hugging-face-mcp-course/unit2/unit2.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Test with known examples
        test_cases = [("I love this!", "positive"), ("This is terrible", "negative"), ("The sky is blue", "neutral")]

        for text, expected in test_cases:
            result = module.sentiment_analysis(text)

            # Check result structure
            if not isinstance(result, dict):
                print(f"❌ Result is not a dictionary for text: '{text}'")
                return False

            required_keys = {"polarity", "subjectivity", "assessment"}
            if not all(key in result for key in required_keys):
                print(f"❌ Result missing required keys for text: '{text}'")
                return False

            # Check assessment matches expected
            if result["assessment"] != expected:
                print(f"❌ Unexpected assessment for text: '{text}'")
                print(f"   Expected: {expected}")
                print(f"   Got: {result['assessment']}")
                return False

            print(f"✅ Test case passed: '{text}'")
            print(f"   Polarity: {result['polarity']:.2f}")
            print(f"   Subjectivity: {result['subjectivity']:.2f}")
            print(f"   Assessment: {result['assessment']}")

        return True
    except Exception as e:
        print(f"❌ Error testing sentiment function: {e}")
        return False


def main():
    """Run Task 2.1 verification checks."""
    print("🔍 Verifying Task 2.1: Basic Sentiment Analysis Server")
    print("=" * 50)

    # Check server file
    if not check_server_file():
        print("\n❌ Server file verification failed")
        return 1

    # Test sentiment function
    print("\nTesting sentiment analysis function...")
    if not test_sentiment_function():
        print("\n❌ Sentiment function test failed")
        return 1

    print("\n✨ Task 2.1 verification complete!")
    print("Server implementation is correct and functional.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
