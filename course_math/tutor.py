"""
Interactive PDE Coursework Tutor and Syllabus Companion.

Enables students and teammates to:
1. Review step-by-step analytical derivations for every topic in Chapters 1 & 2.
2. Verify exam problems against exact textbook solutions.
3. Understand the direct mathematical bridge between Section 1.4 Laplace's equation
   and the Rover Engine.
"""

import sys
import argparse

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from course_math.elimination import EXAMPLES, explain_elimination
from course_math.first_order import PROBLEMS as FIRST_ORDER_PROBS, explain_first_order
from course_math.higher_order import PROBLEMS as HIGHER_ORDER_PROBS, explain_higher_order
from course_math.non_homogeneous import PROBLEMS as NON_HOMO_PROBS, explain_non_homogeneous


BANNER = r"""
===========================================================================
  [PDE COURSEWORK TUTOR: ANALYTICAL METHODS COMPANION]
  College Syllabus: Methods of Solving Partial Differential Equations
===========================================================================
"""


def rover_bridge_lesson() -> None:
    print("=" * 75)
    print(" [THE BRIDGE LESSON: FROM CHAPTER 1.4 TO AUTONOMOUS ROVER NAVIGATION]")
    print("=" * 75)
    print(
        """
1. IN YOUR LECTURE NOTES (Page 33, Example 5):
   You are asked to solve:
       (D_x^2 + D_y^2)z = 0   <-- Laplace's Equation

   The textbook solution:
   - Put D_x = m, D_y = 1 ==> Auxiliary Equation: m^2 + 1 = 0
   - Roots: m = +i, m = -i (Complex conjugates)
   - General Solution: z = Phi_1(y + i*x) + Phi_2(y - i*x)

2. THE REAL-WORLD ENGINEERING PROBLEM:
   - On a blank infinite sheet or a clean circle, we can use Phi_1 and Phi_2.
   - But in planetary exploration, a Mars crater has thousands of jagged rocks,
     cliffs, and irregular boundary walls!
   - You cannot write a simple pencil-and-paper formula for Phi_1 and Phi_2 that
     satisfies 10,000 irregular boundary points.

3. THE COMPUTER SCALE-UP (THE 5-POINT STENCIL):
   - We replace the continuous derivatives with second-order Taylor differences:
         d2phi/dx2 approx (phi[i+1, j] - 2*phi[i, j] + phi[i-1, j]) / h^2
         d2phi/dy2 approx (phi[i, j+1] - 2*phi[i, j] + phi[i, j-1]) / h^2
   - Adding them together yields:
         phi[i, j] = (1/4) * (phi[i+1, j] + phi[i-1, j] + phi[i, j+1] + phi[i, j-1])
   - Meaning: EVERY CELL IS SIMPLY THE ARITHMETIC AVERAGE OF ITS 4 NEIGHBOURS!

4. WHY LAPLACE GUARANTEES THE ROVER NEVER GETS TRAPPED:
   - By the Maximum Principle (proved in Section 1.4), a harmonic function
     CANNOT have local minima or maxima in the interior of the domain.
   - Extrema ONLY exist on boundaries:
         Start cell: phi = 1.0 (Highest potential)
         Goal cell : phi = 0.0 (Lowest potential)
         Crater walls: dphi/dn = 0 (No-flux Neumann insulation)
   - Because no interior local minima can exist, gradient descent (-grad phi)
     is mathematically guaranteed to guide the rover to the goal without
     ever getting stuck in a dead-end crater!
"""
    )
    print("=" * 75)


def run_all_coursework() -> None:
    print(BANNER)
    print(">>> 1. SECTION 1.2: ELIMINATION OF ARBITRARY CONSTANTS")
    for k in EXAMPLES:
        explain_elimination(k)
        print()

    print("\n>>> 2. SECTION 1.3: 1ST-ORDER METHODS (LAGRANGE, FORMS 1-4, CHARPIT)")
    for k in FIRST_ORDER_PROBS:
        explain_first_order(k)
        print()

    print("\n>>> 3. SECTION 1.4: HIGHER-ORDER LINEAR EQUATIONS (C.F. & P.I.)")
    for k in HIGHER_ORDER_PROBS:
        explain_higher_order(k)
        print()

    print("\n>>> 4. CHAPTER 2: NON-HOMOGENEOUS EQUATIONS (REDUCIBLE / IRREDUCIBLE)")
    for k in NON_HOMO_PROBS:
        explain_non_homogeneous(k)
        print()

    rover_bridge_lesson()


def interactive_menu() -> None:
    print(BANNER)
    while True:
        print("\nSelect a Semester Syllabus Module to Explore:")
        print("  [1] Section 1.2: Elimination of Arbitrary Constants")
        print("  [2] Section 1.3: First-Order Methods (Lagrange, Forms 1-4, Charpit)")
        print("  [3] Section 1.4: Higher-Order Constant Coefficients (C.F. & P.I.)")
        print("  [4] Chapter 2  : Non-Homogeneous Operators (Reducible / Irreducible)")
        print("  [5] [ROVER BRIDGE]: From Laplace (m = +/-i) to Mars Autonomous Navigation")
        print("  [6] Run All Verifications (Full Coursework Dump)")
        print("  [0] Exit")

        choice = input("\nEnter choice [0-6]: ").strip()
        print()
        if choice == "1":
            for k in EXAMPLES:
                explain_elimination(k)
        elif choice == "2":
            for k in FIRST_ORDER_PROBS:
                explain_first_order(k)
        elif choice == "3":
            for k in HIGHER_ORDER_PROBS:
                explain_higher_order(k)
        elif choice == "4":
            for k in NON_HOMO_PROBS:
                explain_non_homogeneous(k)
        elif choice == "5":
            rover_bridge_lesson()
        elif choice == "6":
            run_all_coursework()
        elif choice in ("0", "q", "exit"):
            print("Good luck with your PDE semester studies!")
            break
        else:
            print("Invalid choice, please enter 0 through 6.")


def main() -> None:
    parser = argparse.ArgumentParser(description="PDE Coursework Interactive Tutor")
    parser.add_argument("--all", action="store_true", help="Print all coursework derivations")
    parser.add_argument("--bridge", action="store_true", help="Print the Rover-PDE bridge lesson")
    args = parser.parse_args()

    if args.all:
        run_all_coursework()
    elif args.bridge:
        rover_bridge_lesson()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
