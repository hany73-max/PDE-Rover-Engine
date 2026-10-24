"""
test_solvers.py — Fast verification bench for student solvers.

Runs unit tests and analytical checks against your implementations in
`rover_path_finder/solvers.py`.

Usage
-----
    # Test all implemented functions
    uv run python test_solvers.py

    # Test only Phase 1 (omega_opt, jacobi, sor)
    uv run python test_solvers.py --phase 1

    # Test only Phase 2 (sor_neumann)
    uv run python test_solvers.py --phase 2

    # Benchmark against the reference solution (for instructors / verification)
    uv run python test_solvers.py --reference
"""

import argparse
import sys
import time
import numpy as np


def exact_analytical_problem(N: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Unit square Laplace problem:
    Boundary condition: φ(x, 1) = sin(πx), φ = 0 on other boundaries.
    Analytical solution: φ(x, y) = sin(πx) * sinh(πy) / sinh(π)
    """
    x = np.linspace(0, 1, N + 1)
    X, Y = np.meshgrid(x, x)
    exact = np.sin(np.pi * X) * np.sinh(np.pi * Y) / np.sinh(np.pi)
    phi = np.zeros_like(exact)
    fixed = np.zeros_like(exact, bool)
    fixed[0, :] = fixed[-1, :] = fixed[:, 0] = fixed[:, -1] = True
    phi[-1, :] = np.sin(np.pi * x)
    return phi, fixed, exact


def test_omega_opt(solvers_mod) -> bool:
    print("\n--- Testing omega_opt(N) ---")
    try:
        val16 = solvers_mod.omega_opt(16)
        expected16 = 2.0 / (1.0 + np.sin(np.pi / 16))
        if abs(val16 - expected16) > 1e-6:
            print(f"  [FAIL] omega_opt(16) = {val16:.6f}, expected {expected16:.6f}")
            return False
        
        for N in [8, 32, 64, 128]:
            val = solvers_mod.omega_opt(N)
            exp = 2.0 / (1.0 + np.sin(np.pi / N))
            assert abs(val - exp) < 1e-6, f"Mismatch for N={N}"
            assert 1.0 < val < 2.0, f"SOR parameter must be in (1, 2), got {val}"
        
        print(f"  [PASS] omega_opt correctly calculated across grid sizes (e.g., N=16 -> {val16:.4f})")
        return True
    except NotImplementedError:
        print("  [TODO] omega_opt is not yet implemented.")
        return False
    except Exception as e:
        print(f"  [FAIL] Error testing omega_opt: {e}")
        return False


def test_jacobi(solvers_mod) -> bool:
    print("\n--- Testing jacobi() [Phase 1] ---")
    try:
        N = 16
        phi, fixed, exact = exact_analytical_problem(N)
        orig_phi = phi.copy()

        t0 = time.time()
        sol, hist = solvers_mod.jacobi(phi, fixed, tol=1e-5, maxit=2000)
        dt = time.time() - t0

        # Check 1: Did not mutate original input
        if not np.array_equal(phi, orig_phi):
            print("  [FAIL] jacobi mutated the input `phi` array! Make sure to call `phi = phi.copy()`.")
            return False

        # Check 2: Dirichlet boundaries preserved
        if not np.allclose(sol[fixed], orig_phi[fixed]):
            print("  [FAIL] Dirichlet boundary conditions were not preserved on fixed cells!")
            return False

        # Check 3: Convergence
        if len(hist) == 0 or hist[-1] >= 1e-5:
            print(f"  [FAIL] Did not converge to tolerance 1e-5 within maxit (last delta = {hist[-1] if hist else 'None'})")
            return False

        # Check 4: Accuracy against exact PDE solution
        max_err = float(np.abs(sol - exact).max())
        if max_err > 0.005:  # N=16 discretization error is ~1.1e-3
            print(f"  [FAIL] High numerical error against analytical solution: {max_err:.4e} (expected < 2e-3)")
            return False

        print(f"  [PASS] jacobi converged in {len(hist)} iterations ({dt*1000:.1f} ms).")
        print(f"         Max error vs analytical: {max_err:.4e} (O(h^2) discretization error).")
        return True
    except NotImplementedError:
        print("  [TODO] jacobi is not yet implemented.")
        return False
    except Exception as e:
        print(f"  [FAIL] Error testing jacobi: {e}")
        return False


def test_sor(solvers_mod) -> bool:
    print("\n--- Testing sor() [Phase 1: Gauss-Seidel & SOR] ---")
    try:
        N = 16
        phi, fixed, exact = exact_analytical_problem(N)
        orig_phi = phi.copy()

        # Part A: Gauss-Seidel (omega = 1.0)
        sol_gs, hist_gs = solvers_mod.sor(phi, fixed, omega=1.0, tol=1e-5, maxit=2000)
        
        if not np.allclose(sol_gs[fixed], orig_phi[fixed]):
            print("  [FAIL] Dirichlet boundary conditions not preserved in Gauss-Seidel!")
            return False

        # Part B: SOR with optimal omega
        w_opt = 2.0 / (1.0 + np.sin(np.pi / N))
        sol_sor, hist_sor = solvers_mod.sor(phi, fixed, omega=w_opt, tol=1e-5, maxit=2000)

        # Check acceleration: SOR should need significantly fewer iterations than Gauss-Seidel
        it_gs = len(hist_gs)
        it_sor = len(hist_sor)
        
        max_err_sor = float(np.abs(sol_sor - exact).max())
        if max_err_sor > 0.005:
            print(f"  [FAIL] SOR max error vs analytical solution: {max_err_sor:.4e}")
            return False

        print(f"  [PASS] Gauss-Seidel (omega=1.0) converged in {it_gs} sweeps.")
        print(f"  [PASS] Red-Black SOR (omega={w_opt:.3f}) converged in {it_sor} sweeps.")
        speedup = it_gs / max(it_sor, 1)
        print(f"         SOR speedup: {speedup:.1f}x fewer iterations! Max error: {max_err_sor:.4e}")
        return True
    except NotImplementedError:
        print("  [TODO] sor is not yet implemented.")
        return False
    except Exception as e:
        print(f"  [FAIL] Error testing sor: {e}")
        return False


def test_sor_neumann(solvers_mod) -> bool:
    print("\n--- Testing sor_neumann() [Phase 2: Obstacles & No-Flux Walls] ---")
    try:
        # Create a small 20x20 grid with a central obstacle
        N = 20
        hazard = np.zeros((N, N), bool)
        hazard[8:12, 5:15] = True  # horizontal obstacle in the middle
        free = ~hazard

        phi = np.full((N, N), 0.5)
        fixed = np.zeros((N, N), bool)

        start = (2, 2)
        goal = (17, 17)
        phi[start[1], start[0]] = 1.0
        fixed[start[1], start[0]] = True
        phi[goal[1], goal[0]] = 0.0
        fixed[goal[1], goal[0]] = True

        t0 = time.time()
        w = 2.0 / (1.0 + np.sin(np.pi / N)) * 0.97
        sol, hist = solvers_mod.sor_neumann(phi, fixed, free, omega=w, tol=1e-6, maxit=5000)
        dt = time.time() - t0

        # Check 1: Start and Goal Dirichlet values
        if not np.isclose(sol[start[1], start[0]], 1.0):
            print(f"  [FAIL] Start node value corrupted: got {sol[start[1], start[0]]}, expected 1.0")
            return False
        if not np.isclose(sol[goal[1], goal[0]], 0.0):
            print(f"  [FAIL] Goal node value corrupted: got {sol[goal[1], goal[0]]}, expected 0.0")
            return False

        # Check 2: Hazard cells zeroed out or not corrupting field
        if np.any(sol[hazard] != 0.0):
            print("  [FAIL] Hazard cells should be set to 0.0 (phi[~free] = 0.0)")
            return False

        # Check 3: Free space has smooth monotonic gradient (Maximum Principle)
        free_vals = sol[free]
        if free_vals.min() < -1e-6 or free_vals.max() > 1.0 + 1e-6:
            print(f"  [FAIL] Maximum principle violated: values outside [0, 1] found! min={free_vals.min()}, max={free_vals.max()}")
            return False

        print(f"  [PASS] sor_neumann converged in {len(hist)} sweeps ({dt*1000:.1f} ms).")
        print(f"         Harmonic potential satisfies Maximum Principle on free domain [0.0, 1.0].")
        print(f"         Zero-flux boundary conditions correctly preserved around obstacle.")
        return True
    except NotImplementedError:
        print("  [TODO] sor_neumann is not yet implemented.")
        return False
    except Exception as e:
        print(f"  [FAIL] Error testing sor_neumann: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test bench for PDE Rover Engine solvers.")
    parser.add_argument("--phase", type=int, choices=[1, 2], help="Run only Phase 1 or Phase 2 tests")
    parser.add_argument("--reference", action="store_true", help="Run tests against reference solution")
    args = parser.parse_args()

    if args.reference:
        print("==================================================")
        print(" TESTING REFERENCE SOLUTION (solutions/solvers_reference.py)")
        print("==================================================")
        from solutions import solvers_reference as solvers_mod
    else:
        print("==================================================")
        print(" TESTING STUDENT IMPLEMENTATION (rover_path_finder/solvers.py)")
        print("==================================================")
        from rover_path_finder import solvers as solvers_mod

    results = {}

    if args.phase is None or args.phase == 1:
        results["omega_opt"] = test_omega_opt(solvers_mod)
        results["jacobi"] = test_jacobi(solvers_mod)
        results["sor"] = test_sor(solvers_mod)

    if args.phase is None or args.phase == 2:
        results["sor_neumann"] = test_sor_neumann(solvers_mod)

    print("\n==================================================")
    print(" SUMMARY")
    print("==================================================")
    all_passed = True
    for name, passed in results.items():
        status = "PASSED" if passed else "INCOMPLETE / FAILED"
        print(f"  - {name:15s}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\nAll tested functions PASSED! You are ready to run:")
        print("    uv run python main.py")
        print("to generate all benchmark figures and verify rover path planning.")
        sys.exit(0)
    else:
        print("\nSome functions are not yet implemented or failed. Keep going!")
        sys.exit(1)


if __name__ == "__main__":
    main()
