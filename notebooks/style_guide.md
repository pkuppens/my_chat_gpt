# Style Guide

## Type Hinting
- Use type hints for function arguments and return values.
- Example:
  ```python
  def add(a: int, b: int) -> int:
      return a + b
  ```

## Docstrings
- Use docstrings to document functions, classes, and modules.
- Follow the Google style for docstrings.
- Example:
  ```python
  def add(a: int, b: int) -> int:
      """Add two integers.

      Args:
          a (int): The first integer.
          b (int): The second integer.

      Returns:
          int: The sum of the two integers.
      """
      return a + b
  ```

## Testability
- Write testable code by following the principles of modularity and separation of concerns.
- Use dependency injection to make code more testable.
- Write unit tests for all functions and classes.
- Example:
  ```python
  def add(a: int, b: int) -> int:
      return a + b

  def test_add():
      assert add(1, 2) == 3
  ```
