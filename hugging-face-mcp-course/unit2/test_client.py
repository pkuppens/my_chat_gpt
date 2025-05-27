#!/usr/bin/env python3
"""
Simple test script for the MCP Gradio client functionality.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

# Import our client functions
from mcp_gradio_client import call_gradio_api_directly, load_mcp_config, test_server_connection


def test_config_loading():
    """Test loading the MCP configuration."""
    print("Testing MCP configuration loading...")
    config = load_mcp_config()
    if config:
        print(f"✅ Config loaded successfully: {config['name']}")
        print(f"   Server URL: {config['transport']['url']}")
        return True
    else:
        print("❌ Failed to load config")
        return False


def test_server_connectivity():
    """Test server connectivity."""
    print("\nTesting server connectivity...")
    config = load_mcp_config()
    if not config:
        print("❌ No config available")
        return False

    server_url = config["transport"]["url"].replace("/gradio_api/mcp/sse", "")
    print(f"Testing connection to: {server_url}")

    if test_server_connection(server_url):
        print("✅ Server is accessible")
        return True
    else:
        print("❌ Server is not accessible")
        return False


def test_sentiment_analysis():
    """Test sentiment analysis functionality."""
    print("\nTesting sentiment analysis...")
    config = load_mcp_config()
    if not config:
        print("❌ No config available")
        return False

    server_url = config["transport"]["url"].replace("/gradio_api/mcp/sse", "")
    test_text = "I love this amazing feature!"

    print(f"Analyzing text: '{test_text}'")
    result = call_gradio_api_directly(test_text, server_url)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    else:
        print("✅ Analysis successful:")
        print(f"   Polarity: {result.get('polarity', 'N/A')}")
        print(f"   Subjectivity: {result.get('subjectivity', 'N/A')}")
        print(f"   Assessment: {result.get('assessment', 'N/A')}")
        return True


def main():
    """Run all tests."""
    print("🧪 MCP Gradio Client Test Suite")
    print("=" * 40)

    tests = [test_config_loading, test_server_connectivity, test_sentiment_analysis]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the server status.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
