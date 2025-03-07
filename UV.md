# UV Package Management System

This document explains the use of `uv` package manager for Python projects.
The original github repo can be found [here](https://github.com/astral-sh/uv).

## Benefits of Using `uv`

- **Speed**: `uv` is significantly faster than `pip` and `poetry` for resolving dependencies and installing packages, reducing setup time for projects.
- **Efficiency**: `uv` optimizes installation through parallel downloads and minimizing redundant operations.
- **Reliability**: `uv` provides consistent, reproducible environments with precise dependency resolution.
- **Compatibility**: `uv` maintains compatibility with existing Python packaging tools while offering improved performance.
- **Modern Features**: Includes advanced caching, lockfile support, and virtual environment management.

## Installation Steps - Once per system.

1. Ensure you have Python installed on your machine.

2. Install `uv` using pip:

    ```sh
    pip install uv
    ```

3. Install `Rust`

    Go to:
    https://www.rust-lang.org/tools/install
    and/or immediately download:
    https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe

    Follow the default installation instructions, and restart the command terminal/restart visual studio code.


## Creating a New Environment with `uv`

1. Create a new virtual environment:
    Use version 3.12 to prevent some incompatibilities with earlier or later versions.

    ```sh
    uv venv --python=3.12
    ```
   
   Or specify a location:
   
    ```sh
    uv venv /path/to/venv
    ```

2. Activate the environment:

    ```sh
    # On Windows
    /path/to/venv/Scripts/activate
    
    # On macOS/Linux
    source /path/to/venv/bin/activate
    ```

## Managing Dependencies

### Installing Packages

To install packages:

```sh
# Install a single package
uv pip install requests

# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv pip install -e .
```

3. Create or check the `pyproject.toml` file in the root directory of your project with the necessary configurations. Here is an example:

    ```toml
    [tool.uv]
    name = "your_project_name"
    version = "0.1.0"
    description = "A project using the uv package management system"
    authors = ["Your Name <your.email@example.com>"]
    license = {name = "MIT", file = "LICENSE"}

    [tool.uv.dependencies]
    ```

4. Add your project dependencies to the `pyproject.toml` file under `[tool.uv.dependencies]`. You can copy the dependencies from your existing `requirements.txt` file.

5. Install the dependencies using `uv`:

    ```sh
    uv install
    ```

## Installing and Removing Packages

### Installing Packages

To install a package using `uv`, use the following command:

```sh
uv add <package-name>
```

### Removing Packages

To remove a package using `uv`, use the following command:

```sh
uv remove <package-name>
```

## Detecting and Handling Compatibility Issues

### Detecting Compatibility Issues

`uv` provides mechanisms to detect compatibility issues during the installation process. If a compatibility issue is detected, `uv` will display an error message with details about the conflicting packages and versions.

### Handling Compatibility Issues

To handle compatibility issues, you can try the following steps:

1. **Update Packages**: Update the conflicting packages to their latest versions using the following command:

    ```sh
    uv update
    ```

2. **Override Compatibility**: If a security fix is required and it breaks compatibility specifications, you can override compatibility by using the following command:

    ```sh
    uv add <package-name> --force
    ```

3. **Check Documentation**: Refer to the documentation of the conflicting packages for any known compatibility issues and recommended solutions.

4. **Community Support**: Seek help from the `uv` community for any unresolved compatibility issues.

## Updating Packages

To update the packages to their recent versions while maintaining compatibility, use the following command:

```sh
uv update
```

## Overriding Compatibility

In case a security fix is required, even if it breaks compatibility specifications, you can override compatibility by using the following command:

```sh
uv add <package-name> --force
```
