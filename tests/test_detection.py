import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from vault_rig.detection import EdnReader, detect
from vault_rig.__main__ import main


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(path.relative_to(root).as_posix().encode())
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def vault(root: Path, config: str = "{}") -> None:
    (root / "logseq").mkdir()
    (root / "pages").mkdir()
    (root / "journals").mkdir()
    (root / "logseq" / "config.edn").write_text(config, encoding="utf-8")


class DetectionTests(unittest.TestCase):
    def test_reader_supports_maps_strings_keywords_comments_and_rejects_reader_forms(self):
        values = EdnReader('{:path "notes" ; comment\n :mode :triple-lowbar :nested {:x ["y"]} :tags #{"NOW" "TODO"} :query (has-ref ?b ?ref)}').read()
        self.assertEqual(values[":path"], "notes")
        self.assertEqual(values[":mode"], ":triple-lowbar")
        self.assertEqual(values[":tags"], ["NOW", "TODO"])
        self.assertEqual(values[":query"], ["has-ref", "?b", "?ref"])
        with self.assertRaises(ValueError):
            EdnReader('{:path #foo "notes"}').read()

    def test_default_and_custom_descriptors_are_stable_and_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "vault"
            root.mkdir()
            vault(root)
            before = tree_hash(root)
            default = detect(root).to_dict()
            self.assertEqual(before, tree_hash(root))
            self.assertTrue(Path(default["root"]).samefile(root))
            self.assertFalse(Path(default["pages_directory"]).is_absolute())
            self.assertFalse(Path(default["journals_directory"]).is_absolute())
            self.assertEqual(default["pages_directory"], "pages")
            self.assertEqual(default["journal_filename_format"], "yyyy_MM_dd")
            self.assertEqual(json.dumps(default, sort_keys=True), json.dumps(detect(root).to_dict(), sort_keys=True))

            custom = Path(temporary) / "custom"
            custom.mkdir()
            vault(custom, '{:pages-directory "notes" :journals-directory "daily" :file/name-format :triple-lowbar :journal/file-name-format "yyyy-MM-dd"}')
            (custom / "pages").rmdir()
            (custom / "journals").rmdir()
            (custom / "notes").mkdir()
            (custom / "daily").mkdir()
            descriptor = detect(custom).to_dict()
            self.assertEqual((descriptor["pages_directory"], descriptor["journals_directory"]), ("notes", "daily"))

    def test_failure_codes_and_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = {
                "plain": ("non_vault", None),
                "malformed": ("malformed_config", "{:pages-directory"),
                "escape": ("path_escape", '{:pages-directory "../notes"}'),
                "mode": ("unsupported_filename_mode", "{:file/name-format :legacy}"),
                "journal": ("unsupported_journal_format", '{:journal/file-name-format ".."}'),
                "list": ("malformed_config", "{:pages-directory (foo)}"),
            }
            for name, (code, config) in cases.items():
                root = base / name
                root.mkdir()
                if config is not None:
                    vault(root, config)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(main(["detect", str(root)]), 2)
                self.assertEqual(json.loads(stderr.getvalue())["code"], code)

            db = base / "db"
            db.mkdir()
            (db / "db.sqlite").write_bytes(b"")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(main(["detect", str(db)]), 2)
            self.assertEqual(json.loads(stderr.getvalue())["code"], "db_graph")

            good = base / "good"
            good.mkdir()
            vault(good)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(main(["detect", str(good)]), 0)
            self.assertEqual(json.loads(stdout.getvalue())["pages_directory"], "pages")
