"""
Module to set up Python path for local development.

This module should be imported before any other local imports to ensure
the repository root is in the Python path.
"""

import sys
from pathlib import Path


def setup_path() -> None:
    """Add repository root to Python path if not already present."""
    repo_root = str(Path(__file__).resolve().parents[1])
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


# Set up path when module is imported
setup_path()
