import json
import tempfile
from pathlib import Path

from oceanplovers2f_kit.core import Oceanplovers2fTool


def test_valid_json_is_normalized():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp, "a.json")
        path.write_text('{"b": 1, "a": 2}', encoding="utf-8")
        ok, payload = Oceanplovers2fTool().check(path)
        assert ok
        assert json.loads(payload) == {"a": 2, "b": 1}


def test_missing_file_is_reported():
    ok, reason = Oceanplovers2fTool().check("/no/such/file.json")
    assert not ok and reason == "file not found"


def test_broken_json_reports_position():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp, "bad.json")
        path.write_text("{", encoding="utf-8")
        ok, reason = Oceanplovers2fTool().check(path)
        assert not ok and "invalid JSON" in reason
