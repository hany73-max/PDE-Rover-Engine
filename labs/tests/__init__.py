"""
Test suites and numerical symbolic evaluation engine for the 6 DeepLearning.AI-style PDE Rover Labs.
"""

import re
import sys
import numpy as np

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
    YELLOW = "\033[93m"
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


def normalize_math_expr(expr: str) -> str:
    """Convert human mathematical notation (e.g. '4z', '2(x-a)', 'p^2', 'Phi1(...)') into valid Python."""
    if not isinstance(expr, str):
        raise ValueError("Expected a string expression.")
    s = expr.strip()
    if not s:
        raise ValueError("Expression cannot be empty.")

    # Normalize common derivative notations
    s = re.sub(r"\(\s*dz\s*/\s*dx\s*\)", "p", s, flags=re.IGNORECASE)
    s = re.sub(r"\(\s*dz\s*/\s*dy\s*\)", "q", s, flags=re.IGNORECASE)
    s = re.sub(r"dz\s*/\s*dx", "p", s, flags=re.IGNORECASE)
    s = re.sub(r"dz\s*/\s*dy", "q", s, flags=re.IGNORECASE)

    # Normalize Phi_1, phi_1, \Phi_1, \phi_1
    s = s.replace("\\Phi", "Phi").replace("\\phi", "Phi")
    s = re.sub(r"phi_?1", "Phi1", s, flags=re.IGNORECASE)
    s = re.sub(r"phi_?2", "Phi2", s, flags=re.IGNORECASE)
    s = re.sub(r"\bphi\b", "Phi1", s, flags=re.IGNORECASE)

    # Normalize e^(...) -> exp(...)
    s = re.sub(r"\be\s*\^\s*\(", "exp(", s)
    s = re.sub(r"\be\s*\*\*\s*\(", "exp(", s)
    s = re.sub(r"\be\s*\^\s*([+-]?[0-9a-zA-Z_./]+)", r"exp(\1)", s)

    # Caret to Python power
    s = s.replace("^", "**")

    # Insert explicit multiplication:
    # 1) digit followed by letter or '(' (but NOT after a letter like Phi1( or atan2(): (?<![a-zA-Z])\d)
    s = re.sub(r"(?<![a-zA-Z])(\d)\s*([a-zA-Z\(])", r"\1*\2", s)
    # 2) ')' followed by letter, digit, or '(' : (x+y)z -> (x+y)*z
    s = re.sub(r"\)\s*([a-zA-Z0-9\(])", r")*\1", s)
    # 3) two single-letter variables next to each other (xp, yq, ax, by, ab, kx):
    # Only split known variable pairs so function names like sin, cos, exp, sqrt, Phi1 stay intact.
    known_vars = "xyzpqabk"
    for _ in range(3):
        s = re.sub(
            rf"\b([{known_vars}])([{known_vars}])\b",
            r"\1*\2",
            s,
        )
        s = re.sub(
            rf"\b([{known_vars}])\s*\(",
            r"\1*(",
            s,
        )
    return s


def eval_math_side(expr: str, env: dict) -> np.ndarray:
    """Safely evaluate one side of a normalized mathematical expression on numpy arrays."""
    safe_globals = {
        "__builtins__": {},
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "ln": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "pi": np.pi,
        "Phi1": env.get("Phi1", lambda u: np.sin(u) + 0.5 * np.cos(u)),
        "Phi2": env.get("Phi2", lambda u: np.cos(u) - 0.3 * np.sin(u)),
    }
    local_env = {k: v for k, v in env.items() if k not in ("Phi1", "Phi2")}
    code = normalize_math_expr(expr)
    return eval(code, safe_globals, local_env)


def eval_equation_residual(eq_str: str, env: dict) -> np.ndarray:
    """Evaluate LHS - RHS for an equation 'LHS = RHS' (or 'EXPR' assumed '= 0')."""
    if not isinstance(eq_str, str) or not eq_str.strip():
        raise ValueError("Please provide a non-empty equation string.")
    if "=" in eq_str:
        parts = eq_str.split("=")
        if len(parts) != 2:
            raise ValueError(f"Equation '{eq_str}' should contain a single '=' sign.")
        lhs = eval_math_side(parts[0], env)
        rhs = eval_math_side(parts[1], env)
        return np.asarray(lhs, dtype=float) - np.asarray(rhs, dtype=float)
    else:
        return np.asarray(eval_math_side(eq_str, env), dtype=float)
