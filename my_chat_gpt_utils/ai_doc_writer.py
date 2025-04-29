#!/usr/bin/env python3
"""Module for AI-powered document writing and content generation."""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from my_chat_gpt_utils.openai_utils import get_openai_client
from my_chat_gpt_utils.prompts import get_documentation_prompt


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """
    Read and parse JSON data from a file.

    Single JSON objects are converted to a list containing one item.
    On failure or empty file, returns an empty list.

    Args:
    ----
        file_path: Path to the JSON file to read

    Returns:
    -------
        List of dictionaries parsed from JSON

    Raises:
    ------
        FileNotFoundError: If the specified file does not exist

    """
    try:
        # Check if file exists
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' not found")
            return []

        # Check if file is empty
        if os.path.getsize(file_path) == 0:
            print(f"Warning: File '{file_path}' is empty")
            return []

        with open(file_path, encoding="utf-8") as file:
            json_data = json.load(file)

            # Convert single item to list if it's not already a list
            if not isinstance(json_data, list):
                return [json_data]
            return json_data

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from '{file_path}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error reading '{file_path}': {e}")
        return []


def write_content_to_file(content: str, file_path: str, current_directory: str) -> None:
    """Write content to a file, creating directories if needed."""
    full_path = os.path.join(current_directory, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Wrote content to {file_path}")


def process_items(items: list[dict[str, Any]], current_directory: str) -> None:
    """Process a list of items and generate documentation for each."""
    client = get_openai_client()
    for item in items:
        prompt = get_documentation_prompt(item)
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        write_content_to_file(content, item["file_path"], current_directory)


def main(file_path: str | None = None, current_directory: Path | None = None) -> int:
    """
    Process JSON input and generate documentation files.

    Args:
    ----
        file_path: Path to the input JSON file. If None, reads from command line.
        current_directory: Base directory for output files. If None, uses current directory.

    Returns:
    -------
        int: Exit code (0 for success, 1 for failure).

    """
    # If no file path provided, get from command line args
    if file_path is None:
        if len(sys.argv) < 2:
            print(f"Usage: python {sys.argv[0]} <json_file>")
            return 1
        file_path = sys.argv[1]

    # Read JSON items
    items = read_json_file(file_path)

    if not items:
        print("No items to process")
        return 1

    # Process items
    process_items(items, current_directory)

    # Print summary
    print(f"\nProcessing complete: {len(items)} items successfully processed")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
