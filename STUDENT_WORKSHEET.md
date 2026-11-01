# 📝 Student Lab Worksheet: From Analytical PDEs to Planetary Robotics
**Department of Mathematics & Aerospace Engineering — Applied PDE Course**

---

## 🧑‍🎓 Student Information
* **Student Name:** ____________________________________
* **Team Name:** _______________________________________
* **Date:** ________________________

---

## 🎯 Lab Objectives
1. **Master Semester Analytical Theory:** Solve canonical 1st-order and higher-order PDEs on paper using the methods taught in your syllabus (Elimination of Constants, Lagrange Auxiliary Systems, Operator Auxiliary Roots).
2. **Bridge Paper Math to Discrete Grids:** Hand-calculate a 4-node discrete Laplacian potential field using the 5-point discrete Mean Value Property.
3. **The Engineering Scale-Up:** Understand how the exact same equations scale from a 3×3 paper grid to a 25,600-pixel digital elevation model (DEM) of Mars to guide an autonomous planetary rover.

---

## ✍️ PART I: Pencil-and-Paper Calculations (The Coursework Core)

### 📌 Problem 1: Derivation of a PDE by Eliminating Arbitrary Constants (Section 1.2)
**Given the family of parabolic surfaces:**
$$z = a x + b y + a^2 + b^2$$
where $a$ and $b$ are arbitrary constants.

1. Compute $p = \frac{\partial z}{\partial x}$:
   $$\frac{\partial z}{\partial x} = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
2. Compute $q = \frac{\partial z}{\partial y}$:
   $$\frac{\partial z}{\partial y} = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
3. Eliminate $a$ and $b$ by substituting your expressions back into the original relation.  
   **Your Final PDE:**
   $$\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$

*(Self-check: Compare your answer using `python -m course_math.tutor` -> Option 1).*

---

### 📌 Problem 2: Analytical Solution of Laplace's Equation (Section 1.4, Page 33)
**Consider the 2D Laplace Equation with zero forcing:**
$$(D_x^2 + D_y^2)z = 0$$

1. Set $D_x = m$ and $D_y = 1$ to form the **Auxiliary Equation (A.E.)**:
   $$m^2 + 1 = 0$$
2. Solve for the characteristic roots $m$:
   $$m_1 = \_\_\_\_\_\_\_\_, \quad m_2 = \_\_\_\_\_\_\_\_$$
3. By the theorem for complex conjugate roots, write down the **General Solution**:
   $$z(x, y) = \phi_1(\_\_\_\_\_\_\_\_\_\_\_\_) + \phi_2(\_\_\_\_\_\_\_\_\_\_\_\_)$$

> 💡 **Instructor Insight:** This exact formula proves that any 2D potential field is formed by arbitrary analytic harmonic functions!

---

### 📌 Problem 3: The 3×3 Grid Hand-Calculation (Discretization)
On Mars, crater walls and canyons prevent us from writing a simple formula for $\phi_1$ and $\phi_2$. We must discretize $(D_x^2 + D_y^2)\phi = 0$.

Using Taylor series expansion, the continuous Laplace equation turns into the **5-point discrete Mean Value Property**:
$$\phi_{i,j} = \frac{1}{4}\left(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}\right)$$
> *"Every cell is the arithmetic average of its four orthogonal neighbors."*

#### 🧪 The Hand Experiment:
Consider a small $4 \times 4$ grid with boundary conditions:
* **Top boundary (Start / Source):** $\phi = 1.0$
* **Bottom boundary (Goal / Sink):** $\phi = 0.0$
* **Left & Right boundaries (Insulated walls):** $\phi = 0.5$
* **Initial interior guess:** $\phi_{1,1} = \phi_{1,2} = \phi_{2,1} = \phi_{2,2} = 0.0$

```
   [ 1.0 ]   [ 1.0 ]   [ 1.0 ]   [ 1.0 ]  <-- Start (Source φ = 1.0)
   [ 0.5 ]   [  A  ]   [  B  ]   [ 0.5 ]
   [ 0.5 ]   [  C  ]   [  D  ]   [ 0.5 ]
   [ 0.0 ]   [ 0.0 ]   [ 0.0 ]   [ 0.0 ]  <-- Goal (Sink φ = 0.0)
```

**Perform Sweep 1 (Jacobi update) by hand for cell A ($\phi_{1,1}$):**
$$\phi_A^{(1)} = \frac{\phi_{\text{up}} + \phi_{\text{down}} + \phi_{\text{left}} + \phi_{\text{right}}}{4} = \frac{1.0 + 0.0 + 0.5 + 0.0}{4} = \_\_\_\_\_\_\_\_$$

**Perform Sweep 1 for cell B ($\phi_{1,2}$):**
$$\phi_B^{(1)} = \frac{1.0 + 0.0 + 0.0 + 0.5}{4} = \_\_\_\_\_\_\_\_$$

Notice what is happening: **Potential information from the Start is flowing into the interior cells!**

---

### 📌 Problem 4: Tracing the Rover Path via Lagrange's Method (Section 1.3.1)
Once the potential field $\phi(x, y)$ is calculated, the rover rolls downhill along velocity vector $\mathbf{v} = (u, v) = -\nabla\phi$.

The streamline trajectories follow the quasi-linear transport equation:
$$u \frac{\partial \phi}{\partial x} + v \frac{\partial \phi}{\partial y} = 0$$

1. Write down **Lagrange's auxiliary equation** for the streamline:
   $$\frac{dx}{u} = \frac{dy}{v}$$
2. For a constant slope vector $u = 2, v = -1$, solve the ordinary differential equation:
   $$v \, dx - u \, dy = 0 \implies -1 \, dx - 2 \, dy = 0$$
3. Integrate to find the streamline path equation:
   $$y(x) = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$

> 💡 **Conclusion:** Lagrange's method traces the exact trajectory curve that the rover drives!

---

## 🚀 PART II: The Scale-Up to Mars (Computer Execution)

### Why We Use Python for the Full Mission
On paper, calculating 4 cells took you 2 minutes.  
On the NASA Mars HiRISE Digital Elevation Model (`data/kasei.IMG`):
* The grid is **$160 \times 160 = 25,600$ cells**.
* There are over **3,400 crater obstacle cells**.
* Solving 25,600 coupled equations by hand would take **over 800 hours**.

The computer executes your exact paper math:
* **Jacobi Iteration:** Takes 21,400 sweeps.
* **SOR (Successive Over-Relaxation with Young's $\omega$):** Takes only **322 sweeps (66× faster!)**.

---

## 🖥️ PART III: Verifying the Mission in Code

Run the full benchmark suite in your terminal:

```powershell
# 1. Run your coursework analytical verification suite:
.venv\Scripts\python.exe -m course_math.tutor --all

# 2. Run the unit test bench (Jacobi, SOR, Neumann boundaries):
.venv\Scripts\python.exe test_solvers.py

# 3. Launch the full Mars Rover navigation benchmark:
.venv\Scripts\python.exe main.py
```

### Expected Deliverables for Your Team Report:
* Open `outputs/fig1_terrain.png`: Observe synthetic lunar crater terrain.
* Open `outputs/fig2_solution_and_path.png`: Observe the harmonic potential field and the rover descent path.
* Open `outputs/fig3_validation_and_solvers.png`: Observe convergence comparison (Jacobi vs Gauss-Seidel vs SOR).
* Open `outputs/fig4_trap_comparison.png`: Observe how Laplace's Maximum Principle prevents the rover from getting stuck in dead-end traps!

