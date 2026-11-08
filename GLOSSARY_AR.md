<div dir="rtl" style="text-align:right">

# 📖 مسرد المصطلحات الرياضية والبرمجية (Arabic–English Glossary)

هذا المسرد يوحّد جميع المصطلحات المستخدمة في **اللابات الستة (`labs_ar/`)** و**دليل الفريق (`TEAM_GUIDE_AR.md`)** و**ورقة عمل الطالب (`STUDENT_WORKSHEET_AR.md`)**، مع ربط كل مصطلح بالصفحة المقابلة في **مذكرات المنهج (PDF)** وبالدالة المقابلة في كود المشروع (`rover_path_finder/`).

---

## 1. أساسيات المعادلات التفاضلية الجزئية (الباب الأول — القسم 1.1 و 1.2)

| المصطلح بالعربية | المصطلح بالإنجليزية (في المذكرة) | الرمز الرياضي | موقعه في المذكرة | أين يظهر في كود المشروع؟ |
|---|---|---|---|---|
| **معادلة تفاضلية جزئية** | Partial Differential Equation (PDE) | $f(x, y, z, p, q, \dots) = 0$ | ص 1 (Section 1.1) | المحرك الرياضي الكامل للمشروع |
| **متغيرات مستقلة** | Independent Variables | $x, y$ | ص 1، ص 3 | إحداثيات الشبكة `(x, y)` (الأعمدة والصفوف) |
| **متغير تابع** | Dependent Variable | $z(x,y)$ أو $\phi(x,y)$ | ص 1، ص 3 | الارتفاع `h[y, x]` أو جهد الملاحة `phi[y, x]` |
| **المشتقات الجزئية الأولى (الميول)** | First Partial Derivatives (Slopes) | $p = \frac{\partial z}{\partial x}, \; q = \frac{\partial z}{\partial y}$ | ص 3 (Section 1.1.6) | [`slope_map`](rover_path_finder/terrain.py) يحسب $p, q$ بـ `np.gradient` |
| **المشتقات الجزئية الثانية** | Second Partial Derivatives | $r = z_{xx}, \; s = z_{xy}, \; t = z_{yy}$ | ص 3 (Section 1.1.6) | استنتاج صيغة الـ 5 نقاط في [`solvers.py`](rover_path_finder/solvers.py) |
| **رتبة المعادلة** | Order of a PDE | أعلى رتبة مشتقة | ص 2 (Section 1.1.3) | الرتبة 1 (اللابات 1–3)، الرتبة 2 (اللابات 4–6) |
| **درجة المعادلة** | Degree of a PDE | أس أعلى مشتقة | ص 2 (Section 1.1.4) | الدرجة 1 (لاجرانج)، الدرجة 2 (Eikonal $p^2+q^2=1$) |
| **ثوابت اختيارية** | Arbitrary Constants | $a, b, c$ | ص 6 (Section 1.2) | اللاب 1: حذف موقع الحفرة $(a,b)$ لكشف المنحدرات |
| **قاعدة العمل** | Working Rule | خطوات الحل القياسية | ص 11 (Section 1.3.2) | خطوات الحل المرقمة في كل لاب |

---

## 2. معادلات الرتبة الأولى: لاجرانج وشاربيت (الباب الأول — القسم 1.3)

| المصطلح بالعربية | المصطلح بالإنجليزية (في المذكرة) | الرمز الرياضي | موقعه في المذكرة | أين يظهر في كود المشروع؟ |
|---|---|---|---|---|
| **معادلة شبه خطية (معادلة لاجرانج)** | Quasi-Linear / Lagrange Equation | $P p + Q q = R$ | ص 4، ص 11 (Section 1.3.1) | اللاب 2: معادلة دالة الانسياب $\phi_x \psi_x + \phi_y \psi_y = 0$ |
| **معادلات لاجرانج المساعدة** | Lagrange's Auxiliary Equations | $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$ | ص 11 (Section 1.3.2) | اللاب 2: معادلة مسار المركبة $\frac{dx}{u} = \frac{dy}{v}$ في [`descend`](rover_path_finder/planners.py) |
| **منحنى مميز / خط انسياب** | Characteristic Curve / Streamline | $u(x,y,z) = c_1, \; v(x,y,z) = c_2$ | ص 11–12 | المسار الفعلي `path` الذي تتبعه المركبة |
| **دالة اختيارية** | Arbitrary Function | $\Phi(u, v) = 0$ | ص 12 | الحل العام لمعادلات الرتبة الأولى والرتب العليا |
| **الحل التام (التكامل التام)** | Complete Integral / Solution | $z = f(x, y, a, b)$ | ص 12، ص 17 | اللاب 3: عائلة الموجات المستوية في الحالات القياسية |
| **الحل العام** | General Solution | $\Phi(u, v) = 0$ | ص 12 | اللاب 2، اللاب 4، اللاب 5 |
| **صيغة كليرو** | Clairaut's Form | $z = px + qy + f(p, q)$ | ص 18–19 (Section 1.3.3) | اللاب 3: تعويض مباشر $p=a, q=b$ |
| **طريقة شاربيت** | Charpit's Method | $\frac{dp}{f_x+pf_z} = \frac{dq}{f_y+qf_z} = \dots$ | ص 24–26 (Section 1.3.6) | اللاب 3: الطريقة العامة لحل أي معادلة غير خطية من الرتبة الأولى |
| **معادلة المسافة (الأيكونال)** | Eikonal / Distance Equation | $p^2 + q^2 = 1 \iff \|\nabla T\| = 1$ | ص 5 (Ex.1)، ص 17 | اللاب 3: حساب مسافة الأمان [`dilate`](rover_path_finder/terrain.py) وأقصر مسار [`dijkstra_length`](rover_path_finder/planners.py) |

---

## 3. مؤثرات الرتب العليا ومعادلة لابلاس (الباب الأول 1.4 والباب الثاني 2.1)

| المصطلح بالعربية | المصطلح بالإنجليزية (في المذكرة) | الرمز الرياضي | موقعه في المذكرة | أين يظهر في كود المشروع؟ |
|---|---|---|---|---|
| **المؤثرات التفاضلية** | Differential Operators | $D_x = \frac{\partial}{\partial x}, \; D_y = \frac{\partial}{\partial y}$ | ص 34 (Section 1.4) | اللاب 4 واللاب 5 |
| **معادلة متجانسة (بمعنى رتب المشتقات)** | Homogeneous Linear PDE | $(A_0 D_x^n + \dots + A_n D_y^n)z = f(x,y)$ | ص 34 (Section 1.4) | اللاب 4: جميع المشتقات من نفس الرتبة $n$ |
| **معادلة غير متجانسة (بمعنى اختلاف الرتب)** | Non-Homogeneous Linear PDE | تحتوي مشتقات من رتب مختلفة | الباب 2، ص 1 (PDF ص 53) | اللاب 5: مثل $(D_x^2 - D_y^2 + D_x)z = 0$ |
| **المعادلة المساعدة (المميزة)** | Auxiliary / Characteristic Equation (A.E.) | $F(m, 1) = 0$ | ص 36 (Section 1.4) | اللاب 4: دالة `solve_operator_roots` |
| **الحل المكمل (الدالة المكملة)** | Complementary Function (C.F.) | $z_c$ (حل المعادلة عند $f=0$) | ص 35، الباب 2 ص 2 | اللاب 4 واللاب 5 |
| **التكامل الخاص (الحل الخاص)** | Particular Integral (P.I.) | $z_p = \frac{1}{F(D_x, D_y)} f(x,y)$ | ص 40–57 | اللاب 4 (الحالات المختصرة للدوال الأسية والمثلثية) |
| **مؤثر قابل للتحليل** | Reducible Operator | يتحلل إلى عوامل $(a D_x + b D_y + c)$ | الباب 2، ص 1–4 (PDF ص 53–56) | اللاب 5: كل عامل خطي يعطي حداً أسياً $e^{-(c/a)x}\Phi(ay-bx)$ |
| **مؤثر غير قابل للتحليل** | Irreducible Operator | لا يتحلل لعوامل خطية | الباب 2، ص 1، ص 5 (PDF ص 53، 57) | اللاب 5: يُحل بمتسلسلة أسية $\sum A_i e^{a_i x + b_i y}$ حيث $F(a_i, b_i)=0$ |
| **معادلة لابلاس** | Laplace's Equation | $(D_x^2 + D_y^2)\phi = \nabla^2\phi = 0$ | ص 39، مثال 5 (PDF ص 33) | اللاب 4 واللاب 6: المعادلة الأساسية لحقل جهد الملاحة |
| **دالة توافقية** | Harmonic Function | أي دالة تحقق $\nabla^2\phi = 0$ | ص 39 | حقل الجهد `phi` الذي توجه به المركبة |

---

## 4. الحل العددي وهندسة ملاحة المركبة (اللاب 6 وكود المشروع)

| المصطلح بالعربية | المصطلح بالإنجليزية | الرمز / الكود | أين يظهر في كود المشروع؟ |
|---|---|---|---|
| **التقطيع الشبكي (الفروق المنتهية)** | Finite-Difference Discretization | تقريب المشتقات على شبكة $N \times N$ | [`solvers.py`](rover_path_finder/solvers.py) |
| **قالب النقاط الخمس** | 5-Point Stencil / Mean Value Property | $\phi_{i,j} = \frac{1}{4}(\phi_{i+1,j}+\phi_{i-1,j}+\phi_{i,j+1}+\phi_{i,j-1})$ | [`_avg(phi)`](rover_path_finder/solvers.py) |
| **مبدأ القيمة العظمى والصغرى** | Maximum Principle *(إثراء خارج المذكرة)* | القيم العظمى والصغرى تقع على الحدود فقط | يفسر استحالة وجود قاع محلي (Local Minimum) داخل المنطقة الحرة |
| **شرط ديريشليه الحدي (قيمة ثابتة)** | Dirichlet Boundary Condition | تثبيت $\phi = 1$ (البداية) و $\phi = 0$ (الهدف) | القناع `fixed` في [`solvers.py`](rover_path_finder/solvers.py) |
| **شرط نيومان الحدي (جدار عازل)** | Neumann No-Flux Condition | $\frac{\partial\phi}{\partial n} = 0$ (استبعاد خلايا العوائق من المتوسط) | القناع `free` والمقام `cnt` في [`sor_neumann`](rover_path_finder/solvers.py) |
| **طريقة جاكوبي التكرارية** | Jacobi Method | تحديث جميع النقاط معاً من القيم القديمة | [`jacobi`](rover_path_finder/solvers.py) |
| **الاسترخاء المتتالي الفائق** | Successive Over-Relaxation (SOR) | $\phi^{(k+1)} = (1-\omega)\phi^{(k)} + \omega\,\text{avg}$ | [`sor`](rover_path_finder/solvers.py) و [`sor_neumann`](rover_path_finder/solvers.py) |
| **معامل الاسترخاء الأمثل (صيغة يونغ)** | Optimal Relaxation Factor (Young's Formula) | $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi/N)}$ | [`omega_opt(N)`](rover_path_finder/solvers.py) |
| **ترتيب رقعة الشطرنج (أحمر-أسود)** | Red-Black Ordering |`(xx + yy) % 2` لتحديث نصف الشبكة بالتناوب | [`sor_neumann`](rover_path_finder/solvers.py) |
| **مجال الجهد الاصطناعي الكلاسيكي** | Artificial Potential Field (APF) | $U = U_{\text{att}} + U_{\text{rep}}$ | [`apf_potential`](rover_path_finder/planners.py) (للمقارنة في اختبار الفخ) |

</div>

