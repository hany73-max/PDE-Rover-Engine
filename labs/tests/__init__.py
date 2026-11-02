"""
Test suites for the 6 DeepLearning.AI-style PDE Rover Labs.
"""

import sys

# Ensure UTF-8 output when possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class TestFeedback:
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def success(cls, msg: str = "All tests passed!"):
        try:
            print(f"{cls.GREEN}{cls.BOLD}[PASS] {msg}{cls.RESET}")
        except UnicodeEncodeError:
            print(f"[PASS] {msg}")

    @classmethod
    def fail(cls, msg: str):
        try:
            print(f"{cls.RED}{cls.BOLD}[FAIL] Test failed:{cls.RESET} {msg}")
        except UnicodeEncodeError:
            print(f"[FAIL] Test failed: {msg}")
        raise AssertionError(msg)

