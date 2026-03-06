import logging

import enhanced_logging as elog


def test_speak_disabled_does_nothing(monkeypatch):
    called = {}

    def fake_popen(*args, **kwargs):
        called["yes"] = True

    monkeypatch.setattr(elog.subprocess, "Popen", fake_popen)
    elog.speak("hello", config=elog.SpeakConfig(enabled=False))

    assert called == {}


def test_speak_enabled_uses_configured_command(monkeypatch):
    seen = {}

    def fake_popen(cmd, stdout=None, stderr=None):
        seen["cmd"] = cmd

    monkeypatch.setattr(elog.subprocess, "Popen", fake_popen)
    cfg = elog.SpeakConfig(enabled=True, min_level=logging.ERROR, cmd="echo")

    elog.speak("hello", config=cfg)

    assert seen["cmd"] == ["echo", "hello"]


def test_maybe_speak_only_at_or_above_threshold(monkeypatch):
    calls = []

    def fake_speak(text, config=None):
        calls.append(text)

    original_speak_config = elog.SpeakConfig

    monkeypatch.setattr(elog, "speak", fake_speak)
    monkeypatch.setattr(
        elog,
        "SpeakConfig",
        lambda: original_speak_config(enabled=True, min_level=logging.ERROR, cmd="echo"),
    )

    event = {"event": "Failure", "level": "error"}
    elog._maybe_speak(None, "", event)

    assert calls == ["Failure"]
