"""
Automated unit tests for Lab 5: Non-Homogeneous Linear PDEs & Exponential Decay.
Uses numerical evaluation to verify reducible operator solutions and decay rates.
"""

from labs.tests import TestFeedback, eval_math_side
import numpy as np


def check_paper_challenge_1(student_sol: str):
    """Verify Student Paper Challenge 1 (Chapter 2 Ex.5 p. 4):
    (2*D_x - 3*D_y + 1)(D_x + 2*D_y - 2)z = 0.
    General solution: z = exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x).
    """
    if not isinstance(student_sol, str) or not student_sol.strip():
        TestFeedback.fail(
            "Please enter the general solution as a string, e.g. "
            "'exp(-x/2)*Phi1(2*y + 3*x) + exp(2*x)*Phi2(y - 2*x)'."
        )

    s = student_sol.strip()
    if "=" in s:
        s = s.split("=")[-1].strip()

    rng = np.random.default_rng(31)
    x = rng.uniform(-1.0, 1.0, 40)
    y = rng.uniform(-1.0, 1.0, 40)
    phi1 = lambda u: np.sin(u) + 0.5 * np.cos(u)
    phi2 = lambda u: np.cos(u) - 0.3 * np.sin(u)

    expected = np.exp(-0.5 * x) * phi1(2.0 * y + 3.0 * x) + np.exp(2.0 * x) * phi2(y - 2.0 * x)

    try:
        val = np.asarray(eval_math_side(s, {"x": x, "y": y, "Phi1": phi1, "Phi2": phi2}), dtype=float)
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_sol}' ({exc}).\n"
            "💡 Write it using exp(...), Phi1(...), and Phi2(...) — for example: "
            "'exp(-x/2)*Phi1(2*y + 3*x) + exp(2*x)*Phi2(y - 2*x)'."
        )

    if np.max(np.abs(val - expected)) < 1e-6:
        TestFeedback.success(
            "Paper Challenge 1 Verified! General solution "
            "z = exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x) confirmed."
        )
    else:
        TestFeedback.fail(
            f"Your solution '{student_sol}' does not match z = exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x).\n"
            "💡 Step check (Chapter 2 p. 2 & p. 4):\n"
            "  • Factor 1 (a=2, b=-3, c=1): z1 = exp(-1/2 * x) * Phi1(2y + 3x)\n"
            "  • Factor 2 (a=1, b=2, c=-2): z2 = exp(2x) * Phi2(y - 2x)"
        )


def check_paper_challenge_2(damping_exponent: float):
    """Verify Exponential Decay Rate Challenge:
    For (D_x + 2*D_y + 1)z = 0 ==> z = exp(-x)*Phi(y - 2x), the exponent k in exp(k*x) is k = -1.0.
    """
    if damping_exponent is None:
        TestFeedback.fail("Please enter the numerical decay rate k = -c/a (e.g. -1.0).")

    try:
        val = float(damping_exponent)
    except Exception as exc:
        TestFeedback.fail(f"Expected a number for damping_rate ({exc}).")

    if abs(val - (-1.0)) < 1e-4:
        TestFeedback.success(
            "Rover Bridge Challenge Verified! Exponential decay rate k = -1.0 confirmed."
        )
    else:
        TestFeedback.fail(
            f"Got {damping_exponent}, expected -1.0.\n"
            "💡 Hint: In (a*D_x + b*D_y + c)z = 0, the exponential factor is exp(-(c/a)*x). "
            "Here a = 1 and c = 1, so k = -c/a = -1.0."
        )


def test_linear_factor_evaluator(target_fn):
    """Verify student coding implementation for extracting (a, b, c)."""
    res1 = target_fn("2*D_x - 3*D_y - 5")
    if res1 != (2.0, -3.0, -5.0):
        TestFeedback.fail(f"For '2*D_x - 3*D_y - 5', expected (2.0, -3.0, -5.0), got {res1}.")

    res2 = target_fn("1*D_x + 2*D_y + 1")
    if res2 != (1.0, 2.0, 1.0):
        TestFeedback.fail(f"For '1*D_x + 2*D_y + 1', expected (1.0, 2.0, 1.0), got {res2}.")

    TestFeedback.success("All tests passed for parse_linear_factor!")
