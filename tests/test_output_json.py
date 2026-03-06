import json

import enhanced_logging as elog


def test_json_output_basic(capsys):
    elog.configure_logging(elog.LogConfig(format="json"))
    log = elog.get_logger("test", component="worker")
    log.info("startup", answer=42)

    out = capsys.readouterr().out.strip()
    data = json.loads(out)

    assert data["event"] == "startup"
    assert data["level"] == "info"
    assert data["component"] == "worker"
    assert "timestamp" in data


def test_json_output_fmt_goes_to_msg(capsys):
    elog.configure_logging(elog.LogConfig(format="json"))
    log = elog.get_logger("test")
    log.info("startup", _fmt="Hello {user}", user="Ada")

    data = json.loads(capsys.readouterr().out.strip())
    assert data["event"] == "startup"
    assert data["msg"] == "Hello Ada"
    assert "_fmt" not in data
    assert "_rendered" not in data


def test_json_output_binds_app_name(capsys):
    elog.configure_logging(elog.LogConfig(format="json", app_name="demo"))
    log = elog.get_logger("test")
    log.info("startup")

    data = json.loads(capsys.readouterr().out.strip())
    assert data["app"] == "demo"
