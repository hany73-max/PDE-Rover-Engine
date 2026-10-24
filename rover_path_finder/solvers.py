"""
Iterative solvers for Laplace's equation (∇²φ = 0).

STUDENT STARTER TEMPLATE
========================
Welcome to the PDE Rover Engine solver template!
Your task is to implement the numerical solvers below using NumPy.
Do NOT use SciPy, iterative solver packages, or ML libraries — everything
must be built from first principles using discrete finite difference stencils.

Mathematical Background:
------------------------
Laplace's equation in 2D Cartesian coordinates:
    ∇²φ = ∂²φ/∂x² + ∂²φ/∂y² = 0

Discretized using a uniform grid (Δx = Δy = h) with standard second-order central
finite differences:
    (φ[i+1, j] - 2φ[i, j] + φ[i-1, j]) / h² + (φ[i, j+1] - 2φ[i, j] + φ[i, j-1]) / h² = 0
Multiplying by h² and solving for φ[i, j] yields the 5-point discrete mean-value property:
    φ[i, j] = 1/4 * (φ[i+1, j] + φ[i-1, j] + φ[i, j+1] + φ[i, j-1])

Functions to Implement:
-----------------------
1. omega_opt    : Compute the optimal SOR over-relaxation parameter for an N×N grid.
2. jacobi       : Standard Jacobi relaxation (simultaneous update).
3. sor          : Red-Black Successive Over-Relaxation (Gauss-Seidel when omega=1.0).
4. sor_neumann  : Red-Black SOR with zero-flux Neumann boundary conditions (∂φ/∂n = 0)
                  on hazard/obstacle boundaries.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Stencil Helpers (Optional reference helper)
# ---------------------------------------------------------------------------

def _avg(phi: np.ndarray) -> np.ndarray:
    """Average of the 4 axis-aligned neighbours (5-point finite-difference stencil).

    Tip: Using np.roll shifts the 2D array along axis 0 (rows) or axis 1 (columns)
    in a fully vectorized operation:
        np.roll(phi,  1, 0) -> down  (phi[i-1, j])
        np.roll(phi, -1, 0) -> up    (phi[i+1, j])
        np.roll(phi,  1, 1) -> right (phi[i, j-1])
        np.roll(phi, -1, 1) -> left  (phi[i, j+1])

    You may use this helper in your solvers or implement your own update logic!
    """
    return 0.25 * (
        np.roll(phi, 1, 0) + np.roll(phi, -1, 0)
        + np.roll(phi, 1, 1) + np.roll(phi, -1, 1)
    )


# ---------------------------------------------------------------------------
# Public API to Implement
# ---------------------------------------------------------------------------

def omega_opt(N: int) -> float:
    r"""Compute the theoretical optimal over-relaxation factor for an N×N Laplace grid.

    Mathematical Formula:
    ---------------------
    For a square Dirichlet domain of size N×N, the spectral radius of the Jacobi
    iteration matrix is:
        ρ_J = cos(π / N)

    The optimal SOR parameter ω_opt is given by Yang's formula:
        ω_opt = 2 / (1 + sqrt(1 - ρ_J²)) = 2 / (1 + sin(π / N))

    Parameters
    ----------
    N : int
        Number of grid intervals along each dimension (domain is (N+1)×(N+1) nodes,
        or an N×N interior problem).

    Returns
    -------
    float
        Optimal relaxation factor ω_opt in the range (1.0, 2.0).
    """
    # TODO: YOUR CODE HERE (Level 1)
    # Compute and return: 2.0 / (1.0 + np.sin(np.pi / N))
    raise NotImplementedError("omega_opt is not implemented yet. See docstring for the formula.")


def jacobi(
    phi: np.ndarray,
    fixed: np.ndarray,
    tol: float = 1e-8,
    maxit: int = 500_000,
) -> tuple[np.ndarray, list[float]]:
    r"""Solve Laplace's equation using the standard Jacobi iterative method.

    In Jacobi iteration, all grid nodes at iteration (k+1) are computed
    simultaneously from values at iteration (k):
        φ_{i,j}^{(k+1)} = 1/4 * (φ_{i+1,j}^{(k)} + φ_{i-1,j}^{(k)} + φ_{i,j+1}^{(k)} + φ_{i,j-1}^{(k)})

    Dirichlet boundary condition cells (`fixed == True`) are kept pinned to their
    prescribed values:
        φ_{i,j}^{(k+1)} = φ_{i,j}^{(0)}   for all (i, j) where fixed[i, j] is True.

    Parameters
    ----------
    phi : np.ndarray, shape (Ny, Nx), dtype float
        Initial potential field guess (includes Dirichlet values at boundary nodes).
    fixed : np.ndarray, shape (Ny, Nx), dtype bool
        Boolean mask where True denotes a cell with fixed Dirichlet boundary condition.
        These cells MUST NOT be updated during relaxation.
    tol : float, default=1e-8
        Convergence stopping threshold based on maximum absolute change:
        max |φ^{(k+1)} - φ^{(k)}| < tol.
    maxit : int, default=500_000
        Safety limit on maximum number of relaxation iterations.

    Returns
    -------
    phi : np.ndarray, shape (Ny, Nx)
        The converged numerical potential field.
    hist : list of float
        History of maximum residual / delta values for each iteration sweep:
        hist[k] = max |φ^{(k+1)} - φ^{(k)}|.

    Implementation Steps:
    ---------------------
    1. Make a copy of `phi` so the input array is not mutated unexpectedly:
       `phi = phi.copy()`
    2. Initialize an empty list `hist = []` to record per-iteration maximum deltas.
    3. Loop `it` from 0 up to `maxit`:
       a. Compute the new candidate field `new_phi` using the 4-neighbour average
          (you can call `_avg(phi)`).
       b. Re-impose the Dirichlet condition: `new_phi[fixed] = phi[fixed]`.
       c. Compute the maximum absolute change: `d = float(np.abs(new_phi - phi).max())`.
       d. Update `phi = new_phi`.
       e. Append `d` to `hist`.
       f. If `d < tol`, break out of the loop.
    4. Return `phi, hist`.
    """
    # TODO: YOUR CODE HERE (Level 1)
    raise NotImplementedError("jacobi is not implemented yet. Follow the docstring steps.")


def sor(
    phi: np.ndarray,
    fixed: np.ndarray,
    omega: float = 1.0,
    tol: float = 1e-8,
    maxit: int = 500_000,
) -> tuple[np.ndarray, list[float]]:
    r"""Solve Laplace's equation using Red-Black Successive Over-Relaxation (SOR).

    When ``omega = 1.0``, this algorithm is mathematically equivalent to Gauss-Seidel.
    When ``1.0 < omega < 2.0``, over-relaxation accelerates convergence by up to
    two orders of magnitude.

    Red-Black Checkerboard Decomposition:
    -------------------------------------
    Standard Gauss-Seidel updates cells sequentially (in-place), which is slow in Python loops.
    Because the 5-point Laplacian stencil only couples a cell to its 4 orthogonal neighbours,
    we partition the grid like a chessboard into two independent sets based on cell parity:
        parity = (i + j) % 2
        - Red cells   : parity == 0 (coupled only to Black neighbours)
        - Black cells : parity == 1 (coupled only to Red neighbours)

    This allows full 2-D vectorized NumPy slicing/masking:
        1. Update all Red cells using current Black neighbour values.
        2. Update all Black cells using the freshly updated Red neighbour values.

    SOR Update Equation:
    --------------------
    For each cell set (Red, then Black):
        φ_{new} = (1 - ω) * φ_{old} + ω * φ_{avg}
    where φ_{avg} is the 4-neighbour average.

    Parameters
    ----------
    phi : np.ndarray, shape (Ny, Nx), dtype float
        Initial guess containing prescribed Dirichlet values.
    fixed : np.ndarray, shape (Ny, Nx), dtype bool
        Boolean mask of Dirichlet boundary cells (fixed potential).
    omega : float, default=1.0
        Relaxation factor (1.0 = Gauss-Seidel, omega_opt(N) = optimal SOR).
    tol : float, default=1e-8
        Convergence stopping tolerance (max delta < tol).
    maxit : int, default=500_000
        Maximum number of sweeps.

    Returns
    -------
    phi : np.ndarray, shape (Ny, Nx)
        The converged potential field.
    hist : list of float
        Max residual / change recorded at each iteration sweep.

    Implementation Steps:
    ---------------------
    1. `phi = phi.copy()`
    2. Determine grid shape: `ny, nx = phi.shape`.
    3. Construct a 2-D coordinate grid using `np.mgrid[0:ny, 0:nx]` to calculate
       `parity = (xx + yy) % 2`.
    4. Create boolean masks for updateable cells in each color:
       `masks = [(parity == c) & ~fixed for c in (0, 1)]`  # (Red, Black)
    5. Loop `it` up to `maxit`:
       a. Track the max delta for this iteration: `d = 0.0`.
       b. For each mask `mk` in `masks`:
          - Save old values: `old = phi[mk]`.
          - Compute relaxed value:
            `phi[mk] = (1.0 - omega) * old + omega * _avg(phi)[mk]`
          - Measure change: `d = max(d, float(np.abs(phi[mk] - old).max()))`.
       c. Append `d` to `hist`.
       d. If `d < tol`, break.
    6. Return `phi, hist`.
    """
    # TODO: YOUR CODE HERE (Level 1)
    raise NotImplementedError("sor is not implemented yet. Follow the docstring steps.")


def sor_neumann(
    phi: np.ndarray,
    fixed: np.ndarray,
    free: np.ndarray,
    omega: float = 1.0,
    tol: float = 1e-10,
    maxit: int = 400_000,
) -> tuple[np.ndarray, list[float]]:
    r"""Red-Black SOR with zero-flux Neumann boundary conditions (∂φ/∂n = 0) on obstacles.

    Why Neumann Boundary Conditions?
    --------------------------------
    If obstacles are treated as fixed Dirichlet boundaries (e.g. φ = 1.0 on all obstacles),
    the harmonic potential inside narrow passages suffers exponential decay ("Formulation A" failure),
    leaving the potential essentially flat with zero gradient for the rover to navigate.

    With zero-flux Neumann walls (∂φ/∂n = 0), obstacles behave as perfectly insulated boundaries.
    Potential lines flow cleanly around obstacles without boundary-layer attenuation,
    guaranteeing smooth descent from start to goal without getting trapped in local minima!

    Discrete Implementation of ∂φ/∂n = 0:
    ------------------------------------
    In finite differences, zero flux across an obstacle wall means the obstacle cell does NOT
    contribute to or absorb potential. Instead of dividing the sum of neighbours by 4,
    we divide by the count of active *free* (non-hazard) neighbours:
        φ_{i,j}^{(k+1)} = (1 - ω) * φ_{i,j}^{(k)} + ω * ( Σ_{free neighbours} φ_{nbr} ) / c_{i,j}
    where c_{i,j} ∈ {1, 2, 3, 4} is the number of 4-connected neighbours of (i, j) that are free.

    Parameters
    ----------
    phi : np.ndarray, shape (Ny, Nx), dtype float
        Initial potential guess. Start cell has φ = 1.0, goal cell has φ = 0.0.
    fixed : np.ndarray, shape (Ny, Nx), dtype bool
        Boolean mask of Dirichlet cells (e.g. Start and Goal locations).
    free : np.ndarray, shape (Ny, Nx), dtype bool
        Boolean mask of navigable cells (`free = ~hazard`).
        Cells where `free == False` are hazard/obstacle cells.
    omega : float, default=1.0
        Relaxation parameter (typically slightly damped optimal SOR, e.g. 0.97 * omega_opt).
    tol : float, default=1e-10
        Convergence stopping tolerance.
    maxit : int, default=400_000
        Maximum sweeps.

    Returns
    -------
    phi : np.ndarray, shape (Ny, Nx)
        The converged harmonic potential field satisfying ∇²φ = 0 in free space
        and ∂φ/∂n = 0 on obstacle boundaries.
    hist : list of float
        Per-sweep convergence residuals.

    Implementation Steps:
    ---------------------
    1. `phi = phi.copy()`
    2. Convert `free` mask to float: `f = free.astype(float)`.
    3. Pre-calculate the free neighbour count `cnt` for every cell:
       `cnt = sum(np.roll(f, s, a) for a in (0, 1) for s in (1, -1))`
       Avoid division by zero in isolated/hazard pockets: `cnt = np.maximum(cnt, 1.0)`.
    4. Compute checkerboard parity:
       `yy, xx = np.mgrid[0:ny, 0:nx]`
       `parity = (xx + yy) % 2`
    5. Build Red and Black masks for updateable cells:
       A cell is updated only if it is FREE, NOT FIXED, and matches parity:
       `masks = [(parity == c) & free & ~fixed for c in (0, 1)]`
    6. Zero out hazard cells so they never introduce spurious potential:
       `phi[~free] = 0.0`
    7. Loop `it` up to `maxit`:
       a. `d = 0.0`
       b. For each mask `mk` in `masks`:
          - Masked field with free cells: `pf = phi * f`
          - Sum up free neighbour potentials:
            `free_sum = (np.roll(pf, 1, 0) + np.roll(pf, -1, 0) + np.roll(pf, 1, 1) + np.roll(pf, -1, 1))`
          - Average: `avg = free_sum / cnt`
          - Update with relaxation:
            `old = phi[mk]`
            `phi[mk] = (1.0 - omega) * old + omega * avg[mk]`
          - Delta: `d = max(d, float(np.abs(phi[mk] - old).max()))`
       c. Append `d` to `hist`.
       d. If `d < tol`, break.
    8. Return `phi, hist`.
    """
    # TODO: YOUR CODE HERE (Level 2)
    raise NotImplementedError("sor_neumann is not implemented yet. Follow the docstring steps.")
