"""
Configure the Python path to include the project root directory.

This module ensures that the project root directory is in the Python path,
allowing imports from the my_chat_gpt_utils package to work correctly.
"""

import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)
