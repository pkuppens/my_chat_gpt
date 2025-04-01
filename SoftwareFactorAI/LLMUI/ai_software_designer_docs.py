"""
Generate documentation for AI software design components.

This module processes JSON input files containing software design information
and generates corresponding documentation files using AI assistance.
"""

import sys
from pathlib import Path
from typing import Optional

from my_chat_gpt_utils.ai_doc_writer import main as ai_doc_writer_main


def main(file_path: Optional[str] = None) -> int:
    """
    Process JSON input and generate documentation files.

    Args:
    ----
        file_path: Path to the JSON file (optional, defaults to command line arg)

    Returns:
    -------
        int: Exit code (0 for success, 1 for error)

    """
    current_directory = Path(__file__).resolve().parent

    if file_path is None:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            file_path = current_directory / "ai_software_designer_docs.json"
    return ai_doc_writer_main(file_path, current_directory)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
