import logging

import pytest
import structlog

import enhanced_logging


@pytest.fixture(autouse=True)
def reset_logging_state():
    root = logging.getLogger()
    old_handlers = root.handlers[:]
    old_level = root.level

    root.handlers.clear()
    root.setLevel(logging.NOTSET)

    enhanced_logging._CONFIG = None
    structlog.reset_defaults()

    yield

    root.handlers.clear()
    root.handlers.extend(old_handlers)
    root.setLevel(old_level)

    enhanced_logging._CONFIG = None
    structlog.reset_defaults()
