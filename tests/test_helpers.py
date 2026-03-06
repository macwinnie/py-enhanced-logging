import logging

from enhanced_logging import LogConfig
from enhanced_logging import _drop_private_keys
from enhanced_logging import _humanize_event
from enhanced_logging import _jsonify_event
from enhanced_logging import _parse_log_level
from enhanced_logging import _render_fmt


def test_parse_log_level_defaults_to_info():
    assert _parse_log_level(None) == logging.INFO
    assert _parse_log_level("bogus") == logging.INFO


def test_parse_log_level_handles_case_and_spaces():
    assert _parse_log_level(" debug ") == logging.DEBUG


def test_render_fmt_success():
    event = {"event": "startup", "_fmt": "Hello {user}", "user": "Ada"}
    out = _render_fmt(None, "", event)
    assert out["_rendered"] == "Hello Ada"


def test_render_fmt_failure_is_nonfatal():
    event = {"event": "startup", "_fmt": "Hello {missing}"}
    out = _render_fmt(None, "", event)
    assert "format_error=KeyError" in out["_rendered"]


def test_drop_private_keys():
    event = {"event": "x", "_fmt": "y", "_rendered": "z"}
    out = _drop_private_keys(None, "", event)
    assert "_fmt" not in out
    assert "_rendered" not in out


def test_humanize_event_replaces_event():
    event = {"event": "startup", "_rendered": "Hello Ada"}
    out = _humanize_event(None, "", event)
    assert out["event"] == "Hello Ada"
    assert out["_event_original"] == "startup"


def test_jsonify_event_keeps_event_and_sets_msg():
    event = {"event": "startup", "_rendered": "Hello Ada"}
    out = _jsonify_event(None, "", event)
    assert out["event"] == "startup"
    assert out["msg"] == "Hello Ada"


def test_want_callsite_auto_debug_true():
    cfg = LogConfig(level=logging.DEBUG, callsite="auto")
    assert cfg.want_callsite() is True


def test_want_callsite_auto_info_false():
    cfg = LogConfig(level=logging.INFO, callsite="auto")
    assert cfg.want_callsite() is False
