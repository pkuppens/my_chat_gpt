#!/usr/bin/env python3
"""
Script to test and verify Python package dependencies.

This script checks if all required packages from requirements files can be imported.
It assumes packages are already installed in the environment and only verifies import capability.
"""

import importlib
import sys


def get_import_mapping() -> dict[str, str]:
    """
    Get mapping between package names and their import names.

    Returns
    -------
        Dict[str, str]: Dictionary mapping package names to their import names.

    """
    return {
        "scikit-learn": "sklearn",
        "PyYAML": "yaml",
        "PyGithub": "github",
    }


def get_required_packages() -> list[str]:
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
    with open("requirements.github.workflow") as f:
        for _line in f:
            line = _line.strip()
            if line and not line.startswith("#"):
                if line.startswith("-r"):
                    # Handle requirements file inclusion
                    req_file = line[3:].strip()
                    with open(req_file) as subf:
                        for _subline in subf:
                            subline = _subline.strip()
                            if subline and not subline.startswith("#"):
                                # Split on any of the common version specifiers
                                package = (
                                    subline.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].split("!=")[0]
                                )
                                packages.append(package)
                else:
                    # Split on any of the common version specifiers
                    package = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].split("!=")[0]
                    packages.append(package)

    return packages


def check_package_imports(packages: list[str]) -> list[tuple[str, bool, str]]:
    """
    Check if each package can be imported.

    Attempts to import each package and reports success or failure.
    Assumes packages are already installed in the environment.

    Args:
    ----
        packages (List[str]): List of package names to check.

    Returns:
    -------
        List[Tuple[str, bool, str]]: List of tuples containing (package_name, success, error_message).

    """
    import_mapping = get_import_mapping()
    results = []

    for package in packages:
        try:
            # Use the mapped import name if it exists, otherwise use the package name
            import_name = import_mapping.get(package, package)
            importlib.import_module(import_name)
            results.append((package, True, ""))
        except ImportError as e:
            results.append((package, False, str(e)))
    return results


def main() -> None:
    """
    Run the dependency verification process.

    This function orchestrates the entire dependency checking process:
    1. Gets the list of required packages
    2. Checks if each package can be imported
    3. Reports the overall status and any failures
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

    # Report overall status
    import_failures = [p for p, s, _ in import_results if not s]

    if import_failures:
        print("\n❌ Dependency check failed!")
        print(f"Failed imports: {', '.join(import_failures)}")
        print("\nNote: Make sure all required packages are installed in the environment.")
        sys.exit(1)
    else:
        print("\n✓ All dependencies verified successfully!")


if __name__ == "__main__":
    main()
