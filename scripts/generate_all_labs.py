"""
Comprehensive Generator for the 6 DeepLearning.AI-Style Course Labs.
Builds:
- labs/Lab_1_Elimination_of_Constants.ipynb
- labs/Lab_2_Lagrange_Method.ipynb
- labs/Lab_3_Nonlinear_Charpit.ipynb
- labs/Lab_4_HigherOrder_Operators.ipynb
- labs/Lab_5_NonHomogeneous_PDEs.ipynb
- labs/Lab_6_Mars_Rover_Capstone.ipynb
"""

import json
import os

os.makedirs("labs", exist_ok=True)


class NotebookBuilder:
    def __init__(self, filename: str, target_dir: str = "labs"):
        self.filename = filename
        self.target_dir = target_dir
        self.cells = []

    def colab_badge(self):
        url = f"https://colab.research.google.com/github/hany73-max/PDE-Rover-Engine/blob/main/labs/{self.filename}"
        badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"
        self.md(badge)

    def colab_setup(self):
        source = (
            "# 🚀 GOOGLE COLAB SETUP\n"
            "# If you are running this notebook on Google Colab, execute this cell to clone the repo and set paths:\n"
            "import os, sys\n"
            "try:\n"
            "    if 'google.colab' in str(get_ipython()):\n"
            "        if not os.path.exists('PDE-Rover-Engine'):\n"
            "            import subprocess\n"
            "            subprocess.run(['git', 'clone', 'https://github.com/hany73-max/PDE-Rover-Engine.git'], check=True)\n"
            "        os.chdir('PDE-Rover-Engine')\n"
            "        if '.' not in sys.path:\n"
            "            sys.path.insert(0, '.')\n"
            "        print('[OK] Google Colab setup complete! Connected to PDE-Rover-Engine repository.')\n"
            "except NameError:\n"
            "    pass"
        )
        self.code(source)

    def md(self, source: str):
        self.cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.strip().split("\n")]
        })

    def code(self, source: str):
        self.cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.strip().split("\n")]
        })

    def save(self):
        os.makedirs(self.target_dir, exist_ok=True)
        nb_json = {
            "cells": self.cells,
            "metadata": {
                "language_info": {"name": "python"}
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        path = os.path.join(self.target_dir, self.filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb_json, f, indent=2)
        print(f"Generated {path} with {len(self.cells)} cells.")


# ===========================================================================
# LAB 1: ELIMINATION OF ARBITRARY CONSTANTS
# ===========================================================================
def build_lab_1(solutions: bool = False, target_dir: str = 'labs'):
    nb = NotebookBuilder("Lab_1_Elimination_of_Constants.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📡 Lab 1: Origin of PDEs, Eliminating Arbitrary Constants, and Terrain Slope Maps
### *Mission Control: Reading Martian Topography & Local Slope Sensors*
**Course:** Applied Partial Differential Equations & Planetary Robotics
**Lecture Notes Reference:** Chapter 1, Sections 1.1 & 1.2 — **Notes pp. 1–10** *(PDF pp. 2–11)*

---
### 🗺️ Where You Are in the Rover Navigation Pipeline
```
📍 [Lab 1: Terrain Slopes (p, q)] ──► [Lab 2: Streamline Paths] ──► [Lab 3: Safety Buffers] ──► [Lab 4–5: Laplace Theory] ──► [Lab 6: Complete Rover Planner]
```

---
### 🧭 The Rosetta Stone: Connecting Lecture Notes to the Rover Engine

| 1. Lecture Notes Math (PDF pp. 2–11) | 2. Geometric & Physical Meaning | 3. Real Project Function (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $z = f(x, y)$ | Elevation (height) of the Martian surface at coordinates $(x, y)$ | `elev` array in [`terrain.py`](rover_path_finder/terrain.py) |
| $p = \frac{\partial z}{\partial x}, \quad q = \frac{\partial z}{\partial y}$ | Directional terrain slope along the East ($x$) and North ($y$) axes | `gy, gx = np.gradient(elev)` in [`terrain.slope_map`](rover_path_finder/terrain.py) |
| $\|\nabla z\| = \sqrt{p^2 + q^2}$ | Total steepness (slope magnitude) used to flag unsafe hills/craters (`> 0.30`) | `np.hypot(gx, gy)` inside [`terrain.slope_map(elev)`](rover_path_finder/terrain.py) |
| Eliminating arbitrary constants $(a, b)$ | Extracting a **universal slope law** $f(x, y, z, p, q) = 0$ independent of crater location $(a, b)$ | Evaluating the PDE residual `(P**2 + Q**2) - 4*Z` across the grid |

---
## 1. Intuition First: Why Do We Eliminate Arbitrary Constants?

Suppose a satellite scans a field of circular craters on Mars. Every crater has the same paraboloid bowl shape, but each sits at a different center $(a, b)$:
$$z(x, y) = (x - a)^2 + (y - b)^2$$

When the rover drives across this terrain, its onboard sensors measure its local height $z$ and the tilt of its wheels in the $x$ and $y$ directions:
$$p = \frac{\partial z}{\partial x}, \qquad q = \frac{\partial z}{\partial y}$$

The rover does **not** know the coordinates $(a, b)$ of every crater center in advance. By **eliminating the arbitrary constants $a$ and $b$** using partial differentiation, we obtain a single **Partial Differential Equation (PDE)** that relates the slope $(p, q)$ directly to the elevation $z$ at every point on every crater, regardless of where $(a, b)$ is located!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab1

%matplotlib inline
print("Lab 1 Environment Initialized! Ready for Terrain Slope Analysis.")
""")

    nb.md(r"""---
## 2. The Mathematical Recipe & Complete Lecture Notes Coverage (PDF pp. 2–11)

Before eliminating constants, let's master the **foundational definitions and classifications** from **Section 1.1 & Section 1.2** of your lecture notes (**Notes pp. 1–10 / PDF pp. 2–11**):

---
### Part A: Monge's Standard Notations, Order, and Degree (PDF pp. 2–4)

In this course, your lecture notes use **Monge's shorthand notations** for the partial derivatives of $z = f(x, y)$:
$$\boxed{p = \frac{\partial z}{\partial x}, \qquad q = \frac{\partial z}{\partial y}, \qquad r = \frac{\partial^2 z}{\partial x^2}, \qquad s = \frac{\partial^2 z}{\partial x \partial y}, \qquad t = \frac{\partial^2 z}{\partial y^2}}$$

* **Order of a PDE:** The order of the **highest partial derivative** appearing in the equation.
* **Degree of a PDE:** The **exponent (power) of that highest-order derivative**, **AFTER clearing all radicals (roots) and fractional powers** of the derivatives!

> ⚠️ **Exam Trap Alert (Notes p. 2, Equation (5) / PDF p. 3):**
> Look at Equation (5) in your lecture notes:
> $$\frac{\partial^2 z}{\partial x^2} = \sqrt{1 + \left(\frac{\partial z}{\partial y}\right)^2}$$
> * What is the **order**? The highest derivative is $\frac{\partial^2 z}{\partial x^2}$, which is **2nd order**.
> * What is the **degree**? Do **not** say 1! Because of the square root $\sqrt{\cdots}$ over a derivative, we must **square both sides first** to make the equation a polynomial in the derivatives:
>   $$\left(\frac{\partial^2 z}{\partial x^2}\right)^2 = 1 + \left(\frac{\partial z}{\partial y}\right)^2$$
>   Now the exponent on the highest derivative $\frac{\partial^2 z}{\partial x^2}$ is **$2$**, so this PDE has **Order = 2, Degree = 2**!

---
### Part B: The 4-Way Linearity Classification (Notes pp. 4–5 / PDF pp. 5–6)

How do we classify a PDE as **Linear**, **Semi-linear**, **Quasi-linear**, or **Fully Non-linear**? Your lecture notes define a clear hierarchy based on where $(x, y)$, $z$, and the highest derivatives appear:

| Classification (PDF pp. 5–6) | Highest-Order Derivatives | Coefficients of Highest Derivatives | Lower-Order Terms | Example from Lecture Notes & Rover Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **1. Linear PDE** | Appear to the **1st power** only (no products) | Depend **only on $(x, y)$** (never on $z$ or derivatives) | Also strictly **linear** in $z$ and its lower derivatives | $y\frac{\partial z}{\partial x} + x\frac{\partial z}{\partial y} = z$ or Laplace's Eq. $\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$ *(Lab 4–6 navigation potential)* |
| **2. Semi-linear PDE** | Appear to the **1st power** only | Depend **only on $(x, y)$** (never on $z$ or derivatives!) | Contain **non-linear** terms in $z$ or lower-order derivatives | $x^2\frac{\partial z}{\partial x} + y^2\frac{\partial z}{\partial y} = z^2$ *(the coefficients $x^2, y^2$ depend only on $x,y$, while the RHS has $z^2$)* |
| **3. Quasi-linear PDE** | Appear to the **1st power** only | May depend on **$z$ and/or lower-order derivatives** as well as $(x,y)$ | Can be non-linear in $z$ or lower derivatives | $(y - z)p + (z - x)q = x - y$ *(Lab 2 Lagrange streamlines where coefficients depend on $z$)* |
| **4. Non-linear PDE** | Raised to powers $>1$ (e.g., $p^2, q^2$) or multiplied together ($pq$) | Arbitrary | Arbitrary | $p^2 + q^2 = 1$ *(Lab 3 Eikonal obstacle safety buffer)* or $p^2 + q^2 = 4z$ *(Lab 1 crater slope law)* |

---
### Part C: Forming PDEs by Eliminating Arbitrary Constants — All 3 Situations (PDF pp. 7–10)

Given a surface family containing arbitrary constants, differentiating partially w.r.t. $x$ and $y$ produces two equations involving $p = \frac{\partial z}{\partial x}$ and $q = \frac{\partial z}{\partial y}$. Your lecture notes (**Notes pp. 6–8 / PDF pp. 7–9**) distinguish **three exact situations**:

#### 🔹 Situation 1: Fewer constants than independent variables ($1 < 2$) — *Notes p. 6 / PDF p. 7*
* **Rule:** Eliminating 1 constant using 2 partial derivatives gives **more than one** 1st-order PDE!
* **Lecture Notes Example ($z = \alpha x + y$):**
  * Differentiating w.r.t. $x$ gives $\frac{\partial z}{\partial x} = \alpha$, which leaves $\alpha$ in the equation unless we differentiate again ($\frac{\partial^2 z}{\partial x^2} = 0$ or $\frac{\partial^2 z}{\partial y\partial x} = 0$).
  * Differentiating w.r.t. $y$ directly eliminates $\alpha$ and yields the 1st-order PDE $\boxed{\frac{\partial z}{\partial y} = 1}$!

#### 🔹 Situation 2: Number of constants equals number of independent variables ($2 = 2$) — *Notes p. 7 / PDF p. 8*
* **Rule:** With 2 constants $(a, b)$ and 2 independent variables $(x, y)$, we have 3 equations (the original relation + the $x$-derivative + the $y$-derivative), which eliminates $(a, b)$ to yield a **unique 1st-order PDE**.
* **Worked Example 1 (Notes p. 8 / PDF pp. 9–10):** Eliminate $a, b$ from the family of planes:
  $$z = a x + b y + a^2 + b^2 \qquad \text{(1)}$$
  1. Differentiate w.r.t. $x$ (holding $y, a, b$ constant): $p = \frac{\partial z}{\partial x} = a \implies a = p \quad \text{(2)}$
  2. Differentiate w.r.t. $y$ (holding $x, a, b$ constant): $q = \frac{\partial z}{\partial y} = b \implies b = q \quad \text{(3)}$
  3. Substitute (2) and (3) into (1): $\boxed{z = p x + q y + p^2 + q^2}$ *(Clairaut form, which we solve in reverse in Lab 3!)*

#### 🔹 Situation 3: More constants than independent variables ($n > 2$) — *Notes p. 8 / PDF p. 9*
* **Rule:** First-order derivatives ($p, q$) only give 2 extra equations, which is not enough to eliminate 3 or more constants! You **must differentiate to 2nd order** ($r = z_{xx}, s = z_{xy}, t = z_{yy}$), giving a **higher-order PDE**.
* **Lecture Notes Example ($z = a x + b y + c x y$, with 3 constants $a, b, c$):**
  1. First derivatives: $p = \frac{\partial z}{\partial x} = a + c y$ and $q = \frac{\partial z}{\partial y} = b + c x$.
  2. Second derivatives immediately eliminate $a$ and $b$:
     $$\frac{\partial^2 z}{\partial x^2} = 0, \qquad \frac{\partial^2 z}{\partial y^2} = 0, \qquad \text{or} \quad \frac{\partial^2 z}{\partial x \partial y} = c \implies z = x\frac{\partial z}{\partial x} + y\frac{\partial z}{\partial y} - x y \frac{\partial^2 z}{\partial x \partial y}$$

> 📌 **PDF Page 9 Typo Alert (Notes p. 8):**
> At the bottom of page 8 in the lecture notes (PDF page 9), the notes write $\frac{\partial^2 y}{\partial x\partial y} = c$. The numerator $y$ is a printing typo in the PDF—the dependent variable is $z$, so it should be $\boxed{\frac{\partial^2 z}{\partial x\partial y} = c}$!

---
### ⚠️ Common Mistakes to Avoid
1. **Leaving $a$ or $b$ in your final answer:** A valid PDE obtained by elimination must contain only $(x, y, z, p, q)$—zero arbitrary constants may remain!
2. **Axis ordering in `np.gradient`:** In Python 2D arrays `Z[row, col]`, axis 0 is `y` (rows) and axis 1 is `x` (columns). Always call `Q, P = np.gradient(Z, dy, dx)` (just like `gy, gx = np.gradient(elev)` in [`terrain.py`](rover_path_finder/terrain.py)) so $P = \partial z/\partial x$ and $Q = \partial z/\partial y$ match the right axes!
""")

    nb.md(r"""---
## 3. 📝 Paper & Pen Challenge 1 (Notes p. 9, Example 2 / PDF p. 10)

**Problem:** Eliminate the arbitrary constants $a$ and $b$ from the family of circular paraboloid craters:
$$z = (x - a)^2 + (y - b)^2$$

**Work through these steps on paper:**
1. Differentiate partially w.r.t. $x$ to find $p = \frac{\partial z}{\partial x}$ in terms of $(x - a)$, then isolate $(x - a)$.
2. Differentiate partially w.r.t. $y$ to find $q = \frac{\partial z}{\partial y}$ in terms of $(y - b)$, then isolate $(y - b)$.
3. Substitute your expressions for $(x - a)$ and $(y - b)$ into the original equation $z = (x - a)^2 + (y - b)^2$ and clear fractions.

<details>
<summary>💡 <b>Hint 1 (Computing Partial Derivatives)</b></summary>

By the chain rule: $p = 2(x - a) \implies (x - a) = \frac{p}{2}$, and $q = 2(y - b) \implies (y - b) = \frac{q}{2}$.
</details>

<details>
<summary>💡 <b>Hint 2 (Substituting & Simplifying)</b></summary>

Substituting into $z = (x - a)^2 + (y - b)^2$ gives $z = \left(\frac{p}{2}\right)^2 + \left(\frac{q}{2}\right)^2 = \frac{p^2 + q^2}{4}$. Multiply both sides by $4$!
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ###
student_pde_1 = "p^2 + q^2 = 4z"
### END CODE HERE ###

# Run numerical verification test:
test_lab1.check_paper_challenge_1(student_pde_1)
""")
    else:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ### (≈ 1 line of code)
# Write the resulting PDE in terms of p, q, z (e.g. "... = ..."):
student_pde_1 = None
### END CODE HERE ###

# Run numerical verification test:
test_lab1.check_paper_challenge_1(student_pde_1)
""")

    nb.md(r"""---
## 4. 🚀 Rover Bridge Challenge (Elliptical Crater Basin)

Now suppose a Martian valley basin is modeled by a family of elliptical paraboloids with unknown curvatures $a$ and $b$:
$$z = \frac{1}{2} a x^2 + \frac{1}{2} b y^2$$

**On your paper:**
1. Differentiate w.r.t. $x$ to find $p = \frac{\partial z}{\partial x}$ and solve for $a$ in terms of $p$ and $x$.
2. Differentiate w.r.t. $y$ to find $q = \frac{\partial z}{\partial y}$ and solve for $b$ in terms of $q$ and $y$.
3. Substitute $a$ and $b$ back into $z = \frac{1}{2} a x^2 + \frac{1}{2} b y^2$ and multiply both sides by $2$.

<details>
<summary>💡 <b>Hint 1 (Isolating a and b)</b></summary>

Since $p = a x$ and $q = b y$, we have $a = \frac{p}{x}$ and $b = \frac{q}{y}$.
</details>

<details>
<summary>💡 <b>Hint 2 (Substituting into z)</b></summary>

Substituting gives $z = \frac{1}{2}\left(\frac{p}{x}\right)x^2 + \frac{1}{2}\left(\frac{q}{y}\right)y^2 = \frac{1}{2}(x p + y q)$. Multiply both sides by 2!
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Rover Bridge Challenge
### START CODE HERE ###
rover_basin_pde = "x*p + y*q = 2z"
### END CODE HERE ###

# Run numerical verification test:
test_lab1.check_paper_challenge_2(rover_basin_pde)
""")
    else:
        nb.code(r"""# GRADED CELL: Rover Bridge Challenge
### START CODE HERE ### (≈ 1 line of code)
# Write the resulting PDE in terms of x, y, p, q, z:
rover_basin_pde = None
### END CODE HERE ###

# Run numerical verification test:
test_lab1.check_paper_challenge_2(rover_basin_pde)
""")

    nb.md(r"""---
## 5. 💻 Python Implementation: Verifying the Crater PDE on a Grid

From Challenge 1, every paraboloid crater $z = (x - a)^2 + (y - b)^2$ satisfies $p^2 + q^2 = 4z$, meaning the **PDE residual**:
$$\text{residual}(x, y) = (p^2 + q^2) - 4z$$
must equal zero everywhere on the surface! Implement `verify_crater_pde(Z, P, Q)` below using vectorized NumPy operations.
""")

    if solutions:
        nb.code(r'''# GRADED FUNCTION: verify_crater_pde
def verify_crater_pde(Z: np.ndarray, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    # Computes the PDE residual: (p^2 + q^2) - 4*z
    ### START CODE HERE ###
    residual = (P**2 + Q**2) - 4.0 * Z
    ### END CODE HERE ###
    return residual

# Run automated test:
test_lab1.test_eliminate_constants_fn(verify_crater_pde)
''')
    else:
        nb.code(r'''# GRADED FUNCTION: verify_crater_pde
def verify_crater_pde(Z: np.ndarray, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    # Computes the PDE residual: (p^2 + q^2) - 4*z
    ### START CODE HERE ### (≈ 1 line of code)
    # Compute the residual array from P, Q, and Z:
    residual = None
    ### END CODE HERE ###
    return residual

# Run automated test:
test_lab1.test_eliminate_constants_fn(verify_crater_pde)
''')

    nb.md(r"""---
## 6. 🎨 Visualizing the Physics & Connecting to `rover_path_finder/terrain.py`

Run the cell below to inspect three views:
1. **Left:** A 3D paraboloid crater $z = (x-a)^2 + (y-b)^2$.
2. **Center:** The 2D slope vector field $(p, q) = (\partial z/\partial x, \partial z/\partial y)$ computed with the exact axis ordering `Q, P = np.gradient(Z, dy, dx)`.
3. **Right:** Calling [`terrain.slope_map(elev)`](rover_path_finder/terrain.py) from our actual rover codebase on synthetic Martian terrain to detect steep hazard regions (`|\nabla z| > 0.30`).
""")

    nb.code(r"""from rover_path_finder import terrain

x = np.linspace(-3, 3, 41)
y = np.linspace(-3, 3, 41)
X, Y = np.meshgrid(x, y)
Z = (X - 0.5)**2 + (Y + 0.5)**2  # Center at (a=0.5, b=-0.5)

dx = x[1] - x[0]
dy = y[1] - y[0]
# Axis 0 is y (rows), Axis 1 is x (cols):
Q, P = np.gradient(Z, dy, dx)

# Real project terrain & slope hazard map from rover_path_finder/terrain.py:
t_data = terrain.make_terrain(N=100, seed=42)
elev, raw_hazard = t_data["h"], t_data["raw"]
slope_mag = terrain.slope_map(elev, cell=1.0)

fig = plt.figure(figsize=(16, 4.8))

ax1 = fig.add_subplot(1, 3, 1, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='copper', alpha=0.88)
ax1.set_title("1. Analytical Crater $z = (x-a)^2 + (y-b)^2$", fontsize=11)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")

ax2 = fig.add_subplot(1, 3, 2)
ax2.contour(X, Y, Z, levels=14, cmap='copper')
ax2.quiver(X[::3, ::3], Y[::3, ::3], P[::3, ::3], Q[::3, ::3], color='crimson')
ax2.set_title(r"2. Slope Vectors $(p, q) = (\partial z/\partial x, \partial z/\partial y)$", fontsize=11)
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_aspect("equal")

ax3 = fig.add_subplot(1, 3, 3)
im = ax3.imshow(slope_mag, cmap='inferno', origin='upper')
ax3.contour(raw_hazard, levels=[0.5], colors='cyan', linewidths=1.2)
plt.colorbar(im, ax=ax3, label=r"$\|\nabla z\| = \sqrt{p^2 + q^2}$")
ax3.set_title("3. Real Engine: terrain.slope_map(elev) & Hazards", fontsize=11)
ax3.set_xlabel("x (pixels)")
ax3.set_ylabel("y (pixels)")

plt.tight_layout()
plt.show()

interior_err = np.abs(verify_crater_pde(Z, P, Q)[1:-1, 1:-1]).max()
print(f"Max interior residual |(p^2 + q^2) - 4z|: {interior_err:.4f}")
print("Lab 1 Takeaways:")
print("  1) Eliminating (a, b) produces a universal PDE relating height z to local slopes (p, q).")
print("  2) In rover_path_finder/terrain.py, slope_map(elev) computes sqrt(p^2 + q^2) to flag steep craters.")
""")

    nb.save()


# ===========================================================================
# LAB 2: LAGRANGE'S METHOD OF CHARACTERISTICS
# ===========================================================================
def build_lab_2(solutions: bool = False, target_dir: str = 'labs'):
    nb = NotebookBuilder("Lab_2_Lagrange_Method.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 🛞 Lab 2: Quasi-Linear First-Order PDEs, Lagrange's Method, and Rover Streamlines
### *Mission Control: Tracing Characteristic Trajectories Down the Potential Field*
**Course:** Applied Partial Differential Equations & Planetary Robotics
**Lecture Notes Reference:** Chapter 1, Sections 1.3.1 & 1.3.2 — **Notes pp. 11–16** *(PDF pp. 12–17)*

---
### 🗺️ Where You Are in the Rover Navigation Pipeline
```
[Lab 1: Terrain Slopes (p, q)] ──► 📍 [Lab 2: Streamline Paths (Lagrange)] ──► [Lab 3: Safety Buffers] ──► [Lab 4–5: Laplace Theory] ──► [Lab 6: Complete Rover Planner]
```

---
### 🧭 The Rosetta Stone: Connecting Lecture Notes to the Rover Engine

| 1. Lecture Notes Math (PDF pp. 12–17) | 2. Geometric & Physical Meaning | 3. Real Project Function (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $P(x,y,z)p + Q(x,y,z)q = R(x,y,z)$ | **Quasi-linear 1st-order PDE:** linear in $(p, q)$ with direction coefficients $(P, Q, R)$ | Flow / transport equation along a vector field |
| $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$ | **Lagrange's Auxiliary Equations:** ODEs governing the characteristic curves (streamlines) | Stepping `(x, y)` along the normalized gradient $(-gx, -gy)$ |
| $u(x,y,z) = c_1, \quad v(x,y,z) = c_2$ | Two independent first integrals whose intersection defines a trajectory curve | Streamline curve connecting the rover's `start` to `goal` |
| $\frac{dx}{-\partial\phi/\partial x} = \frac{dy}{-\partial\phi/\partial y}$ | **Gradient Descent Streamline:** the exact 2D path the rover drives down $\phi(x,y)$ | [`planners.descend(phi, hazard, start, goal)`](rover_path_finder/planners.py) |

---
## 1. Intuition First: Why Does Lagrange's Method Turn a PDE into a Trajectory Curve?

Recall from Calculus that a surface $z = f(x, y)$ can be written implicitly as $F(x, y, z) = f(x, y) - z = 0$, whose normal vector is $\mathbf{n} = (p, q, -1)$.
Now rewrite the quasi-linear PDE $P p + Q q = R$ as a dot product:
$$(P, Q, R) \cdot (p, q, -1) = 0$$

* Since the vector $(P, Q, R)$ is **perpendicular to the surface normal** $(p, q, -1)$ everywhere, the vector $(P, Q, R)$ must be **tangent to the surface**!
* Therefore, if the rover starts on the surface and moves with velocity $(dx/dt, dy/dt, dz/dt) = (P, Q, R)$, it traces out a curve—called a **characteristic curve (or streamline)**—given by **Lagrange's Auxiliary Equations**:
  $$\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$$
* In [`rover_path_finder/planners.py`](rover_path_finder/planners.py), once the navigation potential $\phi(x, y)$ is computed, the function [`descend()`](rover_path_finder/planners.py) steers the rover along the characteristic streamline of the velocity field $(P, Q) = (-\frac{\partial\phi}{\partial x}, -\frac{\partial\phi}{\partial y})$ from `start` to `goal`!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab2

%matplotlib inline
print("Lab 2 Environment Initialized! Ready for Streamline Trajectory Analysis.")
""")

    nb.md(r"""---
## 2. The Mathematical Recipe & All 3 Lagrange Solving Strategies (PDF pp. 12–17)

### Lagrange's Working Rule (Notes p. 11 / PDF p. 12):
To find the general solution of the quasi-linear PDE $P p + Q q = R$:
1. Write **Lagrange's Auxiliary Equations**:
   $$\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$$
2. Find **two independent first integrals** $u(x, y, z) = c_1$ and $v(x, y, z) = c_2$.
3. Write the general solution as $\Phi(u, v) = 0$ (or $u = \phi(v)$).

---
### 🛠️ How Do You Actually Solve $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$? (The 3 Lecture Notes Strategies)

Students often ask: *"Once I write $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$, how do I know which trick integrates it?"*
Your lecture notes (**Notes pp. 12–15 / PDF pp. 13–16**) teach **three distinct strategies** depending on how the variables $(x, y, z)$ are coupled:

---
#### 🔹 Strategy 1: Direct Pairing & Separation of Variables (Notes pp. 12–13, Examples 1 & 2 / PDF pp. 13–14)
* **When to use:** Two of the fractions contain **only those two variables** (the 3rd variable is missing or cancels out!).
* **📖 Worked Example 1 (Notes p. 12 / PDF p. 13):** Solve $2p - 3q = 2x$.
  1. Auxiliary equations: $\frac{dx}{2} = \frac{dy}{-3} = \frac{dz}{2x}$.
  2. **First pair ($\frac{dx}{2} = \frac{dy}{-3}$):** Contains only $dx$ and $dy$! Cross-multiply:
     $$-3\,dx = 2\,dy \implies 3x + 2y = c_1 = u$$
  3. **Second pair ($\frac{dx}{2} = \frac{dz}{2x}$):** Contains only $x$ and $z$! Multiply by $2$:
     $$x\,dx = dz \implies \frac{1}{2}x^2 - z = c_2 = v$$
  4. **General Solution:** $\Phi\left(3x + 2y,\; \frac{1}{2}x^2 - z\right) = 0$.

* **📖 Worked Example 2 (Notes pp. 12–13 / PDF p. 14):** Solve $x y p + y^2 q = z x y - 2x^2$.
  1. Auxiliary equations: $\frac{dx}{xy} = \frac{dy}{y^2} = \frac{dz}{zxy - 2x^2}$.
  2. **First pair ($\frac{dx}{xy} = \frac{dy}{y^2}$):** Cancel $y$ from both denominators to get $\frac{dx}{x} = \frac{dy}{y} \implies \ln|x| - \ln|y| = \ln|a| \implies \boxed{\frac{x}{y} = a}$.
  3. **Second pair:** Now use $y = \frac{x}{a}$ (or divide the 1st and 3rd denominators by $x$) to get $\frac{dx}{y} = \frac{dz}{zy - 2x}$, which reduces to a standard 1st-order linear ODE in $z(x)$!

---
#### 🔹 Strategy 2: Using the First Constant $a$ by Substitution to Unlock the Second Integral (Notes pp. 13–14, Example 3 / PDF pp. 14–15)
* **When to use:** One pair of fractions integrates easily to give $u(x,y,z) = a$, **but** the remaining fractions still have a pesky 3rd variable blocking integration!
* **How it works:** Temporarily replace the blocking variable using $u(x,y,z) = a$ (treating $a$ as a constant during integration!), integrate the second pair, and then **substitute the expression for $a$ back in at the very end**!
* **📖 Worked Example 3 (Notes pp. 13–14 / PDF pp. 14–15):** Solve $x^2 p + y^2 q = z^2$.
  1. **Auxiliary equations:**
     $$\frac{dx}{x^2} = \frac{dy}{y^2} = \frac{dz}{z^2}$$
  2. **First pair ($\frac{dx}{x^2} = \frac{dz}{z^2}$):** Integrate directly ($\int x^{-2}dx = -x^{-1}$):
     $$-\frac{1}{x} = -\frac{1}{z} + a' \implies \boxed{\frac{1}{x} - \frac{1}{z} = a} \qquad \text{(First Integral } u\text{)}$$
  3. **Second pair ($\frac{dx}{x^2} = \frac{dy}{y^2}$):** Integrate directly:
     $$\boxed{\frac{1}{x} - \frac{1}{y} = b} \qquad \text{(Second Integral } v\text{)}$$
  4. **How the PDF demonstrates the Substitution Trick (PDF p. 15):** Suppose your third denominator had both $x$ and $y$, e.g., if you needed to eliminate $x$ using $\frac{1}{x} = b + \frac{1}{y}$ before integrating, you treat $b$ as a constant while integrating, and once integrated, **replace $b$ back with $\left(\frac{1}{x} - \frac{1}{y}\right)$** so the final invariant contains only $(x, y, z)$!

---
#### 🔹 Strategy 3: The Equal-Fractions / Multiplier Rule (Notes pp. 14–15, Example 4 / PDF pp. 15–16)
* **When to use:** Every fraction has mixed variables $(x, y, z)$ in its denominator so **no two fractions separate directly**!
* **The Boxed Theorem (PDF p. 15):** By the algebra of equal ratios, for any multipliers $(\alpha, \beta, \gamma)$ (which can be numbers like $1, 1, 1$ or functions like $x, y, z$):
  $$\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R} = \frac{\alpha\,dx + \beta\,dy + \gamma\,dz}{\alpha P + \beta Q + \gamma R}$$
  > 🎯 **Key Insight:** If you choose multipliers $(\alpha, \beta, \gamma)$ so that the **denominator sum equals ZERO**:
  > $$\alpha P + \beta Q + \gamma R = 0 \implies \boxed{\alpha\,dx + \beta\,dy + \gamma\,dz = 0}$$
  > Then the numerator must also equal **zero**, which you can integrate immediately!

* **📖 Worked Example 4 (Notes pp. 14–15 / PDF pp. 15–16):** Solve:
  $$(y - z)p + (z - x)q = x - y$$
  1. **Auxiliary equations:**
     $$\frac{dx}{y - z} = \frac{dy}{z - x} = \frac{dz}{x - y}$$
     *(Notice that $x, y, z$ are tangled in all three denominators—direct pairing fails!)*
  2. **First Set of Multipliers $(\alpha, \beta, \gamma) = (1, 1, 1)$:**
     Add the denominators directly:
     $$(y - z) + (z - x) + (x - y) = 0$$
     Since the denominator sum is $0$, the numerator sum must also be $0$:
     $$1\cdot dx + 1\cdot dy + 1\cdot dz = 0 \implies \int dx + \int dy + \int dz = a \implies \boxed{x + y + z = a} \qquad \text{(First Integral } u\text{)}$$
  3. **Second Set of Multipliers $(\alpha, \beta, \gamma) = (x, y, z)$:**
     Multiply the top and bottom of the three fractions by $x$, $y$, and $z$ respectively and add:
     $$\text{Denominator: } x(y - z) + y(z - x) + z(x - y) = xy - xz + yz - yx + zx - zy = 0$$
     Again the denominator sum is $0$, so the numerator must vanish:
     $$x\,dx + y\,dy + z\,dz = 0 \implies \frac{1}{2}x^2 + \frac{1}{2}y^2 + \frac{1}{2}z^2 = \frac{b}{2} \implies \boxed{x^2 + y^2 + z^2 = b} \qquad \text{(Second Integral } v\text{)}$$
  4. **General Solution:** $\Phi(x + y + z,\; x^2 + y^2 + z^2) = 0$! *(Geometrically, the characteristic curves are the intersections of planes $x+y+z=a$ with spheres $x^2+y^2+z^2=b$, i.e., circles tilted in 3D space!)*

---
### ⚠️ Crucial Integration Tip: Logarithms & Ratios (`ln|x| - ln|y| = ln|c|`)
When integrating equations like $\frac{dx}{x} = \frac{dy}{y}$ (such as **Exercise 5 on Notes p. 16 / PDF p. 17**):
$$\int \frac{dx}{x} = \int \frac{dy}{y} \implies \ln|x| - \ln|y| = \ln|c_1| \implies \ln\left|\frac{x}{y}\right| = \ln|c_1| \implies \frac{x}{y} = c_1$$
Writing the constant of integration as $\ln|c_1|$ lets you combine the logarithms cleanly into a simple algebraic ratio $u = \frac{x}{y}$!
""")

    nb.md(r"""---
## 3. 📝 Paper & Pen Challenge 1 (Notes p. 16, Exercise 5 / PDF p. 17)

**Problem:** Find two independent invariants $u(x, y) = c_1$ and $v(y, z) = c_2$ for Euler's homogeneous PDE:
$$x p + y q = z$$

**Work through these steps on paper:**
1. Set up Lagrange's auxiliary equations: $\frac{dx}{x} = \frac{dy}{y} = \frac{dz}{z}$.
2. From the first pair $\frac{dx}{x} = \frac{dy}{y}$, integrate both sides to obtain the ratio $u(x, y) = c_1$.
3. From the second pair $\frac{dy}{y} = \frac{dz}{z}$, integrate both sides to obtain the ratio $v(y, z) = c_2$.

<details>
<summary>💡 <b>Hint (Combining Logarithms)</b></summary>

Since $\ln|x| - \ln|y| = \ln|x/y| = \text{const}$, the first invariant is `"x/y"` (or `"y/x"`), and similarly from $\frac{dy}{y} = \frac{dz}{z}$ the second invariant is `"y/z"` (or `"z/y"`).
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ###
student_u = "x/y"
student_v = "y/z"
### END CODE HERE ###

# Run numerical verification test:
test_lab2.check_paper_challenge_1(student_u, student_v)
""")
    else:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ### (≈ 2 lines of code)
# Enter the two invariants u(x, y) and v(y, z) as strings:
student_u = None
student_v = None
### END CODE HERE ###

# Run numerical verification test:
test_lab2.check_paper_challenge_1(student_u, student_v)
""")

    nb.md(r"""---
## 4. 🚀 Rover Bridge Challenge (Analytical Streamline Trajectory)

Suppose in a local valley near the goal $(0, 0)$, the navigation potential field is approximated by the smooth bowl:
$$\phi(x, y) = x^2 + 2y^2$$
The rover drives in the direction of steepest descent $\mathbf{v} = -\nabla\phi = \left(-\frac{\partial\phi}{\partial x}, -\frac{\partial\phi}{\partial y}\right) = (-2x, -4y)$, so any quantity $z$ carried along the streamline satisfies:
$$-2x\,p - 4y\,q = 0$$

**On your paper:**
1. Write the first pair of Lagrange's auxiliary equations: $\frac{dx}{-2x} = \frac{dy}{-4y}$.
2. Divide both denominators by $-2x y$ to separate variables: $\frac{2\,dx}{x} = \frac{dy}{y}$.
3. Integrate both sides ($2\ln|x| + \ln|k| = \ln|y|$) and exponentiate to express $y$ as a function of $x$ and arbitrary constant $k$.

<details>
<summary>💡 <b>Hint 1 (Integrating Separated Variables)</b></summary>

Integrating $\frac{dy}{y} = 2\frac{dx}{x}$ gives $\ln|y| = 2\ln|x| + C = \ln(x^2) + \ln|k| = \ln|k x^2|$.
</details>

<details>
<summary>💡 <b>Hint 2 (Removing the Logarithm)</b></summary>

Exponentiating both sides yields the parabolic family $y = k x^2$.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Rover Streamline Challenge
### START CODE HERE ###
rover_streamline = "y = k*x^2"
### END CODE HERE ###

# Run numerical verification test:
test_lab2.check_paper_challenge_2(rover_streamline)
""")
    else:
        nb.code(r"""# GRADED CELL: Rover Streamline Challenge
### START CODE HERE ### (≈ 1 line of code)
# Write the streamline curve equation in terms of x, y, and constant k:
rover_streamline = None
### END CODE HERE ###

# Run numerical verification test:
test_lab2.check_paper_challenge_2(rover_streamline)
""")

    nb.md(r"""---
## 5. 💻 Python Implementation: Numerical Characteristic Streamline Tracer

On a real Martian terrain grid, the potential $\phi(x, y)$ is stored as a 2D array rather than a simple formula. To trace Lagrange's characteristic equations $\frac{dx}{dt} = P(x, y),\; \frac{dy}{dt} = Q(x, y)$ numerically—just like [`planners.descend()`](rover_path_finder/planners.py) in our rover engine—we step forward iteratively from `start`:
$$\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta t \cdot \mathbf{v}(x_k, y_k)$$

Complete `trace_streamline_rk4` below to trace the rover's path over `steps` time steps.
""")

    if solutions:
        nb.code(r'''# GRADED FUNCTION: trace_streamline_rk4
def trace_streamline_rk4(velocity_fn, start=(1.0, 2.0), dt=0.01, steps=50):
    # Numerically traces a characteristic curve (streamline) of a quasi-linear system
    trajectory = [start]
    curr = np.array(start, dtype=float)

    ### START CODE HERE ###
    for _ in range(steps):
        vx, vy = velocity_fn(curr[0], curr[1])
        v = np.array([vx, vy], dtype=float)
        curr = curr + dt * v
        trajectory.append(tuple(curr))
    ### END CODE HERE ###

    return np.array(trajectory)

# Run automated unit test:
test_lab2.test_rk4_streamline_tracer(trace_streamline_rk4)
''')
    else:
        nb.code(r'''# GRADED FUNCTION: trace_streamline_rk4
def trace_streamline_rk4(velocity_fn, start=(1.0, 2.0), dt=0.01, steps=50):
    # Numerically traces a characteristic curve (streamline) of a quasi-linear system
    trajectory = [start]
    curr = np.array(start, dtype=float)

    ### START CODE HERE ### (≈ 4-5 lines of code)
    # Loop for `steps` iterations:
    # 1. Evaluate vx, vy = velocity_fn(curr[0], curr[1])
    # 2. Form vector v = np.array([vx, vy], dtype=float)
    # 3. Update position: curr = curr + dt * v
    # 4. Append tuple(curr) to trajectory
    pass
    ### END CODE HERE ###

    return np.array(trajectory)

# Run automated unit test:
test_lab2.test_rk4_streamline_tracer(trace_streamline_rk4)
''')

    nb.md(r"""---
## 6. 🎨 Visualizing the Physics: Exact Paper Solution vs. Numerical Streamline Tracer

Starting from $(x_0, y_0) = (1, 2)$, our paper solution $y = k x^2$ gives $2 = k(1)^2 \implies k = 2$, so the exact Lagrange characteristic curve is $y = 2x^2$.
Run the cell below to verify that your numerical tracer rides the exact same curve $y = 2x^2$ down to the goal $(0, 0)$!
""")

    nb.code(r"""def sample_velocity(x, y):
    return -2.0 * x, -4.0 * y

traj = trace_streamline_rk4(sample_velocity, start=(1.0, 2.0), dt=0.02, steps=120)

x_vals = np.linspace(-0.2, 1.2, 25)
y_vals = np.linspace(-0.2, 2.2, 25)
X, Y = np.meshgrid(x_vals, y_vals)
PHI = X**2 + 2 * Y**2
U, V = sample_velocity(X, Y)

x_exact = np.linspace(0.05, 1.0, 100)
y_exact = 2.0 * (x_exact ** 2)

plt.figure(figsize=(8.5, 6))
plt.contour(X, Y, PHI, levels=12, cmap='viridis', alpha=0.5)
plt.streamplot(X, Y, U, V, color='lightgray', density=0.9)
plt.plot(x_exact, y_exact, 'b--', linewidth=3.5, label=r"Paper Solution (Lagrange): $y = 2x^2$")
plt.plot(traj[:, 0], traj[:, 1], 'r-', linewidth=2.2, label="Numerical Tracer (Code)")
plt.plot(1.0, 2.0, 'go', markersize=9, label="Start (1, 2)")
plt.plot(0.0, 0.0, 'y*', markersize=13, label="Goal (0, 0)")
plt.title("Lagrange Characteristic Curve vs. Numerical Streamline Tracer", fontsize=12)
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.show()

print("Lab 2 Takeaways:")
print("  1) Quasi-linear PDEs P*p + Q*q = R are solved via Lagrange's auxiliary ODEs dx/P = dy/Q = dz/R.")
print("  2) Lagrange's characteristic curves are the exact physical streamlines of the rover.")
print("  3) planners.descend() in our codebase is a discrete Lagrange characteristic tracer!")
""")

    nb.save()


# ===========================================================================
# LAB 3: NON-LINEAR PDES & CHARPIT'S METHOD
# ===========================================================================
def build_lab_3(solutions: bool = False, target_dir: str = 'labs'):
    nb = NotebookBuilder("Lab_3_Nonlinear_Charpit.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📻 Lab 3: Non-Linear First-Order PDEs, Charpit's Method, and Obstacle Safety Buffers
### *Mission Control: Euclidean Distance Transforms & The Eikonal Equation*
**Course:** Applied Partial Differential Equations & Planetary Robotics
**Lecture Notes Reference:** Chapter 1, Sections 1.3.2–1.3.6 — **Notes pp. 16–26** *(PDF pp. 17–27)*

---
### 🗺️ Where You Are in the Rover Navigation Pipeline
```
[Lab 1: Terrain Slopes] ──► [Lab 2: Streamline Paths] ──► 📍 [Lab 3: Eikonal Distance & Safety Buffers] ──► [Lab 4–5: Laplace Theory] ──► [Lab 6: Complete Rover Planner]
```

---
### 🧭 The Rosetta Stone: Connecting Lecture Notes to the Rover Engine

| 1. Lecture Notes Math (PDF pp. 17–27) | 2. Geometric & Physical Meaning | 3. Real Project Function (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $f(x, y, z, p, q) = 0$ (non-linear) | 1st-order PDE containing powers or products like $p^2, q^2, pq$ | Euclidean distance & wavefront propagation |
| $p^2 + q^2 = 1$ (or $\|\nabla z\| = 1$) | **Eikonal Equation:** a distance function that grows at unit rate ($1\text{ m/m}$) away from a source | [`terrain.dilate(raw, rover_radius)`](rover_path_finder/terrain.py) (expanding obstacles by the rover's body radius) |
| $z = p x + q y + f(p, q)$ | **Clairaut's Form:** complete integral is $z = a x + b y + f(a, b)$ | Family of tangent plane wavefronts |
| $(x - x_0)^2 + (y - y_0)^2 \le R^2$ | Circular safety buffer of radius $R$ around every rock/crater pixel | `yy**2 + xx**2 <= radius**2` in `terrain.dilate` |

---
## 1. Intuition First: Why Does the Rover Need the Eikonal Equation ($p^2 + q^2 = 1$)?

A Mars rover is not a zero-size point—it has a physical width (`rover_radius`). If our path planner routes the rover's center right along the edge of a crater, its wheels will clip the crater rim!

Before solving for the navigation potential in [`terrain.py`](rover_path_finder/terrain.py), the function [`dilate(raw, radius)`](rover_path_finder/terrain.py) expands every hazard pixel outward by the **Euclidean distance** $R = \text{rover\_radius}$:
* If $z(x, y) = \sqrt{x^2 + y^2}$ denotes the Euclidean distance from a point obstacle at the origin, its partial derivatives are:
  $$p = \frac{\partial z}{\partial x} = \frac{x}{\sqrt{x^2 + y^2}}, \qquad q = \frac{\partial z}{\partial y} = \frac{y}{\sqrt{x^2 + y^2}}$$
* Squaring and adding them yields the famous **Eikonal Equation**:
  $$p^2 + q^2 = 1 \quad \Longleftrightarrow \quad \|\nabla z\| = 1$$

Because $p$ and $q$ are **squared**, this 1st-order PDE is **non-linear**, so Lagrange's method from Lab 2 cannot solve it! Instead, we use the **Four Standard Non-Linear Forms** and **Charpit's General Method** (Notes pp. 16–26 / PDF pp. 17–27).
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab3

%matplotlib inline
print("Lab 3 Environment Initialized! Ready for Non-Linear PDEs & Safety Buffers.")
""")

    nb.md(r"""---
## 2. The Mathematical Recipe: All 4 Standard Forms & Charpit's General Method (PDF pp. 17–27)

For a non-linear 1st-order PDE $f(x, y, z, p, q) = 0$, our goal is to find a **Complete Integral**—a solution containing **two arbitrary constants $(a, b)$** matching the number of independent variables $(x, y)$.

---
### 🧭 Quick Decision Table: Which Non-Linear Method Should You Use?

Before jumping into long algebra, inspect **which variables appear in the PDE**:

| Method in Notes (PDF pp. 17–27) | How to Recognize the PDE Immediately | What Appears in the PDE? | Fast Solution Recipe |
| :--- | :--- | :--- | :--- |
| **Form 1** *(Notes p. 16 / PDF p. 17)* | $f(p, q) = 0$ | **Only $p$ and $q$** (no $x, y, z$) | Set $p = a$, solve $f(a, q) = 0 \implies q = \phi(a)$, write $z = a x + \phi(a) y + c$ |
| **Form 2 (Clairaut)** *(Notes p. 18 / PDF p. 19)* | $z = p x + q y + f(p, q)$ | $z - px - qy$ equals a function of $(p, q)$ | Replace $p \to a$ and $q \to b$ directly: $z = a x + b y + f(a, b)$ *(no $+c$!)* |
| **Form 3** *(Notes p. 20 / PDF p. 21)* | $f(z, p, q) = 0$ | **Only $z, p, q$** ($x$ and $y$ are missing!) | Combine $u = x + a y \implies p = \frac{dz}{du},\; q = a\frac{dz}{du}$ and integrate the ODE for $z(u)$ |
| **Form 4 (Separable)** *(Notes p. 22 / PDF p. 23)* | $f_1(x, p) = f_2(y, q)$ | $z$ is missing, and $(x, p)$ separates from $(y, q)$ | Set $f_1(x, p) = f_2(y, q) = a$, solve for $p(x,a)$ and $q(y,a)$, integrate $dz = p\,dx + q\,dy$ |
| **Charpit's General Method** *(Notes p. 24 / PDF p. 25)* | $f(x, y, z, p, q) = 0$ | General coupling (all 5 variables or mixed $x,y,z$) | Integrate Charpit's 5-fraction auxiliary system to find $q = \psi(x,y,z,p,a)$, then integrate $dz = p\,dx + q\,dy$ |

---
### Part A: Step-by-Step Walkthrough of Each Standard Form (PDF pp. 17–25)

#### 🔹 Form 1: Equations Involving Only $p$ and $q$ — $f(p, q) = 0$ (Notes pp. 16–18 / PDF pp. 17–19)
* **Why it works:** If $p = a$ and $q = b$ are constants satisfying $f(a, b) = 0 \implies b = \phi(a)$, then integrating $dz = p\,dx + q\,dy = a\,dx + \phi(a)\,dy$ immediately gives the plane family:
  $$\boxed{z = a x + \phi(a) y + c}$$
* **📖 Worked Example 1 (Notes p. 17 / PDF p. 18):** Solve $p + q = p q$.
  1. Only $p$ and $q$ appear! Set $p = a$ and $q = b$, where $a + b = a b$.
  2. Solve for $b$ in terms of $a$: $a = b(a - 1) \implies b = \frac{a}{a - 1}$.
  3. Substitute into $z = ax + by + c$: $\boxed{z = a x + \frac{a}{a - 1}y + c}$.
* **📖 Worked Example 2 (Notes p. 17 / PDF p. 18):** Solve $p q = k$ (where $k$ is a given constant).
  1. Set $p = a, q = b$ with $a b = k \implies b = \frac{k}{a}$.
  2. Complete integral: $\boxed{z = a x + \frac{k}{a}y + c}$.

---
#### 🔹 Form 2: Clairaut's Equation — $z = p x + q y + f(p, q)$ (Notes pp. 18–19 / PDF pp. 19–20)
* **Rule:** Whenever the PDE can be written with $z = p x + q y + f(p, q)$, simply replace $p \to a$ and $q \to b$:
  $$\boxed{z = a x + b y + f(a, b)}$$
* **📖 Worked Example 2 (Notes p. 19 / PDF p. 20 — Rearranging into Clairaut's Form!):** Solve $(p + q)(z - x p - y q) = 1$.
  1. At first glance this doesn't look like Clairaut's form! Divide both sides by $(p + q)$ and isolate $z$:
     $$z - x p - y q = \frac{1}{p + q} \implies z = p x + q y + \frac{1}{p + q}$$
  2. Now it is in exact Clairaut form with $f(p, q) = \frac{1}{p + q}$! Replace $p \to a, q \to b$:
     $$\boxed{z = a x + b y + \frac{1}{a + b}}$$

---
#### 🔹 Form 3: Equations Not Involving $x$ and $y$ — $f(z, p, q) = 0$ (Notes pp. 20–22 / PDF pp. 21–23)
* **Why it works:** Since $x$ and $y$ do not appear explicitly, we seek a traveling-wave / combined-coordinate solution $z = \phi(u)$ where $\boxed{u = x + a y}$ ($a$ is an arbitrary constant).
* By the chain rule:
  $$\boxed{p = \frac{\partial z}{\partial x} = \frac{dz}{du}\frac{\partial u}{\partial x} = \frac{dz}{du}, \qquad q = \frac{\partial z}{\partial y} = \frac{dz}{du}\frac{\partial u}{\partial y} = a\frac{dz}{du}}$$
  Substituting $p = \frac{dz}{du}$ and $q = a\frac{dz}{du}$ turns the PDE $f(z, p, q) = 0$ into an **Ordinary Differential Equation (ODE)** in $z$ and $u$!
* **📖 Worked Example 1 (Notes p. 20 / PDF pp. 21–22):** Solve $9(p^2 z + q^2) = 4$.
  1. Notice $x$ and $y$ are absent! Set $u = x + a y$, so $p = \frac{dz}{du}$ and $q = a\frac{dz}{du}$.
  2. Substitute into the PDE:
     $$9\left[z\left(\frac{dz}{du}\right)^2 + a^2\left(\frac{dz}{du}\right)^2\right] = 4 \implies 9(z + a^2)\left(\frac{dz}{du}\right)^2 = 4$$
  3. Take the square root and separate variables ($z$ on the left, $u$ on the right):
     $$\frac{dz}{du} = \pm \frac{2}{3\sqrt{z + a^2}} \implies \sqrt{z + a^2}\,dz = \pm \frac{2}{3}\,du$$
  4. Integrate both sides ($\int (z+a^2)^{1/2}dz = \frac{2}{3}(z+a^2)^{3/2}$):
     $$\frac{2}{3}(z + a^2)^{3/2} = \pm \frac{2}{3}u + c' \implies (z + a^2)^{3/2} = \pm u + b = \pm(x + a y) + b$$
  5. Square both sides to get the complete integral: $\boxed{(z + a^2)^3 = (x + a y + b)^2}$.

---
#### 🔹 Form 4: Separable Equations — $f_1(x, p) = f_2(y, q)$ (Notes pp. 22–24 / PDF pp. 23–25)
* **Why it works:** When $z$ is absent and all $x, p$ terms can be moved to the left while all $y, q$ terms are moved to the right:
  $$f_1(x, p) = f_2(y, q) = a \quad (\text{arbitrary constant})$$
  Why must both sides equal a constant $a$? Because $(x, p)$ and $(y, q)$ can be varied independently! We then solve $f_1(x, p) = a$ for $p = g_1(x, a)$ and $f_2(y, q) = a$ for $q = g_2(y, a)$, and substitute into the **total differential of $z(x, y)$**:
  $$\boxed{dz = p\,dx + q\,dy \implies z = \int g_1(x, a)\,dx + \int g_2(y, a)\,dy + b}$$
* **📖 Worked Example 1 (Notes p. 23 / PDF p. 24):** Solve $p - x^2 = q + y^2$.
  1. Notice the left side depends only on $(x, p)$ and the right side depends only on $(y, q)$! Set both equal to $a$:
     $$p - x^2 = q + y^2 = a \implies p = x^2 + a, \qquad q = a - y^2$$
  2. Substitute $p$ and $q$ into $dz = p\,dx + q\,dy$:
     $$dz = (x^2 + a)\,dx + (a - y^2)\,dy$$
  3. Integrate term by term:
     $$\boxed{z = \frac{1}{3}x^3 + a x + a y - \frac{1}{3}y^3 + b = \frac{1}{3}(x^3 - y^3) + a(x + y) + b}$$

---
### Part B: Charpit's General Method & Full Walkthrough of Example 2 (Notes pp. 24–26 / PDF pp. 25–27)

What if $f(x, y, z, p, q) = 0$ contains coupled variables so none of Forms 1–4 apply?
**Charpit's Method** is the universal master algorithm! Our goal is to find a **second equation relating $p$ and $q$** (with an arbitrary constant $a$) so that we can solve for $p$ and $q$ and integrate $dz = p\,dx + q\,dy$.
To make $dz = p\,dx + q\,dy$ integrable, $(p, q)$ must satisfy **Charpit's Auxiliary Equations** (**Notes p. 25, Eq. 5 / PDF p. 26**):

$$\boxed{\frac{dp}{f_x + p f_z} = \frac{dq}{f_y + q f_z} = \frac{dz}{-p f_p - q f_q} = \frac{dx}{-f_p} = \frac{dy}{-f_q}}$$

> 💡 **See how Charpit's system automatically proves Forms 1 and 2:**
> * **Form 1 ($f(p,q)=0$):** Here $f_x = f_y = f_z = 0$, so the denominators under $dp$ and $dq$ are zero $\implies dp = 0 \implies p = a$ and $dq = 0 \implies q = b$!
> * **Form 2 (Clairaut $f = px + qy + g(p,q) - z = 0$):** Here $f_x = p,\; f_y = q,\; f_z = -1$, so $f_x + p f_z = p - p = 0$ and $f_y + q f_z = q - q = 0 \implies dp = 0, dq = 0 \implies p = a, q = b$!

---
#### 📖 Full Walkthrough: Charpit's Method on Example 2 (Notes pp. 25–26 / PDF pp. 26–27)
**Problem:** Find a complete integral of the general non-linear PDE:
$$2 z x - p x^2 - 2 q x y + p q = 0$$
*(Notice all 5 variables $x, y, z, p, q$ are coupled together—Forms 1, 2, 3, and 4 all fail here!)*

* **Step 1 (Write $f(x,y,z,p,q) = 0$ and compute all 5 partial derivatives):**
  $$f(x, y, z, p, q) = 2 z x - p x^2 - 2 q x y + p q = 0$$
  $$\begin{aligned}
  f_x &= 2z - 2px - 2qy, \qquad & f_y &= -2qx, \qquad & f_z &= 2x \\
  f_p &= -x^2 + q, \qquad & f_q &= -2xy + p
  \end{aligned}$$
  > 📌 **PDF Page 27 Typo Alert (Notes p. 26):**
  > In the printed lecture notes on page 26 (PDF page 27), there is a copy-paste typo in the intermediate list of derivatives where $f_z$ and $f_p$ were accidentally written as $-2qx$, even though **the very next line of the PDF uses the correct values $f_z = 2x$ and $f_p = -x^2 + q$**! Let's verify how the correct values simplify Charpit's denominators:
  * Denominator under $dp$: $f_x + p f_z = (2z - 2px - 2qy) + p(2x) = 2z - 2qy$
  * Denominator under $dq$: $f_y + q f_z = -2qx + q(2x) = \mathbf{0}$!

* **Step 2 (Pick the simplest fraction from Charpit's Auxiliary Equations):**
  $$\frac{dp}{2z - 2qy} = \frac{dq}{\mathbf{0}} = \frac{dz}{-p(q - x^2) - q(p - 2xy)} = \frac{dx}{x^2 - q} = \frac{dy}{2xy - p}$$
  Look at the second fraction $\frac{dq}{0}$! Since its denominator is zero, its numerator must be zero:
  $$dq = 0 \implies \boxed{q = a} \quad (\text{where } a \text{ is an arbitrary constant!})$$

* **Step 3 (Substitute $q = a$ into the original PDE to solve for $p$):**
  $$2 z x - p x^2 - 2 a x y + a p = 0 \implies p(a - x^2) = 2x(ay - z) \implies \boxed{p = \frac{2x(z - ay)}{x^2 - a}}$$

* **Step 4 (Substitute $p$ and $q$ into $dz = p\,dx + q\,dy$ and integrate!):**
  $$dz = \frac{2x(z - ay)}{x^2 - a}\,dx + a\,dy \implies \underbrace{dz - a\,dy}_{d(z - ay)} = \frac{2x(z - ay)}{x^2 - a}\,dx$$
  Notice how $dz - a\,dy = d(z - ay)$ is an exact differential! Separate $(z - ay)$ and $(x^2 - a)$:
  $$\frac{d(z - ay)}{z - ay} = \frac{2x\,dx}{x^2 - a}$$
  Integrate both sides:
  $$\ln|z - ay| = \ln|x^2 - a| + \ln|b| = \ln|b(x^2 - a)| \implies z - ay = b(x^2 - a)$$
  $$\boxed{z = a y + b(x^2 - a)}$$
  We just solved a 5-variable non-linear PDE in 4 clean steps!

---
### ⚠️ Common Mistakes to Avoid
1. **Adding an extra $+ c$ to Clairaut's solution:** In $z = ax + by + f(a,b)$, $(a, b)$ are already your two independent arbitrary constants—do not add a third constant $+ c$!
2. **Planes vs. Cones:** A single complete integral of $p^2 + q^2 = 1$ with $c=0$ is a tilted plane $z = x\cos\alpha + y\sin\alpha$; the circular distance cone $x^2 + y^2 = z^2$ is the **envelope** formed by sweeping the plane direction angle $\alpha$ through all $360^\circ$.
""")

    nb.md(r"""---
## 3. 📝 Paper & Pen Challenge 1 (Notes p. 19, Example 1 / PDF p. 20)

**Problem:** Find the complete integral of Clairaut's PDE:
$$z = p x + q y + p q$$

<details>
<summary>💡 <b>Hint (Clairaut's Rule)</b></summary>

Since the PDE is in Clairaut's form $z = px + qy + f(p,q)$ with $f(p,q) = pq$, substitute $p = a$ and $q = b$ directly without adding any extra constant.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ###
student_clairaut = "z = ax + by + ab"
### END CODE HERE ###

# Run numerical verification test:
test_lab3.check_paper_challenge_1(student_clairaut)
""")
    else:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ### (≈ 1 line of code)
# Enter the complete integral in terms of x, y, a, b:
student_clairaut = None
### END CODE HERE ###

# Run numerical verification test:
test_lab3.check_paper_challenge_1(student_clairaut)
""")

    nb.md(r"""---
## 4. 🚀 Rover Bridge Challenge (From Plane Wavefronts to the Euclidean Distance Cone)

Let's solve the Eikonal equation governing Euclidean obstacle dilation:
$$p^2 + q^2 = 1$$

**Work through the envelope derivation on paper:**
1. By **Form 1 ($f(p, q) = 0$)**, set $p = \cos\alpha$, so $q = \sin\alpha$ (since $\cos^2\alpha + \sin^2\alpha = 1$).
2. The family of planes passing through the origin $(0,0,0)$ is:
   $$z = x\cos\alpha + y\sin\alpha$$
3. To find the **envelope** over all propagation angles $\alpha \in [0, 2\pi)$, differentiate w.r.t. $\alpha$ and set to zero:
   $$\frac{\partial z}{\partial \alpha} = -x\sin\alpha + y\cos\alpha = 0$$
4. Square both equations and add them to eliminate $\alpha$:
   $$z^2 + 0^2 = (x\cos\alpha + y\sin\alpha)^2 + (-x\sin\alpha + y\cos\alpha)^2 = x^2(\cos^2\alpha + \sin^2\alpha) + y^2(\sin^2\alpha + \cos^2\alpha)$$

Simplify the right-hand side and write the resulting distance cone equation relating $x, y, z$:

<details>
<summary>💡 <b>Hint (Pythagorean Identity)</b></summary>

Using $\cos^2\alpha + \sin^2\alpha = 1$, the right-hand side simplifies to $x^2 + y^2$, giving the circular cone equation relating $x^2 + y^2$ and $z^2$.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Rover Wavefront Challenge
### START CODE HERE ###
student_envelope = "x^2 + y^2 = z^2"
### END CODE HERE ###

# Run numerical verification test:
test_lab3.check_paper_challenge_2(student_envelope)
""")
    else:
        nb.code(r"""# GRADED CELL: Rover Wavefront Challenge
### START CODE HERE ### (≈ 1 line of code)
# Write the distance cone equation relating x, y, and z:
student_envelope = None
### END CODE HERE ###

# Run numerical verification test:
test_lab3.check_paper_challenge_2(student_envelope)
""")

    nb.md(r"""---
## 5. 💻 Python Implementation: Euclidean Wavefront & Obstacle Dilation

From $x^2 + y^2 = z^2$ (shifted to a source at $(y_0, x_0)$), the positive distance field is:
$$T(x, y) = \sqrt{(x - x_0)^2 + (y - y_0)^2}$$

In Python, `np.hypot(X - source[1], Y - source[0])` evaluates this exact Euclidean distance, which is the foundation for expanding obstacles by `rover_radius` in [`terrain.dilate()`](rover_path_finder/terrain.py). Complete `compute_eikonal_wavefront` below.
""")

    if solutions:
        nb.code(r'''# GRADED FUNCTION: compute_eikonal_wavefront
def compute_eikonal_wavefront(grid_size=(50, 50), source=(25, 25)):
    # Computes the Euclidean distance field T(x, y) satisfying p^2 + q^2 = 1
    # Note: source = (row_y, col_x)
    Ny, Nx = grid_size
    Y, X = np.ogrid[:Ny, :Nx]

    ### START CODE HERE ###
    dist = np.hypot(X - source[1], Y - source[0])
    ### END CODE HERE ###

    return dist

# Run automated unit test:
test_lab3.test_eikonal_wavefront_distance(compute_eikonal_wavefront)
''')
    else:
        nb.code(r'''# GRADED FUNCTION: compute_eikonal_wavefront
def compute_eikonal_wavefront(grid_size=(50, 50), source=(25, 25)):
    # Computes the Euclidean distance field T(x, y) satisfying p^2 + q^2 = 1
    # Note: source = (row_y, col_x)
    Ny, Nx = grid_size
    Y, X = np.ogrid[:Ny, :Nx]

    ### START CODE HERE ### (≈ 1 line of code)
    # Compute Euclidean distance from (source[1], source[0]) using np.hypot:
    dist = None
    ### END CODE HERE ###

    return dist

# Run automated unit test:
test_lab3.test_eikonal_wavefront_distance(compute_eikonal_wavefront)
''')

    nb.md(r"""---
## 6. 🎨 Visualizing the Physics & Connecting to `rover_path_finder/terrain.py`

Run the cell below to see:
1. **Left:** The circular Eikonal distance field $T(x, y)$ satisfying $\|\nabla T\|^2 = p^2 + q^2 = 1$.
2. **Right:** Calling [`terrain.dilate(raw, rover_radius=3)`](rover_path_finder/terrain.py) from our rover engine to add an orange Euclidean safety buffer around every red Martian hazard!
""")

    nb.code(r"""from rover_path_finder import terrain

wavefront = compute_eikonal_wavefront((60, 60), source=(30, 30))
t_data = terrain.make_terrain(N=100, seed=42, rover_radius=3)
elev, raw_hazard, buffered_hazard = t_data["h"], t_data["raw"], t_data["hazard"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

cs = axes[0].contourf(wavefront, levels=20, cmap='plasma')
plt.colorbar(cs, ax=axes[0], label="Euclidean Distance T(x, y)")
axes[0].plot(30, 30, 'wo', markersize=9, label="Source (x0, y0)")
axes[0].set_title(r"1. Eikonal Distance Field: $\|\nabla T\|^2 = p^2 + q^2 = 1$", fontsize=12)
axes[0].legend()

safety_margin_only = buffered_hazard & (~raw_hazard)
overlay = np.zeros((100, 100, 3))
overlay[~buffered_hazard] = [0.95, 0.95, 0.95]   # Safe navigable ground
overlay[safety_margin_only] = [1.0, 0.65, 0.1]   # Euclidean dilation buffer (r <= 3)
overlay[raw_hazard] = [0.75, 0.1, 0.1]           # Raw rock/crater hazards

axes[1].imshow(overlay, origin='upper')
axes[1].set_title("2. Real Engine: terrain.dilate(raw, rover_radius=3)", fontsize=12)
axes[1].set_xlabel("x (pixels)")
axes[1].set_ylabel("y (pixels)")

plt.tight_layout()
plt.show()

print("Lab 3 Takeaways:")
print("  1) Non-linear 1st-order PDEs are solved via Standard Forms 1-4 or Charpit's Auxiliary Equations.")
print("  2) The Eikonal equation p^2 + q^2 = 1 generates the circular distance cone x^2 + y^2 = z^2.")
print("  3) terrain.dilate() uses this Euclidean distance to inflate hazards by the rover's physical radius.")
""")

    nb.save()


# ===========================================================================
# LAB 4: HIGHER-ORDER OPERATORS & LAPLACE'S EQUATION
# ===========================================================================
def build_lab_4(solutions: bool = False, target_dir: str = 'labs'):
    nb = NotebookBuilder("Lab_4_HigherOrder_Operators.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 🛡️ Lab 4: Higher-Order Homogeneous Linear PDEs & Laplace's Equation
### *Mission Control: Why Laplace's Equation $\nabla^2\phi = 0$ Guarantees Zero Local Minima*
**Course:** Applied Partial Differential Equations & Planetary Robotics
**Lecture Notes Reference:** Chapter 1, Section 1.4 — **Notes pp. 34–57** *(PDF pp. 28–51; Laplace's Equation is Example 5 on Notes p. 39 / PDF p. 33)*

---
### 🗺️ Where You Are in the Rover Navigation Pipeline
```
[Labs 1–3: Slopes, Streamlines, & Safety Buffers] ──► 📍 [Lab 4: Laplace's Equation & Harmonic Potentials] ──► [Lab 5: Reducible Operators & Corridor Decay] ──► [Lab 6: Numerical SOR Engine]
```

---
### 🧭 The Rosetta Stone: Connecting Lecture Notes to the Rover Engine

| 1. Lecture Notes Math (PDF pp. 28–51) | 2. Geometric & Physical Meaning | 3. Real Project Function (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $D_x = \frac{\partial}{\partial x}, \quad D_y = \frac{\partial}{\partial y}$ | Algebraic partial differential operators | Factoring higher-order PDEs like polynomials |
| $(D_x^2 + D_y^2)z = 0$ *(Ex. 5, Notes p. 39 / PDF p. 33)* | **Laplace's Equation:** zero net curvature; behaves like a taut soap film with no interior potholes | Governing equation of our navigation potential in [`solvers.py`](rover_path_finder/solvers.py) |
| $m^2 + 1 = 0 \implies m = \pm i$ | Complex conjugate characteristic roots of Laplace's equation | Proves the solution is a smooth **harmonic function** |
| $\nabla^2\phi \approx \frac{\phi_E + \phi_W + \phi_S + \phi_N - 4\phi_C}{h^2} = 0$ | Every interior point equals the exact average of its 4 neighbors | [`_avg(phi)`](rover_path_finder/solvers.py) in `rover_path_finder/solvers.py` |

---
## 1. Intuition First: Why Do We Need a 2nd-Order PDE (Laplace's Equation)?

In Lab 2 we saw that the rover follows the steepest descent streamline of a potential field $\phi(x, y)$ via [`planners.descend()`](rover_path_finder/planners.py).
**But how do we construct $\phi(x, y)$ so that the rover never gets trapped in an artificial pothole (local minimum) on its way to the goal?**

Imagine stretching an elastic membrane over a frame:
* If we hold the start/walls high ($\phi = 1$) and pin the goal low ($\phi = 0$), the membrane settles into mechanical equilibrium:
  $$\frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} = 0 \quad \Longleftrightarrow \quad (D_x^2 + D_y^2)\phi = 0$$
* Geometrically, $\frac{\partial^2\phi}{\partial x^2}$ is the curvature along $x$, and $\frac{\partial^2\phi}{\partial y^2}$ is the curvature along $y$.
* For their sum to be zero ($\nabla^2\phi = 0$), the surface **cannot curve upward in both $x$ and $y$ at the same time**! Since a strict local minimum requires $\phi_{xx} > 0$ and $\phi_{yy} > 0$ simultaneously (whose sum would be strictly positive, never zero), **an interior local minimum is mathematically impossible**!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab4

%matplotlib inline
print("Lab 4 Environment Initialized! Ready for Higher-Order Operators & Laplace Theory.")
""")

    nb.md(r"""---
## 2. Complete Section 1.4 Coverage: Homogeneous Operators & All 6 Particular Integral Cases (PDF pp. 28–51)

A linear PDE with constant coefficients is called **homogeneous of order $n$** when every derivative term has the same total order $n$:
$$(a_0 D_x^n + a_1 D_x^{n-1} D_y + \dots + a_n D_y^n) z = f(x, y) \quad \Longleftrightarrow \quad F(D_x, D_y) z = f(x, y)$$

Its general solution is $z = z_1\text{ (Complementary Function C.F.)} + z_2\text{ (Particular Integral P.I.)}$.

---
### Part A: Complementary Function $z_1$ (Notes pp. 35–39 / PDF pp. 29–33)
Substituting the trial wave $z = \phi(y + m x)$ into $F(D_x, D_y)z = 0$ replaces $D_x \to m$ and $D_y \to 1$, yielding the **Auxiliary Equation**:
$$F(m, 1) = a_0 m^n + a_1 m^{n-1} + \dots + a_n = 0$$

| Roots of Auxiliary Equation $F(m, 1) = 0$ | Complementary Function $z_1$ in Lecture Notes |
| :--- | :--- |
| **Case 1: Distinct roots** $m_1 \neq m_2$ *(Notes p. 36 / PDF p. 30)* | $z_1 = \phi_1(y + m_1 x) + \phi_2(y + m_2 x)$ |
| **Case 2: Repeated roots ($k$ times)** $m_1 = \dots = m_k = m$ *(Notes p. 37 / PDF p. 31)* | $z_1 = \phi_1(y + m x) + x\,\phi_2(y + m x) + \dots + x^{k-1}\phi_k(y + m x)$ |
| **Case 3: Complex roots** $m = \alpha \pm i\beta$ *(Notes p. 39 / PDF p. 33)* | $z_1 = \phi_1(y + (\alpha + i\beta)x) + \phi_2(y + (\alpha - i\beta)x)$ |

---
### 📖 Key Worked Example: Laplace's Equation (Example 5, Notes p. 39 / PDF p. 33)
**Problem:** Solve the 2D Laplace equation:
$$\frac{\partial^2 z}{\partial x^2} + \frac{\partial^2 z}{\partial y^2} = 0 \quad \Longleftrightarrow \quad (D_x^2 + D_y^2)z = 0$$
1. **Auxiliary Equation:** Set $D_x = m$ and $D_y = 1$:
   $$m^2 + 1 = 0 \implies m^2 = -1 \implies m = \pm i$$
2. **General Solution:**
   $$z = \phi_1(y + i x) + \phi_2(y - i x)$$
   Choosing complex conjugate harmonic combinations (such as $\sin(\pi x)\sinh(\pi y)$) produces smooth, real-valued harmonic surfaces!

---
### Part B: Particular Integral $z_2 = \frac{1}{F(D_x, D_y)} f(x, y)$ — The General Method & All 6 Short Cases (PDF pp. 34–51)

When the right-hand side $f(x, y) \neq 0$, your lecture notes teach **1 General Method** plus **6 Short Methods** depending on the shape of $f(x, y)$:

#### 🧭 Quick Decision Table for All 6 Particular Integral Cases (PDF pp. 34–51)

| Method in Notes | Right-Hand Side $f(x, y)$ | Fast Rule for $z_2 = \frac{1}{F(D_x, D_y)}f(x,y)$ | What if the Denominator Vanishes ($F = 0$)? |
| :--- | :--- | :--- | :--- |
| **General Method** *(Notes p. 40 / PDF p. 34)* | Any general function (e.g., $\sec^2(x+y)$) | Factor $F = \prod(D_x - m_i D_y)$ and solve each 1st-order factor via Lagrange $\frac{dx}{1} = \frac{dy}{-m} = \frac{du}{f}$ | Always works without exception! |
| **Case 1** *(Notes p. 44 / PDF p. 38)* | $e^{ax + by}$ | Replace $D_x \to a$ and $D_y \to b$: $z_2 = \frac{1}{F(a,b)}e^{ax+by}$ | If $F = (D_x - \frac{a}{b}D_y)^r G$: $z_2 = \frac{1}{G(a,b)}\frac{x^r}{r!}e^{ax+by}$ |
| **Case 2** *(Notes p. 47 / PDF p. 41)* | $\sin(ax+by)$ or $\cos(ax+by)$ | Replace $D_x^2 \to -a^2,\; D_x D_y \to -ab,\; D_y^2 \to -b^2$ | Convert to exponentials via Euler's formula $\frac{e^{i\theta} \pm e^{-i\theta}}{2}$ and apply Case 1's resonance rule |
| **Case 3** *(Notes p. 51 / PDF p. 45)* | Polynomial $x^a y^b$ | Factor out lowest power of $D_x$ (or $D_y$) and expand $\frac{1}{1-\theta} = 1 + \theta + \theta^2 + \dots$ | $\frac{1}{D_x}$ means integrating w.r.t. $x$ |
| **Case 4** *(Notes p. 53 / PDF p. 47)* | $e^{ax+by} V(x,y)$ | **Exponential Shift:** Pull $e^{ax+by}$ outside and shift $D_x \to D_x+a,\; D_y \to D_y+b$ | Apply Case 1, 2, or 3 to $V(x,y)$ after shifting |
| **Cases 5 & 6** *(Notes p. 56 / PDF p. 50)* | Any function $g(ax+by)$ | If $F(a,b)\neq 0$: integrate $g(u)$ $n$ times: $\frac{1}{F(a,b)}\int\dots\int g(u)du^n$ | **Case 6:** For $(bD_x - aD_y)^n z = g(ax+by)$: $z_2 = \frac{x^n}{n!\,b^n}g(ax+by)$ |

---
#### 🔹 The General Method (Factoring + Lagrange — Notes pp. 40–44 / PDF pp. 34–38)
* **How it works:** Factor $F(D_x, D_y) = (D_x - m_1 D_y)(D_x - m_2 D_y)$ and let $u_1 = (D_x - m_1 D_y)z$. Then $(D_x - m_2 D_y)u_1 = f(x, y)$ is a 1st-order PDE solved by Lagrange's auxiliary equations $\frac{dx}{1} = \frac{dy}{-m_2} = \frac{du_1}{f(x,y)}$ (from Lab 2!), and we repeat for each factor.
* **📖 Worked Example 1 (Notes pp. 41–43 / PDF pp. 35–37):** For $(D_x^2 - D_y^2)z = \sec^2(x + y)$, factoring $(D_x + D_y)(D_x - D_y)z = \sec^2(x + y)$ and integrating via Lagrange yields $\boxed{z_2 = \frac{x}{2}\tan(x + y)}$.

---
#### 🔹 Case 1: Exponential $f(x, y) = e^{ax + by}$ & The Resonance Rule $F(a, b) = 0$ (Notes pp. 44–47 / PDF pp. 38–41)
* **a) Non-resonant case ($F(a, b) \neq 0$):** Substitute $D_x \to a,\; D_y \to b$:
  $$\boxed{z_2 = \frac{1}{F(a, b)}e^{ax + by}}$$
  * **Example 2 (Notes p. 45 / PDF p. 39):** For $(D_x^2 - D_x D_y - 6D_y^2)z = e^{2x - 3y}$, $a = 2, b = -3 \implies F(2, -3) = 4 - (-6) - 6(9) = -44 \neq 0 \implies \boxed{z_2 = -\frac{1}{44}e^{2x - 3y}}$.
* **b) Resonant case ($F(a, b) = 0$ — Notes pp. 45–47 / PDF pp. 39–41):**
  When $F(a, b) = 0$, $\left(D_x - \frac{a}{b}D_y\right)$ is a factor of $F(D_x, D_y)$ of multiplicity $r$:
  $$F(D_x, D_y) = \left(D_x - \frac{a}{b}D_y\right)^r G(D_x, D_y), \qquad G(a, b) \neq 0$$
  Evaluate $(a, b)$ in the non-zero factor $G(a, b)$, and replace the resonant factor $\frac{1}{(D_x - \frac{a}{b}D_y)^r}$ by **multiplying by $\frac{x^r}{r!}$**:
  $$\boxed{z_2 = \frac{1}{G(a, b)} \frac{x^r}{r!} e^{ax + by}}$$
  * **📖 Worked Example 3 (Notes p. 46 / PDF p. 40):** Solve $(D_x^2 - D_x D_y - 6D_y^2)z = e^{3x + y}$.
    1. Here $a = 3, b = 1 \implies F(3, 1) = 9 - 3 - 6 = 0$!
    2. Factor the operator: $D_x^2 - D_x D_y - 6D_y^2 = (D_x - 3D_y)^1 (D_x + 2D_y)$.
    3. The resonant factor has multiplicity $r = 1$, and $G(D_x, D_y) = D_x + 2D_y \implies G(3, 1) = 3 + 2(1) = 5$.
    4. Apply the resonance formula: $\boxed{z_2 = \frac{1}{5}\frac{x^1}{1!}e^{3x + y} = \frac{x}{5}e^{3x + y}}$.

> 📌 **PDF Page 43 Typo Alert (Notes p. 49, Example 5):**
> At the bottom of Notes page 49 (PDF page 43), when evaluating $F = D_x^2 - 3D_x D_y + 2D_y^2$ on $e^{2x+3y}$ ($a=2, b=3$), the notes write $F(1,1) = 4 - 18 + 18 = 4$. The arithmetic $2^2 - 3(2)(3) + 2(3)^2 = 4 - 18 + 18 = 4$ is completely right for $(2, 3)$, so $F(1,1)$ is just a typo for $\boxed{F(2, 3) = 4}$!

---
#### 🔹 Case 2: Sine & Cosine $f(x, y) = \sin(ax+by)$ or $\cos(ax+by)$ (Notes pp. 47–51 / PDF pp. 41–45)
* **a) When the 2nd-order denominator is non-zero:** Substitute:
  $$\boxed{D_x^2 \to -a^2, \qquad D_x D_y \to -ab, \qquad D_y^2 \to -b^2}$$
  *(Watch the minus signs! For $\sin(2x - 3y)$, $a = 2, b = -3$, so $D_x^2 \to -(2^2) = -4$, $D_y^2 \to -((-3)^2) = -9$, and $D_x D_y \to -(2)(-3) = +6$).*
* **b) When the denominator vanishes (Resonance — Example 6, Notes pp. 50–51 / PDF pp. 44–45):**
  Rewrite $\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2}$ (or $\sin\theta = \frac{e^{i\theta} - e^{-i\theta}}{2i}$) and apply Case 1's resonance rule!

---
#### 🔹 Case 3: Polynomials $f(x, y) = x^a y^b$ via Binomial Series Expansion (Notes pp. 51–53 / PDF pp. 45–47)
* **How it works:** Factor out the lowest power of $D_x$ (or $D_y$) from the denominator so it takes the form $D_x^k [1 - \theta(D_x, D_y)]$, then expand $(1 - \theta)^{-1}$ as a geometric series:
  $$\boxed{\frac{1}{1 - \theta} = 1 + \theta + \theta^2 + \theta^3 + \dots, \qquad \frac{1}{1 + \theta} = 1 - \theta + \theta^2 - \theta^3 + \dots}$$
  Because $x^a y^b$ is a polynomial, its higher derivatives vanish after finitely many terms! Remember that $\frac{1}{D_x}$ means **integrating w.r.t. $x$**.
* **📖 Worked Example 7 (Notes p. 52 / PDF p. 46):** Find $z_2$ for $(D_x^2 - 2D_x D_y)z = x^3 y$.
  1. Factor out $D_x^2$:
     $$z_2 = \frac{1}{D_x^2\left(1 - \frac{2D_y}{D_x}\right)}(x^3 y) = \frac{1}{D_x^2}\left(1 + \frac{2D_y}{D_x} + \dots\right)(x^3 y)$$
  2. Since $D_y(x^3 y) = x^3$ and $D_y^2(x^3 y) = 0$, all higher terms drop out:
     $$z_2 = \frac{1}{D_x^2}\left[x^3 y + \frac{2}{D_x}(x^3)\right] = \frac{1}{D_x^2}\left(x^3 y + \frac{x^4}{2}\right) = \frac{1}{D_x}\left(\frac{x^4 y}{4} + \frac{x^5}{10}\right) = \boxed{\frac{x^5 y}{20} + \frac{x^6}{60}}$$

---
#### 🔹 Case 4: Exponential Shift $f(x, y) = e^{ax + by} V(x, y)$ (Notes pp. 53–55 / PDF pp. 47–50)
* **Exponential Shift Theorem:** Pull $e^{ax + by}$ to the front of the operator by shifting every $D_x \to D_x + a$ and $D_y \to D_y + b$:
  $$\boxed{\frac{1}{F(D_x, D_y)}\left[e^{ax + by} V(x, y)\right] = e^{ax + by} \frac{1}{F(D_x + a, D_y + b)} V(x, y)}$$
* **📖 Worked Example 10 (Notes p. 54 / PDF p. 48):** Solve $(D_x - D_y)^2 z = x e^{x + y}$.
  1. Pull $e^{x + y}$ ($a = 1, b = 1$) out front and shift $D_x \to D_x + 1,\; D_y \to D_y + 1$:
     $$(D_x + 1) - (D_y + 1) = D_x - D_y \implies z_2 = e^{x+y}\frac{1}{(D_x - D_y)^2}(x)$$
  2. Since $D_y(x) = 0$, this reduces to integrating $x$ twice w.r.t. $x$:
     $$\boxed{z_2 = e^{x + y}\frac{1}{D_x^2}(x) = \frac{x^3}{6}e^{x + y}}$$

---
#### 🔹 Cases 5 & 6: Arbitrary Function of a Linear Combination $f(x, y) = g(ax + by)$ (Notes pp. 56–57 / PDF pp. 50–51)
* **Case 5 ($F(a, b) \neq 0$ — Notes p. 56 / PDF p. 50):** Set $u = ax + by$ and integrate $g(u)$ $n$ times (where $n$ is the order of $F$):
  $$\boxed{z_2 = \frac{1}{F(a, b)} \underbrace{\int \dots \int}_{n\text{ times}} g(u)\,du^n}$$
* **Case 6 ($F(a, b) = 0$ where $F(D_x, D_y) = (b D_x - a D_y)^n$ — Notes pp. 56–57 / PDF pp. 50–51):**
  $$\boxed{z_2 = \frac{x^n}{n!\,b^n}\,g(ax + by)}$$
  * **📖 Worked Examples 14 & 15 (Notes p. 57 / PDF p. 51):**
    * **Ex. 14:** $(2D_x - 3D_y)^2 z = \tan(3x + 2y)$ ($a = 3, b = 2, n = 2$) $\implies \boxed{z_2 = \frac{x^2}{2!\cdot 2^2}\tan(3x + 2y) = \frac{x^2}{8}\tan(3x + 2y)}$.
    * **Ex. 15:** $(D_x - 2D_y)^3 z = (2x + y)^2$ ($a = 2, b = 1, n = 3$) $\implies \boxed{z_2 = \frac{x^3}{3!\cdot 1^3}(2x + y)^2 = \frac{x^3}{6}(2x + y)^2}$.

> 📌 **PDF Page 51 Typo Alert (Notes p. 57, Example 14):**
> In the solution of Example 14, the notes write $F(D_x, D_x) = (2D_x - 3D_y)^2$ with $D_x$ repeated twice in the argument list; that is a printing typo for $\boxed{F(D_x, D_y)}$.
""")

    nb.md(r"""---
## 3. 📝 Paper & Pen Challenge 1 (Laplace's Equation — Ex. 5, Notes p. 39 / PDF p. 33)

**Problem:** Find the characteristic roots $m_1, m_2$ of Laplace's equation:
$$(D_x^2 + D_y^2)z = 0$$

In Python, the imaginary unit $i = \sqrt{-1}$ is written `1j`, and $-i$ is written `-1j`.

<details>
<summary>💡 <b>Hint (Solving the Auxiliary Equation)</b></summary>

Setting $D_x = m$ and $D_y = 1$ gives $m^2 + 1 = 0 \implies m = \pm i$, which in Python are `1j` and `-1j`.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ###
m1 = 1j
m2 = -1j
### END CODE HERE ###

# Run numerical verification test:
test_lab4.check_paper_challenge_1(m1, m2)
""")
    else:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ### (≈ 2 lines of code)
# Enter the two complex roots of Laplace's equation in Python:
m1 = None
m2 = None
### END CODE HERE ###

# Run numerical verification test:
test_lab4.check_paper_challenge_1(m1, m2)
""")

    nb.md(r"""---
## 4. 📝 Paper & Pen Challenge 2 (Particular Integral — Ex. 4, Notes p. 48 / PDF p. 42)

**Problem (Notes p. 48, Example 4 / PDF p. 42):** Find the Particular Integral $z_2$ of:
$$(D_x^2 - D_x D_y - 6 D_y^2)z = \sin(2x - 3y)$$

**Work through these steps on paper:**
1. Identify $a = 2$ and $b = -3$ from $\sin(2x - 3y)$.
2. Substitute $D_x^2 \to -a^2$, $D_x D_y \to -ab$, and $D_y^2 \to -b^2$ into the operator $(D_x^2 - D_x D_y - 6 D_y^2)$.
3. Evaluate the numerical denominator and write the resulting formula for $z_2$.

<details>
<summary>💡 <b>Hint 1 (Evaluating the Substitutions)</b></summary>

With $a = 2$ and $b = -3$: $D_x^2 \to -4$, $D_x D_y \to +6$, and $D_y^2 \to -9$.
</details>

<details>
<summary>💡 <b>Hint 2 (Evaluating the Operator Denominator)</b></summary>

Denominator $= (-4) - (6) - 6(-9) = -10 + 54 = 44$, so $z_2 = \frac{1}{44}\sin(2x - 3y)$.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Particular Integral Challenge
### START CODE HERE ###
student_pi = "(1/44)*sin(2x - 3y)"
### END CODE HERE ###

# Run numerical verification test:
test_lab4.check_paper_challenge_2(student_pi)
""")
    else:
        nb.code(r"""# GRADED CELL: Particular Integral Challenge
### START CODE HERE ### (≈ 1 line of code)
# Write your Particular Integral formula in terms of x and y:
student_pi = None
### END CODE HERE ###

# Run numerical verification test:
test_lab4.check_paper_challenge_2(student_pi)
""")

    nb.md(r"""---
## 5. 💻 Python Implementation: Characteristic Operator Root Solver

To solve any homogeneous operator $(a_0 D_x^n + a_1 D_x^{n-1}D_y + \dots + a_n D_y^n)z = 0$ in Python, we pass the polynomial coefficient list `[a_0, a_1, ..., a_n]` into `np.roots(coeffs)`. Complete `solve_operator_roots` below.
""")

    if solutions:
        nb.code(r'''# GRADED FUNCTION: solve_operator_roots
def solve_operator_roots(coeffs: list[float]) -> list[complex]:
    # Finds the characteristic roots of the auxiliary equation F(m, 1) = 0
    ### START CODE HERE ###
    roots = np.roots(coeffs)
    ### END CODE HERE ###
    return list(roots)

# Run automated unit test:
test_lab4.test_characteristic_roots_solver(solve_operator_roots)
''')
    else:
        nb.code(r'''# GRADED FUNCTION: solve_operator_roots
def solve_operator_roots(coeffs: list[float]) -> list[complex]:
    # Finds the characteristic roots of the auxiliary equation F(m, 1) = 0
    ### START CODE HERE ### (≈ 1 line of code)
    # Compute the roots of `coeffs` using np.roots:
    roots = None
    ### END CODE HERE ###
    return list(roots)

# Run automated unit test:
test_lab4.test_characteristic_roots_solver(solve_operator_roots)
''')

    nb.md(r"""---
## 6. 🎨 Bridge to Lab 6: How Analytical Laplace Solutions Connect to `solvers._avg(phi)`

You might wonder: **If we know the analytical solution $z = \phi_1(y + ix) + \phi_2(y - ix)$, why do we need a numerical solver in [`solvers.py`](rover_path_finder/solvers.py)?**
* On a simple empty square, we can write a closed-form harmonic function like $\phi(x, y) = \frac{\sin(\pi x)\sinh(\pi y)}{\sinh(\pi)}$.
* On Mars, however, the map contains **thousands of irregular rock/crater pixels**—no single formula can match 10,000 arbitrary obstacle boundaries!
* When we approximate second derivatives on a uniform pixel grid ($\Delta x = \Delta y = h$):
  $$\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} \approx \frac{\phi_{i,j+1} + \phi_{i,j-1} + \phi_{i+1,j} + \phi_{i-1,j} - 4\phi_{i,j}}{h^2} = 0$$
  Laplace's equation $(D_x^2 + D_y^2)\phi = 0$ states that **every interior point equals the average of its 4 neighbors** (`_avg(phi)` in [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py))!

Run the cell below to see the analytical harmonic surface alongside the 4-neighbor average check using `solvers._avg`:
""")

    nb.code(r"""from rover_path_finder.solvers import _avg

x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.pi * X) * np.sinh(np.pi * Y) / np.sinh(np.pi)

neighbor_diff = np.abs(_avg(Z)[1:-1, 1:-1] - Z[1:-1, 1:-1])

fig = plt.figure(figsize=(13, 5.5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)
ax1.set_title(r"1. Harmonic Surface $\nabla^2\phi = 0$ (Zero Local Minima)", fontsize=11)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel(r"$\phi(x, y)$")
plt.colorbar(surf, ax=ax1, shrink=0.55)

ax2 = fig.add_subplot(1, 2, 2)
im = ax2.imshow(neighbor_diff, origin='lower', extent=[x[1], x[-2], y[1], y[-2]], cmap='magma')
plt.colorbar(im, ax=ax2, label=r"$|\mathrm{\_avg}(\phi) - \phi|$")
ax2.set_title("2. Bridge to solvers.py: 4-Neighbor Average Residual", fontsize=11)
ax2.set_xlabel("x")
ax2.set_ylabel("y")

plt.tight_layout()
plt.show()

print(f"Max difference between analytical harmonic surface and _avg(Z): {neighbor_diff.max():.6f}")
print("Lab 4 Takeaways:")
print("  1) Laplace's equation (D_x^2 + D_y^2)z = 0 has complex roots m = ±i and smooth harmonic solutions.")
print("  2) Harmonic functions obey the 4-neighbor Mean Value Property (_avg in solvers.py), preventing local traps.")
""")

    nb.save()


# ===========================================================================
# LAB 5: NON-HOMOGENEOUS LINEAR PDES & REDUCIBLE OPERATORS
# ===========================================================================
def build_lab_5(solutions: bool = False, target_dir: str = 'labs'):
    nb = NotebookBuilder("Lab_5_NonHomogeneous_PDEs.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 🔋 Lab 5: Non-Homogeneous Linear PDEs, Reducible Operators, and Narrow-Corridor Decay
### *Mission Control: Why Dirichlet Obstacles (`dirichlet_potential`) Fail in Narrow Passages*
**Course:** Applied Partial Differential Equations & Planetary Robotics
**Lecture Notes Reference:** Chapter 2, Section 2.1 — **Notes Chapter 2 pp. 1–10** *(PDF pp. 52–62; Reducible Linear Factor Rule on Ch. 2 p. 2 / PDF p. 54, Worked Ex. 5 on Ch. 2 p. 4 / PDF p. 56)*

---
### 🗺️ Where You Are in the Rover Navigation Pipeline
```
[Labs 1–3: Slopes, Streamlines, & Safety Buffers] ──► [Lab 4: Laplace Theory] ──► 📍 [Lab 5: Reducible Operators & Corridor Decay] ──► [Lab 6: Complete Rover Planner (SOR + Neumann)]
```

---
### 🧭 The Rosetta Stone: Connecting Lecture Notes to the Rover Engine

| 1. Lecture Notes Math (PDF pp. 52–62) | 2. Geometric & Physical Meaning | 3. Real Project Function (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $F(D_x, D_y)z = 0$ (non-homogeneous in order) | Operator mixing derivatives of different orders or a constant term $c$ (e.g. $aD_x + bD_y + c$) | Wave propagation coupled with exponential growth/decay |
| $(a D_x + b D_y + c)z = 0 \implies z = e^{-\frac{c}{a}x}\phi(ay - bx)$ | Every constant offset $c \neq 0$ introduces an exponential envelope $e^{-(c/a)x}$ | Exponential attenuation along a channel |
| $(F_1 \cdot F_2)z = 0 \implies z = z_1 + z_2$ | Factoring a reducible operator into linear factors and summing solutions | Superposition of decaying modes |
| Corridor gradient decay $\|\nabla\phi\| \propto e^{-\pi d / w}$ | Fixing canyon walls at $\phi=1$ causes the gradient to decay exponentially inside narrow passages of width $w$ | Why [`planners.neumann_potential`](rover_path_finder/planners.py) replaces [`planners.dirichlet_potential`](rover_path_finder/planners.py) |

---
## 1. Terminology Clarification: What Does "Non-Homogeneous" Mean in Chapter 2 of the Notes?

When you open **Chapter 2 of the lecture notes (PDF p. 52): "Non-Homogeneous Linear PDEs"**, notice a crucial distinction in terminology:
* In introductory ODEs, "non-homogeneous" usually means a non-zero right-hand side $f(x, y) \neq 0$.
* In **Chapter 2 of our PDE notes (PDF pp. 52–57)**, **"Non-Homogeneous" means the differential operator $F(D_x, D_y)$ on the left-hand side contains derivatives of different orders** (such as a 1st derivative $D_x$ mixed with a 0th-order constant term $c$), even when the right-hand side is zero:
  $$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$

---
## 2. How Does Exponential Decay Connect to `rover_path_finder/planners.py`?

In [`rover_path_finder/planners.py`](rover_path_finder/planners.py), two harmonic potential planners are implemented:
1. **Formulation A (`dirichlet_potential`):** Fixes all obstacle walls at a constant high potential $\phi = 1$ and the goal at $\phi = 0$.
2. **Formulation B (`neumann_potential`):** Treats obstacle walls as insulated zero-flux boundaries ($\partial\phi/\partial n = 0$) with a point source at `start` ($\phi=1$) and point sink at `goal` ($\phi=0$).

**Why does `dirichlet_potential` fail when the rover must pass through a narrow canyon of width $w$?**
Inside a narrow passage of width $w$ whose side walls are clamped at $\phi = 1$, the transverse profile $\sin(\pi y / w)$ introduces an effective constant term $c = \frac{\pi}{w}$ along the corridor axis $x$:
$$\left(D_x + \frac{\pi}{w}\right)\tilde{\phi} = 0 \implies \tilde{\phi}(x, y) \propto e^{-\frac{\pi}{w} x} \sin\left(\frac{\pi y}{w}\right)$$
Because of the exponential factor $e^{-\pi x / w}$, the potential flattens to $\phi \approx 1.000000$ within a few pixels of entering the canyon, causing floating-point underflow and stalling the rover!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab5

%matplotlib inline
print("Lab 5 Environment Initialized! Ready for Reducible Operators & Corridor Decay Analysis.")
""")

    nb.md(r"""---
## 3. Complete Chapter 2 Recipe: Cases (A), (B), (C), (D) & Particular Integrals (PDF pp. 52–62)

### Case (A): Single or Repeated Linear Factor $(a D_x + b D_y + c)^k z = 0$ *(Ch. 2 pp. 2–3 / PDF pp. 54–55)*

#### 1. Where does $z = e^{-\frac{c}{a}x}\phi(a y - b x)$ come from?
1. Rewrite $(a D_x + b D_y + c)z = 0$ as $a p + b q = -c z$ (a Lagrange PDE from Lab 2!).
2. Lagrange's auxiliary equations are:
   $$\frac{dx}{a} = \frac{dy}{b} = \frac{dz}{-c z}$$
3. From the first two fractions: $b\,dx - a\,dy = 0 \implies a y - b x = c_1$.
4. From the first and third fractions ($a \neq 0$): $\frac{dz}{z} = -\frac{c}{a}dx \implies z = c_2 e^{-\frac{c}{a}x}$.
5. Combining both invariants gives the **Linear Factor Theorem**:
   * **When $a \neq 0$:**
     $$\boxed{(a D_x + b D_y + c)z = 0 \implies z = e^{-\frac{c}{a}x}\,\phi(a y - b x)}$$
   * **When $a = 0$ and $b \neq 0$ (or pairing $\frac{dy}{b} = \frac{dz}{-cz}$):**
     $$\boxed{z = e^{-\frac{c}{b}y}\,\phi(a y - b x)}$$

#### 2. What if a linear factor is repeated $k$ times? $(a D_x + b D_y + c)^k z = 0$ (Ch. 2 pp. 2–3 / PDF pp. 54–55)
* **Using the $x$-exponential ($a \neq 0$):** Multiply successive arbitrary functions by $1, x, x^2, \dots, x^{k-1}$:
  $$\boxed{z = e^{-\frac{c}{a}x}\left[\phi_1(ay - bx) + x\,\phi_2(ay - bx) + x^2\,\phi_3(ay - bx) + \dots + x^{k-1}\phi_k(ay - bx)\right]}$$
* **Using the $y$-exponential ($b \neq 0$, especially when $a = 0$):** Multiply by $1, y, y^2, \dots, y^{k-1}$:
  $$\boxed{z = e^{-\frac{c}{b}y}\left[\phi_1(ay - bx) + y\,\phi_2(ay - bx) + \dots + y^{k-1}\phi_k(ay - bx)\right]}$$

> 📌 **PDF Pages 54–55 Typo Alert (Chapter 2 pp. 2–3, Examples 3 & 4):**
> * In **Example 3 (PDF p. 54):** $(2D_x - 3D_y + 2)^2 z = 0$ ($a=2, b=-3, c=2$), the first formula $z = e^{-x}[\phi_1(2y+3x) + x\phi_2(2y+3x)]$ is **100% correct**, whereas the alternative line ("Or $z = e^{\frac{2}{3}y}[\dots]$") mistakenly wrote $x\phi_2$ instead of $y\phi_2$.
> * In **Example 4 (PDF p. 55):** $(D_x - 2D_y + 1)^4 z = 0$ ($a=1, b=-2, c=1, k=4$), the bracket uses powers of $x$ ($1, x, x^2, x^3$), so the prefactor outside the bracket must be $\boxed{e^{-(c/a)x} = e^{-x}}$ (the PDF accidentally printed $e^{\frac{1}{2}y}$ outside the $x$-bracket).
> * **Exam Rule of Thumb:** Whenever $a \neq 0$, always use the standard $x$-form $e^{-(c/a)x}[\phi_1 + x\phi_2 + \dots]$!

---
### Case (B): Reducible Product of Distinct Linear Factors *(Ch. 2 pp. 3–4 / PDF pp. 55–56)*
When $F(D_x, D_y)$ factors into linear operators:
$$(a_1 D_x + b_1 D_y + c_1)(a_2 D_x + b_2 D_y + c_2)z = 0$$
by superposition, the general solution is the sum of the solutions to each factor:
$$z = e^{-\frac{c_1}{a_1}x}\Phi_1(a_1 y - b_1 x) + e^{-\frac{c_2}{a_2}x}\Phi_2(a_2 y - b_2 x)$$

#### 📖 Worked Example (Chapter 2 p. 4, Example 5 / PDF p. 56)
**Problem:** Solve:
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$
1. **First factor $(2 D_x - 3 D_y + 1)z = 0$:**
   * $a_1 = 2,\; b_1 = -3,\; c_1 = 1 \implies -\frac{c_1}{a_1}x = -\frac{1}{2}x$ and $a_1 y - b_1 x = 2y - (-3)x = 2y + 3x$.
   * Solution 1: $z_1 = e^{-x/2}\Phi_1(2y + 3x)$.
2. **Second factor $(D_x + 2 D_y - 2)z = 0$:**
   * $a_2 = 1,\; b_2 = 2,\; c_2 = -2 \implies -\frac{c_2}{a_2}x = 2x$ and $a_2 y - b_2 x = y - 2x$.
   * Solution 2: $z_2 = e^{2x}\Phi_2(y - 2x)$.
3. **General Solution:** $\boxed{z = e^{-x/2}\Phi_1(2y + 3x) + e^{2x}\Phi_2(y - 2x)}$.

*(Similarly, in **Example 7, Ch. 2 p. 5 / PDF p. 57**, $(D_x^2 - D_y^2 - 3D_x + 3D_y)z = 0$ factors by grouping as $(D_x - D_y)(D_x + D_y - 3)z = 0 \implies \boxed{z = \phi_1(y + x) + e^{3x}\phi_2(y - x)}$!)*

---
### Cases (C) & (D): Irreducible Operators *(Ch. 2 pp. 5–8 / PDF pp. 57–60)*
* **When to use Case (C):** When $F(D_x, D_y)$ cannot be factored into linear 1st-order terms—for example, $(D_x - D_y^3)z = 0$, $(D_x^2 + D_x + D_y)z = 0$, or $(D_x^2 - D_y)z = 0$.
* **Lecture Notes Rule (Ch. 2 pp. 5–6 / PDF pp. 57–58):**
  Assume an infinite exponential series trial solution:
  $$\boxed{z = \sum_{i=1}^{\infty} A_i\, e^{a_i x + b_i y} \qquad \text{subject to the characteristic relation } F(a_i, b_i) = 0}$$
* **📖 Worked Examples 8, 9, & 11 (Ch. 2 pp. 6–7 / PDF pp. 58–59):**
  1. **Example 8:** Solve $(D_x - D_y^3)z = 0$.
     * Replacing $D_x \to a_i,\; D_y \to b_i$ gives $a_i - b_i^3 = 0 \implies a_i = b_i^3$.
     * General solution: $\boxed{z = \sum_{i=1}^{\infty} A_i\, e^{b_i^3 x + b_i y}}$.
  2. **Example 9:** Solve $(D_x^2 + D_x + D_y)z = 0$.
     * Relation: $a_i^2 + a_i + b_i = 0 \implies b_i = -a_i(a_i + 1) \implies \boxed{z = \sum_{i=1}^{\infty} A_i\, e^{a_i x - a_i(a_i + 1)y}}$.
  3. **Case (D) — Combined Reducible & Irreducible Factors (Example 11, Ch. 2 p. 7 / PDF p. 59):**
     * For $(D_x - D_y - 1)(D_x - D_y^2)z = 0$: add the reducible C.F. $e^x\phi(y+x)$ and the irreducible C.F. $\sum_{i=1}^\infty A_i e^{b_i^2 x + b_i y}$:
       $$\boxed{z = e^x \phi(y + x) + \sum_{i=1}^{\infty} A_i e^{b_i^2 x + b_i y}}$$

---
### Part D: Particular Integrals in Chapter 2 & The Conjugate Operator Trick (Ch. 2 pp. 8–10 / PDF pp. 60–62)

To find $z_2 = \frac{1}{F(D_x, D_y)}f(x, y)$ when $F(D_x, D_y)$ is non-homogeneous in order, the lecture notes highlight **two essential techniques**:

#### 1. Polynomial Expansion by Factoring Out the Lowest Derivative (Example 12, Ch. 2 p. 8 / PDF p. 60)
* **Problem:** Find the Particular Integral of $(D_x^2 - D_y^2 + D_x)z = x^2 + 2y$.
  * Factor out the **lowest-order term $D_x$** from the denominator:
    $$z_2 = \frac{1}{D_x\left[1 - \left(\frac{D_y^2}{D_x} - D_x\right)\right]}(x^2 + 2y) = \frac{1}{D_x}\left[1 + \left(\frac{D_y^2}{D_x} - D_x\right) + \left(\frac{D_y^2}{D_x} - D_x\right)^2 + \dots\right](x^2 + 2y)$$
  * Since $D_y^2(x^2 + 2y) = 0$, all $D_y^2$ terms vanish, leaving:
    $$z_2 = \frac{1}{D_x}\left(1 - D_x + D_x^2\right)(x^2 + 2y) = \frac{1}{D_x}\left[(x^2 + 2y) - 2x + 2\right] = \boxed{\frac{x^3}{3} + 2xy - x^2 + 2x}$$

#### 2. The Conjugate Operator Trick for $\sin/\cos$ When a 1st Derivative Remains! (Example 14, Ch. 2 pp. 9–10 / PDF pp. 61–62)
* **Problem:** Solve $(D_x^2 - D_y)z = \sin(x - 2y)$.
  1. **Complementary Function $z_1$:** Since $a_i^2 - b_i = 0 \implies b_i = a_i^2$, $z_1 = \sum_{i=1}^\infty A_i e^{a_i x + a_i^2 y}$.
  2. **Particular Integral $z_2$:** For $\sin(x - 2y)$, $a = 1$ and $b = -2$.
     * The sine shortcut only replaces **2nd-order derivatives** ($D_x^2 \to -a^2 = -1$, $D_y^2 \to -b^2 = -4$), leaving a 1st-order $D_y$ in the denominator:
       $$z_2 = \frac{1}{D_x^2 - D_y}\sin(x - 2y) = \frac{1}{-1 - D_y}\sin(x - 2y)$$
     * **The Conjugate Trick:** Multiply top and bottom by the **conjugate operator $(-1 + D_y)$** to turn the denominator into $1 - D_y^2$:
       $$z_2 = \frac{-1 + D_y}{(-1 - D_y)(-1 + D_y)}\sin(x - 2y) = \frac{-1 + D_y}{1 - D_y^2}\sin(x - 2y)$$
     * Now substitute $D_y^2 \to -b^2 = -(-2)^2 = -4$ in the denominator:
       $$z_2 = \frac{-1 + D_y}{1 - (-4)}\sin(x - 2y) = \frac{1}{5}(-1 + D_y)\sin(x - 2y)$$
     * Finally, apply $(-1 + D_y)$ to $\sin(x - 2y)$ (where $D_y[\sin(x - 2y)] = -2\cos(x - 2y)$):
       $$\boxed{z_2 = \frac{1}{5}\big[-\sin(x - 2y) - 2\cos(x - 2y)\big]}$$
""")

    nb.md(r"""---
## 4. 📝 Paper & Pen Challenge 1 (Chapter 2 p. 4, Example 5 / PDF p. 56)

**Problem:** Find the general solution of the reducible PDE:
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$

Write the general solution using `exp(...)`, `Phi1(...)`, and `Phi2(...)`:

<details>
<summary>💡 <b>Hint 1 (First Factor)</b></summary>

For $(2 D_x - 3 D_y + 1)$, $a_1=2, b_1=-3, c_1=1 \implies \text{exp}(-x/2)\text{*Phi1}(2y + 3x)$.
</details>

<details>
<summary>💡 <b>Hint 2 (Second Factor & Sum)</b></summary>

For $(D_x + 2 D_y - 2)$, $a_2=1, b_2=2, c_2=-2 \implies \text{exp}(2x)\text{*Phi2}(y - 2x)$. Add both terms together.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ###
student_solution = "exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x)"
### END CODE HERE ###

# Run numerical verification test:
test_lab5.check_paper_challenge_1(student_solution)
""")
    else:
        nb.code(r"""# GRADED CELL: Paper Challenge 1
### START CODE HERE ### (≈ 1 line of code)
# Enter your general solution string using exp(...), Phi1(...), and Phi2(...):
student_solution = None
### END CODE HERE ###

# Run numerical verification test:
test_lab5.check_paper_challenge_1(student_solution)
""")

    nb.md(r"""---
## 5. 🚀 Paper & Pen Challenge 2 (Computing the Exponential Damping Rate $k = -c/a$)

**Problem:** Given the linear operator equation:
$$(D_x + 2 D_y + 1)z = 0$$

**On your paper:**
1. Identify the coefficients $a, b, c$ from $(a D_x + b D_y + c)z = 0$.
2. Compute the exponential rate $k = -\frac{c}{a}$ in $z = e^{k x}\Phi(a y - b x)$.

<details>
<summary>💡 <b>Hint (Extracting a and c)</b></summary>

Here $a = 1$ (coefficient of $D_x$) and $c = 1$ (constant term), so $k = -c/a = -1/1$.
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Exponential Damping Rate
### START CODE HERE ###
damping_rate = -1.0
### END CODE HERE ###

# Run numerical verification test:
test_lab5.check_paper_challenge_2(damping_rate)
""")
    else:
        nb.code(r"""# GRADED CELL: Exponential Damping Rate
### START CODE HERE ### (≈ 1 line of code)
# Enter the numerical exponential rate k = -c/a:
damping_rate = None
### END CODE HERE ###

# Run numerical verification test:
test_lab5.check_paper_challenge_2(damping_rate)
""")

    nb.md(r"""---
## 6. 💻 Python Implementation: Linear Factor Coefficient Parser

Let's write a helper `parse_linear_factor(factor_str)` that extracts the numerical tuple `(a, b, c)` from a linear factor string like `"2*D_x - 3*D_y - 5"`.
""")

    if solutions:
        nb.code(r'''# GRADED FUNCTION: parse_linear_factor
def parse_linear_factor(factor_str: str) -> tuple[float, float, float]:
    # Parses coefficients a, b, c from a linear factor string "a*D_x + b*D_y + c"
    ### START CODE HERE ###
    import re
    ma = re.search(r'([+-]?\s*\d*)\s*\*?\s*D_x', factor_str)
    mb = re.search(r'([+-]?\s*\d*)\s*\*?\s*D_y', factor_str)
    mc = re.search(r'([+-]?\s*\d+)\s*$', factor_str.replace(" ", ""))

    def to_float(val, default):
        if not val or val.strip() in ['+', '']: return default
        if val.strip() == '-': return -default
        return float(val.replace(" ", ""))

    a = to_float(ma.group(1), 1.0) if ma else 0.0
    b = to_float(mb.group(1), 1.0) if mb else 0.0
    c = float(mc.group(1)) if mc else 0.0
    ### END CODE HERE ###
    return a, b, c

# Run automated unit test:
test_lab5.test_linear_factor_evaluator(parse_linear_factor)
''')
    else:
        nb.code(r'''# GRADED FUNCTION: parse_linear_factor
def parse_linear_factor(factor_str: str) -> tuple[float, float, float]:
    # Parses coefficients a, b, c from a linear factor (e.g. "2*D_x - 3*D_y - 5" -> (2.0, -3.0, -5.0))
    ### START CODE HERE ### (≈ 8-12 lines of code)
    import re
    # Extract coefficients a, b, c using regular expressions or string parsing:
    a = None
    b = None
    c = None
    ### END CODE HERE ###
    return a, b, c

# Run automated unit test:
test_lab5.test_linear_factor_evaluator(parse_linear_factor)
''')

    nb.md(r"""---
## 7. 🎨 Visualizing the Physics & Connecting to `rover_path_finder/planners.py`

Run the cell below to see two plots:
1. **Left:** The exponentially damped wave $z = e^{-0.5x}\sin(y - 2x)$ satisfying $(2D_x + D_y + 1)z = 0$.
2. **Right:** A direct comparison using [`planners.dirichlet_potential`](rover_path_finder/planners.py) vs. [`planners.neumann_potential`](rover_path_finder/planners.py) through a narrow 8-pixel canyon, demonstrating why Dirichlet walls suffer exponential gradient decay $e^{-\pi x / w}$ while Neumann walls maintain a smooth linear gradient!
""")

    nb.code(r"""from rover_path_finder.planners import dirichlet_potential, neumann_potential

x = np.linspace(0, 5, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.exp(-0.5 * X) * np.sin(Y - 2.0 * X)

corridor_hazard = np.zeros((40, 60), dtype=bool)
corridor_hazard[:16, 15:45] = True   # Upper canyon wall
corridor_hazard[24:, 15:45] = True   # Lower canyon wall (corridor width w = 8 pixels)
start_pt, goal_pt = (8, 20), (52, 20)

phi_dir, _, _ = dirichlet_potential(corridor_hazard, goal=goal_pt, tol=1e-8)
phi_neu, _, _ = neumann_potential(corridor_hazard, start=start_pt, goal=goal_pt, tol=1e-6)

fig = plt.figure(figsize=(14, 5.5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='plasma', alpha=0.88)
ax1.set_title(r"1. Linear Factor Solution: $z = e^{-0.5x}\sin(y - 2x)$", fontsize=11)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")
plt.colorbar(surf, ax=ax1, shrink=0.55)

ax2 = fig.add_subplot(1, 2, 2)
center_x = np.arange(8, 53)
ax2.plot(center_x, 1.0 - phi_dir[20, 8:53], 'r--', linewidth=2.5, label=r"1 - dirichlet_potential (Exponential Decay $e^{-\pi x/w}$)")
ax2.plot(center_x, phi_neu[20, 8:53], 'b-', linewidth=2.5, label="neumann_potential (Smooth Linear Gradient)")
ax2.set_yscale('log')
ax2.set_title("2. Real Engine: Narrow Corridor Gradient Decay (Log Scale)", fontsize=11)
ax2.set_xlabel("Position along narrow corridor (x)")
ax2.set_ylabel("Potential Drop (log scale)")
ax2.grid(True, which="both", alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()

print("Lab 5 Takeaways:")
print("  1) A linear factor (a*D_x + b*D_y + c)z = 0 introduces an exponential envelope exp(-(c/a)*x).")
print("  2) In narrow corridors of width w, Dirichlet walls cause exponential gradient decay exp(-pi*x/w).")
print("  3) Switching to insulated Neumann walls (neumann_potential) eliminates corridor decay!")
""")

    nb.save()


# ===========================================================================
# LAB 6: THE CAPSTONE: DISCRETIZATION & AUTONOMOUS ROVER NAVIGATION
# ===========================================================================
def build_lab_6(solutions: bool = False, target_dir: str = 'labs'):
    nb = NotebookBuilder("Lab_6_Mars_Rover_Capstone.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()
    
    nb.md(r"""# 🚀 Lab 6: Capstone — Finite Differences, Red-Black SOR, and Autonomous Mars Navigation
### *Mission Control: Assembling the Complete PDE Path-Planning Engine*
**Course:** Applied Partial Differential Equations & Planetary Robotics  
**Reference:** Integrating Labs 1–5 into [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py) and [`rover_path_finder/planners.py`](rover_path_finder/planners.py)

---
### 🗺️ Full Course Pipeline: How the 5 Lego Bricks (Labs 1–5) Assemble Into the Rover Engine
```
[Lab 1: Terrain Slopes slope_map] ──► [Lab 2: Streamline Paths descend] ──► [Lab 3: Safety Buffers dilate]
                                                                                       │
📍 [Lab 6: Finite-Difference SOR + Neumann Launch] ◄── [Lab 5: Narrow Corridor Decay] ◄── [Lab 4: Laplace Theory _avg]
```

| Building Block (Lab) | Lecture Notes Math (PDF pp. 1–62) | Engineering Problem It Solves on Mars | Real Engine Function (`rover_path_finder/`) |
| :--- | :--- | :--- | :--- |
| **🧱 Brick 1 (Lab 1)** | $p = \frac{\partial z}{\partial x},\; q = \frac{\partial z}{\partial y}$ & Eliminating Constants *(PDF pp. 2–11)* | Computes terrain steepness $\|\nabla z\| = \sqrt{p^2+q^2}$ to flag unsafe crater slopes (`> 0.30`) | [`terrain.slope_map(elev)`](rover_path_finder/terrain.py) |
| **🧱 Brick 2 (Lab 3)** | Non-Linear PDEs & Eikonal Distance $p^2 + q^2 = 1$ *(PDF pp. 17–27)* | Expands every rock/crater outward by the rover's body radius $R$ so wheels never clip rims | [`terrain.dilate(raw, rover_radius)`](rover_path_finder/terrain.py) |
| **🧱 Brick 3 (Lab 4)** | Laplace's Eq. $(D_x^2 + D_y^2)\phi = 0$ & Roots $m = \pm i$ *(PDF pp. 28–51)* | Creates a smooth harmonic potential $\phi(x,y)$ guaranteed to have **zero local minima** | [`solvers._avg(phi)`](rover_path_finder/solvers.py) |
| **🧱 Brick 4 (Lab 5)** | Reducible Factor $(aD_x+bD_y+c)z=0 \implies e^{-(c/a)x}$ *(PDF pp. 52–62)* | Explains exponential corridor decay $e^{-\pi x/w}$ under Dirichlet walls and switches to Neumann walls | [`planners.neumann_potential()`](rover_path_finder/planners.py) |
| **🧱 Brick 5 (Lab 2)** | Lagrange's Characteristics $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$ *(PDF pp. 12–17)* | Traces the steepest-descent streamline $(-\phi_x, -\phi_y)$ from `start` to `goal` | [`planners.descend(phi, hazard, start, goal)`](rover_path_finder/planners.py) |

---
### 🧭 The Rosetta Stone: Connecting Math to `rover_path_finder/`

| 1. Mathematical Concept | 2. Physical & Geometric Meaning | 3. Real Code in `rover_path_finder/` |
| :--- | :--- | :--- |
| $\nabla^2\phi = \frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$ | **Laplace's Equation (Lab 4):** smooth harmonic potential with zero interior local minima | Governing PDE solved in [`solvers.py`](rover_path_finder/solvers.py) |
| $\phi_{i,j} = \frac{1}{4}(\phi_{i+1,j} + \phi_{i-1,j} + \phi_{i,j+1} + \phi_{i,j-1})$ | **5-Point Finite-Difference Stencil:** discrete average over 4 orthogonal neighbors | [`_avg(phi)`](rover_path_finder/solvers.py) in `solvers.py` |
| $\frac{\partial\phi}{\partial n} = 0$ on obstacle walls | **Insulated Neumann BCs (Lab 5):** flow bends around rocks without decaying in narrow corridors | Dividing free-neighbor sum by active count `cnt` in [`sor_neumann`](rover_path_finder/solvers.py) |
| $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi/N)}$ | **Successive Over-Relaxation (SOR):** amplifies each update to accelerate convergence | [`optimal_omega(N)`](rover_path_finder/solvers.py) in `solvers.py` |
| $\frac{dx}{-\phi_x} = \frac{dy}{-\phi_y}$ | **Lagrange Characteristic Streamline (Lab 2):** steepest descent trajectory from `start` to `goal` | [`descend(phi, hazard, start, goal)`](rover_path_finder/planners.py) |

---
## 1. Why Do We Discretize Laplace's Equation onto a Grid?

In Labs 1–5, we solved PDEs analytically on paper. On Mars, however:
* Our synthetic testbed `make_terrain(N=100)` has **$100 \times 100 = 10,000$ grid nodes**, and the real NASA HiRISE DEM (`kasei.IMG` in `main.py`) scales up to **$160 \times 160 = 25,600$ nodes** with thousands of irregular crater walls!
* No closed-form paper formula can satisfy $\frac{\partial\phi}{\partial n} = 0$ on thousands of jagged rock pixels simultaneously.
* Instead, we discretize $\nabla^2\phi = 0$ using the **Finite Difference Method (5-Point Stencil)** and solve the resulting linear system iteratively using **Red-Black Successive Over-Relaxation (SOR)**.

> 📌 **Honest Syllabus Note:** While analytical solutions to Laplace's equation $(D_x^2 + D_y^2)z = 0$ are covered in Chapter 1.4 of the lecture notes (Notes p. 39 / PDF p. 33), **finite-difference discretization, the Discrete Maximum Principle, and SOR** are computational enrichment topics that bridge your lecture notes to real-world engineering software.
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab6

%matplotlib inline
print("Lab 6 Capstone Initialized! Mission Launch Sequence Ready.")
""")

    nb.md(r"""---
## 2. Step-by-Step Mathematical Derivation: Taylor Series & The Discrete Maximum Principle

### Part A: Deriving the 5-Point Stencil from Taylor Series
Expanding $\phi(x \pm h, y)$ around node $(i, j)$ via Taylor's theorem gives:
$$\phi_{i+1, j} = \phi_{i,j} + h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} + \frac{h^3}{6}\left.\frac{\partial^3\phi}{\partial x^3}\right|_{i,j} + \mathcal{O}(h^4)$$
$$\phi_{i-1, j} = \phi_{i,j} - h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} - \frac{h^3}{6}\left.\frac{\partial^3\phi}{\partial x^3}\right|_{i,j} + \mathcal{O}(h^4)$$

Adding the two equations cancels all odd-order derivatives ($\partial\phi/\partial x$ and $\partial^3\phi/\partial x^3$):
$$\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} \approx \frac{\phi_{i+1, j} - 2\phi_{i,j} + \phi_{i-1, j}}{h^2}, \qquad \left.\frac{\partial^2\phi}{\partial y^2}\right|_{i,j} \approx \frac{\phi_{i, j+1} - 2\phi_{i,j} + \phi_{i, j-1}}{h^2}$$

Substituting into Laplace's equation $\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$ and multiplying by $h^2$:
$$(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}) - 4\phi_{i,j} = 0 \implies \boxed{\phi_{i,j} = \frac{1}{4}\left(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}\right)}$$

---
### Part B: 1-Line Proof of the Discrete Maximum Principle (Why Local Traps Are Impossible)
Why is it 100% impossible for the rover to get stuck in an interior local minimum?
* **Proof by contradiction:** Suppose an interior free node $(i, j)$ were a strict local minimum, meaning its value is strictly less than all four of its neighbors:
  $$\phi_{i,j} < \phi_{\text{North}}, \quad \phi_{i,j} < \phi_{\text{South}}, \quad \phi_{i,j} < \phi_{\text{East}}, \quad \phi_{i,j} < \phi_{\text{West}}$$
* Summing these four strict inequalities and dividing by 4 gives:
  $$\phi_{i,j} < \frac{1}{4}\left(\phi_{\text{North}} + \phi_{\text{South}} + \phi_{\text{East}} + \phi_{\text{West}}\right)$$
* Which directly contradicts Laplace's stencil equation $\phi_{i,j} = \frac{1}{4}(\phi_N + \phi_S + \phi_E + \phi_W)$!
* Therefore, **no interior free node can ever be a local minimum**—the only minimum on the entire map is the goal sink ($\phi = 0$)!

---
### Part C: Zero-Flux Neumann Obstacle Walls ($\frac{\partial\phi}{\partial n} = 0$)
When an adjacent pixel is an obstacle (`free == False`), no current may flow into it. In [`solvers.sor_neumann`](rover_path_finder/solvers.py), we mask out obstacle values (`pf = phi * f`) and divide by the **number of active free neighbors** `cnt` (which is 3 along a straight wall, or 2 in a corner):
$$\phi_{i,j} = \frac{\sum_{\text{free neighbors}} \phi_{\text{neighbor}}}{\text{cnt}_{i,j}}$$
""")

    nb.md(r"""---
## 3. 📝 Paper & Pen Challenge 1 (4-Node Hand Calculation — Jacobi Sweep 1)

Let's compute **Sweep 1 of the synchronous Jacobi method** by hand on a $4 \times 4$ grid whose 4 interior cells $(A, B, C, D)$ start at $\phi^{(0)} = 0.0$:

```
             Top Boundary (Fixed Dirichlet: phi = 1.0)
         +--------+--------+--------+--------+
         |  1.0   |  1.0   |  1.0   |  1.0   |
         +--------+--------+--------+--------+
Left     |  0.5   | A(0.0) | B(0.0) |  0.5   | Right Boundary
Boundary +--------+--------+--------+--------+ (Fixed Dirichlet:
(Fixed:  |  0.5   | C(0.0) | D(0.0) |  0.5   |  phi = 0.5)
phi=0.5) +--------+--------+--------+--------+
         |  0.0   |  0.0   |  0.0   |  0.0   |
         +--------+--------+--------+--------+
            Bottom Boundary (Fixed Dirichlet: phi = 0.0)
```

> 📌 **Important:** In a **Jacobi sweep**, all new values $\phi^{(1)}$ are computed simultaneously from the initial values $\phi^{(0)} = 0.0$:
> * Initial neighbors of **Cell A**: North $= 1.0$, South ($C^{(0)}$) $= 0.0$, West $= 0.5$, East ($B^{(0)}$) $= 0.0$.
> * Initial neighbors of **Cell B**: North $= 1.0$, South ($D^{(0)}$) $= 0.0$, West ($A^{(0)}$) $= 0.0$, East $= 0.5$.
> *(Note: If you used sequential Gauss-Seidel instead, Cell B would use the newly updated $A^{(1)} = 0.375$ to get $0.46875$; here we ask for the **synchronous Jacobi** values).*

Compute $\phi_A^{(1)}$ and $\phi_B^{(1)}$ and enter them below:

<details>
<summary>💡 <b>Hint (Averaging the 4 Initial Neighbors)</b></summary>

For Cell A, $(1.0 + 0.0 + 0.5 + 0.0) / 4 = 1.5 / 4 = 0.375$. By left-right symmetry, Cell B has the exact same initial neighbor sum!
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: 4-Node Hand Calculation (Jacobi Sweep 1)
### START CODE HERE ###
phi_A = 0.375
phi_B = 0.375
### END CODE HERE ###

# Run numerical verification test:
test_lab6.check_paper_challenge_1(phi_A, phi_B)
""")
    else:
        nb.code(r"""# GRADED CELL: 4-Node Hand Calculation (Jacobi Sweep 1)
### START CODE HERE ### (≈ 2 lines of code)
# Enter your hand-calculated values for phi_A and phi_B after Jacobi Sweep 1:
phi_A = None
phi_B = None
### END CODE HERE ###

# Run numerical verification test:
test_lab6.check_paper_challenge_1(phi_A, phi_B)
""")

    nb.md(r"""---
## 4. 🚀 Paper & Pen Challenge 2 (Optimal SOR Factor $\omega_{\text{opt}}$ — `solvers.optimal_omega`)

Standard Jacobi relaxation is slow on large grids because boundary information propagates by only 1 pixel per sweep.
**Successive Over-Relaxation (SOR)** accelerates convergence dramatically by over-shooting the Gauss-Seidel average by a factor $\omega \in (1, 2)$:
$$\phi_{i,j}^{\text{new}} = (1 - \omega)\,\phi_{i,j}^{\text{old}} + \omega\,\text{avg}_{i,j}$$

By Young's Theorem (implemented in [`solvers.optimal_omega(N)`](rover_path_finder/solvers.py)), the theoretical optimal relaxation parameter on an $N \times N$ grid is:
$$\omega_{\text{opt}} = \frac{2}{1 + \sin\left(\frac{\pi}{N}\right)}$$

Compute $\omega_{\text{opt}}$ for $N = 16$:

<details>
<summary>💡 <b>Hint (Evaluating Young's Formula)</b></summary>

Substitute $N = 16$ into `2.0 / (1.0 + np.sin(np.pi / 16))` (which evaluates to approximately `1.6735`).
</details>
""")

    if solutions:
        nb.code(r"""# GRADED CELL: Optimal Omega for N=16
### START CODE HERE ###
omega_16 = 2.0 / (1.0 + np.sin(np.pi / 16))
### END CODE HERE ###

# Run numerical verification test:
test_lab6.check_paper_challenge_2(omega_16)
""")
    else:
        nb.code(r"""# GRADED CELL: Optimal Omega for N=16
### START CODE HERE ### (≈ 1 line of code)
# Compute the optimal relaxation factor omega_opt for N=16:
omega_16 = None
### END CODE HERE ###

# Run numerical verification test:
test_lab6.check_paper_challenge_2(omega_16)
""")

    nb.md(r"""---
## 5. 💻 Python Implementation: Red-Black SOR with Zero-Flux Neumann Walls

Now implement `sor_neumann_step`, the core solver inside [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py):
1. **Red-Black Checkerboard Splitting (`masks`):** Updates all Red cells (`(x + y) % 2 == 0`) simultaneously using vectorized NumPy rolls, then updates all Black cells (`(x + y) % 2 == 1`) using the freshly updated Red neighbors.
2. **Neumann Zero-Flux Masking (`pf = phi * f` divided by `cnt`):** Prevents potential from leaking into obstacle pixels.
3. **SOR Update:** `phi[mk] = (1 - omega) * old + omega * avg[mk]`.
""")

    if solutions:
        nb.code(r'''# GRADED FUNCTION: sor_neumann_step
def sor_neumann_step(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000):
    # Red-Black SOR solver with zero-flux Neumann crater walls
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    
    # Active free neighbor count (1 to 4) for Neumann boundary condition d(phi)/dn = 0
    cnt = sum(np.roll(f, s, a) for a in (0, 1) for s in (1, -1))
    cnt = np.maximum(cnt, 1.0)
    
    yy, xx = np.mgrid[0:n, 0:m]
    parity = (xx + yy) % 2
    masks = [(parity == c) & free & ~fixed for c in (0, 1)]
    phi[~free] = 0.0
    hist = []
    
    ### START CODE HERE ###
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
    ### END CODE HERE ###
    
    return phi, hist

# Run automated unit test:
test_lab6.test_sor_neumann_step(sor_neumann_step)
''')
    else:
        nb.code(r'''# GRADED FUNCTION: sor_neumann_step
def sor_neumann_step(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000):
    # Red-Black SOR solver with zero-flux Neumann crater walls
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    
    # Active free neighbor count (1 to 4) for Neumann boundary condition d(phi)/dn = 0
    cnt = sum(np.roll(f, s, a) for a in (0, 1) for s in (1, -1))
    cnt = np.maximum(cnt, 1.0)
    
    yy, xx = np.mgrid[0:n, 0:m]
    parity = (xx + yy) % 2
    masks = [(parity == c) & free & ~fixed for c in (0, 1)]
    phi[~free] = 0.0
    hist = []
    
    ### START CODE HERE ### (≈ 10-14 lines of code)
    # Loop for `maxit` iterations:
    # 1. Initialize d = 0.0
    # 2. For each mask `mk` in `masks`:
    #        a) Mask out obstacles: pf = phi * f
    #        b) Compute free-neighbor average:
    #           avg = (np.roll(pf, 1, 0) + np.roll(pf, -1, 0) + np.roll(pf, 1, 1) + np.roll(pf, -1, 1)) / cnt
    #        c) Save current values: old = phi[mk]
    #        d) Apply SOR update: phi[mk] = (1 - omega) * old + omega * avg[mk]
    #        e) Track max change: d = max(d, float(np.abs(phi[mk] - old).max()))
    # 3. Append `d` to `hist`: hist.append(d)
    # 4. If `d < tol`: break
    pass
    ### END CODE HERE ###
    
    return phi, hist

# Run automated unit test:
test_lab6.test_sor_neumann_step(sor_neumann_step)
''')

    nb.md(r"""---
## 6. 🌉 Classical Artificial Potential Fields (APF) vs. Laplace Harmonic Potential

In classical robotics, **Artificial Potential Fields (`planners.apf_potential`)** add an attractive bowl toward the goal and a local repulsive barrier around obstacles:
$$U(\mathbf{x}) = U_{\text{att}}(\mathbf{x}) + U_{\text{rep}}(\mathbf{x})$$

| Feature | Classical APF (`apf_potential`) | Laplace PDE (`neumann_potential`) |
| :--- | :--- | :--- |
| **Governing Equation** | Algebraic sum $U_{\text{att}} + U_{\text{rep}}$ ($\nabla^2 U \neq 0$) | Elliptic PDE $\nabla^2\phi = 0$ with $\frac{\partial\phi}{\partial n} = 0$ |
| **Concave / U-Shaped Obstacles** | Attractive pull and repulsive push cancel out ($\nabla U = \mathbf{0}$), **trapping the rover** | **Zero interior local minima** (Discrete Maximum Principle); streamlines bend cleanly around walls |

---
## 7. 🎨 Grand Mission Finale: Autonomous Navigation on Martian Terrain (`100x100`)

Run the cell below to generate synthetic Martian terrain (`10,000` nodes), solve Laplace's equation with insulated Neumann boundaries (`tol=1e-6`), and trace the rover's trajectory (`p[0]` = $x$, `p[1]` = $y$) cleanly around every red hazard zone!
""")

    nb.code(r"""from rover_path_finder.terrain import make_terrain
from rover_path_finder.planners import neumann_potential, descend, apf_potential, trap_map

# 1. Generate 100x100 Martian terrain with rover_radius=3 safety dilation
t_data = make_terrain(N=100, seed=42, rover_radius=3)
elev, raw_hazards, hazards = t_data["h"], t_data["raw"], t_data["hazard"]
start = t_data["start"]
goal = t_data["goal"]

# 2. Solve Laplace's Equation with Neumann zero-flux walls (tol=1e-6 for fast execution)
phi, sweeps, elapsed = neumann_potential(hazards, start=start, goal=goal, tol=1e-6)

# 3. Trace characteristic streamline via steepest descent
path, reached = descend(phi, hazards, start=start, goal=goal)

# 4. Plot Navigation Field & Path (p[0] is x=col, p[1] is y=row)
fig, ax = plt.subplots(figsize=(9.5, 7.5))
cs = ax.contourf(phi, levels=30, cmap='viridis')
plt.colorbar(cs, ax=ax, label=r"Harmonic Potential $\phi(x, y)$")
ax.contour(hazards, levels=[0.5], colors='red', linewidths=1.5)

px = [p[0] for p in path]
py = [p[1] for p in path]
ax.plot(px, py, color='cyan', linewidth=3, label="Rover Trajectory (Laplace Streamline)")
ax.plot(start[0], start[1], 'go', markersize=10, label=r"Start ($\phi=1$)")
ax.plot(goal[0], goal[1], 'r*', markersize=14, label=r"Goal ($\phi=0$)")

ax.set_title("Ares Rover Navigation: Laplace Streamlines Around Martian Hazards", fontsize=13)
ax.set_xlabel("x (column index)")
ax.set_ylabel("y (row index)")
ax.legend(loc='upper left')
plt.show()

print(f"Mission Status: Reached Goal = {reached} | Path Length = {len(path)} steps | SOR Sweeps = {sweeps} ({elapsed:.2f}s)")
""")

    nb.md(r"""---
## 8. 🪤 The Ultimate Benchmark: Escaping the U-Shaped Box Canyon (`trap_map`)

Run the cell below to compare **Classical APF** (left, permanently stuck inside the U-shaped canyon at $(55, 50)$) against **Laplace PDE with Neumann Walls** (right, smoothly navigating around the canyon wall to reach the goal $(90, 50)$):
""")

    nb.code(r"""u_trap, trap_start, trap_goal = trap_map(N=100)

# 1. Classical APF
apf_field = apf_potential(u_trap, goal=trap_goal)
apf_path, apf_reached = descend(apf_field, u_trap, start=trap_start, goal=trap_goal, maxsteps=200)

# 2. Laplace PDE with Neumann BCs (tol=1e-6)
laplace_field, trap_sweeps, trap_time = neumann_potential(u_trap, start=trap_start, goal=trap_goal, tol=1e-6)
laplace_path, laplace_reached = descend(laplace_field, u_trap, start=trap_start, goal=trap_goal, maxsteps=400)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Classical APF Plot
axes[0].contourf(apf_field, levels=25, cmap='magma')
axes[0].contour(u_trap, levels=[0.5], colors='white', linewidths=1.5)
axes[0].plot([p[0] for p in apf_path], [p[1] for p in apf_path], 'r-', linewidth=3, label="APF Path (Stuck)")
axes[0].plot(trap_start[0], trap_start[1], 'go', markersize=9, label="Start (20, 50)")
axes[0].plot(trap_goal[0], trap_goal[1], 'y*', markersize=13, label="Goal (90, 50)")
axes[0].set_title("Classical Robotics (APF): TRAPPED in Local Minimum", fontsize=12)
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")
axes[0].legend(loc="upper left")

# Laplace PDE Plot
axes[1].contourf(laplace_field, levels=25, cmap='viridis')
axes[1].contour(u_trap, levels=[0.5], colors='red', linewidths=1.5)
axes[1].plot([p[0] for p in laplace_path], [p[1] for p in laplace_path], 'c-', linewidth=3, label="Laplace Path (Escapes)")
axes[1].plot(trap_start[0], trap_start[1], 'go', markersize=9, label="Start (20, 50)")
axes[1].plot(trap_goal[0], trap_goal[1], 'y*', markersize=13, label="Goal (90, 50)")
axes[1].set_title("Laplace PDE: Maneuvers Cleanly Around the U-Trap", fontsize=12)
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")
axes[1].legend(loc="upper left")

plt.tight_layout()
plt.show()

print("Benchmark Results:")
print(f"  • Classical APF: Reached target? {apf_reached} (Permanently trapped inside U-shaped wall)")
print(f"  • Laplace PDE  : Reached target? {laplace_reached} (Safely escaped the trap in {len(laplace_path)} steps, {trap_time:.2f}s!)")
""")

    nb.md(r"""## 🏆 Course Graduation

**Congratulations on completing the Applied PDE & Rover Navigation Lab Suite!**

You have connected every topic in your PDE lecture notes to a working autonomous navigation engine:
1. **Lab 1 (Elimination of Arbitrary Constants):** Connected partial derivatives $(p, q)$ to [`terrain.slope_map`](rover_path_finder/terrain.py).
2. **Lab 2 (Lagrange's Method $Pp+Qq=R$):** Connected characteristic curves to [`planners.descend`](rover_path_finder/planners.py).
3. **Lab 3 (Non-Linear PDEs & Charpit's Method):** Connected the Eikonal distance equation $p^2+q^2=1$ to [`terrain.dilate`](rover_path_finder/terrain.py).
4. **Lab 4 (Higher-Order Homogeneous Operators):** Solved Laplace's equation $(D_x^2+D_y^2)z=0$ and verified the 4-neighbor average [`solvers._avg`](rover_path_finder/solvers.py).
5. **Lab 5 (Non-Homogeneous Operators):** Solved linear factors $(aD_x+bD_y+c)z=0$ and proved why Dirichlet walls decay exponentially in narrow corridors.
6. **Lab 6 (Finite Differences & Red-Black SOR):** Built `sor_neumann_step` with insulated Neumann walls and escaped U-shaped local-minimum traps!
""")

    nb.save()


if __name__ == "__main__":
    import sys
    gen_solutions = "--solutions" in sys.argv

    if gen_solutions:
        print("Building INSTRUCTOR REFERENCE SOLUTION labs in 'solutions/labs/'...")
        build_lab_1(solutions=True, target_dir="solutions/labs")
        build_lab_2(solutions=True, target_dir="solutions/labs")
        build_lab_3(solutions=True, target_dir="solutions/labs")
        build_lab_4(solutions=True, target_dir="solutions/labs")
        build_lab_5(solutions=True, target_dir="solutions/labs")
        build_lab_6(solutions=True, target_dir="solutions/labs")
        print("[OK] All 6 solution labs successfully generated in 'solutions/labs/'!")
    else:
        print("Building STUDENT labs (clean placeholders + Colab badges) in 'labs/'...")
        build_lab_1(solutions=False, target_dir="labs")
        build_lab_2(solutions=False, target_dir="labs")
        build_lab_3(solutions=False, target_dir="labs")
        build_lab_4(solutions=False, target_dir="labs")
        build_lab_5(solutions=False, target_dir="labs")
        build_lab_6(solutions=False, target_dir="labs")
        print("[OK] All 6 student labs successfully generated in 'labs/'!")

        # Also generate reference solutions into solutions/labs
        print("\nGenerating companion solutions in 'solutions/labs/'...")
        build_lab_1(solutions=True, target_dir="solutions/labs")
        build_lab_2(solutions=True, target_dir="solutions/labs")
        build_lab_3(solutions=True, target_dir="solutions/labs")
        build_lab_4(solutions=True, target_dir="solutions/labs")
        build_lab_5(solutions=True, target_dir="solutions/labs")
        build_lab_6(solutions=True, target_dir="solutions/labs")
        print("[OK] All 6 reference solutions successfully generated in 'solutions/labs/'!")
