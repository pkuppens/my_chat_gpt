#!/usr/bin/env python3
"""
Verification script for Task 2.2: Server Testing and Validation
Checks server endpoints and functionality.
"""

import atexit
import subprocess
import sys
import time

import requests

# Global variable to store server process
server_process = None


def start_server():
    """Start the sentiment analysis server."""
    global server_process
    try:
        # Start the server in a subprocess
        server_process = subprocess.Popen(
            ["uv", "run", "python", "hugging-face-mcp-course/unit2/unit2.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Wait for server to start
        print("Starting server...")
        time.sleep(5)  # Give server time to start

        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False


def stop_server():
    """Stop the sentiment analysis server."""
    global server_process
    if server_process:
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()


def test_web_interface():
    """Test the Gradio web interface."""
    try:
        # Try to access the web interface
        response = requests.get("http://localhost:7860")
        if response.status_code == 200:
            print("✅ Web interface is accessible")
            return True
        else:
            print(f"❌ Web interface returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to web interface")
        return False


def test_mcp_endpoints():
    """Test the MCP endpoints."""
    endpoints = {"schema": "http://localhost:7860/gradio_api/mcp/schema", "sse": "http://localhost:7860/gradio_api/mcp/sse"}

    all_ok = True
    for name, url in endpoints.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ MCP {name} endpoint is accessible")
            else:
                print(f"❌ MCP {name} endpoint returned status code: {response.status_code}")
                all_ok = False
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to MCP {name} endpoint")
            all_ok = False

    return all_ok


def test_sentiment_api():
    """Test the sentiment analysis API endpoint."""
    try:
        # Test with a positive text
        response = requests.post("http://localhost:7860/run/predict", json={"data": ["I love this course!"]})

        if response.status_code != 200:
            print(f"❌ API returned status code: {response.status_code}")
            return False

        result = response.json()
        if "data" not in result or not result["data"]:
            print("❌ API response missing data")
            return False

        sentiment = result["data"][0]
        required_keys = {"polarity", "subjectivity", "assessment"}
        if not all(key in sentiment for key in required_keys):
            print("❌ API response missing required keys")
            return False

        print("✅ API test successful")
        print(f"   Polarity: {sentiment['polarity']:.2f}")
        print(f"   Subjectivity: {sentiment['subjectivity']:.2f}")
        print(f"   Assessment: {sentiment['assessment']}")
        return True
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False


def main():
    """Run Task 2.2 verification checks."""
    print("🔍 Verifying Task 2.2: Server Testing and Validation")
    print("=" * 50)

    # Register cleanup handler
    atexit.register(stop_server)

    # Start server
    if not start_server():
        return 1

    try:
        # Test web interface
        print("\nTesting web interface...")
        if not test_web_interface():
            return 1

        # Test MCP endpoints
        print("\nTesting MCP endpoints...")
        if not test_mcp_endpoints():
            return 1

        # Test sentiment API
        print("\nTesting sentiment analysis API...")
        if not test_sentiment_api():
            return 1

        print("\n✨ Task 2.2 verification complete!")
        print("Server is running correctly and all endpoints are accessible.")
        return 0

    finally:
        # Stop server
        stop_server()


if __name__ == "__main__":
    sys.exit(main())
