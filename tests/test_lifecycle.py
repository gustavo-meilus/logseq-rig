import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from logseq_rig.lifecycle import BEGIN, END, CONFIG, INCOMPLETE, LEGACY_BEGIN, LEGACY_CONFIG, LEGACY_END, LEGACY_MANIFEST, MANIFEST, LifecycleError, _atomic_write, _digest, _read_manifest, plan, run


def graph(root: Path):
    (root / "logseq").mkdir(); (root / "pages").mkdir(); (root / "journals").mkdir()
    (root / "logseq" / "config.edn").write_text("{}", encoding="utf-8")


class LifecycleTests(unittest.TestCase):
    def test_manifest_rejects_unsafe_entries(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / ".logseq-rig").mkdir()
            (root / MANIFEST).write_text(json.dumps({"schema": 1, "version": "x", "entries": [{"path": "../x", "mode": "file", "sha256": "0" * 64}]}), encoding="utf-8")
            with self.assertRaises(LifecycleError): _read_manifest(root)

    def test_lifecycle_is_dry_run_safe_idempotent_and_preserves_root_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            protected = hashlib.sha256((root / "logseq" / "config.edn").read_bytes()).hexdigest()
            self.assertEqual(plan(root, "install"), run(root, "install", dry_run=True))
            self.assertFalse((root / "AGENTS.md").exists())
            run(root, "install")
            self.assertTrue((root / MANIFEST).is_file())
            self.assertEqual(run(root, "install"), [type(plan(root, "install")[0])("noop", "AGENTS.md")])
            (root / "AGENTS.md").write_text((root / "AGENTS.md").read_text(encoding="utf-8").replace("Canonical", "Local"), encoding="utf-8")
            self.assertEqual(run(root, "update")[0].kind, "conflict")
            self.assertEqual(hashlib.sha256((root / "logseq" / "config.edn").read_bytes()).hexdigest(), protected)

    def test_file_owned_agents_survives_reinstall_then_uninstall(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            run(root, "install")
            self.assertEqual(run(root, "install"), [type(plan(root, "install")[0])("noop", "AGENTS.md")])
            run(root, "uninstall")
            self.assertFalse((root / "AGENTS.md").exists())

    def test_doctor_and_interruption_are_non_destructive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root); protected = (root / "logseq" / "config.edn").read_bytes()
            run(root, "install")
            self.assertEqual(plan(root, "doctor")[0].kind, "healthy")
            (root / "AGENTS.md").write_text("changed\n", encoding="utf-8")
            self.assertEqual(plan(root, "doctor")[0].kind, "modified")
            (root / "AGENTS.md").unlink()
            self.assertEqual(plan(root, "doctor")[0].kind, "missing")
            self.assertEqual((root / "logseq" / "config.edn").read_bytes(), protected)

            other = Path(temporary) / "other"; other.mkdir(); graph(other)
            writes = iter((_atomic_write, _atomic_write, OSError("injected")))
            def interrupted(*args):
                next_write = next(writes)
                if isinstance(next_write, OSError): raise next_write
                next_write(*args)
            with patch("logseq_rig.lifecycle._atomic_write", side_effect=interrupted):
                with self.assertRaisesRegex(LifecycleError, "incomplete managed state"):
                    run(other, "install")
            self.assertTrue((other / INCOMPLETE).exists())
            self.assertEqual(plan(other, "doctor")[0].kind, "incomplete")
            self.assertEqual((other / "logseq" / "config.edn").read_bytes(), protected)

    def test_lifecycle_uses_custom_detected_graph_layout(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            (root / "pages").rename(root / "notes"); (root / "journals").rename(root / "daily")
            (root / "logseq" / "config.edn").write_text('{:pages-directory "notes" :journals-directory "daily"}', encoding="utf-8")
            self.assertEqual(run(root, "install")[0].kind, "add")
            self.assertEqual(run(root, "doctor")[0].kind, "healthy")
            run(root, "uninstall")

    def test_marker_errors_and_version_mismatch_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            (root / "AGENTS.md").write_text(BEGIN + END + BEGIN + END, encoding="utf-8")
            with self.assertRaises(LifecycleError): plan(root, "install")
            (root / "AGENTS.md").unlink(); run(root, "install")
            manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8")); manifest["version"] = "0.0.0"
            (root / MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(plan(root, "doctor")[0].kind, "version-mismatch")

    def test_region_uninstall_preserves_preexisting_instructions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root); (root / "AGENTS.md").write_text("# Mine\n", encoding="utf-8")
            run(root, "install")
            self.assertIn(BEGIN, (root / "AGENTS.md").read_text(encoding="utf-8"))
            run(root, "uninstall")
            self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), "# Mine\n")
            self.assertFalse((root / MANIFEST).exists())

    def test_codex_payload_is_owned_and_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root); run(root, "install")
            self.assertTrue((root / ".agents/skills/logseq-rig/SKILL.md").is_file())
            self.assertTrue((root / ".codex/hooks.json").is_file())
            (root / ".codex/config.toml").write_text("changed", encoding="utf-8")
            self.assertEqual(plan(root, "uninstall")[0].kind, "conflict")

    def test_clean_legacy_state_migrates_and_conflicts_on_changed_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            old_region = LEGACY_BEGIN + "legacy\n" + LEGACY_END
            old_skill = "legacy\n"
            (root / "AGENTS.md").write_text("# Mine\n" + old_region, encoding="utf-8")
            (root / ".agents/skills/vault-rig").mkdir(parents=True)
            (root / ".agents/skills/vault-rig/SKILL.md").write_text(old_skill, encoding="utf-8")
            (root / ".vault-rig").mkdir()
            legacy = {"schema": 1, "version": "1.0.0", "entries": [{"path": "AGENTS.md", "mode": "region", "sha256": _digest(old_region)}, {"path": ".agents/skills/vault-rig/SKILL.md", "mode": "file", "sha256": _digest(old_skill)}]}
            (root / LEGACY_MANIFEST).write_text(json.dumps(legacy), encoding="utf-8")
            (root / LEGACY_CONFIG).write_text('{"controlled_properties":{"state":["ok"]}}', encoding="utf-8")
            self.assertEqual(plan(root, "doctor")[0].kind, "migration-required")
            self.assertEqual(run(root, "update")[0].kind, "migrate")
            self.assertEqual(plan(root, "doctor")[0].kind, "healthy")
            self.assertTrue((root / CONFIG).is_file())
            self.assertFalse((root / LEGACY_MANIFEST).exists())
            run(root, "uninstall")
            self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), "# Mine\n")

            other = Path(temporary) / "other"; other.mkdir(); graph(other)
            (other / ".vault-rig").mkdir(); (other / LEGACY_MANIFEST).write_text(json.dumps(legacy), encoding="utf-8")
            self.assertEqual(plan(other, "update")[0].kind, "conflict")

    def test_legacy_migration_interruption_is_diagnostic_and_preserves_graph(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root); protected = (root / "logseq" / "config.edn").read_bytes()
            old_region = LEGACY_BEGIN + "legacy\n" + LEGACY_END
            (root / "AGENTS.md").write_text(old_region, encoding="utf-8")
            (root / ".vault-rig").mkdir()
            legacy = {"schema": 1, "version": "1.0.0", "entries": [{"path": "AGENTS.md", "mode": "region", "sha256": _digest(old_region)}]}
            (root / LEGACY_MANIFEST).write_text(json.dumps(legacy), encoding="utf-8")
            writes = iter((_atomic_write, OSError("injected")))
            def interrupted(*args):
                next_write = next(writes)
                if isinstance(next_write, OSError): raise next_write
                next_write(*args)
            with patch("logseq_rig.lifecycle._atomic_write", side_effect=interrupted):
                with self.assertRaisesRegex(LifecycleError, "incomplete managed migration"):
                    run(root, "update")
            self.assertEqual(plan(root, "doctor")[0].kind, "incomplete")
            self.assertEqual((root / "logseq" / "config.edn").read_bytes(), protected)

    def test_legacy_configuration_conflict_does_not_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            old_region = LEGACY_BEGIN + "legacy\n" + LEGACY_END
            (root / "AGENTS.md").write_text(old_region, encoding="utf-8")
            (root / ".vault-rig").mkdir()
            legacy = {"schema": 1, "version": "1.0.0", "entries": [{"path": "AGENTS.md", "mode": "region", "sha256": _digest(old_region)}]}
            (root / LEGACY_MANIFEST).write_text(json.dumps(legacy), encoding="utf-8")
            (root / LEGACY_CONFIG).write_text("old", encoding="utf-8")
            (root / CONFIG).parent.mkdir(); (root / CONFIG).write_text("new", encoding="utf-8")
            self.assertEqual(plan(root, "update")[0].kind, "conflict")
            self.assertEqual((root / CONFIG).read_text(encoding="utf-8"), "new")

    def test_invalid_legacy_configuration_does_not_migrate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); graph(root)
            old_region = LEGACY_BEGIN + "legacy\n" + LEGACY_END
            (root / "AGENTS.md").write_text(old_region, encoding="utf-8")
            (root / ".vault-rig").mkdir()
            legacy = {"schema": 1, "version": "1.0.0", "entries": [{"path": "AGENTS.md", "mode": "region", "sha256": _digest(old_region)}]}
            (root / LEGACY_MANIFEST).write_text(json.dumps(legacy), encoding="utf-8")
            (root / LEGACY_CONFIG).write_text("{not json", encoding="utf-8")
            self.assertEqual(plan(root, "update")[0].kind, "conflict")
            self.assertFalse((root / MANIFEST).exists())
