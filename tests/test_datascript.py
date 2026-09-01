import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from logseq_rig.__main__ import main
from logseq_rig.datascript import Client, QueryError, execute, probe
from logseq_rig.retrieval import load
from logseq_rig.detection import detect


def graph(root: Path) -> None:
    (root / "logseq").mkdir(); (root / "pages").mkdir(); (root / "journals").mkdir()
    (root / "logseq" / "config.edn").write_text("{}", encoding="utf-8")
    (root / "pages" / "Plan.md").write_text("- linked\n  id:: block-1\n", encoding="utf-8")


class Response:
    def __init__(self, value): self.value = value
    def read(self): return json.dumps(self.value).encode()
    def __enter__(self): return self
    def __exit__(self, *_): return False


class DataScriptTests(unittest.TestCase):
    def setUp(self):
        self.environment = {"LOGSEQ_RIG_LOGSEQ_ENDPOINT": "http://127.0.0.1:1234/query", "LOGSEQ_RIG_LOGSEQ_TOKEN": "secret-token"}

    def pages(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); graph(root)
        return load(detect(root))

    def test_configuration_and_registry_fail_before_http(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(QueryError, "configured"): Client.from_environment()
        with patch.dict(os.environ, {**self.environment, "LOGSEQ_RIG_LOGSEQ_ENDPOINT": "https://example.test"}, clear=True):
            with self.assertRaisesRegex(QueryError, "loopback"): Client.from_environment()
        with patch("logseq_rig.datascript.build_opener") as opener, patch.dict(os.environ, self.environment, clear=True):
            for name, arguments in (("missing", []), ("page-by-name", [])):
                with self.assertRaises(QueryError): execute(name, arguments, self.pages())
            with self.assertRaises(QueryError): execute("page-by-name", ["Plan"], self.pages(), registry_version=2)
            opener.assert_not_called()

    def test_success_probe_normalization_and_unresolved_evidence(self):
        with patch.dict(os.environ, self.environment, clear=True), patch("logseq_rig.datascript.build_opener") as opener:
            opener.return_value.open.return_value = Response({"version": "0.10", "result": [{"name": "Plan"}]})
            self.assertEqual(probe()["api_version"], "0.10")
            result = execute("page-by-name", ["Plan"], self.pages())
        self.assertEqual(result["results"][0]["evidence"]["page"], "Plan")
        with patch.dict(os.environ, self.environment, clear=True), patch("logseq_rig.datascript.build_opener") as opener:
            opener.return_value.open.return_value = Response({"result": [{"uuid": "gone"}]})
            self.assertEqual(execute("blocks-referencing-page", ["Plan"], self.pages())["results"][0]["evidence_status"], "unresolved_live_entity")

    def test_http_drift_malformed_result_and_redaction(self):
        with patch.dict(os.environ, self.environment, clear=True), patch("logseq_rig.datascript.build_opener") as opener:
            opener.return_value.open.return_value = Response({"result": {}})
            with self.assertRaisesRegex(QueryError, "list"): execute("page-by-name", ["Plan"], self.pages())
        with patch.dict(os.environ, self.environment, clear=True), patch("logseq_rig.datascript.build_opener") as opener:
            opener.return_value.open.return_value = Response({"unexpected": []})
            with self.assertRaisesRegex(QueryError, "result"): probe()
        with patch.dict(os.environ, self.environment, clear=True), patch("logseq_rig.datascript.build_opener") as opener:
            opener.return_value.open.side_effect = HTTPError("http://127.0.0.1", 401, "unauthorized", {}, None)
            with self.assertRaisesRegex(QueryError, "HTTP 401"): probe()
        with patch.dict(os.environ, self.environment, clear=True), patch("logseq_rig.datascript.build_opener") as opener:
            opener.return_value.open.side_effect = OSError("secret-token")
            with self.assertRaises(QueryError) as error: probe()
        self.assertNotIn("secret-token", str(error.exception))

    def test_cli_remains_offline_without_bridge(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout): self.assertEqual(main(["status", str(root)]), 0)
            self.assertEqual(json.loads(stdout.getvalue())["result"]["pages"], 1)
