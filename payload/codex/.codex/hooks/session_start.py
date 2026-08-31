import json
import subprocess
import sys


def run(*args):
    try:
        result = subprocess.run(["vault-rig", *args], text=True, capture_output=True, timeout=10)
        return "available" if result.returncode == 0 else "unavailable"
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"


data = json.load(sys.stdin)
root = data.get("cwd", ".")
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": f"Vault Rig: {run('status', root)}; integrity: {run('check', root, '--changed')}; git: available."}}))
