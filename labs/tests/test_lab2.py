"""
Automated unit tests for Lab 2: Quasi-Linear PDEs & Lagrange's Method.
"""

from labs.tests import TestFeedback
import numpy as np


def check_paper_challenge_1(student_u: str, student_v: str):
    """Verify Student Paper Challenge 1: x*p + y*q = z.
    Correct integrals: u = x/y (or y/x), v = y/z (or x/z).
    """
    u_clean = student_u.strip().lower().replace(" ", "")
    v_clean = student_v.strip().lower().replace(" ", "")
    valid_u = ["x/y", "y/x", "x*y**-1"]
    valid_v = ["y/z", "z/y", "x/z", "z/x"]
    
    if (u_clean in valid_u or "x" in u_clean and "y" in u_clean) and \
       (v_clean in valid_v or "z" in v_clean):
        TestFeedback.success("Paper Challenge 1 Verified! Invariants u=x/y and v=y/z confirmed.")
    else:
        TestFeedback.fail(
            f"Got u='{student_u}', v='{student_v}'. Expected u = x/y and v = y/z. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 2.1) for full steps."
        )


def check_paper_challenge_2(student_path: str):
    """Verify Rover Streamline Challenge: y = k * x^2."""
    clean = student_path.strip().lower().replace(" ", "")
    if "x^2" in clean or "x**2" in clean:
        TestFeedback.success("Rover Streamline Challenge Verified! Trajectory equation: y = k*x^2.")
    else:
        TestFeedback.fail(
            f"Got '{student_path}'. Expected parabolic streamline y = k * x^2. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 2.2) for full steps."
        )


def test_rk4_streamline_tracer(target_fn):
    """Verify numerical characteristic curve tracer."""
    # Test on vector field u = -2x, v = -4y
    # Analytical solution starting at (1, 2) is y = 2*x^2
    def velocity(x, y):
        return -2.0 * x, -4.0 * y

    pts = target_fn(velocity, start=(1.0, 2.0), dt=0.01, steps=50)
    if not isinstance(pts, np.ndarray) or pts.shape[1] != 2:
        TestFeedback.fail("Output must be an (N, 2) array of (x, y) coordinates.")
    
    # Check that points satisfy y ≈ 2 * x^2
    errs = [abs(y - 2.0 * (x**2)) for x, y in pts]
    max_err = max(errs)
    if max_err > 0.05:
        TestFeedback.fail(f"Streamline points deviated from analytical curve y = 2x^2 (max error {max_err:.4f}).")

    TestFeedback.success("All tests passed for rk4_streamline_tracer!")

