#!/usr/bin/env python3
"""
Script to test and verify Python package dependencies.

This script checks if all required packages from requirements files can be imported
and installed. It provides detailed feedback about any missing or problematic dependencies.
"""

import importlib
import subprocess
import sys
from typing import List, Tuple


def get_required_packages() -> List[str]:
    """
    Get all required packages from requirements files.

    Reads both the main requirements file and any included requirements files
    (specified with -r flag) to build a complete list of required packages.

    Returns
    -------
        List[str]: List of package names without version constraints.

    """
    packages = []

    # Read requirements.github.workflow
    with open('requirements.github.workflow', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith('-r'):
                    # Handle requirements file inclusion
                    req_file = line[3:].strip()
                    with open(req_file, 'r') as subf:
                        for subline in subf:
                            subline = subline.strip()
                            if subline and not subline.startswith('#'):
                                packages.append(subline.split('==')[0])
                else:
                    packages.append(line.split('==')[0])

    return packages


def check_package_imports(packages: List[str]) -> List[Tuple[str, bool, str]]:
    """
    Check if each package can be imported.

    Attempts to import each package and reports success or failure.

    Args:
    ----
        packages (List[str]): List of package names to check.

    Returns:
    -------
        List[Tuple[str, bool, str]]: List of tuples containing (package_name, success, error_message).

    """
    results = []
    for package in packages:
        try:
            importlib.import_module(package)
            results.append((package, True, ""))
        except ImportError as e:
            results.append((package, False, str(e)))
    return results


def verify_pip_install(packages: List[str]) -> List[Tuple[str, bool, str]]:
    """
    Verify packages can be installed via pip.

    Attempts to install each package using pip and reports success or failure.

    Args:
    ----
        packages (List[str]): List of package names to verify.

    Returns:
    -------
        List[Tuple[str, bool, str]]: List of tuples containing (package_name, success, error_message).

    """
    results = []
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package],
                         capture_output=True, text=True, check=True)
            results.append((package, True, ""))
        except subprocess.CalledProcessError as e:
            results.append((package, False, e.stderr))
    return results


def main() -> None:
    """
    Run the dependency verification process.

    This function orchestrates the entire dependency checking process:
    1. Gets the list of required packages
    2. Checks if each package can be imported
    3. Verifies each package can be installed via pip
    4. Reports the overall status and any failures
    """
    print("Testing dependencies...")

    # Get required packages
    packages = get_required_packages()
    print(f"\nFound {len(packages)} required packages:")
    for package in packages:
        print(f"- {package}")

    # Check imports
    print("\nChecking package imports...")
    import_results = check_package_imports(packages)
    for package, success, error in import_results:
        if success:
            print(f"✓ {package} imports successfully")
        else:
            print(f"✗ {package} import failed: {error}")

    # Verify pip installation
    print("\nVerifying pip installation...")
    pip_results = verify_pip_install(packages)
    for package, success, error in pip_results:
        if success:
            print(f"✓ {package} can be installed via pip")
        else:
            print(f"✗ {package} pip installation failed: {error}")

    # Report overall status
    import_failures = [p for p, s, _ in import_results if not s]
    pip_failures = [p for p, s, _ in pip_results if not s]

    if import_failures or pip_failures:
        print("\n❌ Dependency check failed!")
        if import_failures:
            print(f"Failed imports: {', '.join(import_failures)}")
        if pip_failures:
            print(f"Failed pip installations: {', '.join(pip_failures)}")
        sys.exit(1)
    else:
        print("\n✓ All dependencies verified successfully!")


if __name__ == "__main__":
    main()
