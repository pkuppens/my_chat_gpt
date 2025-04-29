"""
setup.py is used to install the package.

It is also used to define the dependencies for the package.

The dependencies are defined in the requirements-base.txt file.
Additional dev dependencies are defined in the requirements-dev.txt file.
Additional test dependencies are defined in the requirements-test.txt file.
"""

import os
from typing import List, Set

from setuptools import find_packages, setup

# Semantic Versioning Strategy (MAJOR.MINOR.PATCH):
#
# Current Development Phase (0.x.x):
# - Keep version at 0.1.0 during initial development
# - Increment MINOR (0.2.0, 0.3.0) for significant feature additions
# - Use PATCH (0.1.1) only for critical bug fixes
# - Stay pre-1.0 until API is stable and core features are complete
#
# Release 1.0.0 when:
# - API is stable and well-documented
# - Core features are complete
# - Ready to maintain backward compatibility
#
# Post 1.0.0:
# - MAJOR: Breaking changes (2.0.0) - Incompatible API changes
# - MINOR: Features (1.1.0) - Backwards-compatible functionality
# - PATCH: Fixes (1.0.1) - Backwards-compatible bug fixes
#
# Example timeline:
# 0.1.0 -> Initial development
# 0.2.0 -> New features added
# 0.2.1 -> Critical bug fix
# 1.0.0 -> First stable release
# 1.1.0 -> New feature
# 1.1.1 -> Bug fix
# 2.0.0 -> Breaking change


def read_requirements(filename: str, processed_files: Set[str] = None) -> List[str]:
    """
    Read requirements from a file and handle -r references safely.

    Args:
    ----
        filename: The requirements file to process
        processed_files: Set of already processed files to prevent infinite recursion

    Returns:
    -------
        List of requirements with duplicates removed

    Note:
    ----
        - Prevents infinite recursion by tracking processed files
        - Handles relative paths correctly
        - Removes duplicates while preserving order
        - setuptools will handle merging of version specifiers

    """
    if processed_files is None:
        processed_files = set()

    # Convert to absolute path for consistent tracking
    abs_filename = os.path.abspath(filename)
    if abs_filename in processed_files:
        return []  # Skip if already processed

    processed_files.add(abs_filename)
    requirements = []

    base_dir = os.path.dirname(abs_filename)

    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("-r "):
                    # Handle requirement file references
                    req_file = line.split(" ")[1]
                    # Convert relative path to absolute
                    req_file_path = os.path.join(base_dir, req_file)
                    # Recursively process the referenced file
                    nested_reqs = read_requirements(req_file_path, processed_files)
                    requirements.extend(nested_reqs)
                else:
                    requirements.append(line)

    except FileNotFoundError:
        print(f"Warning: Requirements file not found: {filename}")
        return []

    # Remove duplicates while preserving order
    seen = set()
    return [req for req in requirements if not (req in seen or seen.add(req))]


setup(
    name="my_chat_gpt",
    version="0.1.0",  # Pre-1.0 development version
    packages=find_packages(),
    install_requires=read_requirements("requirements-base.txt"),
    extras_require={
        "dev": [
            req
            for req in read_requirements("requirements-dev.txt")
            if req not in read_requirements("requirements-base.txt")
        ],
        # dev includes test, otherwise, create a new test extras_require with requirements-test.txt:
        "test": [
            req
            for req in read_requirements("requirements-test.txt")
            if req not in read_requirements("requirements-dev.txt")
        ],
    },
    python_requires=">=3.11",
    description="A ChatGPT/LLM Agent Building Utility Package",
    author="Pieter Kuppens",
    author_email="pieter.kuppens@gmail.com",
    url="https://github.com/pkuppens/my_chat_gpt",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
