# 📝 Student Lab Worksheet: From Analytical PDEs to Planetary Robotics
**Department of Mathematics & Aerospace Engineering — Applied PDE Course**

---

## 🧑‍🎓 Student Information
* **Student Name:** ____________________________________
* **Team Name:** _______________________________________
* **Date:** ________________________

---

## 🎯 Lab Objectives
1. **Master Semester Analytical Theory:** Solve canonical 1st-order and higher-order PDEs on paper using the methods taught in your syllabus (Elimination of Constants, Lagrange Auxiliary Systems, Charpit's Non-Linear Method, and Operator Calculus).
2. **Bridge Paper Math to Discrete Grids:** Hand-calculate a 4-node discrete Laplacian potential field using the 5-point discrete Mean Value Property (`solvers._avg`).
3. **The Engineering Scale-Up:** Understand how the exact same equations scale from a paper grid to a 25,600-pixel digital elevation model (DEM) of Mars to guide an autonomous planetary rover without local minima traps.

> 🔑 **Need Help?** Complete step-by-step master derivations and solutions are available in **[`INSTRUCTOR_ANSWER_KEY.md`](INSTRUCTOR_ANSWER_KEY.md)**, and the Arabic–English mathematical & codebase reference is in **[`GLOSSARY_AR.md`](GLOSSARY_AR.md)**.

---

## ✍️ PART I: Pencil-and-Paper Calculations (The 6-Lab Core)

### 📌 Problem 1 (Lab 1): Derivation of a PDE by Eliminating Constants (Ch. 1, Sec. 1.2 — Notes p. 9 / PDF p. 10, Ex. 2)
**Given the family of rover crater basins:**
$$z = (x - a)^2 + (y - b)^2$$
where $a$ and $b$ are arbitrary constants representing unknown crater centers.

1. Compute $p = \frac{\partial z}{\partial x}$:
   $$\frac{\partial z}{\partial x} = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
2. Compute $q = \frac{\partial z}{\partial y}$:
   $$\frac{\partial z}{\partial y} = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
3. Eliminate $a$ and $b$ by squaring and adding both relations.  
   **Your Final PDE:**
   $$\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$

---

### 📌 Problem 2 (Lab 2): Lagrange's Method & Characteristic Streamlines (Ch. 1, Sec. 1.3.1 — Notes p. 16 / PDF p. 17, Ex. 5)
**Given the quasi-linear equation for rover streamlines:**
$$x p + y q = z$$

1. Write down **Lagrange's auxiliary system**:
   $$\frac{dx}{\_\_\_\_\_} = \frac{dy}{\_\_\_\_\_} = \frac{dz}{\_\_\_\_\_}$$
2. Integrate Fraction 1 & 2 to find invariant $u(x, y, z) = c_1$:
   $$u = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
3. Integrate Fraction 2 & 3 to find invariant $v(x, y, z) = c_2$:
   $$v = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
4. State the **General Solution**: $\Phi(u, v) = 0 \implies \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$

---

### 📌 Problem 3 (Lab 3): Non-Linear PDEs & Charpit's Eikonal Wavefront (Ch. 1, Sec. 1.3.2–1.3.6 — Notes pp. 18–26 / PDF pp. 19–27)
**Given the optical sensor Eikonal travel-time equation:**
$$p^2 + q^2 = 1$$

1. Classify the equation: Standard Form I ($f(p, q) = 0$, where Charpit's equations give $\frac{dp}{0} = \frac{dq}{0} \implies p = a, q = b$).
2. Setting $p = a$, solve for $q$:
   $$q = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
3. Substitute into the total differential $dz = p dx + q dy$ and integrate to obtain the **Complete Integral**:
   $$z(x, y) = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$
4. Eliminate parameter $a$ to find the circular ripple envelope:
   $$\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ = z^2$$

---

### 📌 Problem 4 (Lab 4): Higher-Order Homogeneous Operators & Laplace (Ch. 1, Sec. 1.4 — Notes p. 39 / PDF p. 33, Ex. 5)
**Given the 2D Laplace Equation with zero forcing:**
$$(D_x^2 + D_y^2)z = 0$$

1. Set $D_x = m$ and $D_y = 1$ to form the **Auxiliary Equation (A.E.)**:
   $$m^2 + 1 = 0$$
2. Solve for the characteristic roots $m$:
   $$m_1 = \_\_\_\_\_\_\_\_, \quad m_2 = \_\_\_\_\_\_\_\_$$
3. By the theorem for complex conjugate roots, write down the **General Solution**:
   $$z(x, y) = \phi_1(\_\_\_\_\_\_\_\_\_\_\_\_) + \phi_2(\_\_\_\_\_\_\_\_\_\_\_\_)$$

---

### 📌 Problem 5 (Lab 5): Non-Homogeneous Reducible Operators & Damping (Ch. 2, Sec. 2.1 — Notes Ch. 2 p. 4 / PDF p. 56, Ex. 5)
**Given the dual-source communication beacon operator:**
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$

1. For Factor 1 $(2 D_x - 3 D_y + 1)z_1 = 0$, identify $a_1, b_1, c_1$:
   $$a_1 = \_\_\_\_, \quad b_1 = \_\_\_\_, \quad c_1 = \_\_\_\_$$
   Write $z_1 = e^{-c_1 x / a_1} \phi_1(a_1 y - b_1 x) = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$
2. For Factor 2 $(D_x + 2 D_y - 2)z_2 = 0$, identify $a_2, b_2, c_2$:
   $$a_2 = \_\_\_\_, \quad b_2 = \_\_\_\_, \quad c_2 = \_\_\_\_$$
   Write $z_2 = e^{-c_2 x / a_2} \phi_2(a_2 y - b_2 x) = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$
3. Superpose to find the **General Solution**:
   $$z(x, y) = z_1 + z_2 = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_$$

---

### 📌 Problem 6 (Lab 6): The 4-Node Grid Hand-Calculation (Discretization)
On Mars, crater walls and canyons prevent us from writing a simple closed-form formula for $\phi_1$ and $\phi_2$. We must discretize $(D_x^2 + D_y^2)\phi = 0$.

Using Taylor series expansion, the continuous Laplace equation turns into the **5-point discrete Mean Value Property** implemented in `rover_path_finder/solvers.py` (`_avg`):
$$\phi_{i,j} = \frac{1}{4}\left(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}\right)$$
> *"Every cell is the arithmetic average of its four orthogonal neighbors."*

#### 🧪 The Hand Experiment (Jacobi Sweep 1):
Consider a small $4 \times 4$ grid with fixed Dirichlet boundary values for this toy problem:
* **Top boundary (Start / Source):** $\phi = 1.0$
* **Bottom boundary (Goal / Sink):** $\phi = 0.0$
* **Left & Right boundaries (Fixed side-wall values):** $\phi = 0.5$
* **Initial interior guess ($k=0$):** $\phi_{1,1}^{(0)} = \phi_{1,2}^{(0)} = \phi_{2,1}^{(0)} = \phi_{2,2}^{(0)} = 0.0$

```text
   [ 1.0 ]   [ 1.0 ]   [ 1.0 ]   [ 1.0 ]  <-- Start (Source φ = 1.0)
   [ 0.5 ]   [  A  ]   [  B  ]   [ 0.5 ]
   [ 0.5 ]   [  C  ]   [  D  ]   [ 0.5 ]
   [ 0.0 ]   [ 0.0 ]   [ 0.0 ]   [ 0.0 ]  <-- Goal (Sink φ = 0.0)
```

**Perform Sweep 1 (Jacobi update — using $k=0$ values for all neighbors) by hand for cell A ($\phi_{1,1}$):**
$$\phi_A^{(1)} = \frac{\phi_{\text{up}}^{(0)} + \phi_{\text{down}}^{(0)} + \phi_{\text{left}}^{(0)} + \phi_{\text{right}}^{(0)}}{4} = \frac{1.0 + 0.0 + 0.5 + 0.0}{4} = \_\_\_\_\_\_\_\_$$

**Perform Sweep 1 (Jacobi update) for cell B ($\phi_{1,2}$):**
$$\phi_B^{(1)} = \frac{1.0 + 0.0 + 0.0 + 0.5}{4} = \_\_\_\_\_\_\_\_$$

*(Note: Under in-place Gauss-Seidel, where $\phi_A^{(1)} = 0.375$ is used immediately for the left neighbor of $B$, $\phi_B^{(1)}$ would be $\frac{1.0 + 0.0 + 0.375 + 0.5}{4} = 0.46875$!)*

Notice what is happening: **Potential information from the Start is flowing into the interior cells!**

---

## 🚀 PART II: The Scale-Up to Mars (Computer Execution)

### Why We Use Python for the Full Mission
On paper, calculating 4 cells took you 2 minutes.  
On the NASA Mars HiRISE Digital Elevation Model (`data/kasei.IMG`):
* The grid is **$160 \times 160 = 25,600$ cells**.
* There are over **3,400 crater obstacle cells**.
* Solving 25,600 coupled equations by hand would take **over 800 hours**.

The computer executes your exact paper math:
* **Jacobi Iteration:** Takes 21,356 sweeps.
* **SOR (Successive Over-Relaxation with Young's $\omega$):** Takes only **322 sweeps (66× faster!)**.

---

## 🖥️ PART III: Verifying the Mission in Code

Run the full benchmark suite in your terminal:

```powershell
# 1. Work through the 6 interactive DeepLearning.AI labs:
.venv\Scripts\python.exe -m jupyter notebook labs/

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
