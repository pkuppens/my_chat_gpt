import pytest

def pytest_configure(config):
    """Configure pytest for knight-bishop solver tests."""
    # Add knight marker if not already present
    config.addinivalue_line(
        "markers",
        "knight: marks tests related to the knight-bishop solver"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test items to apply knight-specific settings."""
    # Only run tests in the vibe_coding_samples directory
    items[:] = [item for item in items if "vibe_coding_samples" in str(item.fspath)]

@pytest.fixture(autouse=True)
def _configure_logging():
    """Configure logging for knight-bishop solver tests."""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
        datefmt="%Y-%m-%d %H:%M:%S"
    ) 