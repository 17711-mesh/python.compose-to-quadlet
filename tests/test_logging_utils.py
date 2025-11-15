
import logging
from compose_to_quadlet.logging_utils import configure_logging

def test_configure_logging_sets_level():
    """Tests that the root logger level is set correctly."""
    # Test DEBUG level
    configure_logging("DEBUG")
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG

    # Test INFO level
    configure_logging("INFO")
    assert logging.getLogger().getEffectiveLevel() == logging.INFO

    # Test WARNING level
    configure_logging("WARNING")
    assert logging.getLogger().getEffectiveLevel() == logging.WARNING
