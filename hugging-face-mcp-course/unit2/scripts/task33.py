#!/usr/bin/env python3
"""
Task 3.3 Verification Script
Checks the SmolAgents MCP client implementation and functionality.
"""

import importlib.util
import subprocess
import sys
import time
from pathlib import Path

import requests


def verify_smolagents_client():
    """Verify the SmolAgents MCP client implementation and functionality."""
    print("Verifying SmolAgents client implementation...")

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    client_path = project_root / "unit2" / "smolagents_client.py"

    # Check if file exists
    if not client_path.exists():
        print("❌ Error: smolagents_client.py not found")
        return False

    try:
        # Import the client module
        spec = importlib.util.spec_from_file_location("smolagents_client", client_path)
        client_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(client_module)

        # Verify required imports
        required_imports = ["CodeAgent", "MCPTool"]
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
        server_process = subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

        # Start the SmolAgents client
        print("Starting SmolAgents client...")
        client_cmd = ["uv", "run", "python", str(client_path)]
        client_process = subprocess.Popen(client_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for client to start and process a test query
        time.sleep(10)

        # Check if client process is still running
        if client_process.poll() is not None:
            print("❌ Error: Client process terminated unexpectedly")
            stdout, stderr = client_process.communicate()
            print("Client stdout:", stdout.decode())
            print("Client stderr:", stderr.decode())
            server_process.terminate()
            return False

        print("✅ SmolAgents client implementation verified successfully")
        print("✅ Server and client are running")
        print("Note: Server running on http://localhost:7860")
        print("Note: Client is running and processing queries")

        # Clean up processes
        client_process.terminate()
        server_process.terminate()
        return True

    except Exception as e:
        print(f"❌ Error: Unexpected error: {str(e)}")
        return False


if __name__ == "__main__":
    success = verify_smolagents_client()
    sys.exit(0 if success else 1)
