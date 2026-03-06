import enhanced_logging as elog


def test_human_output_basic(capsys):
    elog.configure_logging(elog.LogConfig(format="human"))
    log = elog.get_logger("test")
    log.info("startup", answer=42)

    out = capsys.readouterr().out
    assert "startup" in out
    assert "answer=42" in out or "42" in out


def test_human_output_uses_rendered_message(capsys):
    elog.configure_logging(elog.LogConfig(format="human"))
    log = elog.get_logger("test")
    log.info("startup", _fmt="Hello {user}", user="Ada")

    out = capsys.readouterr().out
    assert "Hello Ada" in out
    assert "startup" not in out or "event='startup'" not in out
