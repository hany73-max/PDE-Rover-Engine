"""
Section 1.4: Homogeneous Linear Partial Differential Equations with Constant Coefficients.

Covers:
- (1.4.1) Complementary Function (C.F.) via the Auxiliary Equation (A.E.):
    Put D_x = m and D_y = 1 into F(D_x, D_y) = 0 ==> F(m, 1) = 0.
    - Case 1: Distinct real roots m1, m2, ..., mn
    - Case 2: Repeated roots
    - Case 3: Complex conjugate roots (including LAPLACE'S EQUATION: m = ±i, Page 33, Ex. 5)
- (1.4.2) Particular Integral (P.I.) Operator Evaluation & Short Methods:
    - Case 1: f(x, y) = exp(ax + by)
    - Case 2: f(x, y) = sin(ax + by) or cos(ax + by)
    - Case 3: f(x, y) = x^a * y^b (Binomial expansion in ascending powers of D_x/D_y)
    - Case 4: f(x, y) = exp(ax + by) * V(x, y) (Exponential Shift Rule)
    - Case 5 & 6: f(x, y) = g(ax + by)
"""

from dataclasses import dataclass
from typing import List


@dataclass
class HigherOrderProblem:
    id_name: str
    pde_string: str
    operator_F: str
    ae_polynomial: str
    roots: List[str]
    cf_solution: str
    forcing_term: str
    pi_method: str
    pi_solution: str
    general_solution: str
    special_note: str = ""


PROBLEMS = {
    "ex1_distinct": HigherOrderProblem(
        id_name="ex1_distinct",
        pde_string="(D_x^3 + 2*D_x^2*D_y - 5*D_x*D_y^2 - 6*D_y^3)z = 0",
        operator_F="F(D_x, D_y) = D_x^3 + 2*D_x^2*D_y - 5*D_x*D_y^2 - 6*D_y^3",
        ae_polynomial="m^3 + 2*m^2 - 5*m - 6 = 0  ==>  (m + 1)(m + 3)(m - 2) = 0",
        roots=["m1 = -1", "m2 = -3", "m3 = 2"],
        cf_solution="z = Φ1(y - x) + Φ2(y - 3*x) + Φ3(y + 2*x)",
        forcing_term="0 (Homogeneous)",
        pi_method="None",
        pi_solution="0",
        general_solution="z = Φ1(y - x) + Φ2(y - 3*x) + Φ3(y + 2*x)",
        special_note="Case 1: Roots are distinct real numbers.",
    ),
    "ex3_repeated": HigherOrderProblem(
        id_name="ex3_repeated",
        pde_string="(D_x^3 - D_x^2*D_y - 8*D_x*D_y^2 + 12*D_y^3)z = 0",
        operator_F="F(D_x, D_y) = D_x^3 - D_x^2*D_y - 8*D_x*D_y^2 + 12*D_y^3",
        ae_polynomial="m^3 - m^2 - 8*m + 12 = 0  ==>  (m - 2)^2 * (m + 3) = 0",
        roots=["m1 = m2 = 2 (repeated)", "m3 = -3"],
        cf_solution="z = Φ1(y + 2*x) + x*Φ2(y + 2*x) + Φ3(y - 3*x)",
        forcing_term="0 (Homogeneous)",
        pi_method="None",
        pi_solution="0",
        general_solution="z = Φ1(y + 2*x) + x*Φ2(y + 2*x) + Φ3(y - 3*x)",
        special_note="Case 2: Root m=2 is repeated twice, introducing the prefactor 'x'.",
    ),
    "ex5_laplace": HigherOrderProblem(
        id_name="ex5_laplace",
        pde_string="(D_x^2 + D_y^2)z = 0  <-- LAPLACE'S EQUATION (Page 33, Ex 5)",
        operator_F="F(D_x, D_y) = D_x^2 + D_y^2",
        ae_polynomial="m^2 + 1 = 0  ==>  m^2 = -1  ==>  m = ± i",
        roots=["m1 = i", "m2 = -i"],
        cf_solution="z = Φ1(y + i*x) + Φ2(y - i*x)",
        forcing_term="0 (Homogeneous)",
        pi_method="None",
        pi_solution="0",
        general_solution="z = Φ1(y + i*x) + Φ2(y - i*x)",
        special_note=(
            "[THE ROVER CONNECTION]: This is the exact PDE solved by the Rover Engine!\n"
            "   Analytically, any harmonic function is the real part of an analytic function f(x + iy).\n"
            "   Because crater boundaries are irregular on Mars, the Rover Engine uses the discrete\n"
            "   5-point finite difference stencil of this exact equation!"
        ),
    ),
    "pi_case1_exp": HigherOrderProblem(
        id_name="pi_case1_exp",
        pde_string="(D_x^2 - D_x*D_y - 6*D_y^2)z = exp(2*x - 3*y)",
        operator_F="F(D_x, D_y) = D_x^2 - D_x*D_y - 6*D_y^2",
        ae_polynomial="m^2 - m - 6 = 0  ==>  (m - 3)(m + 2) = 0  ==>  m = 3, -2",
        roots=["m1 = 3", "m2 = -2"],
        cf_solution="z1 = Φ1(y + 3*x) + Φ2(y - 2*x)",
        forcing_term="f(x, y) = exp(2*x - 3*y)  (a = 2, b = -3)",
        pi_method="Case 1 (Exponential): Substitute D_x -> a=2, D_y -> b=-3 into F(D_x, D_y)",
        pi_solution="F(2, -3) = (2)^2 - (2)(-3) - 6(-3)^2 = 4 + 6 - 54 = -44 != 0\n  z2 = exp(2*x - 3*y) / -44",
        general_solution="z = Φ1(y + 3*x) + Φ2(y - 2*x) - (1/44)*exp(2*x - 3*y)",
        special_note="Page 40, Ex. 2 from the lecture notes.",
    ),
    "pi_case2_trig": HigherOrderProblem(
        id_name="pi_case2_trig",
        pde_string="(D_x^2 - D_x*D_y - 6*D_y^2)z = sin(2*x - 3*y)",
        operator_F="F(D_x, D_y) = D_x^2 - D_x*D_y - 6*D_y^2",
        ae_polynomial="m^2 - m - 6 = 0  ==>  m = 3, -2",
        roots=["m1 = 3", "m2 = -2"],
        cf_solution="z1 = Φ1(y + 3*x) + Φ2(y - 2*x)",
        forcing_term="f(x, y) = sin(2*x - 3*y)  (a = 2, b = -3)",
        pi_method="Case 2 (Trig): D_x^2 -> -a^2 = -4, D_x*D_y -> -a*b = 6, D_y^2 -> -b^2 = -9",
        pi_solution="F(-4, 6, -9) = -4 - 6 - 6(-9) = -10 + 54 = 44 != 0\n  z2 = (1/44)*sin(2*x - 3*y)",
        general_solution="z = Φ1(y + 3*x) + Φ2(y - 2*x) + (1/44)*sin(2*x - 3*y)",
        special_note="Page 42, Ex. 4 from the lecture notes.",
    ),
    "pi_case3_poly": HigherOrderProblem(
        id_name="pi_case3_poly",
        pde_string="(D_x^2 - 2*D_x*D_y)z = x^3 * y",
        operator_F="F(D_x, D_y) = D_x^2 - 2*D_x*D_y = D_x^2 * [1 - 2*(D_y / D_x)]",
        ae_polynomial="m^2 - 2*m = 0  ==>  m = 0, 2",
        roots=["m1 = 0", "m2 = 2"],
        cf_solution="z1 = Φ1(y) + Φ2(y + 2*x)",
        forcing_term="f(x, y) = x^3 * y",
        pi_method="Case 3 (Polynomial): Factor out D_x^2 and expand [1 - 2*(D_y/D_x)]^-1 in ascending powers",
        pi_solution=(
            "  1/F(D_x, D_y) = (1/D_x^2) * [1 + 2*(D_y/D_x) + 4*(D_y^2/D_x^2) + ...] (x^3 * y)\n"
            "  Applying: D_y(x^3 * y) = x^3, and D_y^2(x^3 * y) = 0\n"
            "  ==> (1/D_x^2) [x^3 * y + 2*(x^4 / 4)] = (1/D_x^2) [x^3 * y + (1/2)*x^4]\n"
            "  ==> Integrating w.r.t x twice: (x^5 * y / 20) + (x^6 / 60)"
        ),
        general_solution="z = Φ1(y) + Φ2(y + 2*x) + (x^5 * y / 20) + (x^6 / 60)",
        special_note="Page 45-46, Ex. 7 from the lecture notes.",
    ),
}


def explain_higher_order(key: str = "ex5_laplace") -> None:
    prob = PROBLEMS.get(key, PROBLEMS["ex5_laplace"])
    print("=" * 75)
    print(f" [{prob.id_name}] - Higher-Order Linear PDE")
    print("=" * 75)
    print(f"PDE Equation       : {prob.pde_string}")
    print(f"Differential Op F  : {prob.operator_F}")
    print(f"Auxiliary Equation : {prob.ae_polynomial}")
    print(f"Characteristic Root: {', '.join(prob.roots)}")
    print(f"Complementary Func : {prob.cf_solution}")
    print("-" * 75)
    if prob.forcing_term != "0 (Homogeneous)":
        print(f"Forcing Term f(x,y): {prob.forcing_term}")
        print(f"P.I. Method        : {prob.pi_method}")
        print(f"Particular Integral: {prob.pi_solution}")
        print("-" * 75)
    print(f"General Solution   : {prob.general_solution}")
    if prob.special_note:
        print("-" * 75)
        print(f"Note:\n{prob.special_note}")
    print("=" * 75)


if __name__ == "__main__":
    for k in PROBLEMS:
        explain_higher_order(k)
        print()
