import json

import enhanced_logging as elog


def test_log_context_binds_fields_within_block(capsys):
    elog.configure_logging(elog.LogConfig(format="json"))
    log = elog.get_logger("test")

    with elog.log_context(request_id="req-1", user_id=42):
        log.info("inside")

    data = json.loads(capsys.readouterr().out.strip())
    assert data["request_id"] == "req-1"
    assert data["user_id"] == 42


def test_log_context_unbinds_after_block(capsys):
    elog.configure_logging(elog.LogConfig(format="json"))
    log = elog.get_logger("test")

    with elog.log_context(request_id="req-1"):
        log.info("inside")
    log.info("outside")

    lines = [line for line in capsys.readouterr().out.splitlines() if line.strip()]
    first = json.loads(lines[0])
    second = json.loads(lines[1])

    assert first["request_id"] == "req-1"
    assert "request_id" not in second
