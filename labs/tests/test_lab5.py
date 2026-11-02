"""
Automated unit tests for Lab 5: Non-Homogeneous Linear PDEs: Reducible Operators.
"""

from labs.tests import TestFeedback


def check_paper_challenge_1(student_sol: str):
    """Verify Student Paper Challenge 1:
    (2*D_x - 3*D_y + 1)(D_x + 2*D_y - 2)z = 0.
    Factors: e^(-x/2)*Phi_1(2y + 3x) + e^(2x)*Phi_2(y - 2x).
    """
    clean = student_sol.strip().lower().replace(" ", "")
    has_factor1 = ("-x/2" in clean or "-0.5x" in clean) and ("2y+3x" in clean or "3x+2y" in clean)
    has_factor2 = ("2x" in clean) and ("y-2x" in clean or "-2x+y" in clean)
    
    if has_factor1 and has_factor2:
        TestFeedback.success(
            "Paper Challenge 1 Verified! Correct general solution: "
            "z = exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x)."
        )
    else:
        TestFeedback.fail(
            f"Your solution '{student_sol}' is missing one of the exponential damping factors. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 5.1) for full steps."
        )


def check_paper_challenge_2(damping_exponent: float):
    """Verify Rover Battery Dissipation Challenge:
    (D_x + 2*D_y + 1)z = 0 ==> z = exp(-x)*Phi(y - 2x).
    Damping exponent factor in exp(k*x) is k = -1.0.
    """
    if abs(damping_exponent - (-1.0)) < 1e-4:
        TestFeedback.success(
            "Rover Bridge Challenge Verified! Battery dissipation rate is k = -1.0."
        )
    else:
        TestFeedback.fail(
            f"Got {damping_exponent}. Expected -1.0 (from exp(-c*x/a) with a=1, c=1). "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 5.2) for full steps."
        )


def test_linear_factor_evaluator(target_fn):
    """Verify student coding implementation for extracting (a, b, c)."""
    # Factor (2*D_x - 3*D_y - 5)
    a, b, c = target_fn("2*D_x - 3*D_y - 5")
    if (a, b, c) != (2, -3, -5):
        TestFeedback.fail(f"Expected (2, -3, -5), got ({a}, {b}, {c}).")
    
    TestFeedback.success("All tests passed for linear_factor_evaluator!")

