import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from vault_rig.__main__ import main


def vault(root: Path, text: str) -> Path:
    (root / "logseq").mkdir(); (root / "pages").mkdir(); (root / "journals").mkdir()
    (root / "logseq" / "config.edn").write_text("{}", encoding="utf-8")
    page = root / "pages" / "Test.md"; page.write_text(text, encoding="utf-8")
    return page


class IntegrityTests(unittest.TestCase):
    def call(self, *args: str):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err): code = main(list(args))
        return code, json.loads(out.getvalue()) if out.getvalue() else json.loads(err.getvalue())

    def test_all_reports_invariants_and_is_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); vault(root, "- duplicate\n  id:: 123\n- duplicate\n  id:: 123\n- ((missing))\n- [asset](../assets/missing.png)\n- [[new page]]\n")
            before = hashlib.sha256((root / "pages" / "Test.md").read_bytes()).hexdigest()
            code, result = self.call("check", str(root), "--all")
            self.assertEqual(code, 1); self.assertEqual(result["status"], "integrity_failure")
            self.assertEqual({item["code"] for item in result["findings"]}, {"invalid_persisted_id", "missing_block_target", "missing_local_asset"})
            self.assertEqual(before, hashlib.sha256((root / "pages" / "Test.md").read_bytes()).hexdigest())

    def test_duplicate_controlled_and_changed_modes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); page = vault(root, "- one\n  id:: 123e4567-e89b-42d3-a456-426614174000\n- two\n  id:: 123e4567-e89b-42d3-a456-426614174000\n  state:: nope\n")
            (root / ".vault-rig").mkdir(); (root / ".vault-rig" / "integrity.json").write_text('{"controlled_properties":{"state":["ok"]}}', encoding="utf-8")
            self.assertEqual({item["code"] for item in self.call("check", str(root), "--all")[1]["findings"]}, {"duplicate_persisted_id", "invalid_controlled_property"})
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True); subprocess.run(["git", "add", "."], cwd=root, check=True); subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-m", "base"], cwd=root, check=True, capture_output=True)
            page.write_text("- ref ((123e4567-e89b-42d3-a456-426614174000))\n", encoding="utf-8")
            code, result = self.call("check", str(root), "--changed", "--expected-path", "pages/Test.md")
            self.assertEqual(code, 1); self.assertIn("referenced_block_deleted", {item["code"] for item in result["findings"]})

    def test_healthy_graph_passes_both_modes_without_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); page = vault(root, "- valid\n  id:: 123e4567-e89b-42d3-a456-426614174000\n- ref ((123e4567-e89b-42d3-a456-426614174000))\n")
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True); subprocess.run(["git", "add", "."], cwd=root, check=True); subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-m", "base"], cwd=root, check=True, capture_output=True)
            before = hashlib.sha256(page.read_bytes()).hexdigest()
            self.assertEqual((self.call("check", str(root), "--all"), self.call("check", str(root), "--changed")), ((0, {"status": "pass", "mode": "all", "findings": []}), (0, {"status": "pass", "mode": "changed", "findings": []})))
            self.assertEqual(before, hashlib.sha256(page.read_bytes()).hexdigest())

    def test_asset_filenames_may_contain_parentheses(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); vault(root, "- [one](../assets/image_(2).png)\n- [two](../assets/nested_(a_(b)).png)\n- [missing](../assets/missing_(1).png)\n")
            assets = root / "assets"; assets.mkdir()
            (assets / "image_(2).png").write_bytes(b"")
            (assets / "nested_(a_(b)).png").write_bytes(b"")
            code, result = self.call("check", str(root), "--all")
            self.assertEqual(code, 1)
            self.assertEqual([item["message"] for item in result["findings"]], ["missing local asset: assets/missing_(1).png"])
