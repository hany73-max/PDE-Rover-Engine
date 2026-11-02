"""
Automated unit tests for Lab 3: Non-Linear PDEs & Charpit's Method.
"""

from labs.tests import TestFeedback
import numpy as np


def check_paper_challenge_1(student_solution: str):
    """Verify Student Paper Challenge 1: z = p*x + q*y + p*q (Clairaut form).
    Correct complete integral: z = a*x + b*y + a*b
    """
    clean = student_solution.strip().lower().replace(" ", "").replace("*", "")
    valid = ["z=ax+by+ab", "ax+by+ab"]
    if clean in valid or ("ax" in clean and "by" in clean and "ab" in clean):
        TestFeedback.success("Paper Challenge 1 Verified! Complete integral: z = ax + by + ab.")
    else:
        TestFeedback.fail(
            f"Got '{student_solution}'. Expected z = ax + by + ab. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 3.1) for full steps."
        )


def check_paper_challenge_2(student_envelope: str):
    """Verify Rover Wavefront Envelope Challenge: p^2 + q^2 = 1.
    Envelope is circular ripple: x^2 + y^2 = z^2.
    """
    clean = student_envelope.strip().lower().replace(" ", "")
    if ("x^2" in clean or "x**2" in clean) and ("y^2" in clean or "y**2" in clean) and ("z" in clean):
        TestFeedback.success(
            "Rover Bridge Challenge Verified! Circular expanding wavefront: x^2 + y^2 = z^2."
        )
    else:
        TestFeedback.fail(
            f"Got '{student_envelope}'. Expected circular wavefront (x - x0)^2 + (y - y0)^2 = z^2. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 3.2) for full steps."
        )


def test_eikonal_wavefront_distance(target_fn):
    """Verify numerical Eikonal distance transform."""
    # Test distance from center (25, 25) on a 50x50 grid
    center = (25, 25)
    dist_grid = target_fn(grid_size=(50, 50), source=center)
    
    if dist_grid.shape != (50, 50):
        TestFeedback.fail(f"Expected shape (50, 50), got {dist_grid.shape}.")
    
    # Check that distance from center to (25, 35) is exactly 10.0
    val = dist_grid[25, 35]
    if abs(val - 10.0) > 0.1:
        TestFeedback.fail(f"Distance at offset 10 expected 10.0, got {val:.2f}.")

    TestFeedback.success("All tests passed for eikonal_wavefront_distance!")
