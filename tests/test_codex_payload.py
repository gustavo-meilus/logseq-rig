import json
import io
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).parents[1]
PAYLOAD = ROOT / "payload" / "codex"


class CodexPayloadTests(unittest.TestCase):
    def hook(self, name, payload, result):
        stdout = io.StringIO()
        with patch("sys.stdin", io.StringIO(json.dumps(payload))), patch("sys.stdout", stdout), patch("subprocess.run", return_value=result):
            runpy.run_path(PAYLOAD / ".codex/hooks" / name, run_name="__main__")
        return json.loads(stdout.getvalue())

    def test_config_and_hook_contract_are_bounded(self):
        config = (PAYLOAD / ".codex/config.toml").read_text(encoding="utf-8")
        self.assertIn('approval_policy = "on-request"', config)
        self.assertIn('sandbox_mode = "workspace-write"', config)
        self.assertIn("network_access = false", config)
        hooks = json.loads((PAYLOAD / ".codex/hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(set(hooks["hooks"]), {"SessionStart", "Stop"})
        for script in ("session_start.py", "stop.py"):
            self.assertNotIn("transcript", (PAYLOAD / ".codex/hooks" / script).read_text(encoding="utf-8"))

    def test_agents_region_and_skill_stay_concise(self):
        self.assertLess(len((PAYLOAD / "AGENTS.md").read_text(encoding="utf-8")), 600)
        self.assertIn("vault-rig check", (PAYLOAD / ".agents/skills/vault-rig/SKILL.md").read_text(encoding="utf-8"))

    def test_session_start_and_stop_are_bounded(self):
        success = type("Result", (), {"returncode": 0})()
        session = self.hook("session_start.py", {"cwd": "/vault", "source": "startup"}, success)
        context = session["hookSpecificOutput"]["additionalContext"]
        self.assertLess(len(context), 500)
        self.assertNotIn("transcript", context)
        self.assertEqual(self.hook("stop.py", {"cwd": "/vault", "stop_hook_active": False}, success), {})
        failed = type("Result", (), {"returncode": 1})()
        self.assertEqual(self.hook("stop.py", {"cwd": "/vault", "stop_hook_active": False}, failed)["decision"], "block")
        self.assertIn("unresolved", self.hook("stop.py", {"cwd": "/vault", "stop_hook_active": True}, failed)["systemMessage"])
