import json
import subprocess
import sys


data = json.load(sys.stdin)
try:
    result = subprocess.run(["vault-rig", "check", data.get("cwd", "."), "--changed"], text=True, capture_output=True, timeout=30)
    failed = result.returncode == 1
except (OSError, subprocess.TimeoutExpired):
    failed = False
if failed and not data.get("stop_hook_active"):
    print(json.dumps({"decision": "block", "reason": "Vault Rig integrity failed; repair the changed canonical files, then recheck."}))
elif failed:
    print(json.dumps({"systemMessage": "Vault Rig integrity still fails after one retry; ending with unresolved findings."}))
else:
    print("{}")
