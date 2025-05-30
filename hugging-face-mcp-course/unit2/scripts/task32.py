#!/usr/bin/env python3
"""
Task 3.2 Verification Script
Checks the Gradio MCP client implementation and functionality.
"""

import sys
import time
from pathlib import Path
import importlib.util
import subprocess
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

        # Verify required imports (gradio is imported as gr), CLient was not needed
        required_imports = ["gr"]
        for import_name in required_imports:
            if not hasattr(client_module, import_name):
                print(f"❌ Error: Required import '{import_name}' not found")
                return False

        # Start the sentiment analysis server in background
        print("Starting sentiment analysis server...")
        server_cmd = [
            "uv",
            "run",
            "python",
            str(project_root / "unit2" / "sentiment_analysis_mcp_server.py"),
        ]
        server_process = subprocess.Popen(
            server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Wait for server to start
        time.sleep(5)

        # Verify server is running
        try:
            response = requests.get("http://localhost:7860/gradio_api/mcp/schema")
            if response.status_code != 200:
                print("❌ Error: Server not responding correctly")
                server_process.terminate()
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to server")
            server_process.terminate()
            return False

        # Start the Gradio client
        print("Starting Gradio client...")
        client_cmd = ["uv", "run", "python", str(client_path)]
        client_process = subprocess.Popen(
            client_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Wait for client to start
        time.sleep(10)

        # Verify client is running
        try:
            response = requests.get("http://localhost:7861")
            if response.status_code != 200:
                print("❌ Error: Client not responding correctly")
                client_process.terminate()
                server_process.terminate()
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to client")
            client_process.terminate()
            server_process.terminate()
            return False

        print("✅ Gradio client implementation verified successfully")
        print("✅ Server and client are running")
        print("Note: Server running on http://localhost:7860")
        print("Note: Client running on http://localhost:7861")

        # Clean up processes
        client_process.terminate()
        server_process.terminate()
        return True

    except Exception as e:
        print(f"❌ Error: Unexpected error: {str(e)}")
        return False


if __name__ == "__main__":
    success = verify_gradio_client()
    sys.exit(0 if success else 1)
