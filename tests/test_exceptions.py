import json

import enhanced_logging as elog


def fail():
    return "one" + 2


def test_json_exception_contains_traceback_once_in_json(capsys):
    elog.configure_logging(elog.LogConfig(format="json"))
    log = elog.get_logger("test")

    try:
        fail()
    except Exception:
        log.exception("Failure")

    out = capsys.readouterr().out.strip()

    try:
        data = json.loads(out)
    except json.JSONDecodeError as e:
        pytest.fail(f"output is not valid JSON: {e}\nCaptured output:\n{out}")

    assert data["event"] == "Failure"
    assert "TypeError" in data["exception"]
    assert "can only concatenate str" in data["exception"]


def test_human_exception_not_duplicated(capsys):
    elog.configure_logging(elog.LogConfig(format="human"))
    log = elog.get_logger("test")

    try:
        fail()
    except Exception:
        log.exception("Failure")

    out = capsys.readouterr().out

    assert "Failure" in out
    assert out.count("TypeError") == 1
    assert out.count("can only concatenate str") == 1


def test_json_exception_with_exc_info_true(capsys):
    elog.configure_logging(elog.LogConfig(format="json"))
    log = elog.get_logger("test")

    try:
        fail()
    except Exception:
        log.error("Failure", exc_info=True)

    data = json.loads(capsys.readouterr().out.strip())
    assert "exception" in data
    assert "TypeError" in data["exception"]
