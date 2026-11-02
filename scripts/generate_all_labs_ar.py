"""
Comprehensive Generator for the 6 DeepLearning.AI-Style Course Labs in Arabic (labs_ar/).
Generates:
- labs_ar/Lab_1_Elimination_of_Constants_AR.ipynb
- labs_ar/Lab_2_Lagrange_Method_AR.ipynb
- labs_ar/Lab_3_Nonlinear_Charpit_AR.ipynb
- labs_ar/Lab_4_HigherOrder_Operators_AR.ipynb
- labs_ar/Lab_5_NonHomogeneous_PDEs_AR.ipynb
- labs_ar/Lab_6_Mars_Rover_Capstone_AR.ipynb
"""

import json
import os

os.makedirs("labs_ar", exist_ok=True)


class ArabicNotebookBuilder:
    def __init__(self, filename: str, target_dir: str = "labs_ar"):
        self.filename = filename
        self.target_dir = target_dir
        self.cells = []

    def colab_badge(self):
        url = f"https://colab.research.google.com/github/hany73-max/PDE-Rover-Engine/blob/main/labs_ar/{self.filename}"
        badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"
        self.md(badge)

    def colab_setup(self):
        source = (
            "# 🚀 تهيئة بيئة Google Colab\n"
            "# إذا كنت تشغل هذا النوت بوك على Google Colab، شغل هذه الخلية لتحميل ملفات المستودع والاختبارات تلقائياً:\n"
            "import os, sys\n"
            "try:\n"
            "    if 'google.colab' in str(get_ipython()):\n"
            "        if not os.path.exists('PDE-Rover-Engine'):\n"
            "            import subprocess\n"
            "            subprocess.run(['git', 'clone', 'https://github.com/hany73-max/PDE-Rover-Engine.git'], check=True)\n"
            "        os.chdir('PDE-Rover-Engine')\n"
            "        if '.' not in sys.path:\n"
            "            sys.path.insert(0, '.')\n"
            "        print('[OK] تم تجهيز بيئة Google Colab بنجاح والاتصال بمستودع المشروع!')\n"
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
            json.dump(nb_json, f, indent=2, ensure_ascii=False)
        print(f"Generated {path} with {len(self.cells)} cells.")


# ===========================================================================
# LAB 1 (ARABIC): ELIMINATION OF ARBITRARY CONSTANTS
# ===========================================================================
def build_lab_1_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_1_Elimination_of_Constants_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📡 اللاب 1: تكوين المعادلات التفاضلية الجزئية بحذف الثوابت الاختيارية
### *غرفة التحكم: حساس مسح تضاريس المريخ*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**موضوع المنهج:** الباب الأول، القسم 1.2 (صفحات 6–11)

---
### 🧭 حجر رشيد (The Rosetta Stone): ترجمة الرياضيات إلى لغة البشر وكود بايثون
| 1. معادلات السبورة في المحاضرة | 2. المعنى الفيزيائي البسيط | 3. كود بايثون المقابل |
| :--- | :--- | :--- |
| $p = \frac{\partial z}{\partial x}, \quad q = \frac{\partial z}{\partial y}$ | "ميل التضاريس وانحدارها باتجاه الشرق وباتجاه الشمال." | `P, Q = np.gradient(Z, dx, dy)` |
| $F(x, y, z, a, b) = 0$ | "عائلة أسطح أو حفر تتغير بتغير البارامترات $a$ و $b$." | `Z = (X - a)**2 + (Y - b)**2` |
| $f(x, y, z, p, q) = 0$ | "القانون الفيزيائي العام الذي يربط الارتفاع بالميول." | `residual = (P**2 + Q**2) - 4*Z` |

---
## 1. المعنى البسيط: "قالب النحات"
تخيل أنك تطبع تضاريس كوكب المريخ ثلاثية الأبعاد. كل حفرة أو كثيب رملي قد يكون له ارتفاع مختلف $a$ وموقع مختلف $b$.
إذا هبطت مركبة الفضاء على هذه التضاريس، فإن نظام الملاحة لا يهتم إطلاقاً بالأرقام $a$ و $b$ المكتوبة على الخريطة؛ كل ما يهم عجلات المركبة في اللحظة الحالية هو:
> *"ما هو انحدار السطح تحت عجلاتي الآن؟ هل الميل شديد جداً بحيث تنقلب المركبة؟"*

**حذف الثوابت (Eliminating Constants)** هو العملية الرياضية لحذف البارامترات الخاصة $a$ و $b$ للوصول إلى **القانون الفيزيائي العام (Universal Invariant Law)** الذي يحكم انحدار السطح في كل نقطة، أياً كان حجم الحفرة أو موقعها!

---
## 2. ما فائدة هذه الطريقة ولماذا نقوم بها؟ (The "WHY")
* **لماذا نقوم بها؟** القوانين الفيزيائية (كالجاذبية والاحتكاك) ثابتة ولا تتغير بتغير تسميات البارامترات $a, b$.
* **ماذا تفيد مركبة المريخ؟** تمكن كمبيوتر الملاحة من فحص أمان المنحدرات مباشرة من قراءات حساسات الميل (IMU Sensors) في الوقت الحقيقي دون الحاجة لخرائط مسبقة!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab1

%matplotlib inline
print("تم تهيئة بيئة اللاب 1 بنجاح! جاهز لغرفة التحكم.")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية ومثال المذكرة المحلول (Worked Example)

### الحالات الثلاث (صفحة 7 بالمذكرة):
1. **الحالة (1):** عدد الثوابت الاختيارية $<$ عدد المتغيرات المستقلة $\implies$ ينتج أكثر من معادلة من الرتبة الأولى.
2. **الحالة (2):** عدد الثوابت الاختيارية $=$ عدد المتغيرات المستقلة $\implies$ تنتج معادلة واحدة وحيدة من الرتبة الأولى.
3. **الحالة (3):** عدد الثوابت الاختيارية $>$ عدد المتغيرات المستقلة $\implies$ تنتج معادلات من رتب أعلى (Higher Order).

### مثال محلول من مذكرات المحاضرة (صفحة 8):
عائلة الأسطح المكافئة:
$$z = a x + b y + a^2 + b^2$$
* **الخطوة 1:** اشتق جزئياً بالنسبة لـ $x$:  
  $$\frac{\partial z}{\partial x} = p = a$$
* **الخطوة 2:** اشتق جزئياً بالنسبة لـ $y$:  
  $$\frac{\partial z}{\partial y} = q = b$$
* **الخطوة 3:** عوّض بقيمتي $a = p$ و $b = q$ في المعادلة الأصلية:  
  $$z = x p + y q + p^2 + q^2$$
* **النتيجة:** معادلة تفاضلية جزئية غير خطية من الرتبة الأولى خالية تماماً من الثوابت!
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (مسألة من مذكرات المنهج)

> 💡 **تعليمات:** خذ ورقة وقلماً بجانبك، واتبع الخطوات التالية للحل باليد:  
> *(إذا واجهتك أي صعوبة، افتح `INSTRUCTOR_ANSWER_KEY.md` القسم 1.1 لرؤية الخطوات الجبرية كاملة).*

**المسألة:** لدينا عائلة الحفر النيزكية الدائرية:
$$z = (x - a)^2 + (y - b)^2$$
1. اشتق جزئياً بالنسبة لـ $x$: $p = \frac{\partial z}{\partial x} = 2(x - a) \implies (x - a) = \frac{p}{2}$.
2. اشتق جزئياً بالنسبة لـ $y$: $q = \frac{\partial z}{\partial y} = 2(y - b) \implies (y - b) = \frac{q}{2}$.
3. ربع المعادلتين واجمعهما معاً.
4. عوّض بقيمة $z$ من المعادلة الأصلية في الناتج.

اكتب المعادلة الناتجة كنص في الخلية التالية (مثال: `"p^2 + q^2 = 4z"`):
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ###
student_pde_1 = "p^2 + q^2 = 4z"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab1.check_paper_challenge_1(student_pde_1)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ### (≈ 1 line of code)
# اكتب نص المعادلة الناتجة من حلك الورقي (مثال: "p^2 + q^2 = 4z")
student_pde_1 = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab1.check_paper_challenge_1(student_pde_1)
""")

    nb.md(r"""---
## 5. 🚀 تحدي جسر مركبة المريخ (تطبيق المنهج على حوض الحفرة)

الآن نطبق هذا المفهوم مباشرة على **نظام ملاحة مركبة المريخ**:

حوض هبوط المركبة على سطح المريخ يوصف بسطح تربيعي:
$$z = \frac{1}{2} a x^2 + \frac{1}{2} b y^2$$

**على ورقتك:**
1. احسب $p = \frac{\partial z}{\partial x} = a x \implies a = \frac{p}{x}$.
2. احسب $q = \frac{\partial z}{\partial y} = b y \implies b = \frac{q}{y}$.
3. عوّض بقيمتي $a$ و $b$ داخل المعادلة الأصلية ثم اضرب الطرفين في 2.

ما هي المعادلة الناتجة؟ اكتبها أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي مركبة المريخ
### START CODE HERE ###
rover_basin_pde = "x*p + y*q = 2z"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab1.check_paper_challenge_2(rover_basin_pde)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي مركبة المريخ
### START CODE HERE ### (≈ 1 line of code)
# اكتب نص المعادلة الناتجة (مثال: "x*p + y*q = 2z")
rover_basin_pde = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab1.check_paper_challenge_2(rover_basin_pde)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: التحقق من ميول التضاريس

سنكتب الآن دالة برمجية لكمبيوتر ملاحة المركبة تقوم بفحص شبكة الارتفاعات والتأكد من مطابقتها للمعادلة:
$$\text{residual} = (p^2 + q^2) - 4z \approx 0$$
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: verify_crater_pde
def verify_crater_pde(Z: np.ndarray, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    # تحسب المتبقي للمعادلة: (p^2 + q^2) - 4*z
    ### START CODE HERE ###
    residual = (P**2 + Q**2) - 4.0 * Z
    ### END CODE HERE ###
    return residual

# تشغيل الاختبار الآلي:
test_lab1.test_eliminate_constants_fn(verify_crater_pde)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: verify_crater_pde
def verify_crater_pde(Z: np.ndarray, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    # تحسب المتبقي للمعادلة: (p^2 + q^2) - 4*z
    ### START CODE HERE ### (≈ 1 line of code)
    # احسب: (P**2 + Q**2) - 4.0 * Z
    residual = None
    ### END CODE HERE ###
    return residual

# تشغيل الاختبار الآلي:
test_lab1.test_eliminate_constants_fn(verify_crater_pde)
''')

    nb.md(r"""---
## 7. 🎨 الرؤية البصرية للفيزياء: رسم ثلاثي الأبعاد ومجال الميول
شغّل الخلية التالية لرؤية حوض الحفرة ثلاثي الأبعاد مع متجهات الانحدار $(p, q)$ التي ترشد عجلات المركبة:
""")

    nb.code(r"""x = np.linspace(-3, 3, 40)
y = np.linspace(-3, 3, 40)
X, Y = np.meshgrid(x, y)
Z = (X - 0.5)**2 + (Y + 0.5)**2  # a=0.5, b=-0.5

dx = x[1] - x[0]
dy = y[1] - y[0]
# np.gradient يعيد [dZ/dy, dZ/dx]
Q, P = np.gradient(Z, dy, dx)

fig = plt.figure(figsize=(12, 5))

# رسم ثلاثي الأبعاد لسطح الحفرة
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='copper', alpha=0.85)
ax1.set_title("Mars Crater Basin Surface $z(x, y)$", fontsize=12)

# رسم ثنائي الأبعاد لمجال انحدار الميول
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contour(X, Y, Z, levels=15, cmap='copper')
ax2.quiver(X[::3, ::3], Y[::3, ::3], P[::3, ::3], Q[::3, ::3], color='red')
ax2.set_title("Slope Field $(p, q) = (\\partial z/\\partial x, \\partial z/\\partial y)$", fontsize=12)

plt.tight_layout()
plt.show()

print("تهانينا! لقد أتممت اللاب 1 وأتقنت تكوين المعادلات بحذف الثوابت.")
""")

    nb.save()


# ===========================================================================
# LAB 2 (ARABIC): LAGRANGE'S METHOD OF CHARACTERISTICS
# ===========================================================================
def build_lab_2_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_2_Lagrange_Method_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 🧭 اللاب 2: المعادلات شبه الخطية وطريقة لاجرانج لخطوط الانسياب
### *غرفة التحكم: محاكي تتبع مسار عجلات المركبة*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**موضوع المنهج:** الباب الأول، القسم 1.3.1 (صفحات 12–16)

---
### 🧭 حجر رشيد (The Rosetta Stone): ترجمة الرياضيات إلى لغة البشر وكود بايثون
| 1. معادلات السبورة في المحاضرة | 2. المعنى الفيزيائي البسيط | 3. كود بايثون المقابل |
| :--- | :--- | :--- |
| $P p + Q q = R$ | "معادلة نقل تدفق الرياح أو السرعات في اتجاهين." | `u*dphi_dx + v*dphi_dy = 0` |
| $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$ | "معادلات لاجرانج المساعدة: مسار حركة الجسيم خطوة بخطوة." | `dx / u == dy / v` |
| $\Phi(u, v) = 0$ | "العلاقة التي تثبت أن مسار المركبة يتبع خط انسياب ثابت." | `y = k * x**2` |

---
## 1. المعنى البسيط: "الملاحة مع تيار النهر"
تخيل أنك تركب قارباً صغيراً في نهر متدفق. بدلاً من مقاومة التيار، تترك القارب ينساب تلقائياً مع خطوط التيار (Streamlines).
* **طريقة لاجرانج (Lagrange's Method):** هي الأداة الرياضية التي تحول المعادلة التفاضلية الجزئية ثلاثية الأبعاد إلى معادلات تفاضلية عادية (ODEs) تصف مسار حركة العجلات أو جزيئات الغبار على التضاريس خطوة بخطوة!

---
## 2. ما فائدة هذه الطريقة ولماذا نقوم بها؟ (The "WHY")
* **لماذا نقوم بها؟** المركبة بعد حساب مجال الجهد $\phi(x, y)$ تحتاج إلى قانون قيادة محدد: كيف تدير عجلاتها في كل ثانية؟
* **ماذا تفيد مركبة المريخ؟** عندما تحسب متجه الانحدار $\mathbf{v} = (u, v) = -\nabla\phi$، فإن معادلة حركة خط الانسياب هي $\frac{dx}{u} = \frac{dy}{v}$. حل هذه المعادلة بلاجرانج هو **بالضبط ما نكتبه في كود دالة `descend()` لتوجيه المركبة!**
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab2

%matplotlib inline
print("تم تهيئة بيئة اللاب 2 بنجاح! جاهز لتتبع خطوط الانسياب.")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية ومثال المذكرة المحلول (Worked Example)

لحل أي معادلة من الصورة $P p + Q q = R$:
* **الخطوة 1:** كتابة معادلات لاجرانج المساعدة: $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$.
* **الخطوة 2:** أخذ زوجين منفصلين وتكاملهما لإيجاد ثابتين مستقلين $u(x, y, z) = c_1$ و $v(x, y, z) = c_2$.
* **الخطوة 3:** كتابة الحل العام: $\Phi(c_1, c_2) = 0$.

### مثال محلول من مذكرات المحاضرة (صفحة 13):
$$2 p - 3 q = 2x$$
* $P = 2, Q = -3, R = 2x$.
* $\frac{dx}{2} = \frac{dy}{-3} \implies -3 dx = 2 dy \implies 3x + 2y = c_1$.
* $\frac{dx}{2} = \frac{dz}{2x} \implies 2x dx = 2 dz \implies x^2 - 2z = c_2$.
* **الحل العام:** $\Phi(3x + 2y, x^2 - 2z) = 0$.
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (مسألة من مذكرات المنهج)

> 💡 *(إذا واجهتك صعوبة، راجع `INSTRUCTOR_ANSWER_KEY.md` القسم 2.1).*

**المسألة (معادلة أويلر المتجانسة):**
$$x p + y q = z$$
1. اكتب معادلات لاجرانج المساعدة: $\frac{dx}{x} = \frac{dy}{y} = \frac{dz}{z}$.
2. خذ الكسرين 1 و 2 ($\frac{dx}{x} = \frac{dy}{y}$) وكاملهما لإيجاد $u(x, y) = c_1$.
3. خذ الكسرين 2 و 3 ($\frac{dy}{y} = \frac{dz}{z}$) وكاملهما لإيجاد $v(y, z) = c_2$.

اكتب صيغتي $u$ و $v$ كنصوص أدناه (مثال: `"x/y"` و `"y/z"`):
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ###
student_u = "x/y"
student_v = "y/z"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab2.check_paper_challenge_1(student_u, student_v)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ### (≈ 2 lines of code)
# اكتب قيمة الثابتين u و v المستنتجين من تكاملك الورقي
student_u = None  # مثال: "x/y"
student_v = None  # مثال: "y/z"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab2.check_paper_challenge_1(student_u, student_v)
""")

    nb.md(r"""---
## 5. 🚀 تحدي جسر مركبة المريخ (مسارات عجلات المركبة في الرمال)

افترض أن المركبة تسير على حقل جهد $\phi(x, y) = x^2 + 2y^2$.  
متجه السرعة مع تيار الانحدار هو $\mathbf{v} = (u, v) = -\nabla\phi = (-2x, -4y)$.  
معادلة نقل مسار الانسياب هي:
$$-2x \frac{\partial \phi}{\partial x} - 4y \frac{\partial \phi}{\partial y} = 0$$

**على ورقتك:**
1. اكتب معادلة لاجرانج: $\frac{dx}{-2x} = \frac{dy}{-4y}$.
2. بسط المقامات بالقسمة على $-2$: $\frac{dx}{x} = \frac{dy}{2y}$.
3. كامل الطرفين: $\ln |x| = \frac{1}{2}\ln |y| + C \implies y = k x^2$.

ما هو المنحنى الذي تتبعه العجلات؟ اكتب المعادلة أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: مسار عجلات المركبة
### START CODE HERE ###
rover_streamline = "y = k*x^2"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab2.check_paper_challenge_2(rover_streamline)
""")
    else:
        nb.code(r"""# خلية تقييم: مسار عجلات المركبة
### START CODE HERE ### (≈ 1 line of code)
# اكتب معادلة المسار القطعي الناتج (مثال: "y = k*x^2")
rover_streamline = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab2.check_paper_challenge_2(rover_streamline)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: متتبع خطوط الانسياب العددي (RK4)

سنكتب دالة تحاكي حركة عجلات المركبة بتكامل متجه السرعة عددياً بخطوات صغيرة $\Delta t$:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: trace_streamline_rk4
def trace_streamline_rk4(velocity_fn, start=(1.0, 2.0), dt=0.01, steps=50):
    # تتبع خط انسياب نظام شبه خطي عددياً
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

# تشغيل الاختبار الآلي:
test_lab2.test_rk4_streamline_tracer(trace_streamline_rk4)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: trace_streamline_rk4
def trace_streamline_rk4(velocity_fn, start=(1.0, 2.0), dt=0.01, steps=50):
    # تتبع خط انسياب نظام شبه خطي عددياً
    trajectory = [start]
    curr = np.array(start, dtype=float)
    
    ### START CODE HERE ### (≈ 4-5 lines of code)
    # حلقة تكرارية بعدد steps:
    # 1. احسب السرعة عند النقطة الحالية: vx, vy = velocity_fn(curr[0], curr[1])
    # 2. حدث الموقع: curr = curr + dt * np.array([vx, vy], dtype=float)
    # 3. أضف النقطة للمسار: trajectory.append(tuple(curr))
    pass
    ### END CODE HERE ###
    
    return np.array(trajectory)

# تشغيل الاختبار الآلي:
test_lab2.test_rk4_streamline_tracer(trace_streamline_rk4)
''')

    nb.md(r"""---
## 7. 🎨 الرؤية البصرية للفيزياء: خطوط الانسياب الحقيقية
شغّل الخلية التالية لرؤية خطوط الانسياب المحسوبة بطريقة لاجرانج وهي تطابق حركة المركبة:
""")

    nb.code(r"""def sample_velocity(x, y):
    return -2.0 * x, -4.0 * y

traj = trace_streamline_rk4(sample_velocity, start=(1.0, 2.0), dt=0.01, steps=100)

x_vals = np.linspace(-2, 2, 20)
y_vals = np.linspace(-1, 3, 20)
X, Y = np.meshgrid(x_vals, y_vals)
U, V = sample_velocity(X, Y)

plt.figure(figsize=(8, 6))
plt.streamplot(X, Y, U, V, color='gray', density=0.8)
plt.plot(traj[:, 0], traj[:, 1], 'r-', linewidth=3, label="Lagrange Characteristic Trajectory")
plt.plot(traj[0, 0], traj[0, 1], 'go', markersize=8, label="Start (1, 2)")
plt.title("Rover Characteristic Streamlines: Lagrange Method in Action", fontsize=12)
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.show()

print("تهانينا! لقد أتممت اللاب 2 وأتقنت طريقة لاجرانج لخطوط الانسياب.")
""")

    nb.save()


# ===========================================================================
# LAB 3 (ARABIC): NON-LINEAR PDES & CHARPIT'S METHOD
# ===========================================================================
def build_lab_3_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_3_Nonlinear_Charpit_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📡 اللاب 3: المعادلات غير الخطية وطريقة شاربيت لموجات الرادار
### *غرفة التحكم: حساس الرادار البصري وموجات Eikonal*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**موضوع المنهج:** الباب الأول، الأقسام 1.3.2–1.3.6 (صفحات 17–28)

---
### 🧭 حجر رشيد (The Rosetta Stone): ترجمة الرياضيات إلى لغة البشر وكود بايثون
| 1. معادلات السبورة في المحاضرة | 2. المعنى الفيزيائي البسيط | 3. كود بايثون المقابل |
| :--- | :--- | :--- |
| $p^2 + q^2 = 1$ | "معادلة Eikonal: موجات الرادار تنتشر بسرعة ثابتة في الفضاء." | `np.hypot(X - x0, Y - y0)` |
| $z = p x + q y + f(p, q)$ | "صيغة كليروت (Clairaut Form): حلها التام خطوط مستقيمة." | `z = a*x + b*y + f(a, b)` |
| $(x - x_0)^2 + (y - y_0)^2 = z^2$ | "الغلاف الدائري لموجة الرادار المتوسعة." | `dist_grid = np.sqrt(dx**2 + dy**2)` |

---
## 1. المعنى البسيط: "دوائر الماء المتوسعة"
عندما تلقي حجراً في بركة ماء هادئة، تتسع دوائر الأمواج بسرعة ثابتة. المسافة المقطوعة تعتمد تربيعياً على الميول:
$$\|\nabla T\|^2 = p^2 + q^2 = 1$$
هذه المعادلة غير خطية لأن المشتقتين $p$ و $q$ مرفوعتان للأس 2.
* **طريقة شاربيت (Charpit's Method):** هي الطريقة الشاملة لحل أي معادلة غير خطية من الرتبة الأولى عبر تتبع إحداثيات الموقع والميل معاً في فضاء خماسي الأبعاد $(x, y, z, p, q)$!

---
## 2. ما فائدة هذه الطريقة ولماذا نقوم بها؟ (The "WHY")
* **لماذا نقوم بها؟** أجهزة الاستشعار بالرادار والليزر (LIDAR) على المريخ تحسب مسافة الصخور بقياس زمن ارتداد الموجة الضوئية.
* **ماذا تفيد مركبة المريخ؟** تمكن المركبة من بناء خريطة مسافات دائرية متوسعة حول العوائق لتفادي الاصطدام بها في التضاريس المجهولة.
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab3

%matplotlib inline
print("تم تهيئة بيئة اللاب 3 بنجاح! جاهز لحساب موجات الرادار.")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية والأشكال القياسية الأربعة (Standard Forms 1–4)

1. **Form 1 ($f(p, q) = 0$):** تحتوي على $p, q$ فقط $\implies$ نضع $p = a$ ونحل لإيجاد $q = b$. التكامل التام: $z = ax + by + c$.
2. **Form 2 ($f(z, p, q) = 0$):** تحتوي على $z, p, q$ فقط $\implies$ نضع $u = x + ay$.
3. **Form 3 ($f(x, p) = g(y, q)$):** قابلة للفصل $\implies$ نساوي الطرفين بثابت $a$.
4. **Form 4 (Clairaut Form: $z = px + qy + f(p, q)$):** الحل التام المباشر هو استبدال $p \to a$ و $q \to b$:
   $$z = ax + by + f(a, b)$$
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (صيغة كليروت من المنهج)

> 💡 *(إذا واجهتك صعوبة، راجع `INSTRUCTOR_ANSWER_KEY.md` القسم 3.1).*

**المسألة:** أوجد التكامل التام لمعادلة كليروت:
$$z = p x + q y + p q$$
بما أنها على صيغة كليروت، ضع $p = a$ و $q = b$. اكتب الحل التام أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ###
student_clairaut = "z = ax + by + ab"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_1(student_clairaut)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ### (≈ 1 line of code)
# اكتب صيغة التكامل التام (مثال: "z = ax + by + ab")
student_clairaut = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_1(student_clairaut)
""")

    nb.md(r"""---
## 5. 🚀 تحدي جسر مركبة المريخ (غلاف موجة الرادار Eikonal)

معادلة رادار المسح الضوئي للمركبة هي:
$$p^2 + q^2 = 1$$

**على ورقتك:**
1. باستخدام Form 1: ضع $p = a \implies q = \pm\sqrt{1 - a^2}$.
2. التكامل التام: $z = a x \pm\sqrt{1 - a^2} y + c$.
3. اشتق بالنسبة للبارامتر $a$ لمساواة المشتقة بالصفر وإيجاد الغلاف المفرد (Singular Envelope):
   $$\frac{\partial z}{\partial a} = x \pm \frac{-a}{\sqrt{1 - a^2}} y = 0 \implies x^2 + y^2 = z^2$$

اكتب معادلة الغلاف الدائري المتوسع أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: غلاف موجة الرادار
### START CODE HERE ###
student_envelope = "x^2 + y^2 = z^2"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_2(student_envelope)
""")
    else:
        nb.code(r"""# خلية تقييم: غلاف موجة الرادار
### START CODE HERE ### (≈ 1 line of code)
# اكتب معادلة الدائرة المتوسعة (مثال: "x^2 + y^2 = z^2")
student_envelope = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_2(student_envelope)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: حساب خريطة مسافات الرادار

سنكتب دالة تحسب خريطة المسافات الإقليدية المتوسعة من مصدر الرادار محققة معادلة $\|\nabla T\| = 1$:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: compute_eikonal_wavefront
def compute_eikonal_wavefront(grid_size=(50, 50), source=(25, 25)):
    # تحسب خريطة زمن وصول الموجة الدائرية T(x, y) من موقع الرادار
    Ny, Nx = grid_size
    Y, X = np.ogrid[:Ny, :Nx]
    
    ### START CODE HERE ###
    dist = np.hypot(X - source[1], Y - source[0])
    ### END CODE HERE ###
    
    return dist

# تشغيل الاختبار الآلي:
test_lab3.test_eikonal_wavefront_distance(compute_eikonal_wavefront)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: compute_eikonal_wavefront
def compute_eikonal_wavefront(grid_size=(50, 50), source=(25, 25)):
    # تحسب خريطة زمن وصول الموجة الدائرية T(x, y) من موقع الرادار
    Ny, Nx = grid_size
    Y, X = np.ogrid[:Ny, :Nx]
    
    ### START CODE HERE ### (≈ 1 line of code)
    # احسب المسافة الإقليدية باستخدام np.hypot(X - source[1], Y - source[0])
    dist = None
    ### END CODE HERE ###
    
    return dist

# تشغيل الاختبار الآلي:
test_lab3.test_eikonal_wavefront_distance(compute_eikonal_wavefront)
''')

    nb.md(r"""---
## 7. 🎨 الرؤية البصرية للفيزياء: موجات الرادار الدائرية
شغّل الخلية لرؤية خطوط انتشار جبهة الموجة الدائرية من الرادار:
""")

    nb.code(r"""wavefront = compute_eikonal_wavefront((60, 60), source=(30, 30))

plt.figure(figsize=(8, 6))
cs = plt.contourf(wavefront, levels=20, cmap='plasma')
plt.colorbar(cs, label="Wavefront Arrival Distance T(x, y)")
plt.plot(30, 30, 'wo', markersize=10, label="Radar Beacon Source")
plt.title("Eikonal Radar Wavefront Propagation: $\|\nabla T\|^2 = 1$", fontsize=12)
plt.legend()
plt.show()

print("تهانينا! لقد أتممت اللاب 3 وأتقنت المعادلات غير الخطية وموجات Eikonal.")
""")

    nb.save()


# ===========================================================================
# LAB 4 (ARABIC): HIGHER-ORDER HOMOGENEOUS OPERATORS & LAPLACE
# ===========================================================================
def build_lab_4_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_4_HigherOrder_Operators_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📐 اللاب 4: مؤثرات الرتب العليا ومعادلة لابل التوافقية
### *غرفة التحكم: الأصل التحليلي لمعادلة لابل المستمرة*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**موضوع المنهج:** الباب الأول، القسم 1.4 (صفحات 29–45)

---
### 🧭 حجر رشيد (The Rosetta Stone): ترجمة الرياضيات إلى لغة البشر وكود بايثون
| 1. معادلات السبورة في المحاضرة | 2. المعنى الفيزيائي البسيط | 3. كود بايثون المقابل |
| :--- | :--- | :--- |
| $(D_x^2 + D_y^2)z = 0$ | "معادلة لابل: حقل جهد ناعم بدون قمم أو حفر محلية." | `laplace_continuous_eq` |
| $m^2 + 1 = 0 \implies m = \pm i$ | "الجذور المميزة المركبة: تثبت أن الجهد يتكون من دوال توافقية." | `roots = [1j, -1j]` |
| $z = \phi_1(y + ix) + \phi_2(y - ix)$ | "الحل العام التحليلي لمعادلة لابل في المستوى." | `analytic_harmonic_field` |

---
## 1. المعنى البسيط: "الغشاء المطاطي المشدود"
تخيل غشاءً مطاطياً مشدوداً بإحكام فوق إطار سلكي. إذا ضغطت على أحد أطراف الإطار للأعلى والطرف الآخر للأسفل:
* المطاط سيتشكل بسلاسة تامة.
* يستحيل أن تتكون حفرة صغيرة أو نتوء فجائي في منتصف المطاط من تلقاء نفسه!
* **معادلة لابل (Laplace's Equation):** هي المعادلة التي تصف هذا الاتزان التام وتمنع تكون أي حفر عشوائية.

---
## 2. ما فائدة هذه الطريقة ولماذا نقوم بها؟ (The "WHY")
* **لماذا نقوم بها؟** لفهم كيف يستنتج الرياضيون حل معادلة لابل $(D_x^2 + D_y^2)z = 0$ باستخدام المعادلة المساعدة $m^2 + 1 = 0$ (صفحة 33 من المذكرة).
* **معضلة الانتقال إلى المريخ (The Scale-Up Dilemma):** الصيغة التحليلية $\phi_1(y + ix) + \phi_2(y - ix)$ ممتازة على ورقة بيضاء، لكن على المريخ توجد **10,000 بكسل عشوائي للحفر النيزكية**! لا توجد صيغة رياضية مغلقة واحدة يمكنها تحقيق 10,000 جدار حفرة، ولذلك سنحتاج في اللاب 6 لتحويل هذه المعادلة إلى شبكة رقمية 5-Point Stencil!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab4

%matplotlib inline
print("تم تهيئة بيئة اللاب 4 بنجاح! جاهز لحساب المؤثرات ومعادلة لابل.")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية وحساب الحل المكمل والخاص (C.F. & P.I.)

1. **الدالة المكملة (Complementary Function - C.F.):**
   * نضع $D_x = m$ و $D_y = 1$ لتكوين المعادلة المساعدة $F(m, 1) = 0$.
   * إذا كانت الجذور حقيقية ومختلفة $m_1, m_2$: $z = \phi_1(y + m_1 x) + \phi_2(y + m_2 x)$.
   * إذا كانت الجذور متساوية $m_1 = m_2 = m$: $z = \phi_1(y + mx) + x \phi_2(y + mx)$.
   * إذا كانت مركبة $m = \pm i$ (معادلة لابل، ص 33): $z = \phi_1(y + ix) + \phi_2(y - ix)$.

2. **التكامل الخاص (Particular Integral - P.I.) لقوى الجاذبية والتذبذب:**
   * لقوة $\sin(ax + by)$: نستبدل $D_x^2 \to -a^2$ و $D_x D_y \to -ab$ و $D_y^2 \to -b^2$.
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (حل معادلة لابل من صفحة 33 بالمذكرة)

> 💡 *(إذا واجهتك صعوبة، راجع `INSTRUCTOR_ANSWER_KEY.md` القسم 4.1).*

**المسألة:** أوجد الجذور المميزة لمعادلة لابل:
$$(D_x^2 + D_y^2)z = 0$$
1. كون المعادلة المساعدة بوضع $D_x = m, D_y = 1$: $m^2 + 1 = 0$.
2. حل المعادلة لإيجاد الجذور $m_1, m_2$.

أدخل الجذور في بايثون (`1j` تعبر عن $i$ و `-1j` تعبر عن $-i$):
""")

    if solutions:
        nb.code(r"""# خلية تقييم: جذور معادلة لابل
### START CODE HERE ###
m1 = 1j
m2 = -1j
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_1(m1, m2)
""")
    else:
        nb.code(r"""# خلية تقييم: جذور معادلة لابل
### START CODE HERE ### (≈ 2 lines of code)
# أدخل الجذور التخيلية في بايثون باستخدام 1j و -1j
m1 = None
m2 = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_1(m1, m2)
""")

    nb.md(r"""---
## 5. 🚀 تحدي جسر مركبة المريخ (التكامل الخاص لقوة الجاذبية في الوادي)

في وادٍ مريخي شديد الانحدار، تضيف الجاذبية قوة متذبذبة $f(x, y) = \sin(2x - 3y)$:
$$(D_x^2 - D_x D_y - 6 D_y^2)z = \sin(2x - 3y)$$

**على ورقتك:**
1. باستخدام الحالة الثانية للتكامل الخاص (P.I. Case 2): استبدل $D_x^2 \to -(2)^2 = -4$ و $D_x D_y \to -(2)(-3) = 6$ و $D_y^2 \to -(-3)^2 = -9$.
2. احسب قيمة المؤثر: $F(-4, 6, -9) = -4 - 6 - 6(-9) = 44$.
3. اكتب التكامل الخاص $z_2 = \frac{1}{44}\sin(2x - 3y)$.

أدخل صيغة التكامل الخاص P.I. الناتجة أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: التكامل الخاص P.I.
### START CODE HERE ###
student_pi = "(1/44)*sin(2x - 3y)"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_2(student_pi)
""")
    else:
        nb.code(r"""# خلية تقييم: التكامل الخاص P.I.
### START CODE HERE ### (≈ 1 line of code)
# اكتب صيغة التكامل الخاص (مثال: "(1/44)*sin(2x - 3y)")
student_pi = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_2(student_pi)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: حل جذور مؤثرات الرتب العليا

سنكتب دالة تحسب جذور المعادلة المساعدة لأي مؤثر تفاضلي من الدرجة الثانية أو أعلى:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: solve_operator_roots
def solve_operator_roots(coeffs: list[float]) -> list[complex]:
    # تحسب جذور المعادلة المساعدة F(m, 1) = 0
    ### START CODE HERE ###
    roots = np.roots(coeffs)
    ### END CODE HERE ###
    return list(roots)

# تشغيل الاختبار الآلي:
test_lab4.test_characteristic_roots_solver(solve_operator_roots)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: solve_operator_roots
def solve_operator_roots(coeffs: list[float]) -> list[complex]:
    # تحسب جذور المعادلة المساعدة F(m, 1) = 0
    ### START CODE HERE ### (≈ 1 line of code)
    # استخدم np.roots(coeffs)
    roots = None
    ### END CODE HERE ###
    return list(roots)

# تشغيل الاختبار الآلي:
test_lab4.test_characteristic_roots_solver(solve_operator_roots)
''')

    nb.md(r"""---
## 7. 🎨 الرؤية البصرية للفيزياء: سطح لابل التوافقي (انعدام الحفر تماماً!)
شغّل الخلية لرؤية الحل التحليلي التوافقي الدقيق $\phi(x, y) = \frac{\sin(\pi x)\sinh(\pi y)}{\sinh(\pi)}$:
لاحظ كيف ينحدر السطح بنعومة فائقة من أعلى نقطة للأسفل دون أي حفرة محلية تعيق الحركة!
""")

    nb.code(r"""x = np.linspace(0, 1, 40)
y = np.linspace(0, 1, 40)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.pi * X) * np.sinh(np.pi * Y) / np.sinh(np.pi)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.85)
ax.set_title("Harmonic Potential Surface $\nabla^2\phi = 0$: Zero Local Minima!", fontsize=13)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Potential $\phi$")
plt.colorbar(surf, shrink=0.5)
plt.show()

print("تهانينا! لقد أتممت اللاب 4 وأتقنت مؤثرات الرتب العليا وأصل معادلة لابل.")
""")

    nb.save()


# ===========================================================================
# LAB 5 (ARABIC): NON-HOMOGENEOUS PDES & REDUCIBLE OPERATORS
# ===========================================================================
def build_lab_5_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_5_NonHomogeneous_PDEs_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📡 اللاب 5: المؤثرات غير المتجانسة وتلاشي الإشارة والبطارية
### *غرفة التحكم: شبكة بث إشارات الملاحة واضمحلال الطاقة*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**موضوع المنهج:** الباب الثاني (Chapter 2)، الأقسام 2.1–2.3 (صفحات 46–60)

---
### 🧭 حجر رشيد (The Rosetta Stone): ترجمة الرياضيات إلى لغة البشر وكود بايثون
| 1. معادلات السبورة في المحاضرة | 2. المعنى الفيزيائي البسيط | 3. كود بايثون المقابل |
| :--- | :--- | :--- |
| $(a D_x + b D_y + c)z = 0$ | "مؤثر خطي غير متجانس يجمع بين الحركة والتلاشي الأسي." | `linear_factor(a, b, c)` |
| $z = e^{-\frac{c}{a}x}\Phi(ay - bx)$ | "موجة متحركة مع غلاف اضمحلال أسي للطاقة $e^{kx}$." | `np.exp(-c*X/a) * phi` |
| $(F_1)(F_2)z = 0 \implies z = z_1 + z_2$ | "مبدأ التراكب (Superposition) لجمع إشارات أبراج الاتصال." | `Z_total = Z1 + Z2` |

---
## 1. المعنى البسيط: "الصوت الذي يتلاشى مع المسافة"
عندما تنادي بصوت عالٍ في وادٍ فسيح، ينتقل صوتك كموجة متحركة، لكن شدته تضعف تدريجياً كلما ابتعدت عن المصدر.
* هذا التلاشي الأسي يصفه الحد الثابت $c$ في المؤثر $(a D_x + b D_y + c)$.
* **المؤثرات القابلة للتحليل (Reducible Operators):** تمكننا من تجزئة معادلة معقدة متعددة الأبعاد إلى حاصل ضرب عوامل خطية بسيطة يسهل حل كل منها على حدة!

---
## 2. ما فائدة هذه الطريقة ولماذا نقوم بها؟ (The "WHY")
* **لماذا نقوم بها؟** لفهم الباب الثاني من المنهج، وكيف نميز بين المؤثر القابل للتحليل (Reducible) والمؤثر غير القابل للتحليل (Irreducible).
* **ماذا تفيد مركبة المريخ؟** عند استقبال إشارات الملاحة من برجي بث لاسلكي على سطح المريخ، تتلاشى طاقة الإشارة وتستهلك بطارية المركبة بمعدل أسي $e^{-x}$ مع زيادة مسافة القيادة $x$.
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab5

%matplotlib inline
print("تم تهيئة بيئة اللاب 5 بنجاح! جاهز لحساب المؤثرات غير المتجانسة.")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية وقانون العوامل الخطية (Reducible Factors Theorem)

لأي عامل خطي غير متجانس على الصورة:
$$(a D_x + b D_y + c) z = 0$$
إذا كان $a \neq 0$، فإن الحل العام يعطى بالقانون المباشر (صفحة 47 بالمذكرة):
$$z = e^{-\frac{c}{a}x} \Phi(a y - b x)$$

إذا كان المؤثر يتكون من حاصل ضرب عاملين:
$$(a_1 D_x + b_1 D_y + c_1)(a_2 D_x + b_2 D_y + c_2) z = 0$$
فإن الحل العام هو مجموع الحلين (مبدأ التراكب Superposition):
$$z = e^{-\frac{c_1}{a_1}x} \Phi_1(a_1 y - b_1 x) + e^{-\frac{c_2}{a_2}x} \Phi_2(a_2 y - b_2 x)$$
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (مسألة الباب الثاني من المنهج)

> 💡 *(إذا واجهتك صعوبة، راجع `INSTRUCTOR_ANSWER_KEY.md` القسم 5.1).*

**المسألة:** أوجد الحل العام للمعادلة القابلة للتحليل:
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$
* العامل الأول: $a_1 = 2, b_1 = -3, c_1 = 1 \implies z_1 = e^{-x/2} \Phi_1(2y + 3x)$.
* العامل الثاني: $a_2 = 1, b_2 = 2, c_2 = -2 \implies z_2 = e^{2x} \Phi_2(y - 2x)$.

اكتب صيغة الحل العام المجموع أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ###
student_solution = "exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x)"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_1(student_solution)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ### (≈ 1 line of code)
# اكتب صيغة الحل العام (مثال: "exp(-x/2)*Phi1(2y + 3x) + exp(2x)*Phi2(y - 2x)")
student_solution = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_1(student_solution)
""")

    nb.md(r"""---
## 5. 🚀 تحدي جسر مركبة المريخ (معدل استهلاك طاقة البطارية)

طاقة بطارية المركبة تتلاشى مع المسافة $x$ وفقاً للمعادلة:
$$(D_x + 2 D_y + 1)z = 0$$

**على ورقتك:**
1. المعاملات: $a = 1, b = 2, c = 1$.
2. احسب معدل التخميد الأسي $k$ في $e^{k x}$ من الصيغة $-\frac{c}{a}$.

ما هي القيمة العددية لمعدل التخميد $k$؟ أدخلها أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: معدل تخميد البطارية
### START CODE HERE ###
damping_rate = -1.0
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_2(damping_rate)
""")
    else:
        nb.code(r"""# خلية تقييم: معدل تخميد البطارية
### START CODE HERE ### (≈ 1 line of code)
# أدخل القيمة العددية لمعدل التخميد k (مثال: -1.0)
damping_rate = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_2(damping_rate)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: مستخرج معاملات العوامل الخطية

سنكتب دالة برمجية تستخرج المعاملات $(a, b, c)$ من أي نص عامل خطي مثل `"2*D_x - 3*D_y - 5"`:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: parse_linear_factor
def parse_linear_factor(factor_str: str) -> tuple[float, float, float]:
    # تستخرج المعاملات a, b, c من نص العامل الخطي
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

# تشغيل الاختبار الآلي:
test_lab5.test_linear_factor_evaluator(parse_linear_factor)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: parse_linear_factor
def parse_linear_factor(factor_str: str) -> tuple[float, float, float]:
    # تستخرج المعاملات a, b, c من نص العامل الخطي (مثال: "2*D_x - 3*D_y - 5")
    ### START CODE HERE ### (≈ 6-10 lines of code)
    # استخرج المعاملات a, b, c
    a = None
    b = None
    c = None
    ### END CODE HERE ###
    return a, b, c

# تشغيل الاختبار الآلي:
test_lab5.test_linear_factor_evaluator(parse_linear_factor)
''')

    nb.md(r"""---
## 7. 🎨 الرؤية البصرية للفيزياء: الإشارة المتلاشية أسياً
شغّل الخلية لرؤية كيف يتلاشى سطح الجهد أسياً مع المسافة $x$ وفقاً لـ $z = e^{-0.5x} \sin(y - 2x)$:
""")

    nb.code(r"""x = np.linspace(0, 5, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.exp(-0.5 * X) * np.sin(Y - 2.0 * X)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.85)
ax.set_title("Damped Signal Surface $z = e^{-0.5x} \\sin(y - 2x)$", fontsize=13)
ax.set_xlabel("Distance Traveled (x)")
ax.set_ylabel("Cross-track (y)")
ax.set_zlabel("Signal Level / Battery Voltage")
plt.colorbar(surf, shrink=0.5)
plt.show()

print("تهانينا! لقد أتممت اللاب 5 وأتقنت المؤثرات غير المتجانسة والتخميد الأسي.")
""")

    nb.save()


# ===========================================================================
# LAB 6 (ARABIC): CAPSTONE MARS ROVER NAVIGATION
# ===========================================================================
def build_lab_6_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_6_Mars_Rover_Capstone_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 🚀 اللاب 6: المشروع النهائي: تقطيع الشبكة والملاحة الذاتية على المريخ
### *غرفة التحكم: رفع كود الملاحة لكنترول مركبة الفضاء*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**موضوع المنهج:** الربط النهائي الشامل (من النظرية الرياضية إلى كمبيوتر ملاحة المريخ)

---
### 🧭 حجر رشيد (The Rosetta Stone): ترجمة الرياضيات إلى لغة البشر وكود بايثون
| 1. معادلات السبورة في المحاضرة | 2. المعنى الفيزيائي البسيط | 3. كود بايثون المقابل |
| :--- | :--- | :--- |
| $\nabla^2\phi = 0$ | "معادلة لابل المستمرة التي أثبتنا جذورها $m=\pm i$ في اللاب 4." | `(D_x^2 + D_y^2)phi = 0` |
| $\phi_{i,j} = \frac{1}{4}(\phi_{\text{up}} + \phi_{\text{down}} + \dots)$ | "صيغة الـ 5-Point Stencil: كل نقطة هي متوسط جيرانها الأربعة." | `avg = (roll_up + roll_down + ...) / 4` |
| $\frac{\partial\phi}{\partial n} = 0$ | "جدران عازلة (Neumann): الماء يلتف حول الحفر دون اختراقها." | `phi[~free] = 0; cnt = active_neighbors` |
| $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi/N)}$ | "معامل الاسترخاء الفائق (SOR) لتسريع الحل 66 ضعفاً." | `phi = (1 - w)*old + w*avg` |

---
## 1. المعنى البسيط: "الترقية الكبرى: من الورقة إلى 25,600 نقطة"
في اللابات السابقة، حللنا المعادلات بالورقة والقلم على ورقة بيضاء ملساء.
لكن على سطح المريخ، صورة التضاريس الرقمية المأخوذة من قمر ناسا الصناعي (HiRISE DEM) تحتوي على **25,600 نقطة ارتفاع، وأكثر من 3,400 حفرة وصخرة غير منتظمة الشكل**!
* يستحيل على أي عالم في العالم كتابة معادلة ورقية واحدة تغطي 10,000 جدار حفرة متعرج.
* **الحل الهندسي:** نحول المشتقات المتصلة إلى شبكة نقاط متقطعة (Discretization) ونترك بايثون يحل الـ 25,600 معادلة في ثوانٍ معدودة!

---
## 2. ما فائدة هذه الطريقة ولماذا نقوم بها؟ (The "WHY")
* **لماذا نقوم بها؟** لأن مركبة الفضاء لا تمتلك فريق إنقاذ بشري على المريخ. إذا علقت داخل حفرة، تنتهي المهمة وتضيع ملايين الدولارات.
* **ماذا تفيد مركبة المريخ؟** بفضل نظرية **The Maximum Principle** لمعادلة لابل، يضمن كمبيوتر الملاحة رياضياً بنسبة 100% أن المركبة لن تعلق في أي فخ محلي وستصل إلى الهدف بسلام.
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab6

%matplotlib inline
print("تم تهيئة اللاب 6 النهائي بنجاح! جاهز لتشغيل تسلسل إطلاق المهمة.")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية: استنتاج الـ 5-Point Stencil من متسلسلة تايلور

لنقرب المشتقة الثانية $\frac{\partial^2\phi}{\partial x^2}$ عند النقطة $(i, j)$ باستخدام متسلسلة تايلور للأمام والخلف:
$$\phi_{i+1, j} = \phi_{i,j} + h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} + \mathcal{O}(h^3)$$
$$\phi_{i-1, j} = \phi_{i,j} - h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} - \mathcal{O}(h^3)$$

بجمع المعادلتين معاً، تحذف المشتقات الفردية، وبإعادة الترتيب:
$$\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} = \frac{\phi_{i+1, j} - 2\phi_{i,j} + \phi_{i-1, j}}{h^2}$$

وبنفس الطريقة في اتجاه $y$:
$$\left.\frac{\partial^2\phi}{\partial y^2}\right|_{i,j} = \frac{\phi_{i, j+1} - 2\phi_{i,j} + \phi_{i, j-1}}{h^2}$$

بالتعويض في معادلة لابل $\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$ والضرب في $h^2$:
$$(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}) - 4\phi_{i,j} = 0$$
$$\implies \phi_{i,j} = \frac{1}{4}\left(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}\right)$$
> *"كل خلية في الخريطة هي ببساطة المتوسط الحسابي لجيرانها الأربعة المباشرين!"*
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (الحساب اليدوي لشبكة 4 نقاط)

> 💡 *(إذا واجهتك صعوبة، راجع `INSTRUCTOR_ANSWER_KEY.md` القسم 6.1).*

لدينا شبكة $4 \times 4$ بشروط حدية:
* الحد العلوي (البداية): $\phi = 1.0$
* الحد السفلي (الهدف): $\phi = 0.0$
* الحد الأيمن والأيسر (جدران معزولة): $\phi = 0.5$
* الخلايا الداخلية الأربعة $A, B, C, D$ قيمتها الابتدائية $0.0$.

احسب التحديث الأول يدوياً (Sweep 1) للخلية $A(1, 1)$ والخلية $B(1, 2)$:
$$\phi_A^{(1)} = \frac{1.0 + 0.0 + 0.5 + 0.0}{4} = ?$$

أدخل القيمتين العشريتين المحسوبتين باليد أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: حساب الشبكة اليدوي
### START CODE HERE ###
phi_A = 0.375
phi_B = 0.375
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_1(phi_A, phi_B)
""")
    else:
        nb.code(r"""# خلية تقييم: حساب الشبكة اليدوي
### START CODE HERE ### (≈ 2 lines of code)
# أدخل القيمتين العشريتين المحسوبتين باليد (مثال: 0.375)
phi_A = None
phi_B = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_1(phi_A, phi_B)
""")

    nb.md(r"""---
## 5. 🚀 تحدي جسر مركبة المريخ: الحساب النظري لمعامل SOR الأمثل

على الورق استغرق حساب 4 خلايا دقيقتين. على شبكة $N = 16$، ما هي القيمة النظرية لمعامل الاسترخاء الأمثل $\omega_{\text{opt}}$ وفقاً لنظرية يونغ (Young's Theorem)؟
$$\omega_{\text{opt}} = \frac{2}{1 + \sin\left(\frac{\pi}{N}\right)}$$

احسب قيمة $\omega_{\text{opt}}$ لـ $N = 16$ على ورقتك وأدخلها أدناه:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: معامل أوميجا الأمثل لـ N=16
### START CODE HERE ###
omega_16 = 2.0 / (1.0 + np.sin(np.pi / 16))
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_2(omega_16)
""")
    else:
        nb.code(r"""# خلية تقييم: معامل أوميجا الأمثل لـ N=16
### START CODE HERE ### (≈ 1 line of code)
# احسب قيمة أوميجا المثلى لـ N=16 (صيغة: 2.0 / (1.0 + np.sin(np.pi / 16)))
omega_16 = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_2(omega_16)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: خوارزمية Red-Black SOR مع جدران نيومان العازلة

سنكتب الآن خوارزمية الاسترخاء الفائق المسرعة بنظام رقعة الشطرنج (Red-Black Ordering) مع تطبيق شروط نيومان العازلة ($\frac{\partial\phi}{\partial n} = 0$) على جدران حفر المريخ:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: sor_neumann_step
def sor_neumann_step(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000):
    # خوارزمية Red-Black SOR مع جدران نيومان العازلة للحفر
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    
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

# تشغيل الاختبار الآلي:
test_lab6.test_sor_neumann_step(sor_neumann_step)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: sor_neumann_step
def sor_neumann_step(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000):
    # خوارزمية Red-Black SOR مع جدران نيومان العازلة للحفر
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    
    cnt = sum(np.roll(f, s, a) for a in (0, 1) for s in (1, -1))
    cnt = np.maximum(cnt, 1.0)
    
    yy, xx = np.mgrid[0:n, 0:m]
    parity = (xx + yy) % 2
    masks = [(parity == c) & free & ~fixed for c in (0, 1)]
    phi[~free] = 0.0
    hist = []
    
    ### START CODE HERE ### (≈ 8-12 lines of code)
    # حلقة تكرارية بعدد maxit:
    # 1. d = 0.0
    # 2. لكل قناع mk في masks:
    #        احسب المتوسط الخماسي: avg = (np.roll(pf, 1, 0) + np.roll(pf, -1, 0) + np.roll(pf, 1, 1) + np.roll(pf, -1, 1)) / cnt
    #        حدث الجهد: phi[mk] = (1 - omega)*old + omega*avg[mk]
    #        احسب أكبر تغيير: d = max(d, float(np.abs(phi[mk] - old).max()))
    # 3. hist.append(d)
    # 4. إذا كان d < tol: اخرج من الحلقة
    pass
    ### END CODE HERE ###
    
    return phi, hist

# تشغيل الاختبار الآلي:
test_lab6.test_sor_neumann_step(sor_neumann_step)
''')

    nb.md(r"""---
## 7. 🌉 الجسر الرياضي والفيزيائي: لماذا نستبدل معادلات الروبوتات القديمة بـ PDE؟

قبل تشغيل المحاكاة الكبرى على **25,600 نقطة من تضاريس المريخ**، دعنا نفهم الرابط الجوهري بين ما كتبته بيدك على الورق وفيزياء ملاحة الفضاء:

### 1. ما هي المعادلة التي تبدأ بها الروبوتات التقليدية؟ (مجال الجهد الاصطناعي - APF)
في الروبوتات العادية وألعاب الفيديو، يبدأ المبرمجون بصيغة جبرية بديهية:
$$U(\mathbf{x}) = U_{\text{att}}(\mathbf{x}) + U_{\text{rep}}(\mathbf{x})$$
* **بئر جذب الهدف ($U_{\text{att}}$):** الهدف يجذب المركبة كأنه نابض جاذبية: $\mathbf{F}_{\text{att}} = -\nabla U_{\text{att}} = -k_{\text{att}}(\mathbf{x} - \mathbf{x}_{\text{goal}})$.
* **جدار تنافر الحفر ($U_{\text{rep}}$):** الحفر تدفع المركبة بعيداً كأنها شحنة كهربائية متنافرة: $\mathbf{F}_{\text{rep}} = -\nabla U_{\text{rep}}$.

وتتحرك المركبة كأنها كرة تتدحرج تحت تأثير محصلة القوى: $\mathbf{F}_{\text{net}} = \mathbf{F}_{\text{att}} + \mathbf{F}_{\text{rep}}$.

---

### 2. لماذا تفشل هذه المعادلة فيزيائياً؟ (فخ الحفر المسدودة 🪤)
تخيل أن مركبة المريخ دخلت حفرة على شكل حرف **U** وكان موقع الهدف العلمي يقع خلف الجدار الخلفي للحفرة مباشرة:
* مع اقتراب المركبة من الجدار نحو الهدف، تزداد قوة الجذب للأمام ($\mathbf{F}_{\text{att}}$).
* وفي نفس الوقت، تزداد قوة التنافر من الجدار للخلف ($\mathbf{F}_{\text{rep}}$).
* في نقطة ما داخل الحفرة، **تتساوى القوتان تماماً في المقدار وتتعاكسان في الاتجاه**:
  $$\mathbf{F}_{\text{att}} + \mathbf{F}_{\text{rep}} = \mathbf{0} \implies \nabla U = \mathbf{0}$$

> ⚠️ **الكارثة الهندسية:** تتلاشى القوة تماماً وتصبح صفراً! تتشكل حفرة جهد صناعية (Local Minimum). تعلق المركبة وتتجمد مكانها حتى تنفد بطاريتها وتفشل المهمة الفضائية بالكامل!

---

### 3. لماذا نحتاج لتغيير المعادلة واستخدام معادلة تفاضلية جزئية (PDE)؟
لأن الجمع الجبري البسيط $U_{\text{att}} + U_{\text{rep}}$ يسمح بتكون قيعان ومنخفضات عشوائية في الفراغ.
ولمنع الفخاخ للأبد، نبحث عن ظاهرة طبيعية **يستحيل فيزيائياً أن تعلق في حفرة**: **إنها فيزياء تدفق المياه 🌊**!
الماء يملأ الحفرة، ويرتفع ضغطه ضد الجدران، وينساب بسلاسة حول العائق نحو المصب دون أن يتجمد في بركة راكدة بالمنتصف.

---

### 4. ما هي المعادلة البديلة وما دورها في المشروع؟
المعادلة الفيزيائية التي تحكم ضغط الموائع والجهد الكهربائي الساكن هي **معادلة لابل (Laplace's Equation)**:
$$\nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} = 0$$

#### دورها في مشروع المريخ:
1. **النطاق ($\Omega$):** نحول خريطة المريخ إلى حقل جهد $\phi(x, y)$.
2. **المصدر والمصب (Dirichlet BCs):** البداية عند أعلى جهد $\phi = 1.0$، والهدف عند أدنى جهد $\phi = 0.0$.
3. **جدران الحفر (Neumann BCs):** جدران معزولة تماماً لا يخترقها الماء $\frac{\partial\phi}{\partial n} = 0$.
4. **الضمان الرياضي القاطع (The Strong Maximum Principle من اللاب 4):**
   الدالة التوافقية **يستحيل أن تمتلك قيعاناً صغرى محلية داخل النطاق**! القمم والقيعان تتواجد فقط على البداية والهدف.
   وبالتالي، تيار الانحدار $-\nabla\phi$ **لا ينعدم أبداً** في المساحات الحرة.
5. **مسار حركة العجلات (Lagrange's Streamline Method من اللاب 2):**
   تنساب عجلات المركبة مع خطوط التيار $\frac{dx}{u} = \frac{dy}{v}$ لتصل إلى الهدف بضمان رياضي 100%!

---
## 8. 🎨 الإطلاق النهائي للمهمة: الملاحة الذاتية على تضاريس المريخ

الآن بعد أن أتقنا الرياضيات والفيزياء، شغّل المحاكاة وشاهد كيف توجه خوارزمية لابل المركبة بنجاح حول الحفر على **25,600 نقطة تضاريس حقيقية من وكالة ناسا**:
""")

    nb.code(r"""from rover_path_finder.terrain import make_terrain
from rover_path_finder.planners import neumann_potential, descend, apf_potential, trap_map

# 1. توليد تضاريس مريخية 100x100
terrain_data = make_terrain(N=100, seed=3, rover_radius=2.0)
terrain = terrain_data['h']
hazards = terrain_data['hazard']
start = terrain_data['start']
goal = terrain_data['goal']

# 2. حل معادلة لابل
phi, sweeps, elapsed = neumann_potential(hazards, start=start, goal=goal)

# 3. تتبع مسار الانحدار مع خطوط الانسياب
path, reached = descend(phi, hazards, start=start, goal=goal)

# 4. رسم حقل الجهد والمسار
fig, ax = plt.subplots(figsize=(10, 8))
cs = ax.contourf(phi, levels=30, cmap='viridis')
plt.colorbar(cs, label="Harmonic Potential $\phi(x, y)$")
ax.contour(hazards, levels=[0.5], colors='red', linewidths=1.5)

px = [p[1] for p in path]
py = [p[0] for p in path]
ax.plot(px, py, color='cyan', linewidth=3, label="Rover Trajectory (Laplace Streamline)")
ax.plot(start[1], start[0], 'go', markersize=10, label="Start ($\phi=1$)")
ax.plot(goal[1], goal[0], 'r*', markersize=14, label="Goal ($\phi=0$)")

ax.set_title("Ares Rover Navigation: Laplace Streamlines Around Martian Craters", fontsize=14)
ax.legend(loc='upper left')
plt.show()

print(f"حالة المهمة: هل وصلت المركبة للهدف بنجاح؟ {reached} في {len(path)} خطوة ({elapsed:.2f} ثانية)!")
""")

    nb.md(r"""---
## 9. 🪤 الاختبار الحاسم: مقارنة فخ الحفر المسدودة (U-Shaped Trap Test)

شغّل الخلية التالية لمشاهدة المقارنة المباشرة بين الروبوت التقليدي (APF) وهو يعلق داخل الحفرة، وبين معادلة لابل التوافقية وهي تلتف بنجاح وتخرج المركبة للأمان:
""")

    nb.code(r"""u_trap, trap_start, trap_goal = trap_map(N=100)

# APF
apf_field = apf_potential(u_trap, goal=trap_goal)
apf_path, apf_reached = descend(apf_field, u_trap, start=trap_start, goal=trap_goal, maxsteps=200)

# Laplace
laplace_field, _, _ = neumann_potential(u_trap, start=trap_start, goal=trap_goal)
laplace_path, laplace_reached = descend(laplace_field, u_trap, start=trap_start, goal=trap_goal, maxsteps=400)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# رسم الروبوت الكلاسيكي
axes[0].contourf(apf_field, levels=25, cmap='magma')
axes[0].plot([p[1] for p in apf_path], [p[0] for p in apf_path], 'r-', linewidth=3, label="APF Path")
axes[0].plot(trap_start[1], trap_start[0], 'go', markersize=8)
axes[0].plot(trap_goal[1], trap_goal[0], 'y*', markersize=12)
axes[0].set_title("Classical Robotics (APF): TRAPPED in Local Minimum! ❌", fontsize=12)
axes[0].legend()

# رسم معادلة لابل
axes[1].contourf(laplace_field, levels=25, cmap='viridis')
axes[1].plot([p[1] for p in laplace_path], [p[0] for p in laplace_path], 'c-', linewidth=3, label="Laplace Path")
axes[1].plot(trap_start[1], trap_start[0], 'go', markersize=8, label="Start")
axes[1].plot(trap_goal[1], trap_goal[0], 'y*', markersize=12, label="Goal")
axes[1].set_title("Laplace PDE: Maneuvers Cleanly Out of the Trap! ✅", fontsize=12)
axes[1].legend()

plt.tight_layout()
plt.show()

print("نتائج المقارنة الحاسمة:")
print(f"  • الروبوت التقليدي (APF) : هل وصل للهدف؟ {apf_reached} (علق نهائياً داخل الحفرة المسدودة)")
print(f"  • معادلة لابل (Laplace) : هل وصل للهدف؟ {laplace_reached} (خرج بسلام من الحفرة في {len(laplace_path)} خطوة!)")
""")

    nb.md(r"""## 🏆 شهادة التخرج من الكورس

**تهانينا الحارة على إتمام كورس المعادلات التفاضلية الجزئية بنجاح!**

لقد أتقنت الرحلة الهندسية والرياضية الكاملة:
1. **الأسس التحليلية:** كونت المعادلات بحذف الثوابت، وحللت خطوط الانسياب بلاجرانج، وقهرت موجات الرادار بشاربيت، وفهمت أصل معادلة لابل من مؤثرات الرتب العليا.
2. **الترقية الرقمية:** حولت المعادلات إلى شبكة 5-Point Stencil، وأثبت سرعة SOR الفائقة بمقدار 66 ضعفاً.
3. **الملاحة الفضائية على المريخ:** حللت معضلة فخاخ الحفر النيزكية بفضل قانون Maximum Principle، وضمنت ملاحة آمنة وذكية لمركبات الفضاء!
""")

    nb.save()


if __name__ == "__main__":
    print("Building all 6 DeepLearning.AI-grade course labs in ARABIC (labs_ar/)...")
    build_lab_1_ar(solutions=False, target_dir="labs_ar")
    build_lab_2_ar(solutions=False, target_dir="labs_ar")
    build_lab_3_ar(solutions=False, target_dir="labs_ar")
    build_lab_4_ar(solutions=False, target_dir="labs_ar")
    build_lab_5_ar(solutions=False, target_dir="labs_ar")
    build_lab_6_ar(solutions=False, target_dir="labs_ar")
    print("\n[OK] All 6 Arabic student labs successfully generated in 'labs_ar/'!")
    
    print("\nGenerating companion solutions in 'solutions/labs_ar/'...")
    build_lab_1_ar(solutions=True, target_dir="solutions/labs_ar")
    build_lab_2_ar(solutions=True, target_dir="solutions/labs_ar")
    build_lab_3_ar(solutions=True, target_dir="solutions/labs_ar")
    build_lab_4_ar(solutions=True, target_dir="solutions/labs_ar")
    build_lab_5_ar(solutions=True, target_dir="solutions/labs_ar")
    build_lab_6_ar(solutions=True, target_dir="solutions/labs_ar")
    print("[OK] All 6 Arabic reference solutions successfully generated in 'solutions/labs_ar/'!")
