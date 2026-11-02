"""
Automated unit tests for Lab 1: Elimination of Arbitrary Constants.
"""

from labs.tests import TestFeedback
import numpy as np


def check_paper_challenge_1(student_pde: str):
    """Verify Student Paper Challenge 1: z = (x - a)^2 + (y - b)^2.
    Correct PDE: p^2 + q^2 = 4z
    """
    clean = student_pde.strip().lower().replace(" ", "").replace("*", "")
    valid = ["p^2+q^2=4z", "4z=p^2+q^2", "(dz/dx)^2+(dz/dy)^2=4z"]
    if clean in valid or ("p" in clean and "q" in clean and "4" in clean and "z" in clean):
        TestFeedback.success("Paper Challenge 1 Verified! Correct equation: p^2 + q^2 = 4z.")
    else:
        TestFeedback.fail(
            f"Your answer '{student_pde}' does not match p^2 + q^2 = 4z. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 1.1) for full steps."
        )


def check_paper_challenge_2(student_pde: str):
    """Verify Rover Basin Challenge: z = 0.5*a*x^2 + 0.5*b*y^2.
    Correct PDE: x*p + y*q = 2z
    """
    clean = student_pde.strip().lower().replace(" ", "").replace("*", "")
    valid = ["xp+yq=2z", "2z=xp+yq"]
    if clean in valid or ("xp" in clean and "yq" in clean and "2z" in clean):
        TestFeedback.success("Rover Bridge Challenge Verified! Correct equation: x*p + y*q = 2z.")
    else:
        TestFeedback.fail(
            f"Your answer '{student_pde}' does not match x*p + y*q = 2z. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 1.2) for full steps."
        )


def test_eliminate_constants_fn(target_fn):
    """Verify student coding implementation for surface slope verification."""
    # Test on a known paraboloid grid: z = (x - 2)^2 + (y - 3)^2
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = (X - 2.0)**2 + (Y - 3.0)**2
    
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    # np.gradient returns [dZ/dy, dZ/dx]
    Q, P = np.gradient(Z, dy, dx)
    
    residual = target_fn(Z, P, Q)
    max_err = float(np.max(np.abs(residual[5:-5, 5:-5])))
    if max_err > 1e-4:
        TestFeedback.fail(
            f"Expected p^2 + q^2 - 4z to be near 0, but max residual is {max_err:.4f}. "
            "Residual formula should be: (P**2 + Q**2) - 4 * Z."
        )
    TestFeedback.success("All tests passed for eliminate_constants_fn!")

