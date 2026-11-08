"""
Automated unit tests for Lab 4: Higher-Order Operators & Laplace's Equation.
Uses numerical evaluation to verify characteristic roots and particular integrals.
"""

from labs.tests import TestFeedback, eval_math_side
import numpy as np


def check_paper_challenge_1(m1: complex, m2: complex):
    """Verify Laplace Auxiliary Roots: (D_x^2 + D_y^2)z = 0.
    A.E. is m^2 + 1 = 0 ==> m = ±i (Page 39 of lecture notes).
    """
    if m1 is None or m2 is None:
        TestFeedback.fail("Please enter both m1 and m2 using Python complex numbers: 1j and -1j.")

    try:
        r1 = complex(m1)
        r2 = complex(m2)
    except Exception as exc:
        TestFeedback.fail(f"Could not convert m1, m2 to complex numbers ({exc}). Use 1j and -1j.")

    # Both roots must satisfy m^2 + 1 = 0 and be distinct (+i and -i)
    ok1 = abs(r1 ** 2 + 1.0) < 1e-6
    ok2 = abs(r2 ** 2 + 1.0) < 1e-6
    distinct = abs(r1 - r2) > 1.0

    if ok1 and ok2 and distinct:
        TestFeedback.success(
            "Paper Challenge 1 Verified! Characteristic roots m1 = i, m2 = -i confirmed "
            "(General solution z = Phi_1(y + ix) + Phi_2(y - ix), Lecture Notes p. 39)."
        )
    else:
        TestFeedback.fail(
            f"Got m1={m1}, m2={m2}. Both roots of m^2 + 1 = 0 must be distinct: +1j and -1j."
        )


def check_paper_challenge_2(student_pi: str):
    """Verify Particular Integral Challenge (Lecture Notes Ex.4 p. 48):
    (D_x^2 - D_x*D_y - 6*D_y^2)z = sin(2x - 3y).
    P.I. is (1/44)*sin(2x - 3y).
    """
    if not isinstance(student_pi, str) or not student_pi.strip():
        TestFeedback.fail(
            "Please enter the particular integral as a string, e.g. '(1/44)*sin(2*x - 3*y)'."
        )

    s = student_pi.strip()
    if "=" in s:
        s = s.split("=")[-1].strip()

    rng = np.random.default_rng(29)
    x = rng.uniform(-3.0, 3.0, 50)
    y = rng.uniform(-3.0, 3.0, 50)
    expected = (1.0 / 44.0) * np.sin(2.0 * x - 3.0 * y)

    try:
        val = np.asarray(eval_math_side(s, {"x": x, "y": y}), dtype=float)
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_pi}' ({exc}). Write e.g. '(1/44)*sin(2*x - 3*y)'."
        )

    if np.max(np.abs(val - expected)) < 1e-6:
        TestFeedback.success(
            "Paper Challenge 2 Verified! Particular Integral z_p = (1/44)*sin(2x - 3y) confirmed."
        )
    else:
        TestFeedback.fail(
            f"Got '{student_pi}', which does not evaluate to (1/44)*sin(2x - 3y).\n"
            "💡 Step check: With a=2 and b=-3, substitute D_x^2 -> -a^2 = -4, "
            "D_x*D_y -> -a*b = +6, D_y^2 -> -b^2 = -9 into (D_x^2 - D_x*D_y - 6*D_y^2): "
            "(-4) - (6) - 6(-9) = -10 + 54 = 44."
        )


def test_characteristic_roots_solver(target_fn):
    """Verify characteristic polynomial root finder."""
    roots = target_fn([1, 0, 1])
    if roots is None:
        TestFeedback.fail("solve_operator_roots returned None. Use np.roots(coeffs).")
    roots_set = {complex(round(r.real, 4), round(r.imag, 4)) for r in roots}
    if {1j, -1j} != roots_set:
        TestFeedback.fail(f"For m^2 + 1 = 0, expected {{1j, -1j}}, got {roots_set}.")

    roots_page46 = target_fn([1, -1, -6])
    roots_set46 = {round(r.real, 2) for r in roots_page46}
    if {3.0, -2.0} != roots_set46:
        TestFeedback.fail(f"For m^2 - m - 6 = 0, expected {{3.0, -2.0}}, got {roots_set46}.")

    TestFeedback.success("All tests passed for solve_operator_roots!")
