"""
Automated unit tests for Lab 6: The Capstone: Discretization & Autonomous Mars Navigation.
"""

from labs.tests import TestFeedback
import numpy as np


def check_paper_challenge_1(phi_A: float, phi_B: float):
    """Verify 4-Node Hand Calculation Sweep."""
    if abs(phi_A - 0.375) < 1e-4 and abs(phi_B - 0.375) < 1e-4:
        TestFeedback.success(
            f"Paper Challenge Verified! phi_A = {phi_A} and phi_B = {phi_B}. "
            "Your pencil-and-paper hand calculation is 100% exact!"
        )
    else:
        TestFeedback.fail(
            f"Expected phi_A = 0.375 and phi_B = 0.375, but got phi_A={phi_A}, phi_B={phi_B}. "
            "Check INSTRUCTOR_ANSWER_KEY.md (Section 6.1) for full steps."
        )


def check_paper_challenge_2(omega_16: float):
    """Verify optimal omega for N=16: 2 / (1 + sin(pi/16)) ≈ 1.6735."""
    if abs(omega_16 - 1.6735) < 1e-2:
        TestFeedback.success(
            f"Rover Bridge Challenge Verified! For N=16, optimal omega = {omega_16:.4f}."
        )
    else:
        TestFeedback.fail(
            f"Got {omega_16}. Expected ≈ 1.6735. Formula: 2 / (1 + sin(pi / 16))."
        )


def test_omega_opt(target_fn):
    """Verify student optimal omega calculation across grids."""
    test_cases = [(4, 1.17157), (16, 1.67351), (160, 1.96149)]
    for n, expected in test_cases:
        res = target_fn(n)
        if abs(res - expected) > 1e-3:
            TestFeedback.fail(f"For N={n}, expected {expected:.4f}, but got {res:.4f}.")
    TestFeedback.success("All tests passed for omega_opt!")


def test_sor_neumann_step(target_fn):
    """Verify SOR with zero-flux Neumann walls."""
    n = 10
    phi = np.zeros((n, n))
    fixed = np.zeros((n, n), dtype=bool)
    free = np.ones((n, n), dtype=bool)
    
    # Boundary Dirichlet
    phi[0, :] = 1.0
    fixed[0, :] = True
    phi[-1, :] = 0.0
    fixed[-1, :] = True
    
    # Obstacle in center
    free[4:6, 4:6] = False
    
    sol, hist = target_fn(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000)
    if hist[-1] >= 1e-5:
        TestFeedback.fail(f"SOR failed to converge within {len(hist)} steps.")
    
    # Maximum principle check
    free_interior = sol[free & ~fixed]
    if free_interior.min() < -1e-5 or free_interior.max() > 1.0 + 1e-5:
        TestFeedback.fail("Maximum Principle violated! Free potential must be bounded in [0, 1].")
        
    TestFeedback.success("All tests passed for sor_neumann_step!")

