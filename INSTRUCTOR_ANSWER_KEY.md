# 🔑 Master Instructor Answer Key & Step-by-Step Solutions
**Course:** Applied Partial Differential Equations & Planetary Robotics  
**Document Purpose:** Comprehensive solution guide for students, teammates, and instructors. Every problem includes exact page references to the 62-page course lecture notes PDF (both handwritten notes page numbers and PDF page numbers) and direct links to the [`rover_path_finder/`](rover_path_finder/) codebase.

---

# 📑 Table of Contents
1. [Lab 1 Solutions: Elimination of Constants (Ch. 1, Sec. 1.1–1.2)](#lab-1-elimination-of-constants)
2. [Lab 2 Solutions: Lagrange's Method of Characteristics (Ch. 1, Sec. 1.3.1)](#lab-2-lagranges-method-of-characteristics)
3. [Lab 3 Solutions: Non-Linear PDEs & Charpit's Method (Ch. 1, Sec. 1.3.2–1.3.6)](#lab-3-non-linear-pdes--charpits-method)
4. [Lab 4 Solutions: Higher-Order Linear Operators & Laplace (Ch. 1, Sec. 1.4)](#lab-4-higher-order-linear-operators--laplace)
5. [Lab 5 Solutions: Non-Homogeneous Reducible Operators (Ch. 2, Sec. 2.1)](#lab-5-non-homogeneous-reducible-operators)
6. [Lab 6 Solutions: Discrete Stencil & Rover Scale-Up](#lab-6-discrete-stencil--rover-scale-up)

---

# Lab 1: Elimination of Constants
* **Lecture Notes Reference:** Chapter 1, Sections 1.1 & 1.2 (Notes pp. 1–10 / PDF pp. 2–11).
  * Worked Example 1 on Notes p. 8 (PDF pp. 9–10): $z = ax + by + a^2 + b^2$ (2-parameter family of planes $\implies z = px + qy + p^2 + q^2$).
  * Worked Example 2 on Notes p. 9 (PDF p. 10): $z = (x - a)^2 + (y - b)^2 \implies p^2 + q^2 = 4z$.
* **Codebase Connection:** [`terrain.slope_map`](rover_path_finder/terrain.py) computes $p = \frac{\partial z}{\partial x}$ and $q = \frac{\partial z}{\partial y}$ via `Q, P = np.gradient(Z, dy, dx)` and returns $\|\nabla z\| = \sqrt{p^2 + q^2}$.

### 📝 Challenge 1.1: Circular Craters (Notes p. 9 / PDF p. 10, Ex. 2)
**Given Equation:**
$$z = (x - a)^2 + (y - b)^2$$
where $a$ and $b$ are arbitrary constants representing the unknown center of the crater.

**Step-by-Step Solution:**
1. Differentiate partially with respect to $x$:
   $$p = \frac{\partial z}{\partial x} = 2(x - a) \implies (x - a) = \frac{p}{2}$$
2. Differentiate partially with respect to $y$:
   $$q = \frac{\partial z}{\partial y} = 2(y - b) \implies (y - b) = \frac{q}{2}$$
3. Square both derived relations:
   $$(x - a)^2 = \frac{p^2}{4}, \quad (y - b)^2 = \frac{q^2}{4}$$
4. Add them together:
   $$(x - a)^2 + (y - b)^2 = \frac{p^2 + q^2}{4}$$
5. Substitute the original relation $z = (x - a)^2 + (y - b)^2$:
   $$z = \frac{p^2 + q^2}{4} \implies p^2 + q^2 = 4z$$

**Final Answer:**
$$\left(\frac{\partial z}{\partial x}\right)^2 + \left(\frac{\partial z}{\partial y}\right)^2 = 4z \quad \text{or} \quad p^2 + q^2 = 4z$$

---

### 📝 Challenge 1.2: Rover Parabolic Basin
**Given Equation:**
$$z = \frac{1}{2} a x^2 + \frac{1}{2} b y^2$$

**Step-by-Step Solution:**
1. Differentiate w.r.t $x$:
   $$p = \frac{\partial z}{\partial x} = a x \implies a = \frac{p}{x}$$
2. Differentiate w.r.t $y$:
   $$q = \frac{\partial z}{\partial y} = b y \implies b = \frac{q}{y}$$
3. Substitute $a$ and $b$ back into the original equation:
   $$z = \frac{1}{2} \left(\frac{p}{x}\right) x^2 + \frac{1}{2} \left(\frac{q}{y}\right) y^2 = \frac{1}{2} x p + \frac{1}{2} y q$$
4. Multiply through by 2:
   $$x p + y q = 2z$$

**Final Answer:**
$$x \frac{\partial z}{\partial x} + y \frac{\partial z}{\partial y} = 2z$$

---

# Lab 2: Lagrange's Method of Characteristics
* **Lecture Notes Reference:** Chapter 1, Section 1.3.1 (Notes pp. 11–16 / PDF pp. 12–17).
  * Worked Example 1 on Notes p. 12 (PDF p. 13): $2p - 3q = 2x$.
  * Exercise 5 on Notes p. 16 (PDF p. 17): $xp + yq = z$.
* **Codebase Connection:** [`planners.descend`](rover_path_finder/planners.py) integrates the characteristic ODE $\frac{dx}{P} = \frac{dy}{Q}$ numerically with step size `step` along the normalized negative gradient $(P, Q) = -\nabla\phi / \|\nabla\phi\|$.

### 📝 Challenge 2.1: Euler's Homogeneous Equation (Notes p. 16 / PDF p. 17, Ex. 5)
**Given Equation:**
$$x p + y q = z$$

**Step-by-Step Solution:**
1. Identify coefficients: $P = x, Q = y, R = z$.
2. Write Lagrange's auxiliary equations:
   $$\frac{dx}{x} = \frac{dy}{y} = \frac{dz}{z}$$
3. Take Fraction 1 and Fraction 2:
   $$\frac{dx}{x} = \frac{dy}{y} \implies \ln |x| - \ln |y| = \ln |c_1| \implies \frac{x}{y} = c_1$$
4. Take Fraction 2 and Fraction 3:
   $$\frac{dy}{y} = \frac{dz}{z} \implies \ln |y| - \ln |z| = \ln |c_2| \implies \frac{y}{z} = c_2$$
5. Form the general solution relation $\Phi(c_1, c_2) = 0$:
   $$\Phi\left(\frac{x}{y}, \frac{y}{z}\right) = 0 \quad \text{or} \quad z = y \cdot f\left(\frac{x}{y}\right)$$

**Final Answer:**
$$u_1 = \frac{x}{y}, \quad u_2 = \frac{y}{z}, \quad \Phi\left(\frac{x}{y}, \frac{y}{z}\right) = 0$$

---

### 📝 Challenge 2.2: Rover Parabolic Streamlines
**Given Potential Field:**
$$\phi(x, y) = x^2 + 2y^2$$
The rover rolls downhill along velocity vector $\mathbf{v} = (u, v) = -\nabla\phi = (-2x, -4y)$.  
Transport equation: $u \frac{\partial \phi}{\partial x} + v \frac{\partial \phi}{\partial y} = 0$.

**Step-by-Step Solution:**
1. Write Lagrange's streamline equation:
   $$\frac{dx}{u} = \frac{dy}{v} \implies \frac{dx}{-2x} = \frac{dy}{-4y}$$
2. Simplify the denominators by dividing by $-2$:
   $$\frac{dx}{x} = \frac{dy}{2y}$$
3. Integrate both sides:
   $$\ln |x| = \frac{1}{2} \ln |y| + C_0 \implies \ln |x| = \ln \sqrt{|y|} + C_0$$
4. Exponentiate both sides:
   $$|x| = C_1 \sqrt{|y|} \implies x^2 = C y \implies y = k x^2$$

**Final Answer:**
$$y = k x^2 \quad \text{(Parabolic tire trajectories in the sand)}$$

---

# Lab 3: Non-Linear PDEs & Charpit's Method
* **Lecture Notes Reference:** Chapter 1, Sections 1.3.2–1.3.6 (Notes pp. 16–26 / PDF pp. 17–27).
  * Standard Form I ($f(p,q)=0$): Notes p. 18 (PDF p. 19).
  * Clairaut's Equation ($z = px + qy + f(p,q)$): Notes p. 19 (PDF p. 20, Ex. 1: $z = px + qy + pq$).
  * Charpit's General Method: Notes pp. 24–26 (PDF pp. 25–27):
    $$\frac{dx}{-f_p} = \frac{dy}{-f_q} = \frac{dz}{-p f_p - q f_q} = \frac{dp}{f_x + p f_z} = \frac{dq}{f_y + q f_z}$$
* **Codebase Connection:** [`terrain.dilate`](rover_path_finder/terrain.py) expands obstacle safety buffers outward by radius $r$, which is the discrete wavefront boundary $z(x,y) \le r$ of the Eikonal equation $p^2 + q^2 = 1$.

### 📝 Challenge 3.1: Clairaut's Standard Form (Notes p. 19 / PDF p. 20, Ex. 1)
**Given Equation:**
$$z = p x + q y + p q$$

**Step-by-Step Solution:**
1. Check the form: $z = p x + q y + f(p, q)$, where $f(p, q) = p q$.
2. By Charpit's auxiliary equations, $f_x + p f_z = 0$ and $f_y + q f_z = 0 \implies dp = 0, dq = 0 \implies p = a, q = b$.
3. Substitute $p = a$ and $q = b$ directly into the PDE to obtain the complete integral:
   $$z = a x + b y + a b$$

**Final Answer:**
$$z = a x + b y + a b$$

---

### 📝 Challenge 3.2: Eikonal Wavefront Equation
**Given Equation:**
$$p^2 + q^2 = 1$$

**Step-by-Step Solution:**
1. This is Standard Form I: $f(p, q) = p^2 + q^2 - 1 = 0$ (contains only $p$ and $q$).
2. From Charpit's system, $\frac{dp}{0} = \frac{dq}{0} \implies p = a, q = b$ with $a^2 + b^2 = 1 \implies b = \pm\sqrt{1 - a^2}$.
3. Substitute into the total differential $dz = p dx + q dy$:
   $$dz = a dx \pm \sqrt{1 - a^2} dy$$
4. Integrate directly:
   $$z(x, y) = a x \pm \sqrt{1 - a^2} y + c$$
5. (Finding the singular envelope representing circular ripples from origin, $c=0$):
   Differentiate w.r.t parameter $a$:
   $$0 = x \mp \frac{a}{\sqrt{1 - a^2}} y \implies a = \pm\frac{x}{\sqrt{x^2 + y^2}}$$
   Substitute $a$ back into $z$ and square both sides:
   $$x^2 + y^2 = z^2$$

**Final Answer:**
* Complete Integral: $z = a x + \sqrt{1 - a^2} y + c$
* Singular Envelope: $x^2 + y^2 = z^2$ (Expanding circular wavefront)

---

# Lab 4: Higher-Order Linear Operators & Laplace
* **Lecture Notes Reference:** Chapter 1, Section 1.4 (Notes pp. 34–57 / PDF pp. 28–51).
  * Homogeneous operators & Auxiliary Equation (A.E.): Notes pp. 34–39 (PDF pp. 28–33).
  * **Laplace's Equation $(D_x^2 + D_y^2)z = 0$:** Worked Example 5 on **Notes p. 39 (PDF p. 33)**.
  * Particular Integral for $\sin(ax+by)$: Shortcut Rule on Notes p. 45 (PDF p. 39); Worked Example 4 on **Notes p. 48 (PDF p. 42)**.
* **Codebase Connection:** [`solvers._avg`](rover_path_finder/solvers.py) discretizes $(D_x^2 + D_y^2)\phi = 0$ into the 4-neighbor average $\phi_{i,j} = \frac{1}{4}(\phi_{i+1,j} + \phi_{i-1,j} + \phi_{i,j+1} + \phi_{i,j-1})$.

### 📝 Challenge 4.1: Laplace's Characteristic Roots (Notes p. 39 / PDF p. 33, Ex. 5)
**Given Equation:**
$$(D_x^2 + D_y^2)z = 0$$

**Step-by-Step Solution:**
1. Replace $D_x \to m$ and $D_y \to 1$ to form the Auxiliary Equation (A.E.):
   $$m^2 + 1 = 0 \implies m^2 = -1$$
2. Take square roots:
   $$m = \pm \sqrt{-1} = \pm i \implies m_1 = i, \quad m_2 = -i$$
3. By Case 3 for distinct roots:
   $$z = \phi_1(y + m_1 x) + \phi_2(y + m_2 x) = \phi_1(y + ix) + \phi_2(y - ix)$$

**Final Answer:**
$$m_1 = i, \quad m_2 = -i \implies z = \phi_1(y + ix) + \phi_2(y - ix)$$

---

### 📝 Challenge 4.2: Particular Integral under Sinusoidal Forcing (Notes p. 48 / PDF p. 42, Ex. 4)
**Given Equation:**
$$(D_x^2 - D_x D_y - 6 D_y^2)z = \sin(2x - 3y)$$

**Step-by-Step Solution:**
1. The forcing term is $\sin(a x + b y)$ with $a = 2, b = -3$.
2. By P.I. Case 2 shortcut rule:
   $$D_x^2 \to -a^2 = -(2)^2 = -4$$
   $$D_x D_y \to -a b = -(2)(-3) = +6$$
   $$D_y^2 \to -b^2 = -(-3)^2 = -9$$
3. Evaluate the operator polynomial $F(-a^2, -ab, -b^2)$:
   $$F(-4, 6, -9) = (-4) - (6) - 6(-9) = -10 + 54 = 44$$
4. Since $44 \neq 0$, the Particular Integral is:
   $$z_2 = \frac{1}{44} \sin(2x - 3y)$$

**Final Answer:**
$$z_2 = \frac{1}{44} \sin(2x - 3y)$$

---

# Lab 5: Non-Homogeneous Reducible Operators
* **Lecture Notes Reference:** Chapter 2, Section 2.1 (Notes Ch. 2 pp. 1–10 / PDF pp. 52–62).
  * Case (A) Theorem for linear factor $(a D_x + b D_y + c)z = 0 \implies z = e^{-(c/a)x}\phi(ay - bx)$: Notes Ch. 2 p. 2 (PDF p. 54).
  * Worked Example 5: $(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$ on **Notes Ch. 2 p. 4 (PDF p. 56)**.
* **Codebase Connection:** Comparing [`planners.dirichlet_potential`](rover_path_finder/planners.py) vs [`planners.neumann_potential`](rover_path_finder/planners.py) in narrow corridors: absorbing Dirichlet walls ($\phi = 0$) introduce an effective transverse eigenvalue $-(\pi/W)^2$ that causes exponential decay $e^{-(\pi/W)x}$ down the corridor, whereas reflective Neumann walls ($\frac{\partial \phi}{\partial n} = 0$) preserve a strong linear gradient.

### 📝 Challenge 5.1: Factoring Reducible Linear Operators (Notes Ch. 2 p. 4 / PDF p. 56, Ex. 5)
**Given Equation:**
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$

**Step-by-Step Solution:**
1. The operator is factored into two linear factors:
   * **Factor 1:** $(2 D_x - 3 D_y + 1)z_1 = 0 \implies a_1 = 2, b_1 = -3, c_1 = 1$.
   * **Factor 2:** $(D_x + 2 D_y - 2)z_2 = 0 \implies a_2 = 1, b_2 = 2, c_2 = -2$.
2. Use the reducible factor theorem $z = e^{-\frac{c}{a}x} \phi(a y - b x)$ (for $a \neq 0$):
   * For Factor 1:
     $$e^{-\frac{c_1}{a_1}x} = e^{-\frac{1}{2}x}, \quad a_1 y - b_1 x = 2y - (-3)x = 2y + 3x$$
     $$z_1 = e^{-\frac{1}{2}x} \phi_1(2y + 3x)$$
   * For Factor 2:
     $$e^{-\frac{c_2}{a_2}x} = e^{-\frac{-2}{1}x} = e^{2x}, \quad a_2 y - b_2 x = y - 2x$$
     $$z_2 = e^{2x} \phi_2(y - 2x)$$
3. Superpose solutions: $z = z_1 + z_2$:
   $$z = e^{-\frac{1}{2}x} \phi_1(2y + 3x) + e^{2x} \phi_2(y - 2x)$$

**Final Answer:**
$$z = e^{-\frac{x}{2}} \phi_1(2y + 3x) + e^{2x} \phi_2(y - 2x)$$

---

### 📝 Challenge 5.2: Signal / Potential Dissipation Rate
**Given Equation:**
$$(D_x + 2 D_y + 1)z = 0$$

**Step-by-Step Solution:**
1. Parameters: $a = 1, b = 2, c = 1$.
2. Solution formula:
   $$z = e^{-\frac{c}{a}x} \phi(a y - b x) = e^{-\frac{1}{1}x} \phi(1y - 2x) = e^{-x} \phi(y - 2x)$$

**Final Answer:**
$$z = e^{-x} \phi(y - 2x) \quad \text{(Exponential damping factor is } e^{-x}\text{)}$$

---

# Lab 6: Discrete Stencil & Rover Scale-Up
* **Codebase Connection:** [`solvers.jacobi`](rover_path_finder/solvers.py), [`solvers.gauss_seidel`](rover_path_finder/solvers.py), [`solvers.sor_dirichlet`](rover_path_finder/solvers.py), [`solvers.sor_neumann`](rover_path_finder/solvers.py), and [`planners.neumann_potential`](rover_path_finder/planners.py).

### 📝 Challenge 6.1: 4-Node Hand Calculation (Jacobi Sweep 1)
**Given Grid:**
* $4 \times 4$ grid with fixed Dirichlet boundary nodes for this toy exercise:
  * Top (Source): $\phi = 1.0$
  * Bottom (Sink): $\phi = 0.0$
  * Left & Right walls: $\phi = 0.5$
* Interior cells $A(1, 1), B(1, 2), C(2, 1), D(2, 2)$ initialized to $\phi^{(0)} = 0.0$.
* Jacobi Sweep 1 formula (using $k=0$ neighbor values simultaneously):
  $$\phi_{i,j}^{(1)} = \frac{1}{4}\left(\phi_{\text{up}}^{(0)} + \phi_{\text{down}}^{(0)} + \phi_{\text{left}}^{(0)} + \phi_{\text{right}}^{(0)}\right)$$

**Step-by-Step Calculation:**
1. **For Cell A ($\phi_{1,1}^{(1)}$):**
   * Up neighbor (Top boundary): $\phi_{\text{up}}^{(0)} = 1.0$
   * Down neighbor (Cell C): $\phi_{\text{down}}^{(0)} = 0.0$
   * Left neighbor (Left boundary): $\phi_{\text{left}}^{(0)} = 0.5$
   * Right neighbor (Cell B): $\phi_{\text{right}}^{(0)} = 0.0$
   * Compute average:
     $$\phi_A^{(1)} = \frac{1.0 + 0.0 + 0.5 + 0.0}{4} = \frac{1.5}{4} = 0.375$$

2. **For Cell B ($\phi_{1,2}^{(1)}$):**
   * Up neighbor (Top boundary): $\phi_{\text{up}}^{(0)} = 1.0$
   * Down neighbor (Cell D): $\phi_{\text{down}}^{(0)} = 0.0$
   * Left neighbor (Cell A): $\phi_{\text{left}}^{(0)} = 0.0$ (Jacobi simultaneous update uses old $k=0$ value)
   * Right neighbor (Right boundary): $\phi_{\text{right}}^{(0)} = 0.5$
   * Compute average:
     $$\phi_B^{(1)} = \frac{1.0 + 0.0 + 0.0 + 0.5}{4} = \frac{1.5}{4} = 0.375$$
   * *(Comparison with Gauss-Seidel: if updated in-place using $\phi_A^{(1)} = 0.375$ immediately, $\phi_B^{(1),\text{GS}} = \frac{1.0 + 0.0 + 0.375 + 0.5}{4} = 0.46875$.)*

**Final Answer:**
$$\phi_A^{(1)} = 0.375, \quad \phi_B^{(1)} = 0.375$$

---

### 📝 Challenge 6.2: Optimal Relaxation Factor Formula
**Formula:**
$$\omega_{\text{opt}} = \frac{2}{1 + \sin\left(\frac{\pi}{N}\right)}$$
* For $N = 16$: $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi / 16)} = \frac{2}{1 + 0.19509} \approx 1.6735$
* For $N = 160$: $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi / 160)} = \frac{2}{1 + 0.01963} \approx 1.9615$

---

### 📝 Challenge 6.3: The Physics & Math Bridge (APF vs. Laplace & Discrete Maximum Principle)
**Question:** Why does classical Artificial Potential Field (APF) fail inside Martian craters, and how does Laplace's equation guarantee the rover will never get trapped?

**Step-by-Step Rationale:**
1. **Classical APF Equation:**
   $$U(\mathbf{x}) = U_{\text{att}}(\mathbf{x}) + U_{\text{rep}}(\mathbf{x})$$
   * At a point inside a U-shaped dead end facing the goal behind a wall, the attractive forward force $\mathbf{F}_{\text{att}} = -\nabla U_{\text{att}}$ is equal and opposite to the repulsive obstacle force $\mathbf{F}_{\text{rep}} = -\nabla U_{\text{rep}}$.
   * Result: $\mathbf{F}_{\text{net}} = -\nabla U = \mathbf{0}$ with positive-definite Hessian. The forces cancel out, creating an **artificial local minimum (pothole)** where the rover freezes permanently.

2. **The Laplace PDE Replacement:**
   $$\nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} = 0$$
   * **Dirichlet Boundary Conditions:** Start fixed at high potential $\phi = 1.0$; Goal fixed at sink potential $\phi = 0.0$.
   * **Neumann Boundary Conditions:** Obstacle crater walls enforced as insulated zero-flux boundaries $\frac{\partial \phi}{\partial n} = 0$ via ghost-point reflection in [`solvers.sor_neumann`](rover_path_finder/solvers.py).

3. **The 1-Line Discrete Maximum Principle Proof:**
   * At every interior free-space cell $(i,j)$, the converged discrete Laplace equation states:
     $$\phi_{i,j} = \frac{1}{4}\left(\phi_{i+1,j} + \phi_{i-1,j} + \phi_{i,j+1} + \phi_{i,j-1}\right)$$
   * **Proof by contradiction:** Suppose an interior cell $(i,j)$ were a strict local minimum, meaning $\phi_{i,j} < \phi_{\text{neighbor}}$ for all 4 neighbors. Then the average of the 4 neighbors would be strictly greater than $\phi_{i,j}$, contradicting $\phi_{i,j} = \frac{1}{4}\sum \phi_{\text{neighbor}}$!
   * Therefore, every interior cell with a non-constant neighborhood always has at least one neighbor with a strictly lower $\phi$, guaranteeing that [`planners.descend`](rover_path_finder/planners.py) reaches the global goal $\phi = 0.0$ without ever getting trapped.
