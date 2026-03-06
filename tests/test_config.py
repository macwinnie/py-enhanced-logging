import logging

import enhanced_logging as elog


def test_get_logger_autoconfigures():
    log = elog.get_logger("test")
    assert log is not None
    assert elog._CONFIG is not None


def test_keep_existing_handlers_false_replaces_handlers():
    root = logging.getLogger()
    root.addHandler(logging.NullHandler())

    elog.configure_logging(elog.LogConfig(keep_existing_handlers=False))

    assert not any(isinstance(h, logging.NullHandler) for h in root.handlers)


def test_keep_existing_handlers_true_keeps_handlers():
    root = logging.getLogger()
    h = logging.NullHandler()
    root.addHandler(h)

    elog.configure_logging(elog.LogConfig(keep_existing_handlers=True))

    assert h in root.handlers
