"""
Automated unit tests for Lab 2: Quasi-Linear PDEs & Lagrange's Method.
Uses numerical evaluation along characteristic trajectories to strictly validate student answers.
"""

from labs.tests import TestFeedback, eval_math_side, eval_equation_residual
import numpy as np


def check_paper_challenge_1(student_u: str, student_v: str):
    """Verify Student Paper Challenge 1: x*p + y*q = z.
    Along any characteristic dx/x = dy/y = dz/z, x(t)=x0*e^t, y(t)=y0*e^t, z(t)=z0*e^t.
    Therefore u(x,y,z) and v(x,y,z) must be constant as t varies, and functionally independent!
    """
    if not isinstance(student_u, str) or not isinstance(student_v, str):
        TestFeedback.fail(
            "Please enter both student_u and student_v as strings, e.g. 'x/y' and 'y/z'."
        )

    rng = np.random.default_rng(11)
    x0, y0, z0 = 2.3, 1.7, 3.9
    t = np.linspace(0.1, 1.5, 30)
    env_char = {"x": x0 * np.exp(t), "y": y0 * np.exp(t), "z": z0 * np.exp(t)}

    try:
        u_vals = np.asarray(eval_math_side(student_u, env_char), dtype=float)
        v_vals = np.asarray(eval_math_side(student_v, env_char), dtype=float)
    except Exception as exc:
        TestFeedback.fail(f"Could not parse u='{student_u}' or v='{student_v}' ({exc}).")

    if np.ptp(u_vals) > 1e-6:
        TestFeedback.fail(
            f"u = '{student_u}' is not constant along the characteristic dx/x = dy/y!\n"
            "💡 Hint: Integrating dx/x = dy/y gives ln|x| - ln|y| = ln|c1|, so x/y = c1."
        )
    if np.ptp(v_vals) > 1e-6:
        TestFeedback.fail(
            f"v = '{student_v}' is not constant along the characteristic dy/y = dz/z!\n"
            "💡 Hint: Integrating dy/y = dz/z gives ln|y| - ln|z| = ln|c2|, so y/z = c2."
        )

    env_rand = {
        "x": rng.uniform(1.0, 5.0, 40),
        "y": rng.uniform(1.0, 5.0, 40),
        "z": rng.uniform(1.0, 5.0, 40),
    }
    u_rand = np.asarray(eval_math_side(student_u, env_rand), dtype=float)
    v_rand = np.asarray(eval_math_side(student_v, env_rand), dtype=float)
    if np.ptp(u_rand) < 1e-4 or np.ptp(v_rand) < 1e-4:
        TestFeedback.fail("u and v must depend on (x, y, z), not be plain numbers.")

    if "z" not in (student_u + student_v).lower():
        TestFeedback.fail(
            "Your two invariants must be independent! One should involve (x, y) and the other should involve z (e.g. 'y/z')."
        )

    TestFeedback.success("Paper Challenge 1 Verified! Independent characteristic invariants confirmed.")


def check_paper_challenge_2(student_path: str):
    """Verify Rover Streamline Challenge:
    For phi(x,y) = x^2 + 2y^2, velocity is (u,v) = (-2x, -4y).
    Stream function PDE: -2x * psi_x - 4y * psi_y = 0  ==> dx/x = dy/(2y) ==> y = k * x^2 (or y/x^2 = k).
    """
    if not isinstance(student_path, str) or not student_path.strip():
        TestFeedback.fail(
            "Please enter the streamline equation as a string, e.g. 'y = k*x^2' or 'y/x^2 = k'."
        )

    x = np.linspace(0.5, 3.0, 40)
    k = np.full_like(x, 2.0)
    y_true = k * (x ** 2)
    y_false = k * x + 1.0

    try:
        res_true = eval_equation_residual(student_path, {"x": x, "y": y_true, "k": k})
        res_false = eval_equation_residual(student_path, {"x": x, "y": y_false, "k": k})
    except Exception as exc:
        TestFeedback.fail(
            f"Could not parse '{student_path}' ({exc}). Use x, y, and k — for example: 'y = k*x^2'."
        )

    if np.max(np.abs(res_true)) < 1e-6 and np.max(np.abs(res_false)) > 0.1:
        TestFeedback.success("Rover Streamline Challenge Verified! Parabolic streamline y = k*x^2 confirmed.")
    else:
        TestFeedback.fail(
            f"Got '{student_path}', which does not satisfy y = k*x^2.\n"
            "💡 Step check: From dx/(-2x) = dy/(-4y), divide denominators by -2 to get dx/x = dy/(2y). "
            "Integrating gives ln|x| = (1/2)ln|y| + C, so y = k*x^2."
        )


def test_rk4_streamline_tracer(target_fn):
    """Verify numerical characteristic curve tracer."""
    def velocity(x, y):
        return -2.0 * x, -4.0 * y

    pts = target_fn(velocity, start=(1.0, 2.0), dt=0.01, steps=50)
    if not isinstance(pts, np.ndarray) or pts.ndim != 2 or pts.shape[1] != 2 or len(pts) < 10:
        TestFeedback.fail("Output must be an (N, 2) numpy array of (x, y) coordinates along the trajectory.")

    errs = [abs(y - 2.0 * (x ** 2)) for x, y in pts]
    max_err = max(errs)
    if max_err > 0.05:
        TestFeedback.fail(
            f"Streamline points deviated from the exact characteristic curve y = 2x^2 (max error {max_err:.4f})."
        )

    TestFeedback.success("All tests passed for trace_streamline_rk4!")
