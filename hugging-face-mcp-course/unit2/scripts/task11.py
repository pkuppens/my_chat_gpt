#!/usr/bin/env python3
"""
Verification script for Task 1.1: Project Structure Setup
Checks dependencies and project structure.
"""

import importlib
import sys
from pathlib import Path


def check_package(package_name: str) -> bool:
    """Check if a package is installed and importable."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False


def main():
    """Run Task 1.1 verification checks."""
    print("🔍 Verifying Task 1.1: Project Structure Setup")
    print("=" * 50)

    # Check project structure
    project_dir = Path("hugging-face-mcp-course/unit2")
    if not project_dir.exists():
        print("❌ Project directory not found at:", project_dir)
        print("   Please run: mkdir -p hugging-face-mcp-course/unit2")
        return 1

    # Check required packages
    required_packages = {
        "gradio": "Gradio with MCP support",
        "textblob": "TextBlob for sentiment analysis",
        "smolagents": "Hugging Face agents framework",
    }

    all_packages_ok = True
    for package, description in required_packages.items():
        if check_package(package):
            print(f"✅ {package} installed ({description})")
        else:
            print(f"❌ {package} not found ({description})")
            print(f"   Please run: uv add {package}")
            all_packages_ok = False

    if not all_packages_ok:
        print("\n⚠️  Some packages are missing. Please install them using UV.")
        return 1

    print("\n✨ Task 1.1 verification complete!")
    print("All dependencies are installed and project structure is correct.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
