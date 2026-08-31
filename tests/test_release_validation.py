from pathlib import Path
import tempfile
import unittest

from vault_rig.release_validation import FIXTURES, _hashes, cli


class ReleaseValidationTests(unittest.TestCase):
    def test_fixture_corpus_has_no_personal_paths_or_addresses(self):
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURES.rglob("*") if path.is_file())
        self.assertNotRegex(corpus, r"(?i)(?:c:|/users/|/home/|@)")

    def test_fast_fixture_is_disposable_and_diagnostic(self):
        fixture = FIXTURES / "default"
        before = _hashes(fixture)
        self.assertEqual(cli(["check", "--fixture", "default"]), 0)
        self.assertEqual(cli(["check", "--fixture", "default", "--break-expectation"]), 1)
        self.assertEqual(_hashes(fixture), before)
