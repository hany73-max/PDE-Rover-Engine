"""
Iterative solvers for Laplace's equation (∇²φ = 0).

Production implementations:
- omega_opt: optimal SOR relaxation factor formula (Young's theorem)
- jacobi: standard Jacobi relaxation with Dirichlet boundary conditions
- sor: Red-Black Successive Over-Relaxation (Gauss-Seidel when omega=1.0)
- sor_neumann: Red-Black SOR with zero-flux Neumann boundary conditions on obstacles
"""

import numpy as np


# ---------------------------------------------------------------------------
# Stencil Helpers
# ---------------------------------------------------------------------------

def _avg(phi: np.ndarray) -> np.ndarray:
    """Average of the 4 axis-aligned neighbours (5-point finite-difference stencil).

    np.roll shifts the 2D array along axis 0 (rows) or axis 1 (columns):
        np.roll(phi,  1, 0) -> down  (phi[i-1, j])
        np.roll(phi, -1, 0) -> up    (phi[i+1, j])
        np.roll(phi,  1, 1) -> right (phi[i, j-1])
        np.roll(phi, -1, 1) -> left  (phi[i, j+1])
    """
    return 0.25 * (
        np.roll(phi, 1, 0) + np.roll(phi, -1, 0)
        + np.roll(phi, 1, 1) + np.roll(phi, -1, 1)
    )


# ---------------------------------------------------------------------------
# Public Solvers API
# ---------------------------------------------------------------------------

def omega_opt(N: int) -> float:
    r"""Compute the theoretical optimal over-relaxation factor for an N×N Laplace grid.

    For a square Dirichlet domain of size N×N, the spectral radius of the Jacobi
    iteration matrix is:
        ρ_J = cos(π / N)

    The optimal SOR parameter ω_opt is given by Young's formula:
        ω_opt = 2 / (1 + sqrt(1 - ρ_J²)) = 2 / (1 + sin(π / N))
    """
    return 2.0 / (1.0 + np.sin(np.pi / N))


def jacobi(
    phi: np.ndarray,
    fixed: np.ndarray,
    tol: float = 1e-8,
    maxit: int = 500_000,
) -> tuple[np.ndarray, list[float]]:
    r"""Solve Laplace's equation using the standard Jacobi iterative method.

    All grid nodes at iteration (k+1) are computed simultaneously from iteration (k):
        φ_{i,j}^{(k+1)} = 1/4 * (φ_{i+1,j}^{(k)} + φ_{i-1,j}^{(k)} + φ_{i,j+1}^{(k)} + φ_{i,j-1}^{(k)})
    """
    phi = phi.copy()
    hist: list[float] = []
    for _ in range(maxit):
        new = _avg(phi)
        new[fixed] = phi[fixed]
        d = float(np.abs(new - phi).max())
        phi = new
        hist.append(d)
        if d < tol:
            break
    return phi, hist


def sor(
    phi: np.ndarray,
    fixed: np.ndarray,
    omega: float = 1.0,
    tol: float = 1e-8,
    maxit: int = 500_000,
) -> tuple[np.ndarray, list[float]]:
    r"""Solve Laplace's equation using Red-Black Successive Over-Relaxation (SOR).

    When omega = 1.0, this behaves as Gauss-Seidel relaxation.
    """
    phi = phi.copy()
    n, m = phi.shape
    yy, xx = np.mgrid[0:n, 0:m]
    parity = (xx + yy) % 2
    masks = [(parity == c) & ~fixed for c in (0, 1)]
    hist: list[float] = []
    for _ in range(maxit):
        d = 0.0
        for mk in masks:
            old = phi[mk]
            phi[mk] = (1 - omega) * old + omega * _avg(phi)[mk]
            d = max(d, float(np.abs(phi[mk] - old).max()))
        hist.append(d)
        if d < tol:
            break
    return phi, hist


def sor_neumann(
    phi: np.ndarray,
    fixed: np.ndarray,
    free: np.ndarray,
    omega: float = 1.0,
    tol: float = 1e-10,
    maxit: int = 400_000,
) -> tuple[np.ndarray, list[float]]:
    r"""Solve Laplace's equation with zero-flux Neumann boundary conditions on obstacles.

    Hazard/obstacle cells are excluded from neighbor averages, implementing ∂φ/∂n = 0.
    """
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    cnt = sum(np.roll(f, s, a) for a in (0, 1) for s in (1, -1))
    cnt = np.maximum(cnt, 1.0)
    yy, xx = np.mgrid[0:n, 0:m]
    parity = (xx + yy) % 2
    masks = [(parity == c) & free & ~fixed for c in (0, 1)]
    phi[~free] = 0.0
    hist: list[float] = []
    for _ in range(maxit):
        d = 0.0
        for mk in masks:
            pf = phi * f
            avg = (
                np.roll(pf, 1, 0) + np.roll(pf, -1, 0)
                + np.roll(pf, 1, 1) + np.roll(pf, -1, 1)
            ) / cnt
            old = phi[mk]
            phi[mk] = (1 - omega) * old + omega * avg[mk]
            d = max(d, float(np.abs(phi[mk] - old).max()))
        hist.append(d)
        if d < tol:
            break
    return phi, hist
