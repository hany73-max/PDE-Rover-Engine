"""
Automated unit tests for Lab 3: Non-Linear PDEs & Charpit's Method.
Uses numerical evaluation to strictly verify complete integrals and distance envelopes.
"""

from labs.tests import TestFeedback, eval_equation_residual
import numpy as np


def check_paper_challenge_1(student_solution: str):
    """Verify Student Paper Challenge 1: z = p*x + q*y + p*q (Clairaut form).
    Correct complete integral: z = a*x + b*y + a*b
    """
    if not isinstance(student_solution, str) or not student_solution.strip():
        TestFeedback.fail(
            "Please enter the complete integral as a string, e.g. 'z = a*x + b*y + a*b'."
        )

    s = student_solution.strip()
    if "=" not in s:
        s = "z = " + s

    rng = np.random.default_rng(19)
    x = rng.uniform(-4.0, 4.0, 40)
    y = rng.uniform(-4.0, 4.0, 40)
    a = rng.uniform(-3.0, 3.0, 40)
    b = rng.uniform(-3.0, 3.0, 40)
    z_true = a * x + b * y + a * b
    z_false = a * x + b * y + 2.0

    try:
        res_true = eval_equation_residual(s, {"x": x, "y": y, "z": z_true, "a": a, "b": b})
        res_false = eval_equation_residual(s, {"x": x, "y": y, "z": z_false, "a": a, "b": b})
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_solution}' ({exc}). Write e.g. 'z = a*x + b*y + a*b'."
        )

    if np.max(np.abs(res_true)) < 1e-6 and np.max(np.abs(res_false)) > 0.1:
        TestFeedback.success("Paper Challenge 1 Verified! Complete integral z = ax + by + ab confirmed.")
    else:
        TestFeedback.fail(
            f"Got '{student_solution}', which does not match z = ax + by + ab.\n"
            "💡 Hint: For Clairaut's equation z = px + qy + f(p,q) (and by Charpit's equations dp=0, dq=0), "
            "simply replace p with a and q with b."
        )


def check_paper_challenge_2(student_envelope: str):
    """Verify Rover Distance / Wavefront Challenge: p^2 + q^2 = 1.
    Conical distance surface from origin: x^2 + y^2 = z^2.
    """
    if not isinstance(student_envelope, str) or not student_envelope.strip():
        TestFeedback.fail(
            "Please enter the distance cone equation as a string, e.g. 'x^2 + y^2 = z^2'."
        )

    rng = np.random.default_rng(23)
    x = rng.uniform(0.5, 5.0, 40)
    y = rng.uniform(0.5, 5.0, 40)
    z_true = np.hypot(x, y)
    z_false = x + y + 1.0

    try:
        res_true = eval_equation_residual(student_envelope, {"x": x, "y": y, "z": z_true})
        res_false = eval_equation_residual(student_envelope, {"x": x, "y": y, "z": z_false})
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_envelope}' ({exc}). Write e.g. 'x^2 + y^2 = z^2'."
        )

    if np.max(np.abs(res_true)) < 1e-6 and np.max(np.abs(res_false)) > 0.1:
        TestFeedback.success(
            "Rover Bridge Challenge Verified! Euclidean distance surface x^2 + y^2 = z^2 confirmed."
        )
    else:
        TestFeedback.fail(
            f"Got '{student_envelope}', which is not equivalent to x^2 + y^2 = z^2.\n"
            "💡 Step check: Eliminating 'a' from z = x*cos(alpha) + y*sin(alpha) using dz/d(alpha) = 0 "
            "yields the distance cone x^2 + y^2 = z^2."
        )


def test_eikonal_wavefront_distance(target_fn):
    """Verify numerical Eikonal distance transform."""
    center = (25, 25)
    dist_grid = target_fn(grid_size=(50, 50), source=center)
    if dist_grid is None or dist_grid.shape != (50, 50):
        TestFeedback.fail(f"Expected a (50, 50) distance array, got {None if dist_grid is None else dist_grid.shape}.")

    val = dist_grid[25, 35]
    if abs(val - 10.0) > 0.1:
        TestFeedback.fail(f"Distance at 10-cell offset expected 10.0, got {val:.2f}.")

    TestFeedback.success("All tests passed for compute_eikonal_wavefront!")
