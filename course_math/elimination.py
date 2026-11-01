"""
Section 1.2: Derivation of Partial Differential Equations by Elimination of Arbitrary Constants.

Covers:
- Situation (1): Number of arbitrary constants < Number of independent variables
- Situation (2): Number of arbitrary constants == Number of independent variables (unique 1st order PDE)
- Situation (3): Number of arbitrary constants > Number of independent variables (higher order PDEs)
- All canonical textbook examples from Pages 6 to 10.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class EliminationExample:
    title: str
    original_relation: str
    constants: List[str]
    independent_vars: List[str]
    situation: int
    steps: List[str]
    resulting_pde: str


EXAMPLES = {
    "1": EliminationExample(
        title="Example 1 (Page 8-9): Paraboloid with Squared Constants",
        original_relation="z = a*x + b*y + a^2 + b^2",
        constants=["a", "b"],
        independent_vars=["x", "y"],
        situation=2,
        steps=[
            "Step 1: Differentiate z partially with respect to x:",
            "         ∂z/∂x = p = a",
            "Step 2: Differentiate z partially with respect to y:",
            "         ∂z/∂y = q = b",
            "Step 3: Substitute a = p and b = q back into the original equation:",
            "         z = x*(p) + y*(q) + (p)^2 + (q)^2",
        ],
        resulting_pde="z = x*(∂z/∂x) + y*(∂z/∂y) + (∂z/∂x)^2 + (∂z/∂y)^2",
    ),
    "2": EliminationExample(
        title="Example 2 (Page 9): Shifted Quadratic Surface",
        original_relation="z = (x - a)^2 + (y - b)^2",
        constants=["a", "b"],
        independent_vars=["x", "y"],
        situation=2,
        steps=[
            "Step 1: Differentiate partially with respect to x:",
            "         ∂z/∂x = p = 2*(x - a)  ==>  (x - a) = (1/2)*p",
            "Step 2: Differentiate partially with respect to y:",
            "         ∂z/∂y = q = 2*(y - b)  ==>  (y - b) = (1/2)*q",
            "Step 3: Square and add both derivative equations:",
            "         p^2 + q^2 = 4*(x - a)^2 + 4*(y - b)^2 = 4*[(x - a)^2 + (y - b)^2]",
            "Step 4: Substitute the original relation z = (x - a)^2 + (y - b)^2:",
            "         p^2 + q^2 = 4*z",
        ],
        resulting_pde="(∂z/∂x)^2 + (∂z/∂y)^2 = 4*z",
    ),
    "3": EliminationExample(
        title="Example 3(a) (Page 9-10): Linear Plane with Additive Offset",
        original_relation="z = a*(x + y) + b",
        constants=["a", "b"],
        independent_vars=["x", "y"],
        situation=2,
        steps=[
            "Step 1: Differentiate partially with respect to x:",
            "         ∂z/∂x = p = a",
            "Step 2: Differentiate partially with respect to y:",
            "         ∂z/∂y = q = a",
            "Step 3: Equating the two expressions for constant 'a':",
            "         p = q",
        ],
        resulting_pde="∂z/∂x = ∂z/∂y  (or  p - q = 0)",
    ),
    "4": EliminationExample(
        title="Situation 1 Example (Page 7): Single Constant, Two Variables",
        original_relation="z = a*x + y",
        constants=["a"],
        independent_vars=["x", "y"],
        situation=1,
        steps=[
            "Number of constants (1) < Number of independent variables (2).",
            "Step 1: Differentiate w.r.t x:  ∂z/∂x = a",
            "Step 2: Differentiate w.r.t y:  ∂z/∂y = 1",
            "Step 3: Eliminate 'a' using eq(1): z = x*(∂z/∂x) + y",
            "Note: Since ∂z/∂y = 1 contains no constant, it is already a valid PDE!",
        ],
        resulting_pde="Two valid PDEs arise: (1) z = x*p + y   and   (2) q = 1",
    ),
}


def explain_elimination(example_key: str = "1") -> None:
    ex = EXAMPLES.get(example_key, EXAMPLES["1"])
    print("=" * 70)
    print(f" {ex.title}")
    print("=" * 70)
    print(f"Given Relation      : {ex.original_relation}")
    print(f"Arbitrary Constants : {', '.join(ex.constants)}")
    print(f"Independent Vars    : {', '.join(ex.independent_vars)}")
    print(f"Situation Class     : Situation ({ex.situation})")
    print("-" * 70)
    print("Step-by-Step Derivation:")
    for step in ex.steps:
        print(f"  {step}")
    print("-" * 70)
    print(f"Resulting PDE: {ex.resulting_pde}")
    print("=" * 70)


if __name__ == "__main__":
    for k in EXAMPLES:
        explain_elimination(k)
        print()

