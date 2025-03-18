#!/usr/bin/env python3
"""
AI Generated Document Writer

This module reads JSON data from a file, where the JSON data contains a list of generated documents.
It writes their content to individual files based on the specified file names in the JSON data.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read and parse JSON data from a file.

    Single JSON objects are converted to a list containing one item.
    On failure or empty file, returns an empty list.

    Args:
        file_path: Path to the JSON file to read

    Returns:
        List of dictionaries parsed from JSON

    Raises:
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

        with open(file_path, "r", encoding="utf-8") as file:
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


def write_content_to_file(item: Dict[str, Any], current_directory: Path) -> bool:
    """
    Extract content from a JSON item and write it to a file with the name specified in the item.

    Args:
        item: Dictionary containing 'name' and 'content' keys

    Returns:
        True if writing was successful, False otherwise

    Raises:
        KeyError: If the required keys are missing from the item
    """
    try:
        # Validate required keys exist
        if "name" not in item or "content" not in item:
            print(f"Error: Missing required keys in item: {item}")
            return False

        file_name: str = current_directory / item["name"]
        content: str = item["content"]

        # Write content to file
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Successfully wrote content to '{file_name}'")
        return True

    except IOError as e:
        print(f"Error writing to file '{item.get('name', 'unknown')}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error processing item: {e}")
        return False


def process_items(items: List[Dict[str, Any]], current_directory: Path) -> int:
    """
    Process a list of items by writing their content to files.

    Args:
        items: List of dictionaries containing 'name' and 'content' keys

    Returns:
        Number of items successfully processed
    """
    successful_writes: int = 0

    for i, item in enumerate(items):
        print(f"Processing item {i+1}/{len(items)}...")

        if write_content_to_file(item, current_directory):
            successful_writes += 1

    return successful_writes


def main(file_path: Optional[str] = None, current_directory: Optional[Path] = None) -> int:
    """
    Main function to read JSON, process items, and write content to files.

    Args:
        file_path: Path to the JSON file (optional, defaults to command line arg)

    Returns:
        Exit code (0 for success, 1 for error)
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
    successful_count = process_items(items, current_directory)

    # Print summary
    print(f"\nProcessing complete: {successful_count}/{len(items)} items successfully processed")

    return 0 if successful_count == len(items) else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
