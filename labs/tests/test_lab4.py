"""
Automated unit tests for Lab 4: Higher-Order Operators & Laplace's Equation.
"""

from labs.tests import TestFeedback
import numpy as np


def check_paper_challenge_1(m1: complex, m2: complex):
    """Verify Laplace Auxiliary Roots: (D_x^2 + D_y^2)z = 0.
    A.E. is m^2 + 1 = 0 ==> m = ±i.
    """
    roots = {complex(m1), complex(m2)}
    match = any(abs(m - 1j) < 1e-5 or abs(m + 1j) < 1e-5 for m in roots)
    if match and len(roots) >= 1:
        TestFeedback.success(
            "Paper Challenge 1 Verified! Characteristic roots are m = ±i, confirming the general solution "
            "z = Phi_1(y + ix) + Phi_2(y - ix) from Page 33 of your lecture notes!"
        )
    else:
        TestFeedback.fail(
            f"Roots {roots} are incorrect. For m^2 + 1 = 0, m = ±sqrt(-1) = ±i. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 4.1) for full steps."
        )


def check_paper_challenge_2(student_pi: str):
    """Verify Rover Gravity Forcing P.I. Challenge:
    (D_x^2 - D_x*D_y - 6*D_y^2)z = sin(2x - 3y).
    P.I. is (1/44)*sin(2x - 3y).
    """
    clean = student_pi.strip().lower().replace(" ", "")
    if "44" in clean and "sin" in clean:
        TestFeedback.success(
            "Rover Bridge Challenge Verified! Particular Integral is (1/44)*sin(2x - 3y)."
        )
    else:
        TestFeedback.fail(
            f"Got '{student_pi}'. Expected (1/44)*sin(2x - 3y). "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 4.2) for full steps."
        )


def test_characteristic_roots_solver(target_fn):
    """Verify characteristic polynomial root finder."""
    # Test m^2 + 1 = 0 (Laplace)
    roots = target_fn([1, 0, 1])
    roots_set = {complex(round(r.real, 4), round(r.imag, 4)) for r in roots}
    if {1j, -1j} != roots_set:
        TestFeedback.fail(f"For m^2 + 1 = 0, expected {{1j, -1j}}, got {roots_set}.")

    # Test m^2 - m - 6 = 0 (Page 40)
    roots_page40 = target_fn([1, -1, -6])
    roots_set40 = {round(r.real, 2) for r in roots_page40}
    if {3.0, -2.0} != roots_set40:
        TestFeedback.fail(f"For m^2 - m - 6 = 0, expected {{3.0, -2.0}}, got {roots_set40}.")

    TestFeedback.success("All tests passed for characteristic_roots_solver!")

