"""
Test suite for the logging configuration module.

This module provides comprehensive tests for validating the logger configuration,
including format verification, log level filtering, buffering control,
and context management functionality.
"""

import io
import logging
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple, Union
from unittest.mock import MagicMock, patch

import pytest

# Import the module to test - adjust the import path as needed
from my_chat_gpt_utils.logger import LoggerContext, configure_logger


class TestLogger:
    """Test suite for logger configuration and functionality."""

    def setup_method(self) -> None:
        """Set up test environment before each test method."""
        # Reset the root logger to avoid interference between tests
        root = logging.getLogger()
        root.handlers = []
        # Reset the module logger
        module_logger = logging.getLogger("my_chat_gpt_utils.logger")
        module_logger.handlers = []
        module_logger.setLevel(logging.INFO)  # Reset to default level
        # Store original environment for restoration
        self.original_env = os.environ.copy()

    def teardown_method(self) -> None:
        """Clean up after each test method."""
        # Restore the original environment
        os.environ.clear()
        os.environ.update(self.original_env)

    def capture_log_output(self, logger: logging.Logger) -> Tuple[io.StringIO, logging.Handler]:
        """
        Capture log output for testing.

        Args:
            logger: The logger instance to capture output from

        Returns:
            Tuple containing the StringIO object capturing the output and the handler
        """
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        if logger.handlers and hasattr(logger.handlers[0], "formatter"):
            formatter = logger.handlers[0].formatter
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return log_capture, handler

    def test_logger_name(self) -> None:
        """Test that the logger name is correctly set."""
        test_name = "test_logger_name"
        logger = configure_logger(name=test_name)
        assert logger.name == test_name

    def test_default_level(self) -> None:
        """Test that the default logging level is INFO."""
        logger = configure_logger()
        assert logger.level == logging.INFO

    def test_custom_level(self) -> None:
        """Test that a custom logging level is correctly applied."""
        logger = configure_logger(level=logging.DEBUG)
        assert logger.level == logging.DEBUG

        # Test string-based level
        logger = configure_logger(level="ERROR")
        assert logger.level == logging.ERROR

    @pytest.mark.parametrize(
        "log_level,message_level,should_log",
        [
            (logging.INFO, logging.DEBUG, False),
            (logging.INFO, logging.INFO, True),
            (logging.INFO, logging.WARNING, True),
            (logging.DEBUG, logging.DEBUG, True),
            (logging.WARNING, logging.INFO, False),
        ],
    )
    def test_level_filtering(self, log_level: int, message_level: int, should_log: bool) -> None:
        """
        Test that messages are filtered based on the configured log level.

        Args:
            log_level: The level to configure the logger with
            message_level: The level to log a message at
            should_log: Whether the message should appear in the log
        """
        logger = configure_logger(level=log_level)
        log_capture, handler = self.capture_log_output(logger)

        # Log a message at the specified level
        log_method = getattr(logger, logging.getLevelName(message_level).lower())
        log_method("Test message")

        # Check if the message was logged
        log_output = log_capture.getvalue()
        logger.removeHandler(handler)

        if should_log:
            assert "Test message" in log_output
        else:
            assert "Test message" not in log_output

    def test_file_info_inclusion(self) -> None:
        """Test that filename and line number are included in log messages when requested."""
        logger = configure_logger(include_file_info=True)
        log_capture, handler = self.capture_log_output(logger)

        logger.info("Test message with file info")
        log_output = log_capture.getvalue()
        logger.removeHandler(handler)

        # Check for filename and line number pattern
        # The pattern should match something like [test_logger.py:123]
        filename_pattern = r"\[([^:]+):(\d+)\]"
        assert re.search(filename_pattern, log_output) is not None

    def test_no_file_info(self) -> None:
        """Test that filename and line number are excluded when not requested."""
        logger = configure_logger(include_file_info=False)
        log_capture, handler = self.capture_log_output(logger)

        logger.info("Test message without file info")
        log_output = log_capture.getvalue()
        logger.removeHandler(handler)

        # The standard bracket pattern for file info should not be present
        filename_pattern = r"\[[^:]+:\d+\]"
        assert re.search(filename_pattern, log_output) is None

    def test_custom_format(self) -> None:
        """Test that a custom format string is correctly applied."""
        custom_format = "%(levelname)s - CUSTOM - %(message)s"
        logger = configure_logger(format_string=custom_format)
        log_capture, handler = self.capture_log_output(logger)

        logger.warning("Custom format test")
        log_output = log_capture.getvalue()
        logger.removeHandler(handler)

        assert "CUSTOM" in log_output

    @patch("sys.stdout")
    def test_force_unbuffered(self, mock_stdout: MagicMock) -> None:
        """Test that stdout is configured to be unbuffered when requested."""
        # Mock reconfigure method to check if it's called
        mock_stdout.reconfigure = MagicMock()

        configure_logger(force_unbuffered=True)

        # Check if reconfigure was called to make stdout unbuffered
        mock_stdout.reconfigure.assert_called_once_with(line_buffering=True)

    @patch.dict(os.environ, {"PYTHONUNBUFFERED": "1"})
    @patch("sys.stdout")
    def test_env_unbuffered(self, mock_stdout: MagicMock) -> None:
        """Test that stdout is configured based on PYTHONUNBUFFERED environment variable."""
        # Mock reconfigure method
        mock_stdout.reconfigure = MagicMock()

        configure_logger()

        # Check if reconfigure was called due to environment variable
        mock_stdout.reconfigure.assert_called_once_with(line_buffering=True)

    @patch.dict(os.environ, {"LOG_LEVEL": "ERROR"})
    def test_env_log_level(self) -> None:
        """Test that the log level is set from the LOG_LEVEL environment variable."""
        logger = configure_logger()
        assert logger.level == logging.ERROR

    def test_file_handler(self) -> None:
        """Test that a file handler is correctly added when requested."""
        test_log_file = "test_application.log"
        logger = configure_logger(add_file_handler=True, log_file_path=test_log_file)

        # Check if we have a FileHandler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) == 1
        assert file_handlers[0].baseFilename.endswith(test_log_file)

        # Clean up the test log file
        try:
            os.remove(test_log_file)
        except OSError:
            pass  # Ignore if file doesn't exist

    def test_logger_context(self) -> None:
        """Test that LoggerContext temporarily changes the logging level."""
        logger = configure_logger(level=logging.WARNING)
        assert logger.level == logging.WARNING

        # Capture before entering context
        before_capture, before_handler = self.capture_log_output(logger)
        logger.info("Before context - should not log")

        # Within context at DEBUG level
        with LoggerContext(logger, logging.DEBUG):
            assert logger.level == logging.DEBUG

            # Capture within context
            in_context_capture, in_context_handler = self.capture_log_output(logger)
            logger.debug("In context - should log")
            logger.info("In context info - should log")

            # Check logs within context
            in_context_output = in_context_capture.getvalue()
            logger.removeHandler(in_context_handler)
            assert "In context - should log" in in_context_output
            assert "In context info - should log" in in_context_output

        # After exiting context
        assert logger.level == logging.WARNING
        logger.info("After context - should not log")

        # Check before/after logs
        before_output = before_capture.getvalue()
        logger.removeHandler(before_handler)
        assert "Before context - should not log" not in before_output
        assert "After context - should not log" not in before_output

    def test_multiple_handlers_avoided(self) -> None:
        """Test that multiple handlers are not added when configuring the same logger twice."""
        logger_name = "test_multiple_handlers"
        logger1 = configure_logger(name=logger_name)
        initial_handler_count = len(logger1.handlers)

        # Configure the same logger again
        logger2 = configure_logger(name=logger_name)

        # Check that handlers weren't duplicated
        assert logger1 is logger2  # Same logger instance
        assert len(logger2.handlers) == initial_handler_count

    def test_demo_script(self) -> None:
        """Test an integrated demonstration of the logger functionality."""
        # This test doubles as an example usage script that would demonstrate the logger
        # capabilities when run directly

        def run_demo() -> None:
            """Run a demonstration of logger functionality."""
            # Configure a demo logger
            demo_logger = configure_logger(name="demo_logger", level="INFO", include_file_info=True)

            # Show normal logging
            demo_logger.info("This is an INFO message with file info")
            demo_logger.warning("This is a WARNING message")
            demo_logger.error("This is an ERROR message")

            # DEBUG shouldn't appear at INFO level
            demo_logger.debug("This DEBUG message should NOT appear")

            # Use context manager to temporarily change log level
            print("\n--- Changing log level to DEBUG within context ---")
            with LoggerContext(demo_logger, logging.DEBUG):
                demo_logger.debug("This DEBUG message SHOULD appear")
                demo_logger.info("This INFO message SHOULD appear")

            print("\n--- Back to INFO level outside context ---")
            demo_logger.debug("This DEBUG message should NOT appear again")
            demo_logger.info("This INFO message SHOULD appear again")

            # Show custom logger with different settings
            print("\n--- Custom logger without file info ---")
            custom_logger = configure_logger(name="custom_logger", level="WARNING", include_file_info=False)

            custom_logger.info("This INFO message should NOT appear")
            custom_logger.warning("This WARNING message should appear without file info")

        # Capture stdout and log output for verification
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Add temporary handler to capture log output
            root_logger = logging.getLogger()
            root_logger.addHandler(handler)
            try:
                run_demo()
                output = mock_stdout.getvalue()
                log_output = log_capture.getvalue()
            finally:
                root_logger.removeHandler(handler)

        # Verify key elements in both stdout and log output
        combined_output = output + log_output
        assert "This is an INFO message with file info" in combined_output
        assert "This is a WARNING message" in combined_output
        assert "This is an ERROR message" in combined_output
        assert "This DEBUG message should NOT appear" not in combined_output
        assert "This DEBUG message SHOULD appear" in combined_output
        assert "This INFO message SHOULD appear" in combined_output
        assert "This DEBUG message should NOT appear again" not in combined_output
        assert "This INFO message SHOULD appear again" in combined_output
        assert "This WARNING message should appear without file info" in combined_output


if __name__ == "__main__":
    """
    When run directly, this script demonstrates the logger functionality.

    This serves as both a test and an example of how to use the logger module.
    """
    # Configure logger for demonstration
    from my_chat_gpt_utils.logger import LoggerContext, configure_logger

    # Create a logger that shows file info
    logger = configure_logger(name="demo", level="INFO", include_file_info=True)

    # Show basic logging functionality
    print("=== Basic logging demonstration ===")
    logger.info("This is an information message with file location")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.debug("This DEBUG message shouldn't appear at INFO level")

    # Demonstrate context manager
    print("\n=== LoggerContext demonstration ===")
    print("Temporarily changing to DEBUG level...")
    with LoggerContext(logger, "DEBUG"):
        logger.debug("This DEBUG message should now appear")
        logger.info("This INFO message should still appear")

    print("\nBack to original level...")
    logger.debug("This DEBUG message shouldn't appear again")
    logger.info("This INFO message should still appear")

    # Show file handler functionality
    print("\n=== File logging demonstration ===")
    file_logger = configure_logger(name="file_demo", level="INFO", add_file_handler=True, log_file_path="demo.log")
    file_logger.info("This message goes to both console and file")
    print(f"Check demo.log for file output")

    # Run some tests programmatically
    print("\n=== Running basic verification tests ===")
    test_instance = TestLogger()
    test_instance.setup_method()
    test_instance.test_logger_name()
    test_instance.test_level_filtering(logging.INFO, logging.DEBUG, False)
    test_instance.test_level_filtering(logging.INFO, logging.WARNING, True)
    test_instance.test_file_info_inclusion()
    test_instance.teardown_method()
    print("Basic verification tests completed successfully!")
