"""
Automated unit tests for Lab 1: Elimination of Arbitrary Constants.
Uses numerical substitution across random domain points to strictly validate student PDEs.
"""

from labs.tests import TestFeedback, eval_equation_residual
import numpy as np


def check_paper_challenge_1(student_pde: str):
    """Verify Student Paper Challenge 1: z = (x - a)^2 + (y - b)^2.
    Correct PDE: p^2 + q^2 = 4z (or any algebraically equivalent form).
    """
    if not isinstance(student_pde, str) or not student_pde.strip():
        TestFeedback.fail(
            "Please enter your PDE as a string, e.g. 'p^2 + q^2 = 4*z'.\n"
            "💡 تلميح / Hint: Differentiate z = (x-a)^2 + (y-b)^2 with respect to x and y, "
            "then square both p and q and add them."
        )

    rng = np.random.default_rng(42)
    x = rng.uniform(-5.0, 5.0, 50)
    y = rng.uniform(-5.0, 5.0, 50)
    a = rng.uniform(-3.0, 3.0, 50)
    b = rng.uniform(-3.0, 3.0, 50)
    z = (x - a) ** 2 + (y - b) ** 2
    p = 2.0 * (x - a)
    q = 2.0 * (y - b)

    clean_lower = student_pde.lower()
    if "a" in clean_lower or "b" in clean_lower:
        TestFeedback.fail(
            f"Your equation '{student_pde}' still contains the arbitrary constants 'a' or 'b'! "
            "The goal is to eliminate them completely using p, q, and z."
        )

    try:
        res_true = eval_equation_residual(student_pde, {"x": x, "y": y, "z": z, "p": p, "q": q})
        res_false = eval_equation_residual(student_pde, {"x": x, "y": y, "z": z + 2.5, "p": p, "q": q})
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_pde}' ({exc}).\n"
            "💡 Write it using p, q, and z — for example: 'p^2 + q^2 = 4*z'."
        )

    if np.max(np.abs(res_true)) < 1e-6 and np.max(np.abs(res_false)) > 0.1:
        TestFeedback.success("Paper Challenge 1 Verified! Exact PDE confirmed: p^2 + q^2 = 4z.")
    else:
        TestFeedback.fail(
            f"Your answer '{student_pde}' is not algebraically equivalent to p^2 + q^2 = 4z.\n"
            "💡 Step check: Since p = 2(x-a) and q = 2(y-b), squaring and adding gives "
            "p^2 + q^2 = 4[(x-a)^2 + (y-b)^2] = 4z. Did you remember to square p and q?"
        )


def check_paper_challenge_2(student_pde: str):
    """Verify Rover Basin Challenge: z = 0.5*a*x^2 + 0.5*b*y^2.
    Correct PDE: x*p + y*q = 2z (or any algebraically equivalent form).
    """
    if not isinstance(student_pde, str) or not student_pde.strip():
        TestFeedback.fail(
            "Please enter your PDE as a string, e.g. 'x*p + y*q = 2*z'.\n"
            "💡 تلميح / Hint: Solve p = a*x for a, and q = b*y for b, then substitute into z."
        )

    clean_lower = student_pde.lower()
    if "a" in clean_lower or "b" in clean_lower:
        TestFeedback.fail(
            f"Your equation '{student_pde}' still contains 'a' or 'b'! Eliminate them using p/x and q/y."
        )

    rng = np.random.default_rng(7)
    x = rng.uniform(0.5, 5.0, 50)
    y = rng.uniform(0.5, 5.0, 50)
    a = rng.uniform(0.5, 3.0, 50)
    b = rng.uniform(0.5, 3.0, 50)
    z = 0.5 * a * (x ** 2) + 0.5 * b * (y ** 2)
    p = a * x
    q = b * y

    try:
        res_true = eval_equation_residual(student_pde, {"x": x, "y": y, "z": z, "p": p, "q": q})
        res_false = eval_equation_residual(student_pde, {"x": x, "y": y, "z": z + 1.5, "p": p, "q": q})
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_pde}' ({exc}). Use x, y, z, p, q."
        )

    if np.max(np.abs(res_true)) < 1e-6 and np.max(np.abs(res_false)) > 0.1:
        TestFeedback.success("Rover Bridge Challenge Verified! Exact PDE confirmed: x*p + y*q = 2z.")
    else:
        TestFeedback.fail(
            f"Your answer '{student_pde}' does not match x*p + y*q = 2z.\n"
            "💡 Step check: Substituting a = p/x and b = q/y into z = (1/2)ax^2 + (1/2)by^2 "
            "gives z = (1/2)xp + (1/2)yq. Multiply both sides by 2!"
        )


def test_eliminate_constants_fn(target_fn):
    """Verify student coding implementation for surface slope verification."""
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = (X - 2.0) ** 2 + (Y - 3.0) ** 2

    dx = x[1] - x[0]
    dy = y[1] - y[0]
    # np.gradient returns [dZ/dy (rows), dZ/dx (cols)]
    Q, P = np.gradient(Z, dy, dx)

    residual = target_fn(Z, P, Q)
    if residual is None:
        TestFeedback.fail("verify_crater_pde returned None. Compute (P**2 + Q**2) - 4.0 * Z.")

    max_err = float(np.max(np.abs(residual[5:-5, 5:-5])))
    if max_err > 1e-4:
        TestFeedback.fail(
            f"Expected p^2 + q^2 - 4z to be near 0, but max residual is {max_err:.4f}. "
            "Check your formula: (P**2 + Q**2) - 4.0 * Z."
        )
    TestFeedback.success("All tests passed for verify_crater_pde!")
