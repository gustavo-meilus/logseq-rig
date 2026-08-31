import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from vault_rig.__main__ import main


def vault(root: Path, *, custom: bool = False) -> None:
    pages, journals = ("notes", "daily") if custom else ("pages", "journals")
    (root / "logseq").mkdir(parents=True)
    (root / pages).mkdir()
    (root / journals).mkdir()
    config = '{:pages-directory "notes" :journals-directory "daily"}' if custom else "{}"
    (root / "logseq" / "config.edn").write_text(config, encoding="utf-8")
    (root / pages / "Projects___Roadmap.md").write_text("alias:: [[Plan]]\n- TODO Ship [[Client]]\n  id:: root-id\n  - child ((root-id)) needle\n", encoding="utf-8")
    (root / pages / "Client.md").write_text("- Links [[Plan]]\n", encoding="utf-8")


class RetrievalTests(unittest.TestCase):
    def call(self, *args: str) -> tuple[int, dict[str, object], str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(args))
        return code, json.loads(stdout.getvalue()) if stdout.getvalue() else {}, stderr.getvalue()

    def test_file_commands_preserve_logseq_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault(root, custom=True)
            code, payload, _ = self.call("resolve", str(root), "Plan")
            self.assertEqual(code, 0); self.assertEqual(payload["result"]["page"], "Projects/Roadmap")
            code, payload, _ = self.call("find", str(root), "root-id")
            self.assertEqual(code, 0); self.assertIn("root-id", [item.get("id") for item in payload["result"]])
            for query in ("Client", "id", "TODO"):
                self.assertEqual(self.call("find", str(root), query)[0], 0)
            code, payload, _ = self.call("context", str(root), "needle", "--children", "1")
            self.assertEqual(code, 0); self.assertEqual(payload["result"][0]["ancestors"][0]["id"], "root-id")
            self.assertEqual(self.call("page", str(root), "Plan")[1]["result"]["aliases"], ["Plan"])
            self.assertEqual(self.call("block", str(root), "root-id")[1]["result"]["page"], "Projects/Roadmap")
            self.assertEqual(self.call("status", str(root))[1]["result"]["pages"], 2)
            self.assertEqual(len(self.call("backlinks", str(root), "Plan")[1]["result"]), 1)
            self.assertEqual(len(self.call("refs", str(root), "Plan")[1]["result"]), 2)

    def test_errors_and_history_are_machine_readable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault(root)
            code, _, error = self.call("resolve", str(root), "missing")
            self.assertEqual(code, 2); self.assertEqual(json.loads(error)["code"], "not_found")
            (root / "pages" / "Duplicate.md").write_text("alias:: [[Plan]]\n", encoding="utf-8")
            code, _, error = self.call("resolve", str(root), "Plan")
            self.assertEqual(code, 2); self.assertEqual(json.loads(error)["code"], "ambiguous_page")
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "add roadmap"], cwd=root, check=True, capture_output=True)
            code, payload, _ = self.call("history", str(root), "needle")
            self.assertEqual(code, 0); self.assertEqual(len(payload["result"]), 1)
            code, payload, _ = self.call("history", str(root), "pages/Projects___Roadmap.md")
            self.assertEqual(code, 0); self.assertEqual(payload["result"][0]["files"], ["pages/Projects___Roadmap.md"])
