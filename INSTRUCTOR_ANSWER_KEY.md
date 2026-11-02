# 🔑 Master Instructor Answer Key & Step-by-Step Solutions
**Course:** Applied Partial Differential Equations & Planetary Robotics  
**Document Purpose:** Comprehensive solution guide for students, teammates, and instructors. If you get stuck on any paper-and-pencil problem in the labs, consult this guide for the complete step-by-step derivation.

---

# 📑 Table of Contents
1. [Lab 1 Solutions: Elimination of Constants](#lab-1-elimination-of-constants)
2. [Lab 2 Solutions: Lagrange's Method of Characteristics](#lab-2-lagranges-method-of-characteristics)
3. [Lab 3 Solutions: Non-Linear PDEs & Charpit's Method](#lab-3-non-linear-pdes--charpits-method)
4. [Lab 4 Solutions: Higher-Order Linear Operators & Laplace](#lab-4-higher-order-linear-operators--laplace)
5. [Lab 5 Solutions: Non-Homogeneous Reducible Operators](#lab-5-non-homogeneous-reducible-operators)
6. [Lab 6 Solutions: Discrete Stencil & Rover Scale-Up](#lab-6-discrete-stencil--rover-scale-up)

---

# Lab 1: Elimination of Constants

### 📝 Challenge 1.1: Circular Craters
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

### 📝 Challenge 2.1: Euler's Homogeneous Equation
**Given Equation:**
$$x p + y q = z$$

**Step-by-Step Solution:**
1. Identify coefficients: $P = x, Q = y, R = z$.
2. Write Lagrange's auxiliary equations:
   $$\frac{dx}{x} = \frac{dy}{y} = \frac{dz}{z}$$
3. Take Fraction 1 and Fraction 2:
   $$\frac{dx}{x} = \frac{dy}{y} \implies \ln x - \ln y = \ln c_1 \implies \frac{x}{y} = c_1$$
4. Take Fraction 2 and Fraction 3:
   $$\frac{dy}{y} = \frac{dz}{z} \implies \ln y - \ln z = \ln c_2 \implies \frac{y}{z} = c_2$$
5. Form the general solution relation $\Phi(c_1, c_2) = 0$:
   $$\Phi\left(\frac{x}{y}, \frac{y}{z}\right) = 0 \quad \text{or} \quad z = y \cdot f\left(\frac{x}{y}\right)$$

**Final Answer:**
$$\Phi\left(\frac{x}{y}, \frac{y}{z}\right) = 0$$

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

### 📝 Challenge 3.1: Clairaut's Standard Form
**Given Equation:**
$$z = p x + q y + p q$$

**Step-by-Step Solution:**
1. Check the form: $z = p x + q y + f(p, q)$, where $f(p, q) = p q$.
2. By Clairaut's theorem, we set $p = a$ and $q = b$ (where $a$ and $b$ are arbitrary constants).
3. The complete integral is obtained by direct substitution:
   $$z = a x + b y + a b$$

**Final Answer:**
$$z = a x + b y + a b$$

---

### 📝 Challenge 3.2: Eikonal Wavefront Equation
**Given Equation:**
$$p^2 + q^2 = 1$$

**Step-by-Step Solution:**
1. This is Standard Form 1: $f(p, q) = 0$ (contains only $p$ and $q$).
2. Let $p = a$ and $q = b$. Then $a^2 + b^2 = 1 \implies b = \pm\sqrt{1 - a^2}$.
3. Substitute into the total differential $dz = p dx + q dy$:
   $$dz = a dx \pm \sqrt{1 - a^2} dy$$
4. Integrate directly:
   $$z(x, y) = a x \pm \sqrt{1 - a^2} y + c$$
5. (Finding the singular envelope representing circular ripples from origin):
   Differentiate w.r.t parameter $a$:
   $$0 = x \pm \frac{-2a}{2\sqrt{1 - a^2}} y \implies x = \frac{a}{\sqrt{1 - a^2}} y \implies a = \frac{x}{\sqrt{x^2 + y^2}}$$
   Substitute $a$ back into $z$:
   $$z = \frac{x^2}{\sqrt{x^2 + y^2}} + \frac{y^2}{\sqrt{x^2 + y^2}} = \frac{x^2 + y^2}{\sqrt{x^2 + y^2}} = \sqrt{x^2 + y^2}$$
   Squaring both sides yields:
   $$x^2 + y^2 = z^2$$

**Final Answer:**
* Complete Integral: $z = a x \pm \sqrt{1 - a^2} y + c$
* Singular Envelope: $(x - x_0)^2 + (y - y_0)^2 = z^2$ (Expanding circular wavefront)

---

# Lab 4: Higher-Order Linear Operators & Laplace

### 📝 Challenge 4.1: Laplace's Characteristic Roots
**Given Equation:**
$$(D_x^2 + D_y^2)z = 0$$

**Step-by-Step Solution:**
1. Replace $D_x \to m$ and $D_y \to 1$ to form the Auxiliary Equation (A.E.):
   $$m^2 + 1 = 0 \implies m^2 = -1$$
2. Take square roots:
   $$m = \pm \sqrt{-1} = \pm i \implies m_1 = i, \quad m_2 = -i$$
3. By the theorem for complex conjugate roots $m = \alpha \pm i\beta$ with $\alpha = 0, \beta = 1$:
   $$z = \phi_1(y + m_1 x) + \phi_2(y + m_2 x) = \phi_1(y + ix) + \phi_2(y - ix)$$

**Final Answer:**
$$m_1 = i, \quad m_2 = -i \implies z = \phi_1(y + ix) + \phi_2(y - ix)$$

---

### 📝 Challenge 4.2: Particular Integral under Sinusoidal Forcing
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

### 📝 Challenge 5.1: Factoring Reducible Linear Operators
**Given Equation:**
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$

**Step-by-Step Solution:**
1. The operator is factored into two linear factors:
   * **Factor 1:** $(2 D_x - 3 D_y + 1)z_1 = 0 \implies a_1 = 2, b_1 = -3, c_1 = 1$.
   * **Factor 2:** $(D_x + 2 D_y - 2)z_2 = 0 \implies a_2 = 1, b_2 = 2, c_2 = -2$.
2. Use the reducible factor theorem: $z = e^{-\frac{c}{a}x} \phi(a y - b x)$ (since $a \neq 0$):
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

### 📝 Challenge 5.2: Battery Dissipation Rate
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

### 📝 Challenge 6.1: 4-Node Hand Calculation Sweep
**Given Grid:**
* $4 \times 4$ grid with boundary nodes:
  * Top (Source): $\phi = 1.0$
  * Bottom (Sink): $\phi = 0.0$
  * Left & Right: $\phi = 0.5$
* Interior cells $A(1, 1), B(1, 2), C(2, 1), D(2, 2)$ initialized to $0.0$.
* Stencil formula: $\phi_{i,j}^{(1)} = \frac{1}{4}(\phi_{\text{up}} + \phi_{\text{down}} + \phi_{\text{left}} + \phi_{\text{right}})$.

**Step-by-Step Calculation:**
1. **For Cell A:**
   * Up neighbor (Top boundary): $\phi_{\text{up}} = 1.0$
   * Down neighbor (Cell C): $\phi_{\text{down}} = 0.0$
   * Left neighbor (Left boundary): $\phi_{\text{left}} = 0.5$
   * Right neighbor (Cell B): $\phi_{\text{right}} = 0.0$
   * Compute average:
     $$\phi_A^{(1)} = \frac{1.0 + 0.0 + 0.5 + 0.0}{4} = \frac{1.5}{4} = 0.375$$

2. **For Cell B:**
   * Up neighbor (Top boundary): $\phi_{\text{up}} = 1.0$
   * Down neighbor (Cell D): $\phi_{\text{down}} = 0.0$
   * Left neighbor (Cell A): $\phi_{\text{left}} = 0.0$ (using Jacobi simultaneous values)
   * Right neighbor (Right boundary): $\phi_{\text{right}} = 0.5$
   * Compute average:
     $$\phi_B^{(1)} = \frac{1.0 + 0.0 + 0.0 + 0.5}{4} = \frac{1.5}{4} = 0.375$$

**Final Answer:**
$$\phi_A^{(1)} = 0.375, \quad \phi_B^{(1)} = 0.375$$

---

### 📝 Challenge 6.2: Optimal Relaxation Factor Formula
**Formula:**
$$\omega_{\text{opt}} = \frac{2}{1 + \sin\left(\frac{\pi}{N}\right)}$$
* For $N = 16$: $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi / 16)} = \frac{2}{1 + 0.19509} \approx 1.6735$
* For $N = 160$: $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi / 160)} = \frac{2}{1 + 0.01963} \approx 1.9615$

