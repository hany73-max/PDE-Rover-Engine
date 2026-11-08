"""
Automated unit tests for Lab 6: The Capstone: Discretization & Autonomous Mars Navigation.
"""

from labs.tests import TestFeedback
import numpy as np


def check_paper_challenge_1(phi_A: float, phi_B: float):
    """Verify 4-Node Hand Calculation (Jacobi Sweep 1)."""
    if phi_A is None or phi_B is None:
        TestFeedback.fail(
            "Please enter both phi_A and phi_B as floating-point numbers (e.g. 0.375)."
        )

    try:
        a_val = float(phi_A)
        b_val = float(phi_B)
    except Exception as exc:
        TestFeedback.fail(f"Expected numbers for phi_A and phi_B ({exc}).")

    if abs(a_val - 0.375) < 1e-4 and abs(b_val - 0.375) < 1e-4:
        TestFeedback.success(
            f"Paper Challenge Verified! Jacobi Sweep 1 gives phi_A = {a_val} and phi_B = {b_val}."
        )
    elif abs(a_val - 0.375) < 1e-4 and abs(b_val - 0.46875) < 1e-4:
        TestFeedback.fail(
            "You computed phi_B = 0.46875, which is the Gauss-Seidel update (using the new phi_A = 0.375)! "
            "For a simultaneous Jacobi sweep, use the old value phi_A^(0) = 0.0 so phi_B^(1) = (1.0 + 0.0 + 0.0 + 0.5)/4 = 0.375."
        )
    else:
        TestFeedback.fail(
            f"Got phi_A={phi_A}, phi_B={phi_B}. Expected 0.375 and 0.375.\n"
            "💡 Hint: Using the 5-point average (up + down + left + right) / 4 with old interior values = 0.0:\n"
            "  phi_A^(1) = (1.0 + 0.0 + 0.5 + 0.0) / 4 = 1.5 / 4 = 0.375."
        )


def check_paper_challenge_2(omega_16: float):
    """Verify optimal omega for N=16: 2 / (1 + sin(pi/16)) ≈ 1.6735."""
    if omega_16 is None:
        TestFeedback.fail("Please compute omega_16 = 2.0 / (1.0 + np.sin(np.pi / 16)).")

    try:
        val = float(omega_16)
    except Exception as exc:
        TestFeedback.fail(f"Expected a floating-point number for omega_16 ({exc}).")

    if abs(val - 1.6735) < 1e-2:
        TestFeedback.success(
            f"Rover Bridge Challenge Verified! For N=16, optimal SOR omega = {val:.4f}."
        )
    else:
        TestFeedback.fail(
            f"Got {omega_16}. Expected ≈ 1.6735 from Young's formula: 2 / (1 + sin(pi / 16))."
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

    phi[0, :] = 1.0
    fixed[0, :] = True
    phi[-1, :] = 0.0
    fixed[-1, :] = True

    free[4:6, 4:6] = False

    sol, hist = target_fn(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000)
    if not hist or hist[-1] >= 1e-5:
        TestFeedback.fail(
            f"SOR failed to converge within {len(hist)} steps. "
            "Make sure you compute pf = phi * f inside the loop before taking the 4-neighbor roll average!"
        )

    free_interior = sol[free & ~fixed]
    if free_interior.min() < -1e-5 or free_interior.max() > 1.0 + 1e-5:
        TestFeedback.fail("Discrete Maximum Principle violated! Free potential must stay bounded in [0, 1].")

    TestFeedback.success("All tests passed for sor_neumann_step!")
