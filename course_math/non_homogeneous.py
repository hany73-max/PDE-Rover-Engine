"""
Chapter 2, Section 2.1: Non-Homogeneous Linear PDEs with Constant Coefficients.

Covers:
- Classification of Operators: Reducible vs Irreducible
    - Reducible: Can be factored into linear factors (a*D_x + b*D_y + c)
    - Irreducible: Cannot be factored into linear factors
- (2.1.1) Complementary Function (C.F.) of Reducible Operators:
    Factor: (a*D_x + b*D_y + c)^k * z = 0
    Solution: z = exp(-c*x / a) * [Φ1(a*y - b*x) + x*Φ2(a*y - b*x) + ...]  (for a != 0)
          or: z = exp(-c*y / b) * [Φ1(a*y - b*x) + x*Φ2(a*y - b*x) + ...]  (for b != 0)
- Solutions for Irreducible Operators:
    z = sum_{i=1}^inf A_i * exp(a_i*x + b_i*y) where F(a_i, b_i) = 0
- Canonical textbook examples from Pages 53 to 62.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class NonHomogeneousProblem:
    id_name: str
    equation: str
    is_reducible: bool
    factors: List[str]
    steps: List[str]
    solution: str


PROBLEMS = {
    "ex1_single_linear": NonHomogeneousProblem(
        id_name="ex1_single_linear",
        equation="(2*D_x - 3*D_y - 5)z = 0",
        is_reducible=True,
        factors=["(2*D_x - 3*D_y - 5)"],
        steps=[
            "Step 1: Check form: (a*D_x + b*D_y + c) * z = 0",
            "         Identify parameters: a = 2, b = -3, c = -5, multiplicity k = 1",
            "Step 2: Since a = 2 != 0, formula gives:",
            "         z = exp(-c*x / a) * Φ(a*y - b*x)",
            "         -c / a = -(-5) / 2 = 5/2",
            "         a*y - b*x = 2*y - (-3)*x = 2*y + 3*x",
        ],
        solution="z = exp((5/2)*x) * Φ(2*y + 3*x)   (Φ is an arbitrary function)",
    ),
    "ex5_two_factors": NonHomogeneousProblem(
        id_name="ex5_two_factors",
        equation="(2*D_x - 3*D_y + 1)(D_x + 2*D_y - 2)z = 0",
        is_reducible=True,
        factors=["Factor 1: (2*D_x - 3*D_y + 1)", "Factor 2: (D_x + 2*D_y - 2)"],
        steps=[
            "Step 1: Operator is already factored into two distinct linear factors.",
            "Step 2: Factor 1: a1 = 2, b1 = -3, c1 = 1",
            "         z1 = exp(-c1*x / a1) * Φ1(a1*y - b1*x) = exp(-x / 2) * Φ1(2*y + 3*x)",
            "Step 3: Factor 2: a2 = 1, b2 = 2, c2 = -2",
            "         z2 = exp(-c2*x / a2) * Φ2(a2*y - b2*x) = exp(2*x) * Φ2(y - 2*x)",
            "Step 4: By superposition, general solution is z = z1 + z2:",
        ],
        solution="z = exp(-x / 2)*Φ1(2*y + 3*x) + exp(2*x)*Φ2(y - 2*x)",
    ),
    "ex8_irreducible": NonHomogeneousProblem(
        id_name="ex8_irreducible",
        equation="(D_x - D_y^3)z = 0",
        is_reducible=False,
        factors=["Cannot be factored into linear factors (Irreducible)"],
        steps=[
            "Step 1: The operator F(D_x, D_y) = D_x - D_y^3 cannot be decomposed into (a*D_x + b*D_y + c).",
            "Step 2: For irreducible operators, the general solution is expressed as a series:",
            "         z = sum_{i=1}^inf A_i * exp(a_i*x + b_i*y)",
            "         subject to the characteristic relation: F(a_i, b_i) = 0",
            "Step 3: F(a_i, b_i) = a_i - b_i^3 = 0  ==>  a_i = b_i^3",
            "Step 4: Substitute a_i = b_i^3 into the exponential series:",
        ],
        solution="z = sum_{i=1}^inf A_i * exp(b_i^3 * x + b_i * y)   (A_i, b_i are constants)",
    ),
}


def explain_non_homogeneous(key: str = "ex1_single_linear") -> None:
    prob = PROBLEMS.get(key, PROBLEMS["ex1_single_linear"])
    print("=" * 75)
    print(f" [{prob.id_name}] - Chapter 2: Non-Homogeneous PDE")
    print("=" * 75)
    print(f"Given PDE      : {prob.equation}")
    print(f"Classification : {'Reducible' if prob.is_reducible else 'Irreducible'}")
    print(f"Operator Factor: {', '.join(prob.factors)}")
    print("-" * 75)
    print("Step-by-Step Analytical Derivation:")
    for step in prob.steps:
        print(f"  {step}")
    print("-" * 75)
    print(f"General Solution:\n  {prob.solution}")
    print("=" * 75)


if __name__ == "__main__":
    for k in PROBLEMS:
        explain_non_homogeneous(k)
        print()

