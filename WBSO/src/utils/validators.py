def is_valid_email(email: str) -> bool:
    """Checks if the given string is a valid email address (basic check)."""
    if "@" in email and "." in email.split("@")[-1]:
        return True
    return False


def is_non_empty_string(value: str) -> bool:
    """Checks if the string is not None and not empty after stripping whitespace."""
    return value is not None and bool(value.strip())
