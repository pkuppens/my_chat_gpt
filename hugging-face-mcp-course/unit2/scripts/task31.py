#!/usr/bin/env python3
"""
Task 3.1 Verification Script
Checks the MCP configuration setup for the sentiment analysis server.
"""

import json
import sys
from pathlib import Path


def verify_mcp_config():
    """Verify the MCP configuration file exists and has correct format."""
    print("Verifying MCP configuration setup...")

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / "unit2" / "mcp-config.json"

    # Check if file exists
    if not config_path.exists():
        print("❌ Error: mcp-config.json not found")
        return False

    try:
        # Read and parse JSON
        with open(config_path, "r") as f:
            config = json.load(f)

        # Verify required fields
        if "servers" not in config:
            print("❌ Error: 'servers' field missing in config")
            return False

        if not isinstance(config["servers"], list):
            print("❌ Error: 'servers' must be a list")
            return False

        if len(config["servers"]) == 0:
            print("❌ Error: No servers defined in config")
            return False

        server = config["servers"][0]

        # Verify server configuration
        required_fields = ["name", "transport"]
        for field in required_fields:
            if field not in server:
                print(f"❌ Error: '{field}' field missing in server config")
                return False

        # Verify transport configuration
        transport = server["transport"]
        if "type" not in transport or transport["type"] != "sse":
            print("❌ Error: Invalid transport type")
            return False

        if "url" not in transport or not transport["url"].startswith("http"):
            print("❌ Error: Invalid transport URL")
            return False

        print("✅ MCP configuration verified successfully")
        print(f"  Server name: {server['name']}")
        print(f"  (not yet active) Transport URL: {transport['url']}")
        return True

    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in mcp-config.json")
        return False
    except Exception as e:
        print(f"❌ Error: Unexpected error: {str(e)}")
        return False


if __name__ == "__main__":
    success = verify_mcp_config()
    sys.exit(0 if success else 1)
