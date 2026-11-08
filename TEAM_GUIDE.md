# 🎓 PDE Rover Engine: A Comprehensive Course in Applied PDEs & Planetary Robotics

Welcome to your college **Partial Differential Equations (PDE)** team project!

This guide is designed as an interactive **two-part university course**:
1. **Part I: The Semester Coursework Theory (Analytical & Exact Methods):** Master the exact pencil-and-paper techniques taught in your lecture notes (Eliminating Constants, Lagrange's Method, Charpit's Method, and Differential Operator Calculus $D_x, D_y$).
2. **Part II: The Planetary Rover Application (Computational Scale-Up):** Understand why analytical formulas cannot easily handle complex geometry (like 10,000 jagged Mars crater walls), and how the exact same PDE is discretized and scaled up using Python to guide an autonomous planetary rover on real NASA elevation models.

> 📚 **Your Coursework Toolkit:**
> - 🌟 **DeepLearning.AI 6-Lab Suite:** [`labs/`](labs/) — Interactive Andrew Ng-style notebooks with graded tests and visualizations.
> - 🔑 **Instructor Answer Key:** [`INSTRUCTOR_ANSWER_KEY.md`](INSTRUCTOR_ANSWER_KEY.md) — Complete step-by-step master derivations and solutions.
> - 📝 **Student Lab Worksheet:** [`STUDENT_WORKSHEET.md`](STUDENT_WORKSHEET.md) — 6-problem pencil-and-paper companion worksheet for your team.
> - 🚀 **Rover Simulation Engine:** Run `.venv\Scripts\python.exe main.py` to see the complete planetary navigation benchmark.

---

## 📚 Course Curriculum at a Glance

```mermaid
flowchart TD
    M0["<b>Module 0: The Semester Theory (The Book)</b><br/>Analytical Methods: Lagrange, Charpit, Operator Calculus D_x, D_y"] --> M1["<b>Module 1: The Real-World Engineering Problem</b><br/>Why traditional robotics fails in craters (The Local Minima Trap)"]
    M1 --> M2["<b>Module 2: The Governing PDE (Laplace)</b><br/>(D_x² + D_y²)φ = 0 & The Strong Maximum Principle"]
    M2 --> M3["<b>Module 3: Discretization Math</b><br/>Taylor Series Expansion → 5-Point Discrete Mean Value Stencil"]
    M3 --> M4["<b>Module 4: Iterative Solvers Race</b><br/>Jacobi vs. Gauss-Seidel vs. SOR (Young's Theorem)"]
    M4 --> M5["<b>Module 5: Boundary Physics</b><br/>Dirichlet (Source/Sink) vs. Neumann Ghost Cells (No-Flux Walls)"]
    M5 --> M6["<b>Module 6: The Final Destination</b><br/>Steepest Gradient Descent Navigation on Mars DEMs"]
```

---

## 📖 Module 0: The Semester Coursework Theory (Analytical Methods)

Before turning to computers, every engineer must understand the **analytical methods** used to solve PDEs on paper.

### 1. Eliminating Arbitrary Constants (Ch. 1, Sec. 1.2 — Notes pp. 1–10 / PDF pp. 2–11)
Given a geometric family of surfaces $F(x, y, z, a, b) = 0$, we eliminate the arbitrary parameters $a$ and $b$ by computing:
$$p = \frac{\partial z}{\partial x}, \quad q = \frac{\partial z}{\partial y}$$
* **Worked Example 1 (Notes p. 8 / PDF pp. 9–10):** $z = ax + by + a^2 + b^2$ (2-parameter family of planes) $\implies z = xp + yq + p^2 + q^2$.
* **Worked Example 2 (Notes p. 9 / PDF p. 10):** $z = (x - a)^2 + (y - b)^2 \implies p^2 + q^2 = 4z$.
* **The Rover Connection:** [`terrain.slope_map`](rover_path_finder/terrain.py) computes $p$ and $q$ across the DEM to flag steep craters via $\|\nabla z\| = \sqrt{p^2 + q^2}$.

### 2. First-Order Quasi-Linear PDEs: Lagrange's Method (Ch. 1, Sec. 1.3.1 — Notes pp. 11–16 / PDF pp. 12–17)
Any first-order equation linear in partial derivatives $P p + Q q = R$ is solved by finding two independent integrals $u(x, y, z) = c_1$ and $v(x, y, z) = c_2$ from the **auxiliary equations**:
$$\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$$
* **The Rover Connection:** [`planners.descend`](rover_path_finder/planners.py) integrates the characteristic streamline $\frac{dx}{u} = \frac{dy}{v}$ along $(u, v) = -\nabla\phi$.

### 3. Special Non-Linear Forms & Charpit's Method (Ch. 1, Sec. 1.3.2–1.3.6 — Notes pp. 16–26 / PDF pp. 17–27)
* **Standard Form I ($f(p, q) = 0$, Notes p. 18 / PDF p. 19):** $p = a, q = b \implies z = ax + by + c$.  
  *Crucial Example:* The Eikonal wavefront equation $\|\nabla z\|^2 = p^2 + q^2 = 1$ is Standard Form I, whose singular envelope $x^2 + y^2 = z^2$ governs the circular safety buffer in [`terrain.dilate`](rover_path_finder/terrain.py)!
* **Clairaut's Form ($z = px + qy + f(p, q)$, Notes p. 19 / PDF p. 20):** Complete integral $z = ax + by + f(a, b)$.
* **Charpit's General Method (Notes pp. 24–26 / PDF pp. 25–27):**
  $$\frac{dx}{-f_p} = \frac{dy}{-f_q} = \frac{dz}{-p f_p - q f_q} = \frac{dp}{f_x + p f_z} = \frac{dq}{f_y + q f_z}$$

### 4. Higher-Order Homogeneous Linear PDEs (Ch. 1, Sec. 1.4 — Notes pp. 34–57 / PDF pp. 28–51)
For differential operator $F(D_x, D_y)z = 0$, put $D_x = m, D_y = 1$ to form the **Auxiliary Equation (A.E.)** $F(m, 1) = 0$:
* **Laplace's Equation (Notes p. 39 / PDF p. 33, Example 5):**
  $$(D_x^2 + D_y^2)z = 0 \implies m^2 + 1 = 0 \implies m = \pm i$$
  General Solution: $z = \phi_1(y + ix) + \phi_2(y - ix)$, discretized via [`solvers._avg`](rover_path_finder/solvers.py).
* **Particular Integrals (P.I.):** Shortcut rules for exponential forcing ($e^{ax+by}$) and sinusoidal forcing ($\sin(ax+by)$, Notes p. 48 / PDF p. 42, Example 4).

### 5. Non-Homogeneous Reducible Linear PDEs (Ch. 2, Sec. 2.1 — Notes Ch. 2 pp. 1–10 / PDF pp. 52–62)
When a differential operator factors into linear terms $(a D_x + b D_y + c)z = 0$ containing a 0th-order constant $c \neq 0$, Case (A) (Notes Ch. 2 p. 2 / PDF p. 54) yields:
$$z(x, y) = e^{-\frac{c}{a}x}\phi(a y - b x)$$
* **The Rover Connection:** Explains why [`planners.dirichlet_potential`](rover_path_finder/planners.py) suffers from exponential gradient decay $e^{-(\pi/W)x}$ inside narrow passages of width $W$, whereas [`planners.neumann_potential`](rover_path_finder/planners.py) preserves a strong linear gradient!

---

## 🌉 The Educational Bridge: Why Paper Math Needs Computer Math

Ask your team this fundamental question:
> *"If we already have the exact analytical solution $z = \phi_1(y + ix) + \phi_2(y - ix)$ for Laplace's equation, why can't we just use that formula for Mars?"*

* **The Answer:** On a smooth geometric domain (like an infinite flat plane or a perfect circular disc), paper math works beautifully.
* **The Catch:** A real Mars crater terrain has **over 10,000 irregular boundary pixels**. It is mathematically impossible to write down a closed-form formula for $\phi_1$ and $\phi_2$ that fits 10,000 jagged crater boundaries.
* **The Engineering Solution:** We convert the continuous operator $(D_x^2 + D_y^2)$ into a **discrete 5-point stencil** and let Python compute the values across the entire grid!

---

## 🪐 Module 1: The Real-World Problem (Why We Need PDEs)

Imagine an autonomous planetary rover on Mars (or the Moon) tasked with driving from a landing site to an exploration target.

### The Classic Approach: Artificial Potential Fields (APF)
In traditional video games and classical robotics, developers use an intuitive idea called **Artificial Potential Fields (APF)**:
1. The **Goal** exerts an *attractive gravitational force* pulling the rover in: $U_{\text{att}}(x) \propto \|x - x_{\text{goal}}\|^2$.
2. Every **Obstacle** exerts a *repulsive electrostatic force* pushing the rover away: $U_{\text{rep}}(x) \propto \frac{1}{d(x)^2}$.
3. Total potential: $U(x) = U_{\text{att}}(x) + U_{\text{rep}}(x)$. The rover rolls downhill along $-\nabla U$.

### The Fatal Flaw: The Local Minimum Trap 🪤
Consider a U-shaped crater or a dead-end canyon:
- As the rover enters the canyon heading toward the goal behind the back wall, the forward pull toward the goal is **exactly balanced** by the backward repulsion from the crater wall.
- Result: $\nabla U = \mathbf{0}$. The forces cancel out!
- The rover enters a **local minimum** and becomes permanently stuck in a trap, rocking back and forth or freezing forever.

**How do we fix this?** We need a mathematical field that is *physically incapable* of forming interior potholes or local traps. That field is governed by **Laplace's Equation**.

---

## 📐 Module 2: The Core PDE Theory (Harmonic Functions)

We replace ad-hoc heuristic forces with a fundamental equation of physics and mathematics: **Laplace's Equation** in 2D:

$$\nabla^2\phi = \frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$$

Any smooth function $\phi(x, y)$ that satisfies Laplace's equation is called a **harmonic function**. Harmonic functions possess two extraordinary mathematical properties that make them ideal for path planning:

### 1. The Mean Value Property
For any point $(x_0, y_0)$ in the domain and any circle of radius $R$ centered at $(x_0, y_0)$ inside the domain:
$$\phi(x_0, y_0) = \frac{1}{2\pi R} \oint_{\partial B_R} \phi(s) \, ds$$
> **In plain English:** The value at *any* point is strictly equal to the arithmetic average of the values in its immediate neighborhood.

### 2. The Strong Maximum (and Minimum) Principle
> **Theorem:** Let $\phi$ be harmonic in a connected open domain $\Omega$. If $\phi$ attains a local maximum or minimum in the interior of $\Omega$, then $\phi$ must be constant everywhere.

**Why this matters for our rover:**
- If $\phi$ is non-constant, **local minima CANNOT exist inside the domain**!
- Extrema can **only occur on the boundary**:
  - We set the start position as a high-potential source: $\phi = 1.0$.
  - We set the goal target as the lowest-potential sink: $\phi = 0.0$.
- Because no interior local minima can exist, gradient descent ($-\nabla\phi$) is **mathematically guaranteed to guide the rover to the goal without ever getting stuck**, no matter how complex the maze of craters is!

---

## 🧮 Module 3: Discretization Math (Taylor Series to 5-Point Stencil)

Computers cannot solve continuous differential equations directly on continuous space. We must discretize the 2D plane into a grid with spacing $\Delta x = \Delta y = h$.

### The Taylor Series Derivation
Let's approximate $\frac{\partial^2\phi}{\partial x^2}$ at grid point $(i, j)$ using Taylor series:

$$\phi(x + h, y) = \phi_{i+1, j} = \phi_{i,j} + h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} + \frac{h^3}{6}\left.\frac{\partial^3\phi}{\partial x^3}\right|_{i,j} + \mathcal{O}(h^4)$$

$$\phi(x - h, y) = \phi_{i-1, j} = \phi_{i,j} - h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} - \frac{h^3}{6}\left.\frac{\partial^3\phi}{\partial x^3}\right|_{i,j} + \mathcal{O}(h^4)$$

Notice what happens when we **add** these two equations together:
- The first-order derivatives $h \frac{\partial\phi}{\partial x}$ cancel out!
- The third-order derivatives $\frac{h^3}{6} \frac{\partial^3\phi}{\partial x^3}$ cancel out!
- We are left with:
  $$\phi_{i+1, j} + \phi_{i-1, j} = 2\phi_{i,j} + h^2 \left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} + \mathcal{O}(h^4)$$

Rearranging gives the second-order central difference approximation:
$$\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} = \frac{\phi_{i+1, j} - 2\phi_{i,j} + \phi_{i-1, j}}{h^2} + \mathcal{O}(h^2)$$

Applying the exact same derivation in the $y$-direction:
$$\left.\frac{\partial^2\phi}{\partial y^2}\right|_{i,j} = \frac{\phi_{i, j+1} - 2\phi_{i,j} + \phi_{i, j-1}}{h^2} + \mathcal{O}(h^2)$$

### The 5-Point Discrete Laplacian
Now substitute both into Laplace's equation $\nabla^2\phi = 0$:
$$\frac{\phi_{i+1, j} - 2\phi_{i,j} + \phi_{i-1, j}}{h^2} + \frac{\phi_{i, j+1} - 2\phi_{i,j} + \phi_{i, j-1}}{h^2} = 0$$

Multiply the entire equation by $h^2$:
$$(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}) - 4\phi_{i,j} = 0$$

Solving for the center node $\phi_{i,j}$:
$$\phi_{i,j} = \frac{1}{4}\left(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}\right)$$

> **Key Takeaway:** The continuous Mean Value Property turns directly into the discrete 5-point stencil: **every cell is simply the average of its 4 orthogonal neighbours!**

---

## 🏎️ Module 4: The Numerical Solvers Race (Why 3 Solvers?)

On a $100 \times 100$ terrain map, we have up to $10,000$ interconnected grid cells. This forms a massive linear system:
$$A \mathbf{\Phi} = \mathbf{b}$$
Where $A$ is a $10,000 \times 10,000$ sparse matrix.
- Direct Gaussian elimination would require $\mathcal{O}(M^3) = \mathcal{O}(10^{12})$ operations — far too slow and memory-intensive!
- Instead, we use **iterative relaxation methods**. We start with an initial guess and repeatedly sweep through the grid until the solution converges.

### 1. Jacobi Iteration (The Baseline)
At iteration step $k+1$, every cell is updated simultaneously using values from step $k$:
$$\phi_{i,j}^{(k+1)} = \frac{1}{4}\left(\phi_{i+1,j}^{(k)} + \phi_{i-1,j}^{(k)} + \phi_{i,j+1}^{(k)} + \phi_{i,j-1}^{(k)}\right)$$
- **Why it's slow:** Potential information only moves **one grid cell per sweep**.
- For an $N \times N$ grid, the spectral radius of the iteration matrix is $\rho_J = \cos(\pi / N) \approx 1 - \frac{\pi^2}{2N^2}$.
- To reduce error by a factor of $\epsilon$, Jacobi requires $\mathcal{O}(N^2)$ iterations. For $N=160$, this takes over **21,000 iterations**!

### 2. Gauss-Seidel Relaxation (Use fresh information immediately)
Instead of waiting for the next sweep, Gauss-Seidel uses freshly computed values as soon as they become available:
$$\phi_{i,j}^{(k+1)} = \frac{1}{4}\left(\phi_{i+1,j}^{(k)} + \phi_{i-1,j}^{(k+1)} + \phi_{i,j+1}^{(k)} + \phi_{i,j-1}^{(k+1)}\right)$$
- **Performance:** As proved by the Gauss-Seidel theorem, spectral radius $\rho_{\text{GS}} = \rho_J^2$, which cuts the required iteration count **cleanly in half** ($\sim 12,000$ sweeps).

### 3. Successive Over-Relaxation (SOR) with Young's Theorem 🚀
Why settle for taking tiny steps toward the equilibrium average? We can **extrapolate** (over-relax) in the direction of the correction:
$$\phi_{i,j}^{(k+1)} = (1 - \omega)\phi_{i,j}^{(k)} + \omega \cdot \phi_{i,j}^{\text{avg}}$$
- If $\omega = 1.0$: This is standard Gauss-Seidel.
- If $1.0 < \omega < 2.0$: Over-relaxation accelerates convergence.
- **Young's Theorem:** For a 2-cyclic consistently ordered matrix, the optimal parameter is:
  $$\omega_{\text{opt}} = \frac{2}{1 + \sqrt{1 - \rho_J^2}} = \frac{2}{1 + \sqrt{1 - \cos^2(\pi/N)}} = \frac{2}{1 + \sin(\pi/N)}$$
- **Performance:** Iteration count drops from $\mathcal{O}(N^2)$ down to $\mathcal{O}(N)$. For $N=160$, SOR finishes in **only 322 sweeps** — a **66x speedup**!

### Why Red-Black Ordering? (Vectorization in NumPy)
Sequential Gauss-Seidel updates cell $(i, j)$ using $(i-1, j)$, which normally forces slow nested `for` loops in Python.
- Notice that the 5-point stencil only couples cells with **opposite parity**: $(i+j) \pmod 2$.
- We color the grid like a chessboard into **Red** (even) and **Black** (odd) sets.
- Red cells depend ONLY on Black neighbours. Black cells depend ONLY on Red neighbours!
- This enables **100% vectorized array slicing in NumPy** without any race conditions!

---

## 🧱 Module 5: Boundary Physics (Dirichlet vs. Neumann Walls)

A PDE is completely defined by its **Boundary Conditions (BCs)**. How we handle obstacle walls determines whether our rover navigates successfully or fails completely!

```mermaid
graph LR
    subgraph "Formulation A: Dirichlet BC on Obstacles (FAIL)"
        A1["Obstacle walls fixed at phi = 1.0"] --> A2["Narrow passages suffer exponential decay: e^(-pi*d/w)"]
        A2 --> A3["Potential field becomes completely flat"]
        A3 --> A4["Gradient vanishes: Rover stalls!"]
    end
    subgraph "Formulation B: Neumann BC on Obstacles (SUCCESS)"
        B1["Zero-Flux Condition: dphi/dn = 0"] --> B2["Obstacles act as insulated riverbanks"]
        B2 --> B3["Streamlines flow cleanly around contours"]
        B3 --> B4["Guaranteed non-vanishing gradient: Rover reaches goal!"]
    end
```

### The Failure of Formulation A (Dirichlet Obstacles)
If you treat obstacle walls as fixed potential $\phi = 1.0$ (hoping high potential pushes the rover away):
- In any narrow pass of width $w$ and length $d$, the potential decays exponentially as:
  $$\phi(x) \propto e^{-\pi d / w}$$
- Over a long corridor, $\phi$ drops to machine precision ($10^{-16}$). The potential becomes completely flat ($0.00000000$), the gradient vanishes ($\nabla\phi \approx \mathbf{0}$), and the rover has no slope to follow!

### The Triumph of Formulation B (Zero-Flux Neumann Walls)
Instead of forcing potential on obstacles, we declare obstacles to be **perfectly insulated boundaries** where no flux can enter or leave:
$$\frac{\partial\phi}{\partial n} = \nabla\phi \cdot \hat{\mathbf{n}} = 0$$

#### The Ghost Cell Derivation
At a wall boundary $x = x_0$, approximate the normal derivative with a central difference using a fictitious **ghost cell** $\phi_{-1}$ inside the obstacle:
$$\left.\frac{\partial\phi}{\partial x}\right|_{x_0} \approx \frac{\phi_1 - \phi_{-1}}{2h} = 0 \implies \phi_{-1} = \phi_1$$

Substitute $\phi_{-1} = \phi_1$ back into the 5-point discrete Laplacian stencil:
$$\phi(x_0, y) = \frac{\phi_1 + \phi_{-1} + \phi_{\text{up}} + \phi_{\text{down}}}{4} = \frac{2\phi_1 + \phi_{\text{up}} + \phi_{\text{down}}}{4}$$

On an arbitrary terrain grid, this reflection condition means: **the obstacle cell is simply excluded, and we average over only the $c_{i,j} \in \{1, 2, 3, 4\}$ active free neighbours that exist!**

---

## 🎯 Module 6: The Final Destination (What We End Up With)

Once your PDE solver converges, you have computed a smooth 2D potential field $\phi(x, y)$ across the entire planet surface.

### 1. Steepest Descent Navigation
The rover determines its next step $(x_{k+1}, y_{k+1})$ by simply rolling downhill along the negative gradient:
$$\mathbf{v} = -\nabla\phi(x, y)$$
On our discrete 8-connected grid, the rover looks at all 8 surrounding cells and steps to whichever reachable neighbor has the lowest $\phi$ value.

### 2. What the Output Proves (Your Project Deliverables)
When you run the project, your team will see:
1. **Convergence study (`fig3_validation_and_solvers.png`):** Validates second-order accuracy against the analytical solution $\phi = \frac{\sin(\pi x)\sinh(\pi y)}{\sinh(\pi)}$.
2. **Never-stuck test:** Tests 400 random starting positions across lunar terrain — 400 out of 400 safely reach the goal.
3. **Trap test (`fig4_trap_comparison.png`):** Demonstrates side-by-side how classic APF gets trapped inside a U-shaped dead end, while Laplace Formulation B smoothly maneuvers out and around to the goal.
4. **Real Mars Missions:** Real-world paths through HiRISE Mars elevation models (Opportunity landing site and Kasei Valles canyon).

---

## 🛠️ Module 7: Hands-On Laboratory Guide (How to Learn & Execute)

### Step 1: Work Through the 6 Interactive DeepLearning.AI Labs
Launch the modular laboratory series in [`labs/`](labs/) (or in Arabic in [`labs_ar/`](labs_ar/)):
* **[Lab 1: Elimination of Constants](labs/Lab_1_Elimination_of_Constants.ipynb)** — Terrain slope gradients $(p, q)$ & hazard detection (`terrain.slope_map`).
* **[Lab 2: Lagrange's Method](labs/Lab_2_Lagrange_Method.ipynb)** — Characteristic curves & steepest-descent path tracing (`planners.descend`).
* **[Lab 3: Non-Linear Charpit](labs/Lab_3_Nonlinear_Charpit.ipynb)** — Eikonal wavefront propagation $p^2+q^2=1$ & obstacle safety buffers (`terrain.dilate`).
* **[Lab 4: Higher-Order Operators](labs/Lab_4_HigherOrder_Operators.ipynb)** — Laplace's equation $(D_x^2+D_y^2)\phi=0$, complex characteristic roots, and the 4-neighbor average (`solvers._avg`).
* **[Lab 5: Non-Homogeneous PDEs](labs/Lab_5_NonHomogeneous_PDEs.ipynb)** — Reducible operators and narrow-corridor exponential decay (`dirichlet_potential` vs `neumann_potential`).
* **[Lab 6: Mars Rover Capstone](labs/Lab_6_Mars_Rover_Capstone.ipynb)** — Discrete Maximum Principle proof, Red-Black SOR (`solvers.sor_neumann`), and escaping the U-shaped box canyon.

*(Use [`STUDENT_WORKSHEET.md`](STUDENT_WORKSHEET.md) for your team's pencil-and-paper scratch calculations, and [`INSTRUCTOR_ANSWER_KEY.md`](INSTRUCTOR_ANSWER_KEY.md) for complete master derivations!)*

### Step 2: Consult the Master Instructor Answer Key
If you or your teammates ever get stuck on the analytical derivations in any of the 6 labs:
* Open [`INSTRUCTOR_ANSWER_KEY.md`](INSTRUCTOR_ANSWER_KEY.md) to inspect the complete step-by-step mathematical working.
* Every challenge (Textbook problems and Rover Bridge problems) has its full algebraic expansion and physical reasoning detailed.

### Step 3: Verify the Production Rover Solvers
Run the fast unit test bench to verify that the discrete solvers are working properly:
```powershell
.venv\Scripts\python.exe test_solvers.py
```

### Step 4: Full Simulation & Planetary Navigation
Launch the full planetary rover benchmark suite:
```powershell
.venv\Scripts\python.exe main.py
```
This runs the solver across lunar terrain and generates the 4 key report figures in `outputs/`:
* `outputs/fig1_terrain.png`: Synthetic lunar craters and hazardous slope thresholding.
* `outputs/fig2_solution_and_path.png`: The harmonic potential field and steepest descent path.
* `outputs/fig3_validation_and_solvers.png`: Solver convergence race (Jacobi vs SOR).
* `outputs/fig4_trap_comparison.png`: Dead-end canyon trap comparison (APF vs Laplace).
This generates all figures in `outputs/` and reproduces the full project benchmarks!

---

## 📊 Module 8: How to Read the Terminal Output

When you run `uv run python main.py`, look for these mathematical confirmations:

```text
== Validation against the exact solution (Laplace on the unit square) ==
N=  16  max error = 1.109e-03
N=  32  max error = 2.780e-04  (ratio to previous = 3.99)
N=  64  max error = 6.963e-05  (ratio to previous = 3.99)
N= 128  max error = 1.741e-05  (ratio to previous = 4.00)
```
> **PDE Milestone:** The error ratio is **4.00**, confirming that our spatial discretization achieves true **second-order spatial accuracy $\mathcal{O}(h^2)$** ($2^2 = 4$).

```text
== Iterations needed to reach tol=1e-6 ==
N= 160  Jacobi= 21356  Gauss-Seidel= 12477  SOR= 322
```
> **Numerical Analysis Milestone:** SOR converges in **322 iterations**, compared to 21,356 for Jacobi — demonstrating the power of Young's over-relaxation theorem!

```text
Trap test (U-shaped dead end):
Classic potential field: reached goal = False (stuck at (52, 50))
Laplace (formulation B): reached goal = True (path length 110.3 cells)
```
> **Robotics & Physical Milestone:** Concrete proof that the Maximum Principle eliminates local traps!
