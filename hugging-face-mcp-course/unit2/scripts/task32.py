#!/usr/bin/env python3
"""
Task 3.2 Verification Script
Checks the Gradio MCP client implementation and functionality.

IMPORTANT: Before running this script, you need to:
1. Start the sentiment analysis server in a separate terminal:
   python unit2/sentiment_analysis_mcp_server.py
2. Start the Gradio client in another separate terminal:
   python unit2/mcp_gradio_client.py

The script will then verify that both services are running correctly.
"""

import importlib.util
import sys
from pathlib import Path

import requests


def verify_gradio_client():
    """Verify the Gradio MCP client implementation and functionality."""
    print("Verifying Gradio MCP client implementation...")

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    client_path = project_root / "unit2" / "mcp_gradio_client.py"

    # Check if file exists
    if not client_path.exists():
        print("❌ Error: mcp_gradio_client.py not found")
        return False

    try:
        # Import the client module
        spec = importlib.util.spec_from_file_location("mcp_gradio_client", client_path)
        client_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(client_module)

        # Verify required imports (gradio is imported as gr)
        required_imports = ["gr"]
        for import_name in required_imports:
            if not hasattr(client_module, import_name):
                print(f"❌ Error: Required import '{import_name}' not found")
                return False

        # Verify server is running
        print("Checking if server is running...")
        try:
            response = requests.get("http://localhost:7860/gradio_api/mcp/schema")
            if response.status_code != 200:
                print("❌ Error: Server not responding correctly")
                print("To fix this:")
                print("1. Open a new terminal window")
                print("2. Navigate to the project root directory")
                print("3. Run: python unit2/sentiment_analysis_mcp_server.py")
                print(
                    "4. Wait for the server to start (you should see a message about port 7860)"
                )
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to server")
            print("To fix this:")
            print("1. Open a new terminal window")
            print("2. Navigate to the project root directory")
            print("3. Run: python unit2/sentiment_analysis_mcp_server.py")
            print(
                "4. Wait for the server to start (you should see a message about port 7860)"
            )
            return False

        # Verify client is running
        print("Checking if client is running...")
        try:
            response = requests.get("http://localhost:7861")
            if response.status_code != 200:
                print("❌ Error: Client not responding correctly")
                print("To fix this:")
                print("1. Open a new terminal window")
                print("2. Navigate to the project root directory")
                print("3. Run: python unit2/mcp_gradio_client.py")
                print(
                    "4. Wait for the client to start (you should see a message about port 7861)"
                )
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to client")
            print("To fix this:")
            print("1. Open a new terminal window")
            print("2. Navigate to the project root directory")
            print("3. Run: python unit2/mcp_gradio_client.py")
            print(
                "4. Wait for the client to start (you should see a message about port 7861)"
            )
            return False

        print("✅ Gradio client implementation verified successfully")
        print("✅ Server and client are running")
        print("Note: Server running on http://localhost:7860")
        print("Note: Client running on http://localhost:7861")
        return True

    except Exception as e:
        print(f"❌ Error: Unexpected error: {str(e)}")
        return False


if __name__ == "__main__":
    success = verify_gradio_client()
    sys.exit(0 if success else 1)
