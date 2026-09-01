import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from logseq_rig.__main__ import FORBIDDEN_PATHS, REQUIRED_PATHS, main


class CliTests(unittest.TestCase):
    def test_help_and_version_exit_successfully(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as help_exit:
                main(["--help"])
            with self.assertRaises(SystemExit) as version_exit:
                main(["--version"])
        self.assertEqual(help_exit.exception.code, 0)
        self.assertEqual(version_exit.exception.code, 0)

    def test_layout_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for path in REQUIRED_PATHS:
                (root / path).mkdir(parents=True)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--check-layout", str(root)]), 0)

            (root / FORBIDDEN_PATHS[0]).mkdir(parents=True)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["--check-layout", str(root)]), 1)
