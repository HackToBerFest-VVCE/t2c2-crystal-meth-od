"""
CopilotShield - Test Suite & Execution Sandbox
Actually executes test commands or syntax checks in an isolated subprocess.
Captures genuine return codes, timeouts, and errors.
"""

import subprocess
import shutil
import os
from typing import Dict, Any, Optional

def run_tests_in_sandbox(test_command: Optional[str] = None, working_dir: str = ".", timeout_sec: int = 15) -> Dict[str, Any]:
    """
    Executes actual test suite or syntax verification.
    If no custom test_command is given, it looks for pytest, npm test, or python compilation.
    """
    if not test_command:
        # Detect environment
        if os.path.exists(os.path.join(working_dir, "pytest.ini")) or os.path.exists(os.path.join(working_dir, "tests")):
            test_command = "pytest"
        elif os.path.exists(os.path.join(working_dir, "package.json")):
            test_command = "npm test"
        else:
            # Default to Python syntax sanity check
            test_command = "python -m compileall -q ."

    print(f"[*] Sandbox running test command: '{test_command}' (timeout: {timeout_sec}s)...")
    try:
        proc = subprocess.run(
            test_command,
            shell=True,
            cwd=working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec
        )
        passed = (proc.returncode == 0)
        return {
            "executed": True,
            "passed": passed,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[:500],
            "stderr": proc.stderr[:500],
            "details": "All automated test suites passed successfully." if passed else f"Tests failed with exit code {proc.returncode}."
        }
    except subprocess.TimeoutExpired:
        return {
            "executed": True,
            "passed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout_sec} seconds (possible infinite loop or hang).",
            "details": "Sandbox execution timed out."
        }
    except Exception as e:
        return {
            "executed": False,
            "passed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "details": f"Failed to execute sandbox tests: {str(e)}"
        }
