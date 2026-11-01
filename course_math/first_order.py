"""
Section 1.3: Methods for Solving Linear and Non-Linear First-Order PDEs.

Covers:
- (1.3.1) Lagrange's Method for Quasi-Linear PDEs: P*p + Q*q = R
- (1.3.2) Standard Form 1: f(p, q) = 0
- (1.3.3) Standard Form 2: Clairaut's Form z = p*x + q*y + f(p, q)
- (1.3.4) Standard Form 3: f(z, p, q) = 0 (Substitution u = x + a*y)
- (1.3.5) Standard Form 4: Separable f1(x, p) = f2(y, q)
- (1.3.6) Charpit's Method: Universal general solver for 1st-order non-linear PDEs
"""

from dataclasses import dataclass
from typing import List


@dataclass
class FirstOrderProblem:
    id_name: str
    category: str
    equation: str
    method_name: str
    steps: List[str]
    complete_or_general_solution: str


PROBLEMS = {
    "lagrange_ex1": FirstOrderProblem(
        id_name="lagrange_ex1",
        category="1.3.1 Lagrange's Method",
        equation="2*(∂z/∂x) - 3*(∂z/∂y) = 2*x   (or 2*p - 3*q = 2*x)",
        method_name="Lagrange Auxiliary System: dx/P = dy/Q = dz/R",
        steps=[
            "Step 1: Identify coefficients: P = 2, Q = -3, R = 2*x",
            "Step 2: Write Lagrange's auxiliary equations:",
            "         dx / 2 = dy / -3 = dz / (2*x)",
            "Step 3: Pair 1: dx / 2 = dy / -3",
            "         -3*dx - 2*dy = 0  ==>  Integrate: -3*x - 2*y = a",
            "Step 4: Pair 2: dx / 2 = dz / (2*x)",
            "         x*dx = dz  ==>  x*dx - dz = 0  ==>  Integrate: x^2 / 2 - z = b",
            "Step 5: General Solution is given by arbitrary function Φ(a, b) = 0",
        ],
        complete_or_general_solution="Φ(-3*x - 2*y, x^2 / 2 - z) = 0   (or z = x^2/2 + ψ(3*x + 2*y))",
    ),
    "lagrange_ex4": FirstOrderProblem(
        id_name="lagrange_ex4",
        category="1.3.1 Lagrange's Method (Multipliers)",
        equation="(y - z)*p + (z - x)*q = x - y",
        method_name="Lagrange's Multipliers Rule (Denominator sum = 0 ==> Numerator sum = 0)",
        steps=[
            "Step 1: Auxiliary equations: dx / (y - z) = dy / (z - x) = dz / (x - y)",
            "Step 2: Multipliers (1, 1, 1):",
            "         Denominator: (y - z) + (z - x) + (x - y) = 0",
            "         ==> dx + dy + dz = 0  ==>  Integrate: x + y + z = a",
            "Step 3: Multipliers (x, y, z):",
            "         Denominator: x*(y - z) + y*(z - x) + z*(x - y) = 0",
            "         ==> x*dx + y*dy + z*dz = 0 ==> Integrate: x^2/2 + y^2/2 + z^2/2 = b",
            "Step 4: Form the general solution relation Φ(a, b) = 0",
        ],
        complete_or_general_solution="Φ(x + y + z, x^2 + y^2 + z^2) = 0",
    ),
    "form1_ex1": FirstOrderProblem(
        id_name="form1_ex1",
        category="1.3.2 Non-Linear Form 1: f(p, q) = 0",
        equation="p^2 + p = q^2",
        method_name="Substitute p = a, q = b",
        steps=[
            "Step 1: Check form: Contains only derivatives p and q. f(p, q) = p^2 + p - q^2 = 0",
            "Step 2: Assume p = a and q = b are constants:",
            "         a^2 + a - b^2 = 0  ==>  b = ± sqrt(a^2 + a)",
            "Step 3: Integrate total differential dz = p*dx + q*dy:",
            "         dz = a*dx + b*dy  ==>  z = a*x + b*y + c",
            "Step 4: Substitute b in terms of a:",
        ],
        complete_or_general_solution="z = a*x ± sqrt(a^2 + a)*y + c   (a, c are arbitrary constants)",
    ),
    "clairaut_ex1": FirstOrderProblem(
        id_name="clairaut_ex1",
        category="1.3.3 Clairaut's Form",
        equation="z = p*x + q*y + p*q",
        method_name="Clairaut Solution: z = a*x + b*y + f(a, b)",
        steps=[
            "Step 1: Confirm equation matches Clairaut standard form: z = p*x + q*y + f(p, q)",
            "         Here, f(p, q) = p*q",
            "Step 2: By Clairaut's theorem, the complete integral is obtained directly",
            "         by replacing p -> a and q -> b (where a, b are arbitrary constants):",
        ],
        complete_or_general_solution="z = a*x + b*y + a*b",
    ),
    "form3_ex1": FirstOrderProblem(
        id_name="form3_ex1",
        category="1.3.4 Non-Linear Form 3: f(z, p, q) = 0",
        equation="z = p + q",
        method_name="Substitution u = x + a*y",
        steps=[
            "Step 1: Let u = x + a*y (where 'a' is an arbitrary constant)",
            "Step 2: By chain rule: p = dz/dx = (dz/du)*(∂u/∂x) = dz/du",
            "         q = dz/dy = (dz/du)*(∂u/∂y) = a*(dz/du)",
            "Step 3: Substitute into the PDE:",
            "         z = dz/du + a*(dz/du) = (1 + a)*(dz/du)",
            "Step 4: Separate variables:",
            "         du = (1 + a) * (dz / z)",
            "Step 5: Integrate both sides: u + c = (1 + a)*ln(z)",
            "Step 6: Substitute back u = x + a*y:",
            "         x + a*y + c = (1 + a)*ln(z)  ==>  z = e^{(x + a*y + c)/(1 + a)}",
        ],
        complete_or_general_solution="z = exp((x + a*y + c) / (1 + a))",
    ),
    "form4_ex1": FirstOrderProblem(
        id_name="form4_ex1",
        category="1.3.5 Non-Linear Form 4: Separable f1(x, p) = f2(y, q)",
        equation="p = 2*x * q^2",
        method_name="Separation of Variables: equate both to arbitrary constant 'a'",
        steps=[
            "Step 1: Separate terms containing x, p from y, q:",
            "         p / x = 2*q^2",
            "Step 2: Set both sides equal to constant 'a':",
            "         p / x = a    ==>  p = a*x",
            "         2*q^2 = a    ==>  q = ± sqrt(a / 2)",
            "Step 3: Substitute p and q into dz = p*dx + q*dy:",
            "         dz = (a*x)*dx ± sqrt(a/2)*dy",
            "Step 4: Integrate both sides directly:",
            "         z = (a/2)*x^2 ± sqrt(a/2)*y + b",
        ],
        complete_or_general_solution="z = (a/2)*x^2 ± sqrt(a/2)*y + b",
    ),
    "charpit_ex1": FirstOrderProblem(
        id_name="charpit_ex1",
        category="1.3.6 Charpit's Method",
        equation="z = p*x + q*y + p^2 + q^2",
        method_name="Charpit Auxiliary Equations",
        steps=[
            "Step 1: Define f(x, y, z, p, q) = z - p*x - q*y - p^2 - q^2 = 0",
            "Step 2: Compute partial derivatives:",
            "         fx = -p,  fy = -q,  fz = 1,  fp = -x - 2p,  fq = -y - 2q",
            "Step 3: Charpit's auxiliary equations:",
            "         dp / (fx + p*fz) = dq / (fy + q*fz) = dz / (-p*fp - q*fq) = dx / -fp = dy / -fq",
            "Step 4: Evaluate denominators for dp and dq:",
            "         fx + p*fz = -p + p*(1) = 0   ==>  dp / 0",
            "         fy + q*fz = -q + q*(1) = 0   ==>  dq / 0",
            "Step 5: Taking dp = 0 ==> p = a;  and dq = 0 ==> q = b",
            "Step 6: Substitute p=a and q=b into original equation:",
        ],
        complete_or_general_solution="z = a*x + b*y + a^2 + b^2   (Complete Integral)",
    ),
}


def explain_first_order(key: str = "lagrange_ex1") -> None:
    prob = PROBLEMS.get(key, PROBLEMS["lagrange_ex1"])
    print("=" * 75)
    print(f" [{prob.category}] - {prob.id_name}")
    print("=" * 75)
    print(f"Given PDE      : {prob.equation}")
    print(f"Solution Method: {prob.method_name}")
    print("-" * 75)
    print("Step-by-Step Analytical Derivation:")
    for step in prob.steps:
        print(f"  {step}")
    print("-" * 75)
    print(f"Complete / General Solution:\n  {prob.complete_or_general_solution}")
    print("=" * 75)


if __name__ == "__main__":
    for k in PROBLEMS:
        explain_first_order(k)
        print()

