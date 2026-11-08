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
import re

os.makedirs("labs_ar", exist_ok=True)

RLM = "\u200f"  # Unicode Right-to-Left Mark
LRM = "\u200e"  # Unicode Left-to-Right Mark


def _protect_inline_segments(line: str, in_table: bool = False) -> str:
    """Converts inline math, code, links, bold, and italics into Colab-safe RTL/LTR HTML."""
    math_store: list[str] = []
    code_store: list[str] = []

    # 1. Extract inline $...$ math first so *, _, [] inside LaTeX are untouched
    def _save_math(m: re.Match) -> str:
        expr = m.group(1).strip().replace(r"\|", r"\Vert ")
        nowrap = " white-space:nowrap;" if in_table else ""
        html = (
            f'{RLM}<span dir="ltr" style="direction:ltr; display:inline-block; '
            f'unicode-bidi:isolate;{nowrap}">${{{expr}}}$</span>{RLM}'
        )
        idx = len(math_store)
        math_store.append(html)
        return f"\x00MATH{idx}\x00"

    line = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", _save_math, line)

    # 2. Extract inline `...` code spans second so ** or _ inside code are untouched
    def _save_code(m: re.Match) -> str:
        raw_code = m.group(1)
        has_arabic = bool(re.search(r"[\u0600-\u06FF]", raw_code))
        code_txt = (
            raw_code.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("*", "&#42;")
            .replace("_", "&#95;")
        )
        c_dir = "rtl" if has_arabic else "ltr"
        html = (
            f'{RLM}<code dir="{c_dir}" style="direction:{c_dir}; display:inline-block; '
            f'unicode-bidi:isolate; padding:1px 5px; border-radius:3px;">{code_txt}</code>{RLM}'
        )
        idx = len(code_store)
        code_store.append(html)
        return f"\x00CODE{idx}\x00"

    line = re.sub(r"`([^`]+)`", _save_code, line)

    # 3. Convert Markdown links [label](url) -> <a href="url">label</a>
    line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', line)

    # 4. Convert **bold** -> <b>bold</b> and *italic* -> <i>italic</i>
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", line)

    # 5. Restore code and math placeholders
    for idx, html in enumerate(code_store):
        line = line.replace(f"\x00CODE{idx}\x00", html)
    for idx, html in enumerate(math_store):
        line = line.replace(f"\x00MATH{idx}\x00", html)

    return line


def _render_rtl_table(table_lines: list[str]) -> str:
    """Converts a Markdown table into a Colab-proof 100%-width RTL HTML table."""
    rows = []
    for raw in table_lines:
        s = raw.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", s)]
        rows.append(cells)

    if len(rows) < 2:
        return "\n".join(table_lines)

    header = rows[0]
    body_start = 2 if all(re.match(r"^:?-{2,}:?$", c.replace(" ", "")) for c in rows[1]) else 1
    body = rows[body_start:]

    out = [
        '<div dir="rtl" style="direction:rtl; text-align:right; overflow-x:auto; width:100%; margin:14px 0;">',
        '<table dir="rtl" style="display:table; width:100%; border-collapse:collapse; direction:rtl; text-align:right;">',
        "<thead>",
        "<tr>",
    ]
    for h in header:
        h_clean = _protect_inline_segments(h, in_table=True)
        out.append(
            '<th dir="rtl" align="right" style="direction:rtl; text-align:right; padding:9px 12px; '
            'border:1px solid rgba(128,128,128,0.4); background-color:rgba(128,128,128,0.16); '
            'font-weight:bold; line-height:1.75; vertical-align:middle;">\n\n'
            f"{RLM}{h_clean}\n\n</th>"
        )
    out.extend(["</tr>", "</thead>", "<tbody>"])

    for r in body:
        out.append("<tr>")
        for c in r:
            c_clean = _protect_inline_segments(c, in_table=True)
            out.append(
                '<td dir="rtl" align="right" style="direction:rtl; text-align:right; padding:8px 12px; '
                'border:1px solid rgba(128,128,128,0.35); vertical-align:middle; line-height:1.8;">\n\n'
                f"{RLM}{c_clean}\n\n</td>"
            )
        out.append("</tr>")

    out.extend(["</tbody>", "</table>", "</div>"])
    return "\n".join(out)


def _format_rtl_section(section_text: str) -> str:
    """Formats a single Arabic Markdown section so Google Colab renders RTL text, lists, and math cleanly."""
    lines = section_text.strip().split("\n")
    out_blocks: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 1. Blank line
        if not stripped:
            out_blocks.append("")
            i += 1
            continue

        # 2. Code fence ``` ... ```
        if stripped.startswith("```"):
            fence_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                fence_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            code_body = (
                "\n".join(fence_lines)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            out_blocks.append(
                '\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; '
                'background-color:rgba(128,128,128,0.12); padding:10px 14px; border-radius:6px; '
                'overflow-x:auto; margin:10px 0; font-family:monospace; white-space:pre;">'
                f"{RLM}{code_body}</div>\n"
            )
            continue

        # 3. Single-line or multi-line display math $$ ... $$
        if stripped.startswith("$$"):
            if stripped.endswith("$$") and len(stripped) > 4:
                math_content = stripped
                i += 1
            else:
                math_lines = [stripped]
                i += 1
                while i < n:
                    math_lines.append(lines[i].strip())
                    if lines[i].strip().endswith("$$"):
                        i += 1
                        break
                    i += 1
                math_content = "\n".join(math_lines)
            out_blocks.append(
                '\n<div dir="ltr" align="center" style="direction:ltr; text-align:center; margin:12px 0; overflow-x:auto;">\n\n'
                f"{math_content}\n\n</div>\n"
            )
            continue

        # 4. Markdown Table (consecutive lines starting with |)
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i])
                i += 1
            out_blocks.append("\n" + _render_rtl_table(table_lines) + "\n")
            continue

        # 5. Blockquote (> ...)
        if stripped.startswith(">"):
            bq_lines = []
            while i < n and lines[i].strip().startswith(">"):
                content = re.sub(r"^>\s?", "", lines[i].strip())
                bq_lines.append(f"{RLM}{_protect_inline_segments(content)}")
                i += 1
            bq_body = "<br>\n".join(bq_lines)
            out_blocks.append(
                '\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; '
                'border-right:4px solid #f59e0b; background-color:rgba(245,158,11,0.08); '
                'padding:10px 14px; margin:12px 0; border-radius:4px; line-height:1.85;">\n\n'
                f"{bq_body}\n\n</div>\n"
            )
            continue

        # 6. HTML tags like <details>, </details>, <summary>...</summary>
        if stripped.startswith("<details"):
            out_blocks.append(
                '\n<details dir="rtl" style="direction:rtl; text-align:right; margin:8px 0; padding:6px 10px;">\n'
            )
            i += 1
            continue
        if stripped.startswith("<summary>"):
            inner = stripped[len("<summary>") : -len("</summary>")] if stripped.endswith("</summary>") else stripped[9:]
            inner = _protect_inline_segments(inner)
            out_blocks.append(
                f'<summary dir="rtl" style="direction:rtl; text-align:right; cursor:pointer; font-weight:bold;">\n\n{RLM}{inner}\n\n</summary>\n'
            )
            i += 1
            continue
        if stripped.startswith("</details>"):
            out_blocks.append("\n</details>\n")
            i += 1
            continue

        # 7. Bullet list item (* ... or - ...)
        m_bullet = re.match(r"^(\s*)[\*\-]\s+(.*)$", line)
        if m_bullet:
            indent_len = len(m_bullet.group(1))
            content = _protect_inline_segments(m_bullet.group(2).strip())
            pad_right = 34 if indent_len >= 2 else 14
            marker = "▪" if indent_len >= 2 else "•"
            out_blocks.append(
                f'\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; '
                f'margin:5px 0; padding-right:{pad_right}px; line-height:1.85;">\n\n'
                f"{RLM}{marker} {content}\n\n</div>\n"
            )
            i += 1
            continue

        # 8. Numbered list item (1. ...)
        m_num = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m_num:
            indent_len = len(m_num.group(1))
            num_str = m_num.group(2)
            content = _protect_inline_segments(m_num.group(3).strip())
            pad_right = 26 if indent_len >= 2 else 8
            out_blocks.append(
                f'\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; '
                f'margin:7px 0; padding-right:{pad_right}px; line-height:1.85;">\n\n'
                f"{RLM}<b>{num_str}.</b> {content}\n\n</div>\n"
            )
            i += 1
            continue

        # 9. Markdown Heading (#, ##, ###, ####)
        m_head = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m_head:
            hashes = m_head.group(1)
            title = _protect_inline_segments(m_head.group(2).strip())
            out_blocks.append(
                f'\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; margin:12px 0 6px 0;">\n\n'
                f"{hashes} {RLM}{title}\n\n</div>\n"
            )
            i += 1
            continue

        # 10. Regular paragraph line (check if inline $$...$$ appears inside the line)
        if "$$" in stripped:
            parts = re.split(r"(\$\$.+?\$\$)", stripped)
            for p in parts:
                p_s = p.strip()
                if not p_s:
                    continue
                if p_s.startswith("$$") and p_s.endswith("$$"):
                    out_blocks.append(
                        '\n<div dir="ltr" align="center" style="direction:ltr; text-align:center; margin:12px 0; overflow-x:auto;">\n\n'
                        f"{p_s}\n\n</div>\n"
                    )
                else:
                    out_blocks.append(
                        '\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; margin:6px 0; line-height:1.85;">\n\n'
                        f"{RLM}{_protect_inline_segments(p_s)}\n\n</div>\n"
                    )
            i += 1
            continue

        out_blocks.append(
            '\n<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; margin:6px 0; line-height:1.85;">\n\n'
            f"{RLM}{_protect_inline_segments(stripped)}\n\n</div>\n"
        )
        i += 1

    body = "\n".join(out_blocks).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return (
        '<div dir="rtl" align="right" style="direction:rtl; text-align:right; unicode-bidi:embed; '
        'width:calc(100vw - 140px); max-width:calc(100vw - 140px); min-width:100%; box-sizing:border-box; '
        'line-height:1.85; padding:6px 14px 16px 14px;">\n'
        '<style>.markdown, .markdown-body, :host { max-width: 100% !important; width: 100% !important; }</style>\n\n'
        f"{body}\n\n</div>"
    )


class ArabicNotebookBuilder:
    def __init__(self, filename: str, target_dir: str = "labs_ar"):
        self.filename = filename
        self.target_dir = target_dir
        self.cells = []

    def colab_badge(self):
        url = f"https://colab.research.google.com/github/hany73-max/PDE-Rover-Engine/blob/main/labs_ar/{self.filename}"
        badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"
        self.md(badge, rtl=False)

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
            "        else:\n"
            "            import subprocess\n"
            "            subprocess.run(['git', '-C', 'PDE-Rover-Engine', 'pull', '--ff-only'], check=False)\n"
            "        os.chdir('PDE-Rover-Engine')\n"
            "        if '.' not in sys.path:\n"
            "            sys.path.insert(0, '.')\n"
            "        print('[OK] تم تجهيز بيئة Google Colab بنجاح والاتصال بمستودع المشروع!')\n"
            "except NameError:\n"
            "    pass"
        )
        self.code(source)

    def md(self, source: str, rtl: bool = True):
        text = source.strip()
        if not rtl:
            self.cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + "\n" for line in text.split("\n")]
            })
            return

        # Remove leading/trailing --- and split multi-part sections on \n---\n
        # so Google Colab never clips giant multi-section cells
        text = re.sub(r"^\s*---\s*\n", "", text)
        text = re.sub(r"\n\s*---\s*$", "", text)
        sections = [s.strip() for s in re.split(r"\n\s*---\s*\n", text) if s.strip()]

        for sec in sections:
            formatted = _format_rtl_section(sec)
            self.cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + "\n" for line in formatted.split("\n")]
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
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في ملاحة المركبات الفضائية  
**المرجع في المذكرة:** الباب الأول، القسم 1.1 و 1.2 (صفحات المذكرة 1–10 / صفحات ملف PDF: 2–11)

> 🗺️ **أين يقع هذا اللاب في خط عمل المشروع؟**  
> `خريطة الارتفاعات h(x,y)` $\longrightarrow$ **`[اللاب 1: حساب الميول p, q وكشف العوائق slope_map]`** $\longrightarrow$ `نطاق الأمان` $\longrightarrow$ `معادلة لابلاس` $\longrightarrow$ `مسار المركبة`  
> **الملف الحقيقي في المشروع:** [`rover_path_finder/terrain.py`](../rover_path_finder/terrain.py) — الدالة `slope_map(h, cell)`

---
### 🧭 قاموس الربط: الرياضيات $\longleftrightarrow$ المعنى الفيزيائي $\longleftrightarrow$ كود المشروع
| 1. الرمز في مذكرة المحاضرة | 2. المعنى الفيزيائي على أرض المريخ | 3. الكود الفعلي في `terrain.py` |
| :--- | :--- | :--- |
| $z = h(x, y)$ | ارتفاع سطح الأرض (بالمتر) عند الإحداثيات $(x, y)$ | مصفوفة الارتفاعات `h` ثنائية الأبعاد |
| $p = \frac{\partial z}{\partial x}, \quad q = \frac{\partial z}{\partial y}$ | ميل السطح باتجاه الشرق ($x$) وباتجاه الشمال ($y$) | `gy, gx = np.gradient(h, cell)` |
| $\sqrt{p^2 + q^2}$ | مقدار الانحدار الكلي للسطح (ظل زاوية الميل $\tan\theta$) | `slope = np.degrees(np.arctan(np.hypot(gx, gy)))` |
| $F(x, y, z, a, b) = 0$ | عائلة أسطح (مثلاً حفر بمراكز مختلفة $a, b$) | `Z = (X - a)**2 + (Y - b)**2` |
| $f(x, y, z, p, q) = 0$ | **المعادلة التفاضلية الجزئية (PDE):** قانون يربط الميل بالارتفاع بغض النظر عن قيمة $(a,b)$ | `residual = (P**2 + Q**2) - 4*Z` |

---
## 1. الفكرة ببساطة: لماذا نحذف الثوابت الاختيارية؟
تخيل أن على سطح المريخ مئات الحفر الدائرية. كل حفرة لها مركز مختلف $(a, b)$ على الخريطة:
$$z = (x - a)^2 + (y - b)^2$$
عندما يفحص حاسوب المركبة خريطة الارتفاعات ليقرر: **«هل هذه النقطة شديدة الانحدار (أكبر من $20^\circ$)؟»**، فإنه لا يعرف أين يقع مركز كل حفرة $(a, b)$ مسبقاً.

**حذف الثوابت الاختيارية (Elimination of Arbitrary Constants)** يحوّل معادلة تعتمد على الموقع الخاص $(a, b)$ إلى **علاقة عامة تربط الميل $(p, q)$ بالعمق $z$ مباشرةً**:
$$p^2 + q^2 = 4z$$
هذه المعادلة تخبرنا بحقيقة هندسية رائعة: **مقدار ميل جدار الحفرة يعتمد فقط على عمق النقطة $z$، ولا يعتمد إطلاقاً على مكان الحفرة $(a, b)$!** ولهذا السبب تعمل دالة `slope_map` في مشروعنا بكفاءة على أي تضاريس دون معرفة معادلاتها أو مراكز الحفر فيها.
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab1

%matplotlib inline
print("تم تهيئة بيئة اللاب 1 بنجاح!")
""")

    nb.md(r"""---
## 2. أساسيات القسم (1.1) وقاعدة عمل القسم (1.2) من المذكرة (PDF ص 2–11)

قبل أن نحذف الثوابت، لنتقن المفاهيم الأساسية في **القسم (1.1) (صفحات المذكرة 1–5 / PDF ص 2–6)** لأنها تأتي دائماً في أسئلة الاختيارات والامتحانات:

### أولاً: رموز مونج الخمسة (Monge's Notations — صفحة 3 بالمذكرة / PDF ص 4)
في كل صفحات المذكرة، عندما تكون $z(x, y)$ دالة في متغيرين مستقلين $x$ و $y$، نستخدم الرموز القياسية التالية:
$$p = \frac{\partial z}{\partial x}, \qquad q = \frac{\partial z}{\partial y}, \qquad r = \frac{\partial^2 z}{\partial x^2}, \qquad s = \frac{\partial^2 z}{\partial x \partial y}, \qquad t = \frac{\partial^2 z}{\partial y^2}$$
*(ملاحظة جميلة للربط بالمشروع: في اللاب 4 واللاب 6 سنرى أن **معادلة لابلاس** للملاحة هي ببساطة $r + t = 0$!)*

---

### ثانياً: الفرق بين الرتبة (Order) والدرجة (Degree) — والفخ الشهير! (ص 2 بالمذكرة / PDF ص 3)
1. **الرتبة (Order):** هي رتبة **أعلى مشتقة جزئية** موجودة في المعادلة.
2. **الدرجة (Degree):** هي **أُس (قوة) أعلى مشتقة جزئية**، ولكن **بشرط جوهري:** يجب أولاً التخلص من أي جذور أو أسس كسرية أو كسور تحتوي على المشتقات!
   * **🔍 مثال الفخ في المذكرة (مثال 5 ص 1–2 / PDF ص 2–3):**
     $$\frac{\partial^2 z}{\partial x^2} = \left(1 + \frac{\partial z}{\partial y}\right)^{\frac{1}{2}}$$
     * لو تسرعت وقرأت الأس قبل التبسيط لقلت الدرجة الأولى! ولكن لوجود الأس الكسري $\frac{1}{2}$ (جذر تربيعي) على المشتقة، **يجب تربيع الطرفين أولاً**:
       $$\left(\frac{\partial^2 z}{\partial x^2}\right)^2 = 1 + \frac{\partial z}{\partial y}$$
     * الآن نقرأ أعلى مشتقة وهي $\frac{\partial^2 z}{\partial x^2}$: **الرتبة = 2 (الثانية)**، ولأنها مرفوعة للأس 2 بعد التربيع فإن **الدرجة = 2 (الثانية)**!

---

### ثالثاً: التصنيف الرباعي لمعادلات الرتبة الأولى (القسم 1.1.7 — ص 4–5 بالمذكرة / PDF ص 5–6)
كيف تفرق بين الأنواع الأربعة لمعادلات الرتبة الأولى $f(x, y, z, p, q) = 0$ بمجرد النظر؟

| النوع في المذكرة (PDF ص 5–6) | الصورة العامة | الشرط المميز في خطوة واحدة | أمثلة المذكرة (PDF ص 5–6) |
| ---: | ---: | ---: | ---: |
| **1. خطية تماماً (Linear)** | $P(x,y)p + Q(x,y)q = R(x,y)z + S(x,y)$ | المشتقتان $p, q$ **وكذلك $z$** كلها من الدرجة الأولى، ولا يوجد ضرب بينها ($zp$ ممنوع!) | $yx^2 p + xy^2 q = xyz + x^2 y^3$ |
| **2. نصف خطية (Semi-linear)** | $P(x,y)p + Q(x,y)q = R(x,y,z)$ | المشتقتان $p, q$ من الدرجة الأولى، ومعاملاتهما $P(x,y), Q(x,y)$ **تعتمد على $x, y$ فقط** (خالية من $z$)، بينما الطرف الأيمن $R$ قد يكون غير خطي في $z$ | $xyp + x^2 y q = x^2 y^2 z^2$ |
| **3. شبه خطية (Quasi-linear)** | $P(x,y,z)p + Q(x,y,z)q = R(x,y,z)$ | المشتقتان $p, q$ من الدرجة الأولى، ولكن معاملاتهما $P, Q$ **تحتوي على $z$** (هذه المعادلة وما سبقها تُحل جميعاً **بطريقة لاجرانج** في اللاب 2!) | $x^2 z p + y^2 z q = xy$ |
| **4. غير خطية (Non-linear)** | $f(x,y,z,p,q) = 0$ | تحتوي على تربيع $p^2, q^2$ أو حاصل ضرب $p \cdot q$ (وتُحل **بطريقة شاربت والأشكال الأربعة** في اللاب 3!) | $p^2 + q^2 = 1$ أو $pq = z$ |

---

### رابعاً: الحالات الثلاث لحذف الثوابت الاختيارية (القسم 1.2 — ص 6–9 بالمذكرة / PDF ص 7–10)
عند حذف ثوابت اختيارية من علاقة $F(x, y, z, a, b) = 0$، نشتق جزئياً بالنسبة لـ $x$ وبالنسبة لـ $y$، وتنشأ إحدى **الحالات الثلاث التالية**:

1. **الحالة (1) — عدد الثوابت $<$ عدد المتغيرات المستقلة (PDF ص 7–8):**
   * **النتيجة:** نحصل على **أكثر من معادلة تفاضلية جزئية** من الرتبة الأولى.
   * **مثال المذكرة (PDF ص 7):** $z = ax + y$ (ثابت واحد $a$ ومتغيران $x, y$):
     * نشتق بالنسبة لـ $x$: $\frac{\partial z}{\partial x} = a \implies$ نعوض عن $a$ في الأصلية فنحصل على المعادلة الأولى: $z = x\frac{\partial z}{\partial x} + y$.
     * نشتق بالنسبة لـ $y$: $\frac{\partial z}{\partial y} = 1$ (وهي خالية من $a$ أصلاً، فتمثل معادلة ثانية!).

2. **الحالة (2) — عدد الثوابت $=$ عدد المتغيرات المستقلة (PDF ص 8):**
   * **النتيجة:** نحصل على **معادلة تفاضلية جزئية واحدة وحيدة** من الرتبة الأولى.
   * **مثال المذكرة (PDF ص 8):** احذف $a, b$ من $az + b = a^2 x + y$:
     * نشتق بالنسبة لـ $x$: $a\frac{\partial z}{\partial x} = a^2 \implies \frac{\partial z}{\partial x} = a$.
     * نشتق بالنسبة لـ $y$: $a\frac{\partial z}{\partial y} = 1$.
     * نعوض عن $a = \frac{\partial z}{\partial x}$ في المعادلة الثانية فنحصل فوراً على: $\left(\frac{\partial z}{\partial x}\right)\left(\frac{\partial z}{\partial y}\right) = 1$ (أي $pq = 1$).

3. **الحالة (3) — عدد الثوابت $>$ عدد المتغيرات المستقلة (PDF ص 8–9):**
   * **النتيجة:** المشتقات الأولى وحدها لا تكفي لحذف جميع الثوابت، فنشتق مرة ثانية للحصول على معادلات من **الرتبة الثانية أو أعلى**.
   * **مثال المذكرة (PDF ص 9):** احذف الثوابت الثلاثة $a, b, c$ من $z = ax + by + cxy$:
     * المشتقات الأولى: $\frac{\partial z}{\partial x} = a + cy \;\cdots(2)$، و $\frac{\partial z}{\partial y} = b + cx \;\cdots(3)$.
     * المشتقات الثانية: $\frac{\partial^2 z}{\partial x^2} = 0$، و $\frac{\partial^2 z}{\partial y^2} = 0 \;\cdots(4)$، والمشتقة المختلطة: $\frac{\partial^2 z}{\partial x \partial y} = c \;\cdots(5)$.
     * بضرب $(2)$ في $x$ وضرب $(3)$ في $y$ وجمعهما:
       $$x\frac{\partial z}{\partial x} + y\frac{\partial z}{\partial y} = \underbrace{ax + by + cxy}_{=\,z} + cxy = z + xy\frac{\partial^2 z}{\partial x \partial y} \;\cdots(6)$$

> ⚠️ **تنبيه خطأ مطبعي في مذكرة الكلية (PDF صفحة 9 — المعادلتان 5 و 6):**
> في ملف الـ PDF (صفحة 9، السطر 6 والسطر 11)، كُتبت المشتقة المختلطة بالخطأ المطبعي $\frac{\partial^2 y}{\partial x \partial y}$ (بحرف $y$ في البسط)، والصواب رياضياً هو $\frac{\partial^2 z}{\partial x \partial y} = c$ لأن $z$ هو المتغير التابع بينما $x, y$ متغيران مستقلان!

---

### 📖 مثال محلول بالتفصيل من المذكرة (Example 1 — صفحة 8 بالمذكرة / PDF ص 9–10):
**المسألة:** كوّن المعادلة التفاضلية الجزئية بحذف الثابتين الاختياريين $a$ و $b$ من عائلة المستويات:
$$z = a x + b y + a^2 + b^2 \qquad \cdots (1)$$

**الحل خطوة بخطوة (مع سبب كل خطوة):**
* **الخطوة 1 (الاشتقاق بالنسبة لـ $x$):** نعتبر $y$ ثابتاً ونشتق المعادلة $(1)$ بالنسبة لـ $x$:
  $$p = \frac{\partial z}{\partial x} = a \qquad \cdots (2)$$
  *(لماذا؟ لأن $by + a^2 + b^2$ كلها ثوابت بالنسبة لـ $x$ فمشتقتها صفر!)*
* **الخطوة 2 (الاشتقاق بالنسبة لـ $y$):** نعتبر $x$ ثابتاً ونشتق المعادلة $(1)$ بالنسبة لـ $y$:
  $$q = \frac{\partial z}{\partial y} = b \qquad \cdots (3)$$
* **الخطوة 3 (التعويض والحذف):** نعوض عن $a = p$ وعن $b = q$ في المعادلة الأصلية $(1)$:
  $$z = x p + y q + p^2 + q^2$$
* **التحقق السريع:** هل بقيت أي رموز $a$ أو $b$؟ لا! إذن حصلنا على معادلة تفاضلية جزئية غير خطية من الرتبة الأولى والدرجة الثانية (وهي على صيغة كليروت التي سنحلها في اللاب 3!).
""")

    nb.md(r"""---
## 3. ✍️ تحدي الورقة والقلم 1 (Example 2 — صفحة 9 بالمذكرة / PDF ص 10)

**المسألة:** احذف الثابتين الاختياريين $a$ و $b$ من معادلة عائلة الأسطح المكافئة الدائرية (حفر المريخ):
$$z = (x - a)^2 + (y - b)^2 \qquad \cdots (1)$$

**جرّب الحل بنفسك على الورقة أولاً!** إذا احتجت مساعدة، افتح التلميحات التدريجية التالية:

<details>
<summary>💡 <b>تلميح 1: كيف نبدأ؟</b> (اضغط للفتح)</summary>

اشتق المعادلة $(1)$ جزئياً بالنسبة لـ $x$ لتحصل على $p$، ثم بالنسبة لـ $y$ لتحصل على $q$. تذكر قاعدة السلسلة: مشتقة $(x-a)^2$ بالنسبة لـ $x$ هي $2(x-a)$.
</details>

<details>
<summary>💡 <b>تلميح 2: كيف نتخلص من $(x-a)$ و $(y-b)$؟</b> (اضغط للفتح)</summary>

أصبح لديك:
$$p = 2(x - a) \quad \text{و} \quad q = 2(y - b)$$
لاحظ أن المعادلة الأصلية $(1)$ تحتوي على $(x-a)^2 + (y-b)^2$. ماذا يحدث لو ربّعت $p$ وربّعت $q$ وجمعتهما؟
</details>

<details>
<summary>💡 <b>تلميح 3: الخطوة الأخيرة</b> (اضغط للفتح)</summary>

$$p^2 + q^2 = 4(x - a)^2 + 4(y - b)^2 = 4\underbrace{\left[(x - a)^2 + (y - b)^2\right]}_{=\,z}$$
استبدل القوس الكبير بـ $z$ من المعادلة $(1)$.
</details>

اكتب المعادلة التفاضلية الجزئية الناتجة كنص في الخلية التالية (بصيغة مثل `"p^2 + q^2 = 4*z"`):
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ###
student_pde_1 = "p^2 + q^2 = 4*z"
### END CODE HERE ###

# يفحص المصحح الآلي معادلتك بالتعويض العددي في عشرات النقاط العشوائية:
test_lab1.check_paper_challenge_1(student_pde_1)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ### (≈ 1 line of code)
# اكتب المعادلة التي توصلت إليها بدلالة p و q و z:
student_pde_1 = None
### END CODE HERE ###

# يفحص المصحح الآلي معادلتك بالتعويض العددي في عشرات النقاط العشوائية:
test_lab1.check_paper_challenge_1(student_pde_1)
""")

    nb.md(r"""---
## 4. 🚀 تحدي الربط بالمشروع: فحص حوض الهبوط الإهليلجي

في تضاريس المريخ، قد تكون الحفرة ممتدة (إهليلجية) بمعامل انحناء $a$ شرقاً و $b$ شمالاً:
$$z = \frac{1}{2} a x^2 + \frac{1}{2} b y^2 \qquad \cdots (1)$$

**المطلوب على ورقتك:**
احذف الثابتين الاختياريين $a$ و $b$ لتكوين المعادلة التفاضلية الجزئية التي تربط الارتفاع $z$ بالميول $(p, q)$ عند أي نقطة $(x, y)$.

<details>
<summary>💡 <b>تلميح 1:</b> احسب $p$ و $q$</summary>

$$p = \frac{\partial z}{\partial x} = a x \implies a = \frac{p}{x}$$
$$q = \frac{\partial z}{\partial y} = b y \implies b = \frac{q}{y}$$
</details>

<details>
<summary>💡 <b>تلميح 2:</b> عوّض في المعادلة الأصلية</summary>

عوّض عن $a = \frac{p}{x}$ وعن $b = \frac{q}{y}$ في المعادلة $(1)$ وبسّط الكسور (يمكنك ضرب الطرفين في $2$ للتخلص من الكسور).
</details>
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي حوض المريخ
### START CODE HERE ###
rover_basin_pde = "x*p + y*q = 2*z"
### END CODE HERE ###

test_lab1.check_paper_challenge_2(rover_basin_pde)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي حوض المريخ
### START CODE HERE ### (≈ 1 line of code)
# اكتب المعادلة الناتجة بدلالة x, y, z, p, q:
rover_basin_pde = None
### END CODE HERE ###

test_lab1.check_paper_challenge_2(rover_basin_pde)
""")

    nb.md(r"""---
## 5. 💻 من الورقة إلى الكود: التحقق العددي على شبكة التضاريس

**كيف نتحقق برمجياً من أن حلنا الورقي صحيح؟**  
إذا كانت المعادلة $p^2 + q^2 = 4z$ صحيحة، فإن الفرق بين الطرف الأيسر والطرف الأيمن (ويسمى **المتبقي Residual**):
$$\text{residual} = (p^2 + q^2) - 4z$$
يجب أن يساوي **صفراً** عند كل نقطة من نقاط الشبكة، أياً كان مركز الحفرة $(a, b)$!

أكمل الدالة `verify_crater_pde` أدناه لحساب مصفوفة المتبقي:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: verify_crater_pde
def verify_crater_pde(Z: np.ndarray, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    """تحسب المتبقي (p^2 + q^2) - 4*z للتحقق من معادلة الحفرة على كامل الشبكة."""
    ### START CODE HERE ###
    residual = (P**2 + Q**2) - 4.0 * Z
    ### END CODE HERE ###
    return residual

test_lab1.test_eliminate_constants_fn(verify_crater_pde)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: verify_crater_pde
def verify_crater_pde(Z: np.ndarray, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    """تحسب المتبقي (p^2 + q^2) - 4*z للتحقق من معادلة الحفرة على كامل الشبكة."""
    ### START CODE HERE ### (≈ 1 line of code)
    # اكتب معادلة المتبقي بدلالة المصفوفات P و Q و Z:
    residual = None
    ### END CODE HERE ###
    return residual

test_lab1.test_eliminate_constants_fn(verify_crater_pde)
''')

    nb.md(r"""---
## 6. 🛰️ الرؤية البصرية والربط الفعلي بكود المشروع (`terrain.slope_map`)

شغّل الخلية التالية لترى شيئين معاً:
1. **على اليسار والوسط:** سطح الحفرة $z=(x-a)^2+(y-b)^2$ ومتجهات الميل $(p, q)$ التي حسبتها على الورق.
2. **على اليمين (من محرك المشروع الفعلي `rover_path_finder/terrain.py`):** كيف تستخدم دالة `slope_map` نفس المشتقتين $(p, q)$ لحساب زاوية الميل بالدرجات $\theta = \arctan\sqrt{p^2+q^2}$ وتحديد المناطق الخطرة (الحمراء $> 20^\circ$) على تضاريس المريخ!
""")

    nb.code(r"""from rover_path_finder.terrain import make_terrain, slope_map

x = np.linspace(-3, 3, 40)
y = np.linspace(-3, 3, 40)
X, Y = np.meshgrid(x, y)
Z = (X - 0.5)**2 + (Y + 0.5)**2  # حفرة مركزها (a=0.5, b=-0.5)

dx = x[1] - x[0]
dy = y[1] - y[0]
# انتبه: المحور 0 هو y (الصفوف) والمحور 1 هو x (الأعمدة)
Q, P = np.gradient(Z, dy, dx)

# استدعاء دالة المشروع الحقيقية لحساب خريطة الميول على تضاريس المريخ
mars_demo = make_terrain(N=100, seed=3)
mars_slopes_deg = slope_map(mars_demo["h"], cell=1.0)

fig = plt.figure(figsize=(16, 4.8))

ax1 = fig.add_subplot(1, 3, 1, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='copper', alpha=0.85)
ax1.set_title("1. Crater Surface z = (x-a)^2 + (y-b)^2", fontsize=11)
ax1.set_xlabel("x")
ax1.set_ylabel("y")

ax2 = fig.add_subplot(1, 3, 2)
ax2.contour(X, Y, Z, levels=15, cmap='copper')
ax2.quiver(X[::3, ::3], Y[::3, ::3], P[::3, ::3], Q[::3, ::3], color='crimson')
ax2.set_title(r"2. Slope Vectors (p, q) = ($\partial z/\partial x$, $\partial z/\partial y$)", fontsize=11)
ax2.set_xlabel("x")
ax2.set_ylabel("y")

ax3 = fig.add_subplot(1, 3, 3)
im = ax3.imshow(mars_slopes_deg, cmap='inferno', origin='lower')
ax3.contour(mars_demo["raw"], levels=[0.5], colors='cyan', linewidths=1.2)
plt.colorbar(im, ax=ax3, label="Slope (degrees)")
ax3.set_title("3. Project Engine: terrain.slope_map() & Hazards (cyan)", fontsize=11)
ax3.set_xlabel("Grid X")
ax3.set_ylabel("Grid Y")

plt.tight_layout()
plt.show()

#📌 ملخص اللاب 1 في 3 نقاط:
print("📌 ملخص اللاب 1:")
print("  1) p = dz/dx و q = dz/dy هما مركبتا ميل التضاريس في اتجاهي x و y.")
print("  2) حذف الثوابت الاختيارية (a, b) يعطينا قانوناً عاماً للميل (p^2 + q^2 = 4z) لا يتوقف على موقع الحفرة.")
print("  3) دالة slope_map() في المشروع تطبق هذا القانون لتحويل خريطة الارتفاعات إلى قناع عوائق (Hazard Mask).")
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
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في ملاحة المركبات الفضائية  
**المرجع في المذكرة:** الباب الأول، القسم 1.1.7 (ص 4–5) والقسم 1.3.1–1.3.2 (صفحات المذكرة 11–16 / صفحات PDF: 12–17)

> 🗺️ **أين يقع هذا اللاب في خط عمل المشروع؟**  
> `خريطة الارتفاعات` $\longrightarrow$ `كشف العوائق` $\longrightarrow$ `نطاق الأمان` $\longrightarrow$ `معادلة لابلاس φ(x,y)` $\longrightarrow$ **`[اللاب 2: تتبع خط الانسياب descend()]`**  
> **الملف الحقيقي في المشروع:** [`rover_path_finder/planners.py`](../rover_path_finder/planners.py) — الدالة `descend(P, hazard, start, goal)`

---
### 🧭 قاموس الربط: الرياضيات $\longleftrightarrow$ المعنى الفيزيائي $\longleftrightarrow$ كود المشروع
| 1. الرمز في مذكرة المحاضرة | 2. المعنى الفيزيائي على أرض المريخ | 3. الكود الفعلي في `planners.py` |
| :--- | :--- | :--- |
| $P(x,y,z)\,p + Q(x,y,z)\,q = R(x,y,z)$ | **معادلة لاجرانج شبه الخطية:** المشتقتان $p, q$ من الدرجة الأولى | $\phi_x \frac{\partial\psi}{\partial x} + \phi_y \frac{\partial\psi}{\partial y} = 0$ (معادلة دالة الانسياب $\psi$) |
| $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$ | **معادلات لاجرانج المساعدة:** معادلات المسار الذي يسلكه الجسيم خطوة بخطوة | $\frac{dx}{-\phi_x} = \frac{dy}{-\phi_y}$ (السير مع أشد انحدار) |
| $u(x,y,z) = a, \quad v(x,y,z) = b$ | ثابتان يبقيان محفوظين طوال حركة المركبة على نفس المسار | منحنى مسار المركبة `path = [(x, y), ...]` |
| $\Phi(u, v) = 0$ | **الحل العام:** يجمع كل المسارات الممكنة بدالة اختيارية $\Phi$ | عائلة خطوط الانسياب الكاملة من البداية للهدف |

---
## 1. الفكرة ببساطة: كيف تتحول معادلة تفاضلية جزئية إلى مسار قيادة؟
بعد أن يحسب حاسوب المركبة حقل الجهد التوافقي $\phi(x, y)$ (حيث البداية عند $\phi=1$ والهدف عند $\phi=0$)، كيف تقود المركبة عجلاتها؟
المركبة تتجه في كل لحظة باتجاه **أشد انحدار للأسفل (Steepest Descent)**:
$$\mathbf{v} = (u, v) = -\nabla\phi = \left(-\frac{\partial\phi}{\partial x},\; -\frac{\partial\phi}{\partial y}\right)$$
إذا أردنا إيجاد **دالة الانسياب $\psi(x, y)$** التي تبقى قيمتها ثابتة على طول مسار المركبة ($d\psi = 0$ على المسار)، فإن $\psi$ تحقق معادلة لاجرانج الخطية من الرتبة الأولى:
$$u \frac{\partial\psi}{\partial x} + v \frac{\partial\psi}{\partial y} = 0 \qquad \text{أي أن:} \qquad P = u,\; Q = v,\; R = 0$$
وعندما نكتب **معادلات لاجرانج المساعدة** لهذه المعادلة نحصل على:
$$\frac{dx}{u} = \frac{dy}{v} = \frac{d\psi}{0} \implies \psi(x,y) = \text{ثابت على طول مسار المركبة!}$$
إذن: **المنحنيات المميزة لطريقة لاجرانج (Characteristic Curves) هي بالضبط المسارات الهندسية التي تسير عليها عجلات المركبة في دالة `descend()`!**
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab2

%matplotlib inline
print("تم تهيئة بيئة اللاب 2 بنجاح!")
""")

    nb.md(r"""---
## 2. قاعدة العمل والاستراتيجيات الثلاث لحل معادلات لاجرانج في المذكرة (PDF ص 12–17)

### 🎯 كيف أميّز معادلة لاجرانج في الامتحان؟ (صفحة 4 و 11 بالمذكرة / PDF ص 5 و 12)
انظر إلى المشتقتين $p$ و $q$: إذا كانتا مرفوعتين **للأس 1 فقط** ولا يوجد ضرب $p \cdot q$، فالمعادلة على الصورة القياسية للاجرانج:
$$P(x, y, z)\,p + Q(x, y, z)\,q = R(x, y, z)$$
وتُحل دائماً بكتابة **معادلات لاجرانج المساعدة (Lagrange's Auxiliary Equations)**:
$$\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$$
ثم نوجد **ثابتين مستقلين** $u(x, y, z) = a$ و $v(x, y, z) = b$، ويكون الحل العام هو:
$$\Phi(u, v) = 0 \qquad (\text{حيث } \Phi \text{ دالة اختيارية})$$

---

### 🧠 الاستراتيجيات الثلاث في المذكرة لإيجاد الثابتين $a$ و $b$ (PDF ص 13–16)
في الامتحان، عند النظر إلى الكسور $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$، ستواجه إحدى **الحالات الثلاث التالية بالضبط** (وقد وردت جميعها في أمثلة المذكرة من Ex.1 إلى Ex.4):

#### 🔹 الاستراتيجية 1: الفصل المباشر بين كسرين (Ex.1 & Ex.2 — ص 12–13 بالمذكرة / PDF ص 13–14)
عندما يحتوي كسران على متغيرين فقط، نضرب طرفين في وسطين ونكامل مباشرة!
* **مثال 1 (PDF ص 13):** حل $2p - 3q = 2x$:
  * المعاملات: $P = 2,\; Q = -3,\; R = 2x \implies \frac{dx}{2} = \frac{dy}{-3} = \frac{dz}{2x}$.
  * **الكسر الأول والثاني:** $\frac{dx}{2} = \frac{dy}{-3} \implies -3\,dx - 2\,dy = 0 \xrightarrow{\int} -3x - 2y = a$.
  * **الكسر الأول والثالث:** $\frac{dx}{2} = \frac{dz}{2x} \implies x\,dx - dz = 0 \xrightarrow{\int} \frac{x^2}{2} - z = b$.
  * **الحل العام:** $\Phi\left(-3x - 2y,\; \frac{x^2}{2} - z\right) = 0$.
* **مثال 2 (PDF ص 13–14):** حل $\left(\frac{y^2 z}{x}\right)p + xzq = y^2$:
  * المعادلات المساعدة: $\frac{dx}{y^2 z / x} = \frac{dy}{xz} = \frac{dz}{y^2}$.
  * **الكسر الأول والثاني:** نختصر $z$ من المقامين ونضرب طرفين في وسطين: $x^2\,dx - y^2\,dy = 0 \implies x^3 - y^3 = a_1$.
  * **الكسر الأول والثالث:** نختصر $y^2$ من المقامين: $x\,dx - z\,dz = 0 \implies x^2 - z^2 = b_1$.
  * **الحل العام:** $\Phi(x^3 - y^3,\; x^2 - z^2) = 0$.

---

#### 🔹 الاستراتيجية 2: استخدام الثابت الأول $a$ بالتعويض لحل الكسر التالي ثم إرجاعه! (Ex.3 — ص 13–14 بالمذكرة / PDF ص 14–15)
ماذا لو كان الكسر الأخير يحتوي على متغيرات إضافية تمنع فصل المتغيرات مباشرة؟ **نستخدم الثوابت التي أوجدناها للتو لتبديل المتغيرات، وبعد التكامل نُرجع الثوابت إلى قيمها الأصلية!**
* **مثال 3 (PDF ص 14–15):** حل $x\frac{\partial z}{\partial x} + y\frac{\partial z}{\partial y} + t\frac{\partial z}{\partial t} = xyt$:
  * المعادلات المساعدة: $\frac{dx}{x} = \frac{dy}{y} = \frac{dt}{t} = \frac{dz}{xyt}$.
  * **الكسر 1 و 2:** $\frac{dx}{x} = \frac{dy}{y} \implies \ln x - \ln y = \ln a \implies \frac{x}{y} = a$.
  * **الكسر 2 و 3:** $\frac{dy}{y} = \frac{dt}{t} \implies \ln y - \ln t = \ln b \implies \frac{y}{t} = b$.
  * **الكسر 2 و 4:** $\frac{dy}{y} = \frac{dz}{xyt} \implies xt\,dy - dz = 0$. *(لا يمكن تكاملها مباشرة لوجود $x$ و $t$ مع $dy$!)*
  * **الحيلة:** من الثابتين السابقين لدينا $x = a y$ و $t = \frac{y}{b} \implies xt = \frac{a}{b}y^2$. نعوض بها في المعادلة:
    $$\frac{a}{b}y^2\,dy - dz = 0 \xrightarrow{\text{نكامل الآن بسهولة!}} \frac{a}{3b}y^3 - z = c$$
  * **خطوة لا تنسها أبداً:** قبل كتابة الحل العام، أرجع $a = \frac{x}{y}$ و $b = \frac{y}{t}$:
    $$\frac{(x/y)}{3(y/t)}y^3 - z = c \implies \frac{1}{3}xyt - z = c \implies \Phi\left(\frac{x}{y},\; \frac{y}{t},\; \frac{1}{3}xyt - z\right) = 0$$

---

#### 🔹 الاستراتيجية 3: قاعدة تساوي الكسور / المضروبات (القاعدة المؤطرة في ص 14 و Ex.4 ص 15 / PDF ص 15–16)
> 📌 **القاعدة الذهبية في المذكرة (PDF ص 15):**
> *"لأي كسور متساوية، **إذا كان مجموع المقامات يساوي صفراً، فإن مجموع البسوط يساوي صفراً أيضاً!**"*
> وبصورة أعم، إذا ضربنا البسوط والمقامات في معاملات (مضروبات) $(l, m, n)$ بحيث يصبح مجموع المقامات الجديد $lP + mQ + nR = 0$، فإن البسط الجديد يساوي صفراً أيضاً:
> $$l\,dx + m\,dy + n\,dz = 0$$

* **مثال 4 (PDF ص 16 — سؤال امتحانات كلاسيكي هام جداً!):** حل المعادلة:
  $$(y - z)p + (z - x)q = x - y$$
  * **الخطوة 1:** المعادلات المساعدة هي:
    $$\frac{dx}{y - z} = \frac{dy}{z - x} = \frac{dz}{x - y}$$
    *(لاحظ أن كل مقام يحتوي على متغيرين مختلطين، فلا يمكن فصل أي كسرين مباشرة!)*
  * **الخطوة 2 (إيجاد الثابت الأول بجمع المقامات مباشرة):**
    اجمع المقامات الثلاثة: $(y - z) + (z - x) + (x - y) = 0$!
    بما أن مجموع المقامات $= 0$، إذن مجموع البسوط $= 0$:
    $$dx + dy + dz = 0 \xrightarrow{\text{بتكامل الطرفين}} x + y + z = a$$
  * **الخطوة 3 (إيجاد الثابت الثاني بضرب الكسور في $x, y, z$ على الترتيب):**
    اضرب الكسر الأول في $x$ والثاني في $y$ والثالث في $z$ واجمع المقامات:
    $$x(y - z) + y(z - x) + z(x - y) = xy - xz + yz - xy + xz - yz = 0$$
    مجموع المقامات الجديد $= 0$، إذن مجموع البسوط الجديد $= 0$:
    $$x\,dx + y\,dy + z\,dz = 0 \xrightarrow{\text{بتكامل الطرفين}} \frac{x^2}{2} + \frac{y^2}{2} + \frac{z^2}{2} = b$$
  * **الخطوة 4 (الحل العام):**
    $$\Phi\left(x + y + z,\; \frac{x^2}{2} + \frac{y^2}{2} + \frac{z^2}{2}\right) = 0$$
""")

    nb.md(r"""---
## 3. ✍️ تحدي الورقة والقلم 1 (التمرين 5 — صفحة 16 بالمذكرة / PDF ص 17)

**المسألة (معادلة أويلر):** أوجد الثابتين المستقلين $u(x,y)$ و $v(y,z)$ للمعادلة:
$$x p + y q = z$$

<details>
<summary>💡 <b>تلميح 1:</b> اكتب المعادلات المساعدة</summary>

هنا $P = x, \; Q = y, \; R = z$، إذن:
$$\frac{dx}{x} = \frac{dy}{y} = \frac{dz}{z}$$
</details>

<details>
<summary>💡 <b>تلميح 2:</b> كامل الكسر الأول مع الثاني، ثم الثاني مع الثالث</summary>

$$\int \frac{dx}{x} = \int \frac{dy}{y} \implies \ln|x| - \ln|y| = \ln|a| \implies \ln\left|\frac{x}{y}\right| = \ln|a|$$
وبالمثل للكسر الثاني والثالث مع $y$ و $z$.
</details>

أدخل صيغتي $u$ و $v$ في الخلية التالية:
""")

    if solutions:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ###
student_u = "x/y"
student_v = "y/z"
### END CODE HERE ###

test_lab2.check_paper_challenge_1(student_u, student_v)
""")
    else:
        nb.code(r"""# خلية تقييم: تحدي الورقة 1
### START CODE HERE ### (≈ 2 lines of code)
# اكتب الثابتين المستقلين u و v المستنتجين من التكامل (مثال: "x/y" و "y/z"):
student_u = None
student_v = None
### END CODE HERE ###

test_lab2.check_paper_challenge_1(student_u, student_v)
""")

    nb.md(r"""---
## 4. 🚀 تحدي الربط بالمشروع: استنتاج معادلة خط انسياب المركبة

لنفترض أن حقل الجهد بالقرب من الهدف يعطى بالدالة:
$$\phi(x, y) = x^2 + 2y^2$$
مركبة المريخ تتحرك باتجاه أشد انحدار للأسفل بسرعة:
$$u = -\frac{\partial\phi}{\partial x} = -2x, \qquad v = -\frac{\partial\phi}{\partial y} = -4y$$
إذن **دالة الانسياب $\psi(x, y)$** التي تبقى ثابتة على مسار المركبة تحقق معادلة لاجرانج:
$$-2x \frac{\partial\psi}{\partial x} - 4y \frac{\partial\psi}{\partial y} = 0$$

**المطلوب على ورقتك:**
استخدم معادلة لاجرانج المساعدة $\frac{dx}{-2x} = \frac{dy}{-4y}$ لإيجاد معادلة منحنى مسار المركبة $y$ بدلالة $x$ والثابت $k$.

<details>
<summary>💡 <b>تلميح 1:</b> بسّط المقامات وفصل المتغيرات</summary>

بقسمة المقامين على $-2$ نحصل على:
$$\frac{dx}{x} = \frac{dy}{2y} \implies 2\frac{dx}{x} = \frac{dy}{y}$$
</details>

<details>
<summary>💡 <b>تلميح 2:</b> كامل الطرفين وخذ الدالة الأسية</summary>

$$2\ln|x| + \ln|k| = \ln|y| \implies \ln(k x^2) = \ln|y| \implies y = k x^2$$
</details>
""")

    if solutions:
        nb.code(r"""# خلية تقييم: معادلة مسار المركبة
### START CODE HERE ###
rover_streamline = "y = k*x^2"
### END CODE HERE ###

test_lab2.check_paper_challenge_2(rover_streamline)
""")
    else:
        nb.code(r"""# خلية تقييم: معادلة مسار المركبة
### START CODE HERE ### (≈ 1 line of code)
# اكتب معادلة مسار الانسياب بدلالة x و y و k (مثال: "y = k*x^2"):
rover_streamline = None
### END CODE HERE ###

test_lab2.check_paper_challenge_2(rover_streamline)
""")

    nb.md(r"""---
## 5. 💻 من الورقة إلى الكود: متتبع خطوط الانسياب العددي

على تضاريس المريخ الحقيقية لا نملك صيغة جبرية بسيطة لـ $\phi(x,y)$، بل لدينا شبكة أرقام. لذلك يتتبع الحاسوب معادلة لاجرانج المساعدة:
$$\frac{dx}{dt} = u(x,y), \qquad \frac{dy}{dt} = v(x,y)$$
بأخذ خطوات زمنية صغيرة $\Delta t$ (طريقة أويلر الأمامية أو طريقة رونج-كوتا):
$$(x_{\text{new}}, y_{\text{new}}) = (x, y) + \Delta t \cdot (u, v)$$
وهي الفكرة ذاتها التي تنفذها دالة `descend()` على الخلايا الثماني المجاورة في `planners.py`!

أكمل الدالة أدناه لتتبع مسار المركبة عددياً ومقارنته بحلك الورقي $y = 2x^2$ (عند الانطلاق من النقطة $(1, 2)$ حيث $k = y_0/x_0^2 = 2$):
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: trace_streamline_rk4
def trace_streamline_rk4(velocity_fn, start=(1.0, 2.0), dt=0.01, steps=50):
    """تتبع خط الانسياب (المنحنى المميز للاجرانج) عددياً بخطوة dt."""
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

test_lab2.test_rk4_streamline_tracer(trace_streamline_rk4)
''')
    else:
        nb.code(r'''# دالة تقييم برمجية: trace_streamline_rk4
def trace_streamline_rk4(velocity_fn, start=(1.0, 2.0), dt=0.01, steps=50):
    """تتبع خط الانسياب (المنحنى المميز للاجرانج) عددياً بخطوة dt."""
    trajectory = [start]
    curr = np.array(start, dtype=float)
    
    ### START CODE HERE ### (≈ 4-5 lines of code)
    # كرر بعدد steps:
    # 1. احسب مركبتي السرعة: vx, vy = velocity_fn(curr[0], curr[1])
    # 2. حدث الموقع: curr = curr + dt * np.array([vx, vy], dtype=float)
    # 3. أضف الموقع الجديد: trajectory.append(tuple(curr))
    pass
    ### END CODE HERE ###
    
    return np.array(trajectory)

test_lab2.test_rk4_streamline_tracer(trace_streamline_rk4)
''')

    nb.md(r"""---
## 6. 🛰️ الرؤية البصرية: تطابق حل لاجرانج الورقي مع المتتبع العددي

شغّل الخلية التالية لترى كيف ينطبق المسار العددي (الخط الأحمر) تماماً فوق المنحنى التحليلي $y = 2x^2$ (الخط المتقطع الأزرق) الذي استنتجته بطريقة لاجرانج على الورق، وكيف يتعامد دائماً مع خطوط تساوي الجهد $\phi = \text{const}$:
""")

    nb.code(r"""def sample_velocity(x, y):
    return -2.0 * x, -4.0 * y

traj = trace_streamline_rk4(sample_velocity, start=(1.0, 2.0), dt=0.01, steps=120)

x_vals = np.linspace(-2, 2, 25)
y_vals = np.linspace(-0.5, 2.5, 25)
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

print("📌 ملخص اللاب 2:")
print("  1) المعادلة شبه الخطية P*p + Q*q = R تُحل بمعادلات لاجرانج المساعدة dx/P = dy/Q = dz/R.")
print("  2) المنحنيات المميزة للاجرانج هي نفسها خطوط انسياب حركة المركبة في حقل الجهد.")
print("  3) دالة descend() في planners.py هي التطبيق الشبكي المباشر لتتبع هذه الخطوط من البداية إلى الهدف.")
""")

    nb.save()


# ===========================================================================
# LAB 3 (ARABIC): NON-LINEAR PDES & CHARPIT'S METHOD
# ===========================================================================
def build_lab_3_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_3_Nonlinear_Charpit_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📡 اللاب 3: المعادلات غير الخطية من الرتبة الأولى، طريقة شاربيت، وهوامش أمان العوائق
### *غرفة التحكم: هامش الأمان الإقليدي حول الصخور ومعادلة المسافة (Eikonal)*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**المرجع في المذكرة:** الباب الأول، الأقسام 1.3.2–1.3.6 — **ترقيم المذكرة ص 16–26** *(صفحات ملف الـ PDF من 17 إلى 27)*

---
### 🗺️ موقعك في سلسلة بناء محرك الملاحة (Rover Pipeline)
```
[اللاب 1: حساب الميول] ──► [اللاب 2: خطوط الانسياب] ──► 📍 [اللاب 3: معادلة المسافة وهوامش الأمان] ──► [اللاب 4–5: نظرية لابلاس] ──► [اللاب 6: محرك الملاحة الكامل]
```

---
### 🧭 حجر رشيد (The Rosetta Stone): الربط بين السبورة ومحرك المركبة

| 1. رمز المذكرة (PDF pp. 17–27) | 2. المعنى الهندسي والفيزيائي | 3. الدالة الفعلية في المشروع (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $f(x, y, z, p, q) = 0$ غير خطية | معادلة تفاضلية تحتوي على $p^2, q^2$ أو $pq$ | حساب المسافات الإقليدية وجبهات الموجات |
| $p^2 + q^2 = 1$ (أو $\|\nabla z\| = 1$) | **معادلة المسافة (Eikonal):** دالة تزداد بمعدل 1 لكل متر نبتعد فيه عن المصدر | [`terrain.dilate(raw, rover_radius)`](rover_path_finder/terrain.py) (توسيع العوائق بنصف قطر المركبة) |
| $z = px + qy + f(p, q)$ | **صيغة كليروت (Clairaut Form):** عائلة مستويات مماسة؛ حلها التام $z = ax + by + f(a,b)$ | تمثيل جبهات الموجات المستوية وزوايا المسح |
| $(x - x_0)^2 + (y - y_0)^2 \le R^2$ | قرص الأمان الدائري حول كل صخرة أو حفرة لحماية هيكل المركبة | `yy**2 + xx**2 <= radius**2` في `terrain.dilate` |

---
## 1. الفكرة ببساطة: كيف تحسب المركبة المسافة الآمنة حول الصخور؟

المركبة الفضائية ليست نقطة هندسية بلا أبعاد، بل لها عرض فعلي (`rover_radius`). إذا خططنا مساراً يمر بمحاذاة حافة حفرة مباشرة، فستسقط عجلات المركبة في الحفرة!

لذلك، قبل حساب حقل الجهد في [`terrain.py`](rover_path_finder/terrain.py)، تقوم الدالة `dilate(raw, radius)` بحساب **خريطة المسافة الإقليدية** حول كل عائق لتوسيعه بمقدار نصف قطر المركبة:
* إذا سمينا المسافة الإقليدية من نقطة الأصل $z(x,y) = \sqrt{x^2 + y^2}$، فإن ميل هذه الدالة في اتجاه $x$ و $y$ هو:
  $$p = \frac{\partial z}{\partial x} = \frac{x}{\sqrt{x^2+y^2}}, \qquad q = \frac{\partial z}{\partial y} = \frac{y}{\sqrt{x^2+y^2}}$$
* بتربيع الطرفين وجمعهما نحصل على أشهر معادلة تفاضلية جزئية غير خطية من الرتبة الأولى (**معادلة Eikonal**):
  $$p^2 + q^2 = 1 \quad \Longleftrightarrow \quad \|\nabla z\| = 1$$

هذه المعادلة **غير خطية** لأن المشتقتين $p$ و $q$ مرفوعتان للأس 2، فلا يمكن حلها بطريقة لاجرانج التي درسناها في اللاب 2! في هذا اللاب سنتعلم كيف نحل المعادلات غير الخطية من الرتبة الأولى باستخدام **الأشكال القياسية الأربعة** و**طريقة شاربيت العامة (Charpit's Method)**.
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab3

%matplotlib inline
print("تم تهيئة بيئة اللاب 3 بنجاح!")
""")

    nb.md(r"""---
## 2. الشرح الكامل للأشكال القياسية الأربعة وطريقة شاربيت العامة (PDF ص 17–27)

عندما تواجه معادلة غير خطية من الرتبة الأولى $f(x, y, z, p, q) = 0$، هدفنا هو إيجاد **التكامل التام (Complete Integral)**، وهو حل يحتوي على **ثابتين اختياريين** $(a, b)$ (أو $a, c$) بعدد المتغيرات المستقلة $(x, y)$.

### 🧭 خريطة القرار السريع: كيف تختار طريقة الحل في 5 ثوانٍ؟

| الشكل القياسي في المذكرة | كيف تميزه بمجرد النظر؟ | خطوات الحل القياسية |
| :--- | :--- | :--- |
| **Form 1 (القسم 1.3.2)** *(PDF ص 17–19)* | $f(p, q) = 0$ (تحتوي على $p, q$ فقط، بلا $x, y, z$) | نضع $p = a, q = b$، ونوجد $b = F_1(a)$ من المعادلة، ونعوض في $z = ax + F_1(a)y + c$ |
| **Form 2 (Clairaut — القسم 1.3.3)** *(PDF ص 19–20)* | $z = px + qy + f(p, q)$ | نضع مباشرةً $p = a$ و $q = b$ فيكون الحل التام: $z = ax + by + f(a, b)$ |
| **Form 3 (القسم 1.3.4)** *(PDF ص 21–23)* | $f(z, p, q) = 0$ (تحتوي على $z, p, q$ فقط، بلا $x, y$) | نفرض $u = x + ay$ ونستبدل $p = \frac{dz}{du}$ و $q = a\frac{dz}{du}$ ونحل المعادلة التفاضلية العادية |
| **Form 4 (Separable — القسم 1.3.5)** *(PDF ص 23–25)* | $f_1(x, p) = f_2(y, q)$ (لا يوجد $z$، ويمكن فصل $x,p$ عن $y,q$) | نساوي الطرفين بثابت $a$: $f_1(x,p)=a, f_2(y,q)=a$، نوجد $p(x), q(y)$ ونكامل $dz = p\,dx + q\,dy$ |
| **طريقة شاربيت العامة (القسم 1.3.6)** *(PDF ص 25–27)* | $f(x, y, z, p, q) = 0$ (جميع المتغيرات مختلطة ولا تنطبق الأشكال 1–4) | نكتب كسور شاربيت الخمسة، نوجد علاقة ثانية بين $p, q$ بثابت $a$، ثم نكامل $dz = p\,dx + q\,dy$ |

---

### 📖 تفصيل الأشكال الأربعة مع أمثلة المذكرة المحلولة خطوة بخطوة:

#### 1️⃣ الشكل الأول $f(p, q) = 0$ (القسم 1.3.2 — ص 16–18 بالمذكرة / PDF ص 17–19):
* **لماذا ينجح؟** إذا كان $p = a$ و $q = b$ ثابتين، فإن التفاضل الكلي $dz = p\,dx + q\,dy = a\,dx + b\,dy$ يعطي بالتكامل $z = ax + by + c$. وبما أن $F(a, b) = 0$، نحسب $b$ بدلالة $a$ ليبقى ثابتان مستقلان فقط $(a, c)$!
* **مثال 1 (PDF ص 18):** حل $p^2 + p = q^2$:
  * نضع $p = a, q = b \implies a^2 + a = b^2 \implies b = \pm\sqrt{a^2 + a}$.
  * إذن التكامل التام هو: $z = ax \pm \sqrt{a^2 + a}\,y + c$.
* **مثال 2 (PDF ص 18–19):** حل $pq = k$ (حيث $k$ ثابت معطى):
  * نضع $p = a, q = b \implies ab = k \implies b = \frac{k}{a}$.
  * إذن التكامل التام هو: $z = ax + \frac{k}{a}y + c$.

---

#### 2️⃣ الشكل الثاني: معادلة كليروت $z = px + qy + f(p, q)$ (القسم 1.3.3 — ص 18–19 بالمذكرة / PDF ص 19–20):
* **قاعدة الحل:** ضع $p = a$ و $q = b$ مباشرةً في المعادلة! **(تنبيه: لا تضف ثابتاً ثالثاً $+c$ لأن $a$ و $b$ مستقلان عن بعضهما هنا!)**
* **مثال 2 (PDF ص 20 — انتبه لخدعة إعادة الترتيب!):** حل $x\frac{\partial z}{\partial x} + y\frac{\partial z}{\partial y} = z - 5\frac{\partial z}{\partial x} + \frac{\partial z}{\partial x}\frac{\partial z}{\partial y}$:
  * نكتبها برموز مونج: $xp + yq = z - 5p + pq$.
  * **نفصل $z$ في طرف بمفرده:** $z = xp + yq + 5p - pq$ (الآن أصبحت على صيغة كليروت تماماً حيث $f(p,q) = 5p - pq$!).
  * نضع $p = a, q = b$ فنحصل على التكامل التام: $\boxed{z = ax + by + 5a - ab}$.

---

#### 3️⃣ الشكل الثالث $f(z, p, q) = 0$ (القسم 1.3.4 — ص 20–22 بالمذكرة / PDF ص 21–23):
عندما تغيب $x$ و $y$ صراحةً عن المعادلة وتظهر $z, p, q$ فقط، نتبع **الخطوات الأربع في المذكرة (PDF ص 21)**:
1. نفرض المتغير المجمع $u = x + ay$ (حيث $a$ ثابت اختياري).
2. باستخدام قاعدة السلسلة ($\frac{\partial u}{\partial x} = 1$ و $\frac{\partial u}{\partial y} = a$) نستبدل:
   $$p = \frac{dz}{du}, \qquad q = a\frac{dz}{du}$$
3. نعوض في المعادلة الأصلية فتتحول إلى معادلة تفاضلية عادية (ODE) من الرتبة الأولى في $z$ و $u$، فنفصل المتغيرات ونكاملها (مع إضافة ثابت التكامل $c$).
4. نعيد استبدال $u$ بـ $x + ay$.
* **مثال 1 (PDF ص 21–22):** حل $z = p + q$:
  * نضع $u = x + ay$ ونعوض عن $p = \frac{dz}{du}$ و $q = a\frac{dz}{du}$:
    $$z = \frac{dz}{du} + a\frac{dz}{du} = (1 + a)\frac{dz}{du} \implies du = (1 + a)\frac{dz}{z}$$
  * بالتكامل: $u + c = (1 + a)\ln z \implies x + ay + c = \ln\left(z^{1+a}\right) \implies \boxed{z = e^{\frac{x + ay + c}{1 + a}}}$.
* **مثال 2 (PDF ص 22–23):** حل $p^2 z - q^2 = 1$:
  * نعوض بـ $p = \frac{dz}{du}, q = a\frac{dz}{du}$:
    $$\left(\frac{dz}{du}\right)^2 z - a^2\left(\frac{dz}{du}\right)^2 = 1 \implies (z - a^2)\left(\frac{dz}{du}\right)^2 = 1 \implies \pm\sqrt{z - a^2}\,dz = du$$
  * بالتكامل والتعويض عن $u = x + ay$: $\boxed{\pm\frac{2}{3}(z - a^2)^{3/2} = x + ay + c}$.

---

#### 4️⃣ الشكل الرابع القابل للفصل $f_1(x, p) = f_2(y, q)$ (القسم 1.3.5 — ص 22–24 بالمذكرة / PDF ص 23–25):
عندما لا يظهر $z$ في المعادلة، ونستطيع عزل كل ما يخص $(x, p)$ في طرف وكل ما يخص $(y, q)$ في الطرف الآخر:
1. نساوي الطرفين بثابت اختياري $a$: $f_1(x, p) = f_2(y, q) = a$.
2. نحل المعادلة الأولى لإيجاد $p = g_1(x, a)$، ونحل الثانية لإيجاد $q = g_2(y, a)$.
3. نعوض في التفاضل الكلي $dz = p\,dx + q\,dy$ ونكامل الطرفين:
   $$\boxed{z = \int g_1(x, a)\,dx + \int g_2(y, a)\,dy + b}$$
* **مثال 1 (PDF ص 23–24):** حل $p = 2xq^2$:
  * بقسمة الطرفين على $x$ نفصل المتغيرات: $\frac{p}{x} = 2q^2 = a$.
  * إذن: $\frac{p}{x} = a \implies p = ax$، و $2q^2 = a \implies q = \pm\sqrt{\frac{a}{2}}$.
  * نعوض في $dz = p\,dx + q\,dy = ax\,dx \pm \sqrt{\frac{a}{2}}\,dy \xrightarrow{\int} \boxed{z = \frac{a}{2}x^2 \pm \sqrt{\frac{a}{2}}\,y + b}$.

---

### 🏛️ خامساً: طريقة شاربيت العامة (Charpit's Method — القسم 1.3.6، ص 24–26 / PDF ص 25–27)

عندما تحتوي المعادلة $f(x, y, z, p, q) = 0$ على $z$ مع $x, y$ ولا تنطبق عليها الأشكال الأربعة السابقة، نستخدم **معادلات شاربيت المساعدة (PDF ص 25)**:
$$\frac{dp}{f_x + p f_z} = \frac{dq}{f_y + q f_z} = \frac{dz}{-p f_p - q f_q} = \frac{dx}{-f_p} = \frac{dy}{-f_q}$$

#### 📖 المثال المحلول الكامل بطريقة شاربيت (Example 2 — ص 25–26 بالمذكرة / PDF ص 26–27):
**المسألة:** حل المعادلة التفاضلية الجزئية غير الخطية بطريقة شاربيت:
$$2zx - px^2 - 2qxy + pq = 0$$

* **الخطوة 1:** نصفر الطرف الأيمن ونعرف الدالة:
  $$f(x, y, z, p, q) = 2zx - px^2 - 2qxy + pq = 0 \qquad \cdots (5)$$
* **الخطوة 2:** نحسب المشتقات الجزئية الخمس للدالة $f$:
  $$f_x = 2z - 2px - 2qy, \qquad f_y = -2qx, \qquad f_z = 2x, \qquad f_p = -x^2 + q, \qquad f_q = -2xy + p$$
  > ⚠️ **تنبيه خطأ مطبعي في مذكرة الكلية (PDF صفحة 27، السطر الأول):**
  > في أعلى صفحة 27 من ملف الـ PDF، التصقت معادلتا $f_z$ و $f_p$ ببعضهما بدون فاصلة فظهرتا هكذا: `$f_z = 2x f_p = -x^2 + q$`! والصواب أنهما مشتقتان منفصلتان: $f_z = 2x$ ، و $f_p = -x^2 + q$.

* **الخطوة 3:** نعوض في معادلات شاربيت المساعدة:
  $$\frac{dp}{(2z - 2px - 2qy) + p(2x)} = \frac{dq}{-2qx + q(2x)} = \frac{dz}{-p(-x^2+q) - q(-2xy+p)} = \frac{dx}{x^2 - q} = \frac{dy}{2xy - p}$$
* **الخطوة 4 (اختيار أسهل كسر):** انظر إلى مقام الكسر الثاني تحت $dq$:
  $$f_y + q f_z = -2qx + 2qx = 0 \implies \frac{dq}{0} \implies dq = 0 \implies \boxed{q = c} \quad (\text{حيث } c \text{ ثابت اختياري!})$$
* **الخطوة 5 (إيجاد $p$ بالتعويض عن $q = c$ في المعادلة الأصلية 5):**
  $$2zx - px^2 - 2cxy + cp = 0 \implies p(x^2 - c) = 2x(z - cy) \implies \boxed{p = \frac{2x(z - cy)}{x^2 - c}}$$
* **الخطوة 6 (التعويض في التفاضل الكلي $dz = p\,dx + q\,dy$ والتكامل):**
  $$dz = \frac{2x(z - cy)}{x^2 - c}dx + c\,dy \implies dz - c\,dy = \frac{2x(z - cy)}{x^2 - c}dx$$
  لاحظ أن البسط على اليسار $dz - c\,dy$ هو تفاضل المقدار $(z - cy)$ لأن $c$ ثابت! نفصل المتغيرات:
  $$\frac{d(z - cy)}{z - cy} = \frac{2x\,dx}{x^2 - c} \xrightarrow{\text{بتكامل الطرفين}} \ln|z - cy| = \ln|x^2 - c| + \ln b$$
  $$z - cy = b(x^2 - c) \implies \boxed{z = b(x^2 - c) + cy}$$
  وهو التكامل التام المحتوي على الثابتين الاختياريين $b$ و $c$!
""")

    nb.md(r"""---
## 3. 📝 تحدي الورقة والقلم 1 (صيغة كليروت — المثال 1 ص 19 / PDF ص 20)

**المسألة:** أوجد التكامل التام لمعادلة كليروت التالية:
$$z = p x + q y + p q$$

**خطوات الحل على ورقتك:**
1. تحقق أن المعادلة على صيغة كليروت $z = px + qy + f(p, q)$ حيث $f(p, q) = pq$.
2. عوض عن الميلين بالثابتين الاختياريين $p = a$ و $q = b$.

<details>
<summary>💡 <b>تلميح (اضغط هنا إذا احتجت مساعدة)</b></summary>

استبدل كل $p$ بـ $a$ وكل $q$ بـ $b$ في المعادلة $z = px + qy + pq$. لا تضف أي ثوابت إضافية لأن $(a, b)$ هما الثابتان الاختياريان بالفعل.
</details>
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
# اكتب معادلة التكامل التام بدلالة x, y, a, b:
student_clairaut = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_1(student_clairaut)
""")

    nb.md(r"""---
## 4. 🚀 تحدي جسر مركبة المريخ (من المستويات إلى مخروط المسافة الإقليدية)

نريد الآن حل معادلة المسافة (Eikonal Equation) التي يعتمد عليها رادار المركبة وتوسيع العوائق:
$$p^2 + q^2 = 1$$

**كيف يرتبط التكامل التام (Form 1) بمخروط المسافة الدائري حول الصخرة؟**
1. المعادلة من **الشكل الأول (Form 1: $f(p,q)=0$)** لأنها تحتوي على $p$ و $q$ فقط.
2. إذا وضعنا $p = \cos\alpha$، فإن $q = \sin\alpha$ (لأن $\cos^2\alpha + \sin^2\alpha = 1$).
3. إذن عائلة المستويات المارة بنقطة الأصل هي:
   $$z = x\cos\alpha + y\sin\alpha$$
   كل قيمة للزاوية $\alpha$ تمثل موجة مستوية تسير في اتجاه الزاوية $\alpha$.
4. لإيجاد **الغلاف الهندسي (Envelope)** لجميع الاتجاهات الممكنة $\alpha \in [0, 2\pi)$، نشتق بالنسبة للبارامتر $\alpha$ ونساوي المشتقة بالصفر:
   $$\frac{\partial z}{\partial \alpha} = -x\sin\alpha + y\cos\alpha = 0$$
5. بتربيع المعادلتين وجمعهما للتخلص من $\alpha$:
   $$z^2 + 0^2 = (x\cos\alpha + y\sin\alpha)^2 + (-x\sin\alpha + y\cos\alpha)^2 = x^2(\cos^2\alpha + \sin^2\alpha) + y^2(\sin^2\alpha + \cos^2\alpha)$$

أكمل تبسيط الطرف الأيمن واكتب معادلة سطح المسافة الناتج بدلالة $x, y, z$:

<details>
<summary>💡 <b>تلميح 1 (المتطابقة المثلثية)</b></summary>

بما أن $\cos^2\alpha + \sin^2\alpha = 1$، يتبسط الطرف الأيمن إلى مجموع مربعي الإحداثيين $x$ و $y$.
</details>

<details>
<summary>💡 <b>تلميح 2 (الصيغة النهائية)</b></summary>

المعادلة تربط بين $x^2 + y^2$ و $z^2$، وتمثل مخروط المسافة الذي مقطعه الأفقي عند أي مسافة $z = R$ هو دائرة نصف قطرها $R$.
</details>
""")

    if solutions:
        nb.code(r"""# خلية تقييم: مخروط المسافة الإقليدية
### START CODE HERE ###
student_envelope = "x^2 + y^2 = z^2"
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_2(student_envelope)
""")
    else:
        nb.code(r"""# خلية تقييم: مخروط المسافة الإقليدية
### START CODE HERE ### (≈ 1 line of code)
# اكتب معادلة مخروط المسافة بدلالة x, y, z:
student_envelope = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab3.check_paper_challenge_2(student_envelope)
""")

    nb.md(r"""---
## 5. 💻 التطبيق البرمجي ببايثون: بناء خريطة المسافات وتوسيع العوائق (`terrain.dilate`)

من المعادلة $x^2 + y^2 = z^2$ (أو بالنسبة لمصدر عند $(y_0, x_0)$: $(x - x_0)^2 + (y - y_0)^2 = T^2$)، نحصل على دالة المسافة الإقليدية:
$$T(x, y) = \sqrt{(x - x_0)^2 + (y - y_0)^2}$$

في بايثون، الدالة `np.hypot(dx, dy)` تحسب الجذر التربيعي $\sqrt{\Delta x^2 + \Delta y^2}$ بدقة عددية عالية، وهي نفس القاعدة الهندسية التي تستخدمها دالة [`terrain.dilate(raw, radius)`](rover_path_finder/terrain.py) لإنشاء قرص الأمان الدائري حول كل صخرة!

أكمل الدالة `compute_eikonal_wavefront` أدناه:
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: compute_eikonal_wavefront
def compute_eikonal_wavefront(grid_size=(50, 50), source=(25, 25)):
    # تحسب خريطة المسافة الإقليدية T(x, y) التي تحقق معادلة Eikonal: p^2 + q^2 = 1
    # ملاحظة: source = (row_y, col_x)
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
    # تحسب خريطة المسافة الإقليدية T(x, y) التي تحقق معادلة Eikonal: p^2 + q^2 = 1
    # ملاحظة: source = (row_y, col_x)
    Ny, Nx = grid_size
    Y, X = np.ogrid[:Ny, :Nx]
    
    ### START CODE HERE ### (≈ 1 line of code)
    # احسب المسافة الإقليدية من المصدر (source[1], source[0]) لكل نقطة (X, Y) باستخدام np.hypot:
    dist = None
    ### END CODE HERE ###
    
    return dist

# تشغيل الاختبار الآلي:
test_lab3.test_eikonal_wavefront_distance(compute_eikonal_wavefront)
''')

    nb.md(r"""---
## 6. 🎨 الرؤية البصرية والربط المباشر بملف `rover_path_finder/terrain.py`
شغّل الخلية التالية لرؤية:
1. **على اليسار:** خريطة المسافة الإقليدية $T(x, y)$ التي تحقق $\|\nabla T\|^2 = p^2 + q^2 = 1$.
2. **على اليمين:** التطبيق الفعلي في المشروع عبر استدعاء دالة `terrain.dilate()` من [`rover_path_finder/terrain.py`](rover_path_finder/terrain.py) لإضافة هامش أمان دائري حول الحفر والصخور قبل تخطيط مسار المركبة!
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

# عرض العوائق الأصلية (بالأحمر الداكن) وهامش الأمان الإقليدي المضاف (بالبرتقالي)
safety_margin_only = buffered_hazard & (~raw_hazard)
overlay = np.zeros((100, 100, 3))
overlay[ ~buffered_hazard ] = [0.95, 0.95, 0.95]   # أرض آمنة
overlay[ safety_margin_only ] = [1.0, 0.65, 0.1]   # هامش الأمان الدائري (r <= 3)
overlay[ raw_hazard ] = [0.75, 0.1, 0.1]           # الصخور والحفر الأصلية

axes[1].imshow(overlay, origin='upper')
axes[1].set_title("2. Real Engine: terrain.dilate(raw, rover_radius=3)", fontsize=12)
axes[1].set_xlabel("x (pixels)")
axes[1].set_ylabel("y (pixels)")

plt.tight_layout()
plt.show()

print("📌 ملخص اللاب 3:")
print("  1) المعادلات غير الخطية من الرتبة الأولى تُحل بالأشكال القياسية الأربعة أو بطريقة شاربيت العامة.")
print("  2) معادلة المسافة p^2 + q^2 = 1 تنتج مخروط المسافة الدائري x^2 + y^2 = z^2.")
print("  3) دالة terrain.dilate() في المشروع تستخدم هذه المسافة الإقليدية لتوسيع العوائق بنصف قطر المركبة.")
""")

    nb.save()


# ===========================================================================
# LAB 4 (ARABIC): HIGHER-ORDER HOMOGENEOUS OPERATORS & LAPLACE
# ===========================================================================
def build_lab_4_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_4_HigherOrder_Operators_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📐 اللاب 4: المعادلات الخطية المتجانسة من الرتب العليا وأصل معادلة لابلاس
### *غرفة التحكم: لماذا تمنع معادلة لابلاس $\nabla^2\phi = 0$ وجود أي مصيدة محلية؟*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**المرجع في المذكرة:** الباب الأول، القسم 1.4 — **ترقيم المذكرة ص 34–57** *(صفحات ملف الـ PDF من 28 إلى 51؛ معادلة لابلاس في ص 39 بالترقيم المكتوب / PDF ص 33)*

---
### 🗺️ موقعك في سلسلة بناء محرك الملاحة (Rover Pipeline)
```
[اللاب 1–3: الميول، مسارات الانسياب، وهوامش الأمان] ──► 📍 [اللاب 4: معادلة لابلاس والجهد التوافقي] ──► [اللاب 5: المؤثرات القابلة للتحليل ومشكلة الاضمحلال] ──► [اللاب 6: الحل العددي SOR]
```

---
### 🧭 حجر رشيد (The Rosetta Stone): الربط بين السبورة ومحرك المركبة

| 1. رمز المذكرة (PDF pp. 28–51) | 2. المعنى الهندسي والفيزيائي | 3. الدالة الفعلية في المشروع (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $D_x = \frac{\partial}{\partial x}, \quad D_y = \frac{\partial}{\partial y}$ | مؤثرات التفاضل الجزئي الجبرية | تحويل المعادلة التفاضلية إلى كثيرة حدود جبرية |
| $(D_x^2 + D_y^2)z = 0$ *(مثال 5 ص 39 / PDF ص 33)* | **معادلة لابلاس (Laplace's Equation):** انعدام التقوس الصافي؛ السطح مشدود كغشاء مطاطي | المعادلة الحاكمة لحقل الجهد الملاحي في [`solvers.py`](rover_path_finder/solvers.py) |
| $m^2 + 1 = 0 \implies m = \pm i$ | الجذور المميزة المركبة المترافقة لمعادلة لابلاس | تثبت أن الحل دالة توافقية ناعمة بلا قمم أو حفر داخلية |
| $\nabla^2 \phi \approx \frac{\phi_{E}+\phi_{W}+\phi_{S}+\phi_{N} - 4\phi_{C}}{h^2} = 0$ | قيمة أي نقطة تساوي تماماً متوسط جيرانها الأربعة | الدالة [`_avg(phi)`](rover_path_finder/solvers.py) في `rover_path_finder/solvers.py` |

---
## 1. الفكرة ببساطة: لماذا نحتاج إلى معادلة من الرتبة الثانية (معادلة لابلاس)؟

في اللاب 2 رأينا أن المركبة تتبع منحدر حقل الجهد $\phi(x, y)$ عبر معادلة لاجرانج (`descend`).
ولكن **كيف نصنع حقل الجهد $\phi(x,y)$ نفسه** بحيث يضمن للمركبة عدم الوقوع في أي "حفرة جهد وهمية" (Local Minimum) قبل وصولها للهدف؟

تخيل غشاءً مطاطياً مشدوداً على إطار:
* إذا ثبتنا ارتفاع الغشاء عند جدران الغرفة (أو العوائق) عند $\phi = 1$، وثبتنا نقطة الهدف فقط عند القاع $\phi = 0$:
* فإن الغشاء المطاطي في الفراغ بينهما يحقق معادلة التوازن التام:
  $$\frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} = 0 \quad \Longleftrightarrow \quad (D_x^2 + D_y^2)\phi = 0$$
* هذه هي **معادلة لابلاس (Laplace's Equation)**!
* هندسياً، المشتقة الثانية $\frac{\partial^2 \phi}{\partial x^2}$ تقيس التقوس في اتجاه $x$، و $\frac{\partial^2 \phi}{\partial y^2}$ تقيس التقوس في اتجاه $y$.
* لكي يكون مجموعهما صفراً ($\nabla^2 \phi = 0$)، لا يمكن للسطح أن يتقوس للأعلى في الاتجاهين معاً في نفس النقطة! أي **يستحيل رياضياً وجود أي قاع محلي (Local Minimum)** داخل المجال المفتوح لأن القاع المحلي يتطلب $\phi_{xx} > 0$ و $\phi_{yy} > 0$ معاً (ومجموع رقمين موجبين لا يمكن أن يساوي صفراً!).
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab4

%matplotlib inline
print("تم تهيئة بيئة اللاب 4 بنجاح!")
""")

    nb.md(r"""---
## 2. التغطية الكاملة للقسم 1.4 في المذكرة: المعادلات المتجانسة وجميع حالات التكامل الخاص الـ 6 (PDF ص 28–51)

نسمي المعادلة التفاضلية الجزئية الخطية **متجانسة في الرتبة (Homogeneous of order $n$)** إذا كانت جميع المشتقات فيها من نفس الرتبة $n$:
$$(a_0 D_x^n + a_1 D_x^{n-1} D_y + \dots + a_n D_y^n) z = f(x, y) \quad \Longleftrightarrow \quad F(D_x, D_y) z = f(x, y)$$

يتكون الحل العام من جزأين: $z = z_1\text{ (الحل المكمل C.F.)} + z_2\text{ (التكامل الخاص P.I.)}$.

---
### أولاً: إيجاد الحل المكمل (Complementary Function $z_1$ — ص 35–39 / PDF ص 29–33)
نفرض حلاً من الشكل $z = \phi(y + mx)$، فتكون $D_x z = m\phi'$ و $D_y z = \phi'$. بالتعويض في $F(D_x, D_y)z = 0$ نحصل على **المعادلة المساعدة (Auxiliary Equation)** بوضع $D_x = m$ و $D_y = 1$:
$$F(m, 1) = a_0 m^n + a_1 m^{n-1} + \dots + a_n = 0$$

| حالة جذور المعادلة المساعدة $F(m, 1) = 0$ | شكل الحل المكمل $z_1$ في المذكرة |
| :--- | :--- |
| **الحالة 1: جذور حقيقية ومختلفة** $m_1 \neq m_2$ *(ص 36 / PDF ص 30)* | $z_1 = \phi_1(y + m_1 x) + \phi_2(y + m_2 x)$ |
| **الحالة 2: جذور مكررة ($k$ مرات)** $m_1 = \dots = m_k = m$ *(ص 37 / PDF ص 31)* | $z_1 = \phi_1(y + mx) + x\,\phi_2(y + mx) + \dots + x^{k-1}\phi_k(y + mx)$ |
| **الحالة 3: جذور مركبة** $m = \alpha \pm i\beta$ *(ص 39 / PDF ص 33)* | $z_1 = \phi_1(y + (\alpha + i\beta)x) + \phi_2(y + (\alpha - i\beta)x)$ |

---
### 📖 المثال المحوري في المذكرة: معادلة لابلاس (مثال 5 ص 39 / PDF ص 33)
**المسألة:** حل معادلة لابلاس ثنائية الأبعاد:
$$\frac{\partial^2 z}{\partial x^2} + \frac{\partial^2 z}{\partial y^2} = 0 \quad \Longleftrightarrow \quad (D_x^2 + D_y^2)z = 0$$
1. **المعادلة المساعدة:** نضع $D_x = m$ و $D_y = 1$:
   $$m^2 + 1 = 0 \implies m^2 = -1 \implies m = \pm i$$
2. **الحل العام التحليلي:**
   $$z = \phi_1(y + ix) + \phi_2(y - ix)$$
   حيث $\phi_1, \phi_2$ دالتان اختياريتان. (وإذا اخترنا مثلاً $\phi_1(w) = \frac{1}{2i}\sin(\pi i w)$ و $\phi_2(w) = -\frac{1}{2i}\sin(\pi i w)$، نحصل على الدالة التوافقية الحقيقية الشهيرة $\sin(\pi x)\sinh(\pi y)$!).

---
### ثانياً: إيجاد التكامل الخاص $z_2 = \frac{1}{F(D_x, D_y)} f(x, y)$ — الطريقة العامة والحالات الست المختصرة (PDF ص 34–51)

عندما يكون الطرف الأيمن $f(x, y) \neq 0$، تشرح المذكرة **طريقة عامة (General Method)** بالإضافة إلى **6 طرق مختصرة (Short Methods)** بحسب شكل الدالة $f(x, y)$:

#### 🧭 جدول القرار السريع لحالات التكامل الخاص الست (PDF ص 34–51)

| الحالة في المذكرة | شكل الطرف الأيمن $f(x, y)$ | القاعدة السريعة لحساب $z_2 = \frac{1}{F(D_x, D_y)}f(x,y)$ | ماذا لو صفر المقام ($F = 0$)؟ |
| :--- | :--- | :--- | :--- |
| **الطريقة العامة** *(ص 40 / PDF ص 34)* | أي دالة عامة (مثل $\sec^2(x+y)$) | حلل $F = \prod(D_x - m_i D_y)$ وحل كل عامل بمعادلة لاجرانج $\frac{dx}{1} = \frac{dy}{-m} = \frac{du}{f}$ | تعمل دائماً بدون استثناء! |
| **الحالة 1** *(ص 44 / PDF ص 38)* | $e^{ax + by}$ | استبدل $D_x \to a$ و $D_y \to b$: $z_2 = \frac{1}{F(a,b)}e^{ax+by}$ | إذا كان $F = (D_x - \frac{a}{b}D_y)^r G$: $z_2 = \frac{1}{G(a,b)}\frac{x^r}{r!}e^{ax+by}$ |
| **الحالة 2** *(ص 47 / PDF ص 41)* | $\sin(ax+by)$ أو $\cos(ax+by)$ | استبدل $D_x^2 \to -a^2,\; D_x D_y \to -ab,\; D_y^2 \to -b^2$ | حوّل لأسية بصيغة أويلر $\frac{e^{i\theta} \pm e^{-i\theta}}{2}$ وطبق رنين الحالة 1 |
| **الحالة 3** *(ص 51 / PDF ص 45)* | كثيرة حدود $x^a y^b$ | اسحب أصغر قوة لـ $D_x$ (أو $D_y$) عامل مشترك وفك $\frac{1}{1-\theta} = 1 + \theta + \theta^2 + \dots$ | التكامل $\frac{1}{D_x}$ يعني التكامل بالنسبة لـ $x$ |
| **الحالة 4** *(ص 53 / PDF ص 47)* | $e^{ax+by} V(x,y)$ | **الإزاحة الأسية:** أخرج $e^{ax+by}$ خارج المؤثر واستبدل $D_x \to D_x+a,\; D_y \to D_y+b$ | طبّق الحالة 1 أو 2 أو 3 على $V(x,y)$ بعد الإزاحة |
| **الحالة 5 و 6** *(ص 56 / PDF ص 50)* | أي دالة $g(ax+by)$ | إذا $F(a,b)\neq 0$: كامل $g(u)$ عدد $n$ مرات: $\frac{1}{F(a,b)}\int\dots\int g(u)du^n$ | **الحالة 6:** لـ $(bD_x - aD_y)^n z = g(ax+by)$: $z_2 = \frac{x^n}{n!\,b^n}g(ax+by)$ |

---
#### 🔹 شرح الطريقة العامة (General Method via Lagrange — ص 40–44 / PDF ص 34–38)
* **متى نستخدمها؟** عندما لا تكون $f(x, y)$ من الدوال القياسية البسيطة (أو عندما نريد الاشتقاق من المبادئ الأولى).
* **الفكرة:** نحلل المؤثر إلى عوامل خطية $F(D_x, D_y) = (D_x - m_1 D_y)(D_x - m_2 D_y)$، ونفرض $u_1 = (D_x - m_1 D_y)z$، فنحصل على معادلة من الرتبة الأولى:
  $$(D_x - m_2 D_y)u_1 = f(x, y) \iff \frac{\partial u_1}{\partial x} - m_2 \frac{\partial u_1}{\partial y} = f(x, y)$$
  نحلها بمعادلات لاجرانج المساعدة من **اللاب 2**: $\frac{dx}{1} = \frac{dy}{-m_2} = \frac{du_1}{f(x,y)}$، ثم نكرر نفس الخطوة لإيجاد $z$!
* **📖 مثال 1 في المذكرة (ص 41–43 / PDF ص 35–37):** حل $(D_x^2 - D_y^2)z = \sec^2(x + y)$.
  * نحلل $(D_x + D_y)(D_x - D_y)z = \sec^2(x + y)$. وبحل العاملين بالتتابع عبر لاجرانج نحصل على التكامل الخاص:
    $$\boxed{z_2 = \frac{x}{2}\tan(x + y)}$$

---
#### 🔹 الحالة 1: الدالة الأسية $f(x, y) = e^{ax + by}$ وحالة الرنين $F(a, b) = 0$ (ص 44–47 / PDF ص 38–41)
* **أ) إذا كان $F(a, b) \neq 0$:** نعوض مباشرة $D_x \to a$ و $D_y \to b$:
  $$\boxed{z_2 = \frac{1}{F(a, b)}e^{ax + by}}$$
  * **مثال 2 (ص 45 / PDF ص 39):** في $(D_x^2 - D_x D_y - 6D_y^2)z = e^{2x - 3y}$، لدينا $a = 2, b = -3$، فيكون $F(2, -3) = 4 - (2)(-3) - 6(-3)^2 = 4 + 6 - 54 = -44 \neq 0 \implies \boxed{z_2 = -\frac{1}{44}e^{2x - 3y}}$.
* **ب) ماذا لو كان المقام يساوي صفراً $F(a, b) = 0$ (حالة الرنين / الفشل)؟ (ص 45–47 / PDF ص 39–41)**
  إذا كان $F(a, b) = 0$، فهذا يعني أن $\left(D_x - \frac{a}{b}D_y\right)$ عامل من عوامل $F(D_x, D_y)$ مكرر $r$ من المرات:
  $$F(D_x, D_y) = \left(D_x - \frac{a}{b}D_y\right)^r G(D_x, D_y), \qquad G(a, b) \neq 0$$
  نعوض بـ $(a, b)$ في الجزء غير الصفري $G(a, b)$ فقط، أما العامل الصفري المكرر $r$ مرات فيتحول إلى **ضرب في $\frac{x^r}{r!}$**:
  $$\boxed{z_2 = \frac{1}{G(a, b)} \frac{x^r}{r!} e^{ax + by}}$$
  * **📖 مثال 3 في المذكرة (ص 46 / PDF ص 40):** حل $(D_x^2 - D_x D_y - 6D_y^2)z = e^{3x + y}$.
    1. هنا $a = 3, b = 1$. لو عوضنا مباشرة: $F(3, 1) = 9 - 3 - 6 = 0$! (حالة رنين لأن $e^{3x+y} = e^{3(x + y/3)}$ هي أصلًا ضمن الحل المكمل!).
    2. نحلل المؤثر: $D_x^2 - D_x D_y - 6D_y^2 = (D_x - 3D_y)^1 (D_x + 2D_y)$.
    3. إذن العامل الصفري هو $(D_x - 3D_y)$ بتكرار $r = 1$، والجزء غير الصفري هو $G(D_x, D_y) = D_x + 2D_y$ حيث $G(3, 1) = 3 + 2(1) = 5$.
    4. نطبق القانون مباشرة: $\boxed{z_2 = \frac{1}{5}\frac{x^1}{1!}e^{3x + y} = \frac{x}{5}e^{3x + y}}$.

> 📌 **تنبيه خطأ مطبعي في المذكرة (ص 49، مثال 5 / PDF ص 43):**
> في السطر الأخير من صفحة 49 بالترقيم المكتوب (PDF ص 43) عند حساب التكامل الخاص للدالة $e^{2x+3y}$ ($a=2, b=3$) للمؤثر $F = D_x^2 - 3D_x D_y + 2D_y^2$، كتبت المذكرة بالخطأ $F(1,1) = 4 - 18 + 18 = 4$. الأرقام المحسوبة ($2^2 - 3(2)(3) + 2(3)^2 = 4 - 18 + 18 = 4$) صحيحة تماماً لـ $(a,b)=(2,3)$، لكن الرمز المكتوب $F(1,1)$ هو خطأ مطبعي والصواب $\boxed{F(2, 3) = 4}$!

---
#### 🔹 الحالة 2: دوال الجيب وجيب التمام $\sin(ax+by)$ أو $\cos(ax+by)$ (ص 47–51 / PDF ص 41–45)
* **أ) في المؤثرات من الرتبة الثانية (بشرط عدم انعدام المقام):** نستبدل كل:
  $$\boxed{D_x^2 \to -a^2, \qquad D_x D_y \to -ab, \qquad D_y^2 \to -b^2}$$
  *(تنبيه الإشارات: السالب خارج التربيع دائماً! فإذا كان $a=2, b=-3$ فإن $D_x^2 \to -4$ و $D_y^2 \to -9$ بينما $D_x D_y \to -(2)(-3) = +6$).*
* **ب) ماذا لو صفر المقام في $\sin$ أو $\cos$؟ (مثال 6 ص 50–51 / PDF ص 44–45):**
  في $(D_x^2 + D_y^2)z = \cos(mx + my)$، لدينا $a = m, b = m$، فالتعويض يعطي $-m^2 + (-m^2)$ أو في حالة $(D_x^2 - D_y^2)z = \cos(mx+my)$ يعطي $-m^2 - (-m^2) = 0$!
  عندما ينعدم المقام (أو في المؤثرات من رتب فردية)، تضع المذكرة $\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2}$ (أو $\sin\theta = \frac{e^{i\theta} - e^{-i\theta}}{2i}$) وتطبق قاعدة الرنين من **الحالة 1**!

---
#### 🔹 الحالة 3: كثيرات الحدود $f(x, y) = x^a y^b$ بطريقة المفكوك (ص 51–53 / PDF ص 45–47)
* **الفكرة:** نسحب العامل ذا أصغر أس لـ $D_x$ (أو $D_y$) من المقام ليصبح المقام على الصورة $D_x^k [1 - \theta(D_x, D_y)]$، ثم نرفعه للبسط بمتسلسلة ذات الحدين (المتسلسلة الهندسية):
  $$\boxed{\frac{1}{1 - \theta} = 1 + \theta + \theta^2 + \theta^3 + \dots, \qquad \frac{1}{1 + \theta} = 1 - \theta + \theta^2 - \theta^3 + \dots}$$
  لماذا تتوقف المتسلسلة ولا تستمر إلى ما لا نهاية؟ لأن $x^a y^b$ كثيرة حدود، فمشتقاتها العليا تصبح **صفراً** بعد عدد محدود من الخطوات! وتذكر أن $\frac{1}{D_x}$ معناه **التكامل بالنسبة لـ $x$** ($\int (\cdots)\,dx$).
* **📖 مثال 7 في المذكرة (ص 52 / PDF ص 46):** أوجد التكامل الخاص لـ $(D_x^2 - 2D_x D_y)z = x^3 y$.
  1. نسحب $D_x^2$ عاملاً مشتركاً من المقام:
     $$z_2 = \frac{1}{D_x^2\left(1 - \frac{2D_y}{D_x}\right)}(x^3 y) = \frac{1}{D_x^2}\left(1 - \frac{2D_y}{D_x}\right)^{-1}(x^3 y)$$
  2. نفك القوس بمتسلسلة هندسية (نحتاج فقط حتى المشتقة الأولى $D_y$ لأن $D_y^2(x^3 y) = 0$!):
     $$z_2 = \frac{1}{D_x^2}\left(1 + \frac{2D_y}{D_x} + \dots\right)(x^3 y) = \frac{1}{D_x^2}\left[x^3 y + \frac{2}{D_x}\underbrace{D_y(x^3 y)}_{x^3}\right]$$
  3. نكامل بالنسبة لـ $x$ ($\frac{1}{D_x}(x^3) = \frac{x^4}{4}$، ثم نكامل مرتين لوجود $\frac{1}{D_x^2}$ خارج القوس):
     $$z_2 = \frac{1}{D_x^2}\left(x^3 y + \frac{x^4}{2}\right) = \frac{1}{D_x}\left(\frac{x^4 y}{4} + \frac{x^5}{10}\right) = \boxed{\frac{x^5 y}{20} + \frac{x^6}{60}}$$

---
#### 🔹 الحالة 4: حاصل ضرب دالة أسية في أي دالة أخرى $f(x, y) = e^{ax + by} V(x, y)$ (ص 53–55 / PDF ص 47–50)
* **نظرية الإزاحة الأسية (Exponential Shift Rule):** يمكنك إخراج الدالة الأسية $e^{ax + by}$ إلى يسار المؤثر الكسري فوراً بشرط **إزاحة كل $D_x \to D_x + a$ وكل $D_y \to D_y + b$**:
  $$\boxed{\frac{1}{F(D_x, D_y)}\left[e^{ax + by} V(x, y)\right] = e^{ax + by} \frac{1}{F(D_x + a, D_y + b)} V(x, y)}$$
  وبعد إخراج $e^{ax+by}$، تصبح المسألة مجرد تأثير على $V(x,y)$ فنحلها بالحالة 1 أو 2 أو 3!
* **📖 مثال 10 في المذكرة (ص 54 / PDF ص 48):** حل $(D_x - D_y)^2 z = x e^{x + y}$.
  1. نخرج $e^{x + y}$ ($a = 1, b = 1$) ونزيح $D_x \to D_x + 1$ و $D_y \to D_y + 1$:
     $$(D_x + 1) - (D_y + 1) = D_x - D_y \implies z_2 = e^{x+y}\frac{1}{(D_x - D_y)^2}(x)$$
  2. الآن $V(x,y) = x^1 y^0$ لا يعتمد على $y$ إطلاقاً ($D_y(x) = 0$)، فيختزل المؤثر إلى $\frac{1}{D_x^2}(x)$ (تكامل $x$ مرتين بالنسبة لـ $x$):
     $$\boxed{z_2 = e^{x + y}\frac{1}{D_x^2}(x) = \frac{x^3}{6}e^{x + y}}$$
  *(وكذلك في **مثال 11 و 12 ص 54–55 / PDF ص 48–50** تطبق المذكرة الإزاحة الأسية مع $\sin(2x+3y)$ ومع $x^2 y$ بنفس الخطوات تماماً!).*

---
#### 🔹 الحالتان 5 و 6: عندما يكون الطرف الأيمن دالة عامة $f(x, y) = g(ax + by)$ (ص 56–57 / PDF ص 50–51)
* **الحالة 5 ($F(a, b) \neq 0$ — ص 56 / PDF ص 50):** نضع $u = ax + by$ ونكامل الدالة $g(u)$ عدد $n$ من المرات (حيث $n$ رتبة المؤثر):
  $$\boxed{z_2 = \frac{1}{F(a, b)} \underbrace{\int \dots \int}_{n\text{ مرات}} g(u)\,du^n}$$
* **الحالة 6 ($F(a, b) = 0$ حيث $F(D_x, D_y) = (b D_x - a D_y)^n$ — ص 56–57 / PDF ص 50–51):**
  إذا كان المؤثر من الصورة $(b D_x - a D_y)^n z = g(ax + by)$، فإن التعويض بـ $(a, b)$ يعطي $(ba - ab)^n = 0$! في هذه الحالة لا نكامل $g$ أصلاً، بل نضرب في $\frac{x^n}{n!\,b^n}$ مباشرة:
  $$\boxed{z_2 = \frac{x^n}{n!\,b^n}\,g(ax + by)}$$
  * **📖 مثال 14 و 15 في المذكرة (ص 57 / PDF ص 51):**
    * في **مثال 14:** $(2D_x - 3D_y)^2 z = \tan(3x + 2y)$، هنا $a = 3, b = 2, n = 2$ و $b D_x - a D_y = 2D_x - 3D_y \implies F(3, 2) = 0$. بتطبيق قانون الحالة 6 فوراً:
      $$\boxed{z_2 = \frac{x^2}{2!\cdot 2^2}\tan(3x + 2y) = \frac{x^2}{8}\tan(3x + 2y)}$$
    * في **مثال 15:** $(D_x - 2D_y)^3 z = (2x + y)^2$، هنا $a = 2, b = 1, n = 3 \implies \boxed{z_2 = \frac{x^3}{3!\cdot 1^3}(2x + y)^2 = \frac{x^3}{6}(2x + y)^2}$.

> 📌 **تنبيه خطأ مطبعي في المذكرة (ص 57، مثال 14 / PDF ص 51):**
> في حل المثال 14 في المذكرة، كُتب رمز المؤثر $F(D_x, D_x) = (2D_x - 3D_y)^2$ بحرف $D_x$ مرتين بين القوسين، وهو خطأ مطبعي بسيط والصواب $\boxed{F(D_x, D_y)}$.
""")

    nb.md(r"""---
## 3. 📝 تحدي الورقة والقلم 1 (جذور معادلة لابلاس — مثال 5 ص 39 / PDF ص 33)

**المسألة:** أوجد الجذور المميزة $m_1, m_2$ للمعادلة المساعدة لمعادلة لابلاس:
$$(D_x^2 + D_y^2)z = 0$$

في بايثون، تُكتب الوحدة التخيلية $i = \sqrt{-1}$ على الصورة `1j`، وتُكتب $-i$ على الصورة `-1j`.

<details>
<summary>💡 <b>تلميح (اضغط هنا إذا احتجت مساعدة)</b></summary>

ضع $D_x = m$ و $D_y = 1$ فتحصل على $m^2 + 1 = 0 \implies m = \pm i$. في بايثون اكتب `1j` و `-1j`.
</details>
""")

    if solutions:
        nb.code(r"""# خلية تقييم: جذور معادلة لابلاس
### START CODE HERE ###
m1 = 1j
m2 = -1j
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_1(m1, m2)
""")
    else:
        nb.code(r"""# خلية تقييم: جذور معادلة لابلاس
### START CODE HERE ### (≈ 2 lines of code)
# أدخل الجذور التخيلية لمعادلة لابلاس في بايثون:
m1 = None
m2 = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_1(m1, m2)
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 2 (التكامل الخاص P.I. — مثال 4 ص 48 / PDF ص 42)

**المسألة (من المذكرة ص 48 / PDF ص 42):** أوجد التكامل الخاص $z_2$ للمعادلة التفاضلية الجزئية غير المتجانسة في الطرف الأيمن:
$$(D_x^2 - D_x D_y - 6 D_y^2)z = \sin(2x - 3y)$$

**خطوات الحل على ورقتك:**
1. حدد معاملات الزاوية في $\sin(ax + by) = \sin(2x - 3y)$: لدينا $a = 2$ و $b = -3$.
2. عوض في المؤثر $\frac{1}{D_x^2 - D_x D_y - 6 D_y^2}$ باستخدام قاعدة الحالة الثانية:
   * $D_x^2 \to -a^2$
   * $D_x D_y \to -ab$
   * $D_y^2 \to -b^2$
3. احسب قيمة المقام العددي الناتج، ثم اكتب صيغة $z_2$.

<details>
<summary>💡 <b>تلميح 1 (حساب البدائل الثلاثة)</b></summary>

بما أن $a = 2$ و $b = -3$:
* $D_x^2 \to -(2)^2 = -4$
* $D_x D_y \to -(2)(-3) = +6$
* $D_y^2 \to -(-3)^2 = -9$
</details>

<details>
<summary>💡 <b>تلميح 2 (التعويض في المقام)</b></summary>

عوض بالأرقام في المقام $(D_x^2) - (D_x D_y) - 6(D_y^2)$:
$$(-4) - (6) - 6(-9) = -10 + 54 = 44$$
إذن التكامل الخاص هو مقلوب هذا العدد مضروباً في $\sin(2x - 3y)$.
</details>
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
# اكتب صيغة التكامل الخاص بدلالة x و y:
student_pi = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab4.check_paper_challenge_2(student_pi)
""")

    nb.md(r"""---
## 5. 💻 التطبيق البرمجي ببايثون: حلال الجذور المميزة للمؤثرات التفاضلية

لحل أي معادلة متجانسة $(a_0 D_x^n + a_1 D_x^{n-1}D_y + \dots + a_n D_y^n)z = 0$ برمجياً، نمرر معاملات المعادلة المساعدة `[a_0, a_1, ..., a_n]` إلى دالة `np.roots(coeffs)` لإيجاد الجذور $m_1, \dots, m_n$ وتصنيف نوع المعادلة.
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: solve_operator_roots
def solve_operator_roots(coeffs: list[float]) -> list[complex]:
    # تحسب جذور المعادلة المساعدة F(m, 1) = 0 لقائمة المعاملات coeffs
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
    # تحسب جذور المعادلة المساعدة F(m, 1) = 0 لقائمة المعاملات coeffs
    ### START CODE HERE ### (≈ 1 line of code)
    # استخدم np.roots(coeffs) لحساب الجذور:
    roots = None
    ### END CODE HERE ###
    return list(roots)

# تشغيل الاختبار الآلي:
test_lab4.test_characteristic_roots_solver(solve_operator_roots)
''')

    nb.md(r"""---
## 6. 🎨 الجسر إلى اللاب 6: كيف تتحول معادلة لابلاس التحليلية إلى دالة `_avg(phi)` في `solvers.py`؟

قد تتساءل: **إذا كان لدينا الحل التحليلي العام لمعادلة لابلاس $z = \phi_1(y + ix) + \phi_2(y - ix)$، فلماذا نحتاج إلى حلال عددي في اللاب 6؟**
* على مربع فارغ منتظم، يمكننا كتابة حل تحليلي مغلق مثل $\phi(x, y) = \frac{\sin(\pi x)\sinh(\pi y)}{\sinh(\pi)}$.
* لكن على خريطة المريخ، توجد **مئات الصخور والحفر بأشكال عشوائية غير منتظمة**! يستحيل إيجاد صيغة تحليلية واحدة تحقق شروط الحدود حول 10,000 عقدة صخرية عشوائية.
* الحل العبقري: عندما نقرب المشتقات الثانية على شبكة بكسل متساوية المسافات ($\Delta x = \Delta y = h$):
  $$\frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} \approx \frac{\phi_{i,j+1} + \phi_{i,j-1} + \phi_{i+1,j} + \phi_{i-1,j} - 4\phi_{i,j}}{h^2} = 0$$
  فإن معادلة لابلاس $(D_x^2 + D_y^2)\phi = 0$ تعني ببساطة أن **قيمة كل نقطة داخلية تساوي متوسط جيرانها الأربعة (`_avg(phi)`)**:
  $$\phi_{i,j} = \frac{1}{4}\left(\phi_{\text{North}} + \phi_{\text{South}} + \phi_{\text{East}} + \phi_{\text{West}}\right)$$

شغّل الخلية التالية لترى السطح التحليلي التوافقي وتتحقق بنفسك أن دالة `_avg` الفعلية من ملف [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py) تطابق السطح التحليلي!
""")

    nb.code(r"""from rover_path_finder.solvers import _avg

x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.pi * X) * np.sinh(np.pi * Y) / np.sinh(np.pi)

# نختبر خاصية المتوسط الحسابي للجيران الأربعة على النقاط الداخلية
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

print(f"✅ أقصى فرق بين السطح التحليلي ومتوسط الجيران الأربعة _avg(Z): {neighbor_diff.max():.6f}")
print("📌 ملخص اللاب 4:")
print("  1) معادلة لابلاس (D_x^2 + D_y^2)z = 0 لها جذور مميزة مركبة m = ±i وحلولها دوال توافقية ملساء.")
print("  2) الدوال التوافقية تحقق خاصية المتوسط الحسابي، لذا يستحيل أن تحتوي على قاع محلي يحبس المركبة.")
""")

    nb.save()


# ===========================================================================
# LAB 5 (ARABIC): NON-HOMOGENEOUS PDES & REDUCIBLE OPERATORS
# ===========================================================================
def build_lab_5_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_5_NonHomogeneous_PDEs_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 📡 اللاب 5: المعادلات الخطية غير المتجانسة في الرتبة، تحليل المؤثرات، واضمحلال الجهد في الممرات الضيقة
### *غرفة التحكم: لماذا يفشل شرط ديريكليه (`dirichlet_potential`) في الممرات الضيقة بسبب الاضمحلال الأسي؟*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**المرجع في المذكرة:** الباب الثاني (Chapter 2)، القسم 2.1 — **ترقيم المذكرة (الباب الثاني) ص 1–10** *(صفحات ملف الـ PDF من 52 إلى 62؛ قانون العوامل الخطية في ص 2 / PDF ص 54، والمثال 5 في ص 4 / PDF ص 56)*

---
### 🗺️ موقعك في سلسلة بناء محرك الملاحة (Rover Pipeline)
```
[اللاب 1–3: الميول، مسارات الانسياب، وهوامش الأمان] ──► [اللاب 4: معادلة لابلاس] ──► 📍 [اللاب 5: المؤثرات غير المتجانسة واضمحلال الجهد] ──► [اللاب 6: محرك الملاحة النهائي SOR + Neumann]
```

---
### 🧭 حجر رشيد (The Rosetta Stone): الربط بين السبورة ومحرك المركبة

| 1. رمز المذكرة (PDF pp. 52–62) | 2. المعنى الهندسي والفيزيائي | 3. الدالة الفعلية في المشروع (`rover_path_finder/`) |
| :--- | :--- | :--- |
| $F(D_x, D_y)z = 0$ غير متجانسة في الرتبة | معادلة تجمع مشتقات من رتب مختلفة أو حداً ثابتاً $c$ (مثل $aD_x + bD_y + c$) | تمثيل التخميد والاضمحلال الأسي على طول مسار الانتشار |
| $(a D_x + b D_y + c)z = 0 \implies z = e^{-\frac{c}{a}x}\phi(ay - bx)$ | كل عامل خطي به ثابت $c \neq 0$ يفرض غلافاً أسياً $e^{-(c/a)x}$ على الحل | الاضمحلال الأسي للانحدار داخل الممرات الضيقة |
| $(F_1 \cdot F_2)z = 0 \implies z = z_1 + z_2$ | تحليل المؤثر إلى عوامل خطية وجمع الحلول (مبدأ التراكب) | تحليل أنماط الجهد إلى مركبات أسية متراكبة |
| تلاشي انحدار الجهد $\|\nabla\phi\| \propto e^{-\pi d / w}$ | عندما نجعل جدران العوائق ثابتة عند $\phi=1$، يتلاشى الميل أسياً داخل أي ممر عرضه $w$ | سبب استبدال [`planners.dirichlet_potential`](rover_path_finder/planners.py) بالدالة [`planners.neumann_potential`](rover_path_finder/planners.py) |

---
## 1. أولاً: توضيح مصطلح مهم جداً في المذكرة ("غير متجانسة" في الباب الثاني!)

عندما تقرأ عنوان **الباب الثاني في المذكرة (PDF ص 52): "Non-Homogeneous Linear PDEs"**، انتبه جيداً للفرق الاصطلاحي:
* في المعادلات العادية (ODEs)، كلمة "غير متجانسة" تعني عادةً وجود طرف أيمن $f(x, y) \neq 0$.
* أما في **الباب الثاني من مذكرتنا (PDF ص 52–57)**، كلمة **Non-Homogeneous (غير متجانسة في الرتبة)** تعني أن **الطرف الأيسر نفسه يحتوي على مشتقات من رتب مختلفة** (مثلاً مشتقة ثانية $D_x^2$ مع مشتقة أولى $D_x$ أو ثابت $c$)، مثل:
  $$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$
  لاحظ أن الطرف الأيمن يساوي صفراً، ومع ذلك تسمى المعادلة **غير متجانسة في الرتبة** بسبب وجود الثابتين $+1$ و $-2$ مع المشتقات الأولى $D_x, D_y$!

---
## 2. كيف يرتبط هذا الاضمحلال الأسي بمشكلة الممرات الضيقة في مركبة المريخ؟

في ملف [`rover_path_finder/planners.py`](rover_path_finder/planners.py)، توجد طريقتان لبناء حقل الجهد التوافقي للمركبة:
1. **الصياغة الأولى (`dirichlet_potential` — Formulation A):** تثبيت جميع العوائق وجدران الخريطة عند جهد مرتفع ثابت $\phi = 1$، والهدف عند $\phi = 0$.
2. **الصياغة الثانية (`neumann_potential` — Formulation B):** جعل العوائق جدراناً عازلة ($\partial\phi/\partial n = 0$) ووضع مصدر عند البداية ($\phi=1$) ومصب عند الهدف ($\phi=0$).

**لماذا تفشل الصياغة الأولى (`dirichlet_potential`) عندما تمر المركبة في ممر ضيق بين صخرتين؟**
إذا دخلت المركبة ممراً ضيقاً عرضه $w$ وطوله $d$ وجدرانه مثبتة عند $\phi = 1$، فإن فرق الجهد $\tilde{\phi} = 1 - \phi$ يحقق نمطاً توافقياً في اتجاه العرض $\sin(\pi y / w)$ مما يفرض معادلة عاملية ذات حد ثابت $c = \pm\frac{\pi}{w}$ في اتجاه الطول $x$:
$$\left(D_x + \frac{\pi}{w}\right)\tilde{\phi} = 0 \implies \tilde{\phi}(x, y) \propto e^{-\frac{\pi}{w} x} \sin\left(\frac{\pi y}{w}\right)$$
أي أن انحدار الجهد يتلاشى أسياً بمعدل $e^{-\pi x / w}$! فإذا كان الممر ضيقاً ($w$ صغير)، يصبح الجهد $\phi \approx 1.000000$ في كل مكان داخل الممر ويتوقف انحدار المركبة تماماً!
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab5

%matplotlib inline
print("تم تهيئة بيئة اللاب 5 بنجاح!")
""")

    nb.md(r"""---
## 3. الوصفة الرياضية الكاملة للباب الثاني في المذكرة (Cases A, B, C, D & P.I. — PDF ص 52–62)

### الحالة (A): عامل خطي واحد أو مكرر $(a D_x + b D_y + c)^k z = 0$ *(الباب الثاني ص 2–3 / PDF ص 54–55)*

#### 1. لماذا يظهر العامل الأسي $e^{-\frac{c}{a}x}$؟
* المعادلة $(a D_x + b D_y + c)z = 0$ هي $a \frac{\partial z}{\partial x} + b \frac{\partial z}{\partial y} = -c z$ (معادلة لاجرانج من اللاب 2 حيث $P=a, Q=b, R=-cz$!).
* من معادلات لاجرانج المساعدة:
  $$\frac{dx}{a} = \frac{dy}{b} = \frac{dz}{-cz}$$
* من الكسر الأول والثاني: $b\,dx - a\,dy = 0 \implies ay - bx = u$.
* من الكسر الأول والثالث (بشرط $a \neq 0$): $\frac{dz}{z} = -\frac{c}{a}dx \implies \ln|z| = -\frac{c}{a}x + \ln|\phi(u)|$.
* إذن **القانون المباشر لأي عامل خطي** هو:
  * **إذا كان $a \neq 0$:**
    $$\boxed{(a D_x + b D_y + c)z = 0 \implies z = e^{-\frac{c}{a}x}\,\phi(a y - b x)}$$
  * **وإذا كان $a = 0$ و $b \neq 0$ (أو إذا اخترنا الكسر الثاني والثالث $\frac{dy}{b} = \frac{dz}{-cz}$):**
    $$\boxed{z = e^{-\frac{c}{b}y}\,\phi(a y - b x)}$$

#### 2. ماذا لو تكرر العامل الخطي $k$ من المرات؟ $(a D_x + b D_y + c)^k z = 0$ (ص 2–3 / PDF ص 54–55)
* **إذا استخدمنا الأس بدلالة $x$ ($a \neq 0$):** نضرب الدوال المتتالية في $1, x, x^2, \dots, x^{k-1}$:
  $$\boxed{z = e^{-\frac{c}{a}x}\left[\phi_1(ay - bx) + x\,\phi_2(ay - bx) + x^2\,\phi_3(ay - bx) + \dots + x^{k-1}\phi_k(ay - bx)\right]}$$
* **وإذا استخدمنا الأس بدلالة $y$ ($b \neq 0$، خاصة عندما $a = 0$):** نضرب في $1, y, y^2, \dots, y^{k-1}$:
  $$\boxed{z = e^{-\frac{c}{b}y}\left[\phi_1(ay - bx) + y\,\phi_2(ay - bx) + \dots + y^{k-1}\phi_k(ay - bx)\right]}$$

> 📌 **تنبيه خطأ مطبعي مهم جداً في المذكرة (الباب الثاني ص 2–3، المثالان 3 و 4 / PDF ص 54–55):**
> * في **المثال 3 (PDF ص 54):** $(2D_x - 3D_y + 2)^2 z = 0$ ($a=2, b=-3, c=2$)، الصيغة الأولى في المذكرة $z = e^{-x}[\phi_1(2y+3x) + x\phi_2(2y+3x)]$ **صحيحة 100%**! لكن في السطر الذي يليه ("Or $z = e^{\frac{2}{3}y}[\dots]$")، كتبت المذكرة $x\phi_2$ بدلاً من $y\phi_2$.
> * وفي **المثال 4 (PDF ص 55):** $(D_x - 2D_y + 1)^4 z = 0$ ($a=1, b=-2, c=1, k=4$)، وضعت المذكرة داخل القوس قوى $x$ ($1, x, x^2, x^3$) ولكنها كتبت خارج القوس بالخطأ $e^{\frac{1}{2}y}$ بدلاً من $e^{-\frac{c}{a}x} = e^{-x}$!
> * **الخلاصة الذهبية لك في الامتحان:** التزم دائماً بصيغة $x$ القياسية (طالما $a \neq 0$): **أخرج $e^{-(c/a)x}$ واضرب بالداخل في قوى $x$ ($1, x, x^2, \dots$)**، فهي الأسهل والأضمن 100%!

---
### الحالة (B): المؤثرات القابلة للتحليل إلى عوامل خطية مختلفة *(الباب الثاني ص 3–4 / PDF ص 55–56)*
إذا أمكن تحليل المؤثر $F(D_x, D_y)$ إلى حاصل ضرب عوامل خطية:
$$(a_1 D_x + b_1 D_y + c_1)(a_2 D_x + b_2 D_y + c_2)z = 0$$
فإن الحل العام هو مجموع حلول كل عامل على حدة:
$$z = e^{-\frac{c_1}{a_1}x}\phi_1(a_1 y - b_1 x) + e^{-\frac{c_2}{a_2}x}\phi_2(a_2 y - b_2 x)$$

#### 📖 مثال محلول بالتفصيل (المثال 5، الباب الثاني ص 4 / PDF ص 56)
**المسألة:** أوجد الحل العام للمعادلة:
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$
1. **العامل الأول $(2 D_x - 3 D_y + 1)z = 0$:**
   * المعاملات: $a_1 = 2,\; b_1 = -3,\; c_1 = 1$.
   * الأس: $-\frac{c_1}{a_1}x = -\frac{1}{2}x$.
   * داخل الدالة الاختيارية: $a_1 y - b_1 x = 2y - (-3)x = 2y + 3x$.
   * إذن الحل الأول: $z_1 = e^{-x/2}\Phi_1(2y + 3x)$.
2. **العامل الثاني $(D_x + 2 D_y - 2)z = 0$:**
   * المعاملات: $a_2 = 1,\; b_2 = 2,\; c_2 = -2$.
   * الأس: $-\frac{c_2}{a_2}x = -\frac{-2}{1}x = 2x$.
   * داخل الدالة الاختيارية: $a_2 y - b_2 x = 1y - 2x = y - 2x$.
   * إذن الحل الثاني: $z_2 = e^{2x}\Phi_2(y - 2x)$.
3. **الحل العام الكلي:** $\boxed{z = e^{-x/2}\Phi_1(2y + 3x) + e^{2x}\Phi_2(y - 2x)}$.

*(وكذلك في **المثال 7 ص 5 / PDF ص 57**: المعادلة $(D_x^2 - D_y^2 - 3D_x + 3D_y)z = 0$ نحللها بالتجميع أولاً: $(D_x - D_y)(D_x + D_y) - 3(D_x - D_y) = (D_x - D_y)(D_x + D_y - 3)z = 0 \implies \boxed{z = \phi_1(y + x) + e^{3x}\phi_2(y - x)}$!)*

---
### الحالتان (C) و (D): المؤثرات غير القابلة للتحليل (Irreducible Operators — الباب الثاني ص 5–8 / PDF ص 57–60)
* **متى نستخدم الحالة (C)؟** عندما لا يمكن تحليل $F(D_x, D_y)$ إلى عوامل خطية من الدرجة الأولى، مثل $(D_x - D_y^3)z = 0$ أو $(D_x^2 + D_x + D_y)z = 0$ أو معادلة الحرارة $(D_x^2 - D_y)z = 0$.
* **قاعدة الحل في المذكرة (ص 5–6 / PDF ص 57–58):**
  نفرض الحل في صورة متسلسلة من الدوال الأسية:
  $$\boxed{z = \sum_{i=1}^{\infty} A_i\, e^{a_i x + b_i y} \qquad \text{بشرط أن تحقق } (a_i, b_i)\text{ المعادلة المميزة: } F(a_i, b_i) = 0}$$
  حيث $A_i$ و $a_i$ (أو $b_i$) ثوابت اختيارية!
* **📖 الأمثلة المحلولة في المذكرة (أمثلة 8 و 9 و 11 — ص 6–7 / PDF ص 58–59):**
  1. **مثال 8:** حل $(D_x - D_y^3)z = 0$.
     * المؤثر غير قابل للتحليل لأن $D_x$ من الرتبة 1 و $D_y^3$ من الرتبة 3!
     * نضع $D_x \to a_i$ و $D_y \to b_i$ في الشرط $F(a_i, b_i) = 0 \implies a_i - b_i^3 = 0 \implies \boxed{a_i = b_i^3}$.
     * نعوض عن $a_i$ بـ $b_i^3$ في المتسلسلة الأسية:
       $$\boxed{z = \sum_{i=1}^{\infty} A_i\, e^{b_i^3 x + b_i y}}$$
  2. **مثال 9:** حل $(D_x^2 + D_x + D_y)z = 0$.
     * الشرط المميز: $a_i^2 + a_i + b_i = 0 \implies \boxed{b_i = -a_i^2 - a_i = -a_i(a_i + 1)}$.
     * الحل العام: $\boxed{z = \sum_{i=1}^{\infty} A_i\, e^{a_i x - a_i(a_i + 1)y}}$.
  3. **الحالة (D) — مزيج من عامل خطي قابل للتحليل وعامل غير قابل للتحليل (مثال 11 ص 7 / PDF ص 59):**
     * في $(D_x - D_y - 1)(D_x - D_y^2)z = 0$:
       * العامل الأول خطي يعطي: $z^{(1)} = e^x \phi(y + x)$.
       * العامل الثاني $(D_x - D_y^2)$ غير قابل للتحليل ($a_i = b_i^2$) يعطي: $z^{(2)} = \sum_{i=1}^{\infty} A_i e^{b_i^2 x + b_i y}$.
       * نجمعهما معاً: $\boxed{z = e^x \phi(y + x) + \sum_{i=1}^{\infty} A_i e^{b_i^2 x + b_i y}}$!

---
### رابعاً: التكامل الخاص (P.I.) في الباب الثاني وحيلة "المرافق التفاضلي" (الباب الثاني ص 8–10 / PDF ص 60–62)

لإيجاد التكامل الخاص $z_2 = \frac{1}{F(D_x, D_y)}f(x, y)$ للمعادلات غير المتجانسة في الرتبة، نستخدم نفس قواعد اللاب 4 مع **مهارتين مهمتين جداً** في نهاية المذكرة:

#### 1. فك كثيرات الحدود بسحب أصغر مشتقة (مثال 12 ص 8 / PDF ص 60)
* **المسألة:** أوجد الحل العام لـ $(D_x^2 - D_y^2 + D_x)z = x^2 + 2y$.
  * لحساب التكامل الخاص $z_2 = \frac{1}{D_x^2 - D_y^2 + D_x}(x^2 + 2y)$، نسحب **أصغر مشتقة وهي $D_x$** من المقام:
    $$z_2 = \frac{1}{D_x\left[1 - \left(\frac{D_y^2}{D_x} - D_x\right)\right]}(x^2 + 2y) = \frac{1}{D_x}\left[1 + \left(\frac{D_y^2}{D_x} - D_x\right) + \left(\frac{D_y^2}{D_x} - D_x\right)^2 + \dots\right](x^2 + 2y)$$
  * بما أن $D_y^2(x^2 + 2y) = 0$، تختفي كل حدود $D_y^2$! ويبقى فقط:
    $$z_2 = \frac{1}{D_x}\left(1 - D_x + D_x^2\right)(x^2 + 2y) = \frac{1}{D_x}\left[(x^2 + 2y) - (2x) + 2\right] = \boxed{\frac{x^3}{3} + 2xy - x^2 + 2x}$$

#### 2. حيلة الضرب في المرافق لدوال $\sin$ و $\cos$ عندما تبقى مشتقة من الرتبة الأولى! (مثال 14 ص 9–10 / PDF ص 61–62)
* **المسألة:** أوجد الحل العام لـ $(D_x^2 - D_y)z = \sin(x - 2y)$.
  1. **الحل المكمل $z_1$:** المؤثر $(D_x^2 - D_y)$ غير قابل للتحليل ($a_i^2 - b_i = 0 \implies b_i = a_i^2$)، إذن $z_1 = \sum_{i=1}^{\infty} A_i e^{a_i x + a_i^2 y}$.
  2. **التكامل الخاص $z_2$:** هنا $f(x,y) = \sin(x - 2y)$ حيث $a = 1,\; b = -2$.
     * قاعدة الجيب تستبدل المشتقات **من الرتبة الثانية فقط** ($D_x^2 \to -a^2 = -1$ و $D_y^2 \to -b^2 = -4$)، ولكن المقام هنا هو $(D_x^2 - D_y)$ فيحتوي على $D_y$ من الرتبة الأولى!
     * **الخطوة 1:** عوض عن $D_x^2 \to -1$ أولاً:
       $$z_2 = \frac{1}{-1 - D_y}\sin(x - 2y)$$
     * **الخطوة 2 (حيلة المرافق!):** كيف نتخلص من $D_y$ في المقام ونحولها إلى $D_y^2$؟ نضرب البسط والمقام في **المرافق $(-1 + D_y)$**!
       $$z_2 = \frac{-1 + D_y}{(-1 - D_y)(-1 + D_y)}\sin(x - 2y) = \frac{-1 + D_y}{1 - D_y^2}\sin(x - 2y)$$
     * **الخطوة 3:** الآن ظهر $D_y^2$ في المقام! نعوض عنه بـ $-b^2 = -(-2)^2 = -4$:
       $$z_2 = \frac{-1 + D_y}{1 - (-4)}\sin(x - 2y) = \frac{1}{5}(-1 + D_y)\sin(x - 2y)$$
     * **الخطوة 4:** الآن $(-1 + D_y)$ في البسط يعني ببساطة: اضرب في $-1$ ثم اجمع المشتقة الجزئية بالنسبة لـ $y$ ($D_y[\sin(x-2y)] = -2\cos(x-2y)$):
       $$\boxed{z_2 = \frac{1}{5}\big[-\sin(x - 2y) - 2\cos(x - 2y)\big]}$$

---
### ⚠️ أخطاء شائعة في الإشارات يجب الحذر منها
1. **نسيان إشارة السالب في الأس $-\frac{c}{a}x$:** إذا كان $c$ موجباً (مثل $+1$)، يكون الأس سالباً ($-x/a$)؛ وإذا كان $c$ سالباً (مثل $-2$)، يصبح الأس موجباً ($+2x/a$).
2. **نسيان إشارة السالب في $(ay - bx)$:** القانون يحتوي على طرح $-bx$! فإذا كان $b = -3$، تصبح $ay - (-3)x = ay + 3x$.
""")

    nb.md(r"""---
## 4. 📝 تحدي الورقة والقلم 1 (المثال 5 من الباب الثاني ص 4 / PDF ص 56)

**المسألة:** أوجد الحل العام للمعادلة التفاضلية الجزئية القابلة للتحليل:
$$(2 D_x - 3 D_y + 1)(D_x + 2 D_y - 2)z = 0$$

اكتب صيغة الحل العام بدلالة `x, y` والدالتين الاختياريتين `Phi1(...)` و `Phi2(...)` والدالة الأسية `exp(...)`:

<details>
<summary>💡 <b>تلميح 1 (العامل الأول)</b></summary>

للعامل $(2 D_x - 3 D_y + 1)$: $a_1=2, b_1=-3, c_1=1 \implies \text{exp}(-x/2)\text{*Phi1}(2y + 3x)$.
</details>

<details>
<summary>💡 <b>تلميح 2 (العامل الثاني والجمع)</b></summary>

للعامل $(D_x + 2 D_y - 2)$: $a_2=1, b_2=2, c_2=-2 \implies \text{exp}(2x)\text{*Phi2}(y - 2x)$. اجمع الحدين معاً.
</details>
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
# اكتب الحل العام بدلالة exp(...) و Phi1(...) و Phi2(...):
student_solution = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_1(student_solution)
""")

    nb.md(r"""---
## 5. 🚀 تحدي الورقة والقلم 2 (حساب معدل الاضمحلال الأسي $k = -c/a$)

**المسألة:** لنفرض أن نمطاً موجياً يخضع للمعادلة العاملية الخطية:
$$(D_x + 2 D_y + 1)z = 0$$

**على ورقتك:**
1. استخرج المعاملات $a, b, c$ من العامل $(a D_x + b D_y + c)$.
2. في الحل العام $z = e^{k x} \Phi(a y - b x)$، يُعطى معدل التخميد الأسي بالعلاقة $k = -\frac{c}{a}$.
3. احسب القيمة العددية لـ $k$ وأدخلها أدناه:

<details>
<summary>💡 <b>تلميح (اضغط هنا إذا احتجت مساعدة)</b></summary>

معامل $D_x$ هو $a = 1$، والحد الثابت هو $c = 1$. إذن $k = -c/a = -1/1$.
</details>
""")

    if solutions:
        nb.code(r"""# خلية تقييم: معدل الاضمحلال الأسي
### START CODE HERE ###
damping_rate = -1.0
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_2(damping_rate)
""")
    else:
        nb.code(r"""# خلية تقييم: معدل الاضمحلال الأسي
### START CODE HERE ### (≈ 1 line of code)
# أدخل القيمة العددية لمعدل الاضمحلال الأسي k = -c/a:
damping_rate = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab5.check_paper_challenge_2(damping_rate)
""")

    nb.md(r"""---
## 6. 💻 التطبيق البرمجي ببايثون: محلل معاملات العوامل الخطية (`parse_linear_factor`)

نريد كتابة دالة برمجية تستقبل نص عامل خطي مثل `"2*D_x - 3*D_y - 5"` وتستخرج منه المعاملات العددية الثلاثة `(a, b, c)` تلقائياً لحساب معدل الاضمحلال الأسي $-c/a$ وزاوية الانتشار $(a, -b)$.
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: parse_linear_factor
def parse_linear_factor(factor_str: str) -> tuple[float, float, float]:
    # تستخرج المعاملات (a, b, c) من نص العامل الخطي "a*D_x + b*D_y + c"
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
    # تستخرج المعاملات (a, b, c) من نص العامل الخطي (مثال: "2*D_x - 3*D_y - 5" -> (2.0, -3.0, -5.0))
    ### START CODE HERE ### (≈ 8-12 lines of code)
    import re
    # يمكنك استخدام التعبيرات النمطية (re.search) أو تحليل السلسلة النصية لاستخراج a, b, c:
    a = None
    b = None
    c = None
    ### END CODE HERE ###
    return a, b, c

# تشغيل الاختبار الآلي:
test_lab5.test_linear_factor_evaluator(parse_linear_factor)
''')

    nb.md(r"""---
## 7. 🎨 الرؤية البصرية والربط المباشر بملف `rover_path_finder/planners.py`

شغّل الخلية التالية لترى:
1. **على اليسار:** السطح الأسي المتلاشي $z = e^{-0.5x}\sin(y - 2x)$ الناتج عن العامل الخطي $(2D_x + D_y + 1)z = 0$.
2. **على اليمين:** مقارنة حقيقية من كود المشروع [`rover_path_finder/planners.py`](rover_path_finder/planners.py) بين دالة `dirichlet_potential` (التي ينهار فيها انحدار الجهد أسياً بمعدل $e^{-\pi x / w}$ داخل ممر ضيق فتتوقف المركبة!) ودالة `neumann_potential` (التي تعزل جدران الممر $\partial\phi/\partial n = 0$ فينحدر الجهد خطياً بسلاسة من البداية إلى الهدف!).
""")

    nb.code(r"""from rover_path_finder.planners import dirichlet_potential, neumann_potential

# 1. السطح التحليلي للعامل الخطي (2 D_x + D_y + 1)z = 0
x = np.linspace(0, 5, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.exp(-0.5 * X) * np.sin(Y - 2.0 * X)

# 2. تجربة ممر ضيق بين جدارين باستخدام دوال المشروع الفعلية
corridor_hazard = np.zeros((40, 60), dtype=bool)
corridor_hazard[:16, 15:45] = True   # الجدار العلوي للممر الضيق
corridor_hazard[24:, 15:45] = True   # الجدار السفلي للممر الضيق (عرض الممر w = 8 بكسل)
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

print("📌 ملخص اللاب 5:")
print("  1) العامل الخطي (a*D_x + b*D_y + c)z = 0 ينتج حلاً مضروباً في غلاف أسي exp(-(c/a)*x).")
print("  2) في الممرات الضيقة، شرط ديريكليه على الجدران يخلق تلاشيًا أسيًا exp(-pi*x/w) يوقف المركبة.")
print("  3) لهذا السبب يستخدم محرك الملاحة في اللاب 6 شروط نيومان العازلة (neumann_potential) بدلاً من ديريكليه!")
""")

    nb.save()


# ===========================================================================
# LAB 6 (ARABIC): CAPSTONE MARS ROVER NAVIGATION
# ===========================================================================
def build_lab_6_ar(solutions: bool = False, target_dir: str = "labs_ar"):
    nb = ArabicNotebookBuilder("Lab_6_Mars_Rover_Capstone_AR.ipynb", target_dir=target_dir)
    nb.colab_badge()
    nb.colab_setup()

    nb.md(r"""# 🚀 اللاب 6: المشروع النهائي الشامل — الفروق المحدودة، خوارزمية SOR، والملاحة الذاتية على المريخ
### *غرفة التحكم: دمج المعادلات التفاضلية الجزئية في محرك ملاحة المركبة الكامل*
**المقرر:** المعادلات التفاضلية الجزئية وتطبيقاتها في الملاحة الفضائية (Applied PDE & Planetary Robotics)  
**المرجع:** التكامل التطبيقي الشامل لما درسناه في اللابات 1–5 مع الكود الفعلي في [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py) و [`rover_path_finder/planners.py`](rover_path_finder/planners.py)

---
### 🗺️ خريطة الكورس الكاملة: كيف تجمّعت قطع الليغو الخمس (اللابات 1–5) لبناء محرك الملاحة؟
```
[اللاب 1: حساب الميول slope_map] ──► [اللاب 2: خطوط لاجرانج descend] ──► [اللاب 3: مسافة الأمان dilate]
                                                                                      │
📍 [اللاب 6: الحل العددي SOR + Neumann وإطلاق المركبة] ◄── [اللاب 5: مشكلة الممرات الضيقة] ◄── [اللاب 4: معادلة لابلاس _avg]
```

| قطعة البناء (اللاب) | القانون الرياضي في مذكرة الـ PDF (ص 1–62) | المهمة الهندسية التي يحلها داخل مركبة المريخ | الدالة الفعلية في المشروع (`rover_path_finder/`) |
| :--- | :--- | :--- | :--- |
| **🧱 القطعة 1 (اللاب 1)** | $p = \frac{\partial z}{\partial x},\; q = \frac{\partial z}{\partial y}$ وحذف الثوابت الاختيارية *(PDF ص 2–11)* | قياس ميل التضاريس $\|\nabla z\| = \sqrt{p^2+q^2}$ واكتشاف المنحدرات الخطرة (`> 0.30`) | [`terrain.slope_map(elev)`](rover_path_finder/terrain.py) |
| **🧱 القطعة 2 (اللاب 3)** | المعادلات غير الخطية ومعادلة المسافة $p^2 + q^2 = 1$ *(PDF ص 17–27)* | توسيع كل صخرة وحفرة بمقدار نصف قطر جسم المركبة $R$ لمنع اصطدام العجلات | [`terrain.dilate(raw, rover_radius)`](rover_path_finder/terrain.py) |
| **🧱 القطعة 3 (اللاب 4)** | معادلة لابلاس $(D_x^2 + D_y^2)\phi = 0$ والجذور المركبة $m = \pm i$ *(PDF ص 28–51)* | بناء سطح جهد توافقي أملس يستحيل رياضياً أن يحتوي على أي قاع محلي يحبس المركبة | [`solvers._avg(phi)`](rover_path_finder/solvers.py) |
| **🧱 القطعة 4 (اللاب 5)** | العامل الخطي $(aD_x+bD_y+c)z=0 \implies e^{-(c/a)x}$ *(PDF ص 52–62)* | تفسير تلاشي الجهد $e^{-\pi x/w}$ في الممرات الضيقة واستبدال ديريكليه بشرط نيومان العازل | [`planners.neumann_potential()`](rover_path_finder/planners.py) |
| **🧱 القطعة 5 (اللاب 2)** | معادلة لاجرانج للخصائص $\frac{dx}{P} = \frac{dy}{Q} = \frac{dz}{R}$ *(PDF ص 12–17)* | تتبع خط الانسياب الأشد انحداراً $(-\phi_x, -\phi_y)$ لقيادة المركبة من البداية للهدف | [`planners.descend(phi, hazard, start, goal)`](rover_path_finder/planners.py) |

---
### 🧭 حجر رشيد (The Rosetta Stone): الربط المباشر بين المعادلات وملفات المشروع

| 1. المفهوم الرياضي | 2. المعنى الفيزيائي والهندسي | 3. الكود الفعلي في `rover_path_finder/` |
| :--- | :--- | :--- |
| $\nabla^2\phi = \frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$ | **معادلة لابلاس (من اللاب 4):** حقل جهد توافقي خالٍ تماماً من القيعان المحلية | المعادلة الحاكمة في [`solvers.py`](rover_path_finder/solvers.py) |
| $\phi_{i,j} = \frac{1}{4}(\phi_{i+1,j} + \phi_{i-1,j} + \phi_{i,j+1} + \phi_{i,j-1})$ | **قالب النقاط الخمس (5-Point Stencil):** تقريب المشتقات الثانية على شبكة بكسل | الدالة [`_avg(phi)`](rover_path_finder/solvers.py) في `solvers.py` |
| $\frac{\partial\phi}{\partial n} = 0$ على حدود العوائق | **شرط نيومان العازل (من اللاب 5):** الجهد ينساب حول الصخور ولا يتلاشى في الممرات الضيقة | قسمة مجموع الجيران الحرة على عددها الفعلي `cnt` في [`sor_neumann`](rover_path_finder/solvers.py) |
| $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi/N)}$ | **معامل الاسترخاء الفائق المتتالي (SOR):** تسريع تقارب الشبكة عشرات المرات | الدالة [`optimal_omega(N)`](rover_path_finder/solvers.py) في `solvers.py` |
| $\frac{dx}{-\phi_x} = \frac{dy}{-\phi_y}$ | **معادلة لاجرانج لخطوط الانسياب (من اللاب 2):** تتبع المسار من البداية للهدف | الدالة [`descend(phi, hazard, start, goal)`](rover_path_finder/planners.py) |

---
## 1. لماذا ننتقل من الحل التحليلي بالورقة والقلم إلى الحل العددي على الشبكة؟

في اللابات 1 إلى 5، حللنا المعادلات التفاضلية الجزئية تحليلياً بالورقة والقلم على نطاقات هندسية بسيطة.
ولكن في مشروع مركبة المريخ لدينا:
* بيئة الاختبار القياسية `make_terrain(N=100)` تتكون من شبكة **$100 \times 100 = 10,000$ عقدة**، وتضاريس وادي كاسي المريخية الحقيقية (`kasei.IMG` في `main.py`) تصل إلى **$160 \times 160 = 25,600$ عقدة** مع آلاف الصخور والحفر غير المنتظمة!
* يستحيل كتابة دالة تحليلية مغلقة واحدة تحقق شرط العزل $\frac{\partial\phi}{\partial n} = 0$ على حدود آلاف الصخور المتعرجة.
* لذلك نحول معادلة لابلاس المستمرة $\nabla^2\phi = 0$ إلى نظام معادلات جبرية على الشبكة باستخدام **طريقة الفروق المحدودة (Finite Difference Method)** ونحله تكرارياً بسرعة فائقة باستخدام **خوارزمية Red-Black SOR**.

> 📌 **ملاحظة منهجية صادقة:** دراسة معادلة لابلاس التحليلية $(D_x^2 + D_y^2)z = 0$ موجودة في المذكرة (ص 39 / PDF ص 33)، أما **تقطيع الشبكة (5-Point Stencil) ومبدأ القيمة العظمى (Maximum Principle) وخوارزمية SOR** فهي الإثراء العددي والهندسي الذي يربط مذكرة المحاضرات بمحرك البرمجيات الحقيقي في [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py).
""")

    nb.code(r"""import numpy as np
import matplotlib.pyplot as plt
from labs.tests import test_lab6

%matplotlib inline
print("تم تهيئة اللاب 6 النهائي بنجاح!")
""")

    nb.md(r"""---
## 2. الاشتقاق الرياضي خطوة بخطوة: من متسلسلة تايلور إلى برهان استحالة المصائد المحلية

### أولاً: اشتقاق قالب النقاط الخمس (5-Point Stencil) من متسلسلة تايلور
عند أي عقدة داخلية $(i, j)$ تبعد مسافة $h$ عن جيرانها الأربعة:
$$\phi_{i+1, j} = \phi_{i,j} + h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} + \frac{h^3}{6}\left.\frac{\partial^3\phi}{\partial x^3}\right|_{i,j} + \mathcal{O}(h^4)$$
$$\phi_{i-1, j} = \phi_{i,j} - h \left.\frac{\partial\phi}{\partial x}\right|_{i,j} + \frac{h^2}{2}\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} - \frac{h^3}{6}\left.\frac{\partial^3\phi}{\partial x^3}\right|_{i,j} + \mathcal{O}(h^4)$$

بجمع المعادلتين معاً، تختفي المشتقات الفردية ($\partial\phi/\partial x$ و $\partial^3\phi/\partial x^3$) تماماً:
$$\left.\frac{\partial^2\phi}{\partial x^2}\right|_{i,j} \approx \frac{\phi_{i+1, j} - 2\phi_{i,j} + \phi_{i-1, j}}{h^2}, \qquad \left.\frac{\partial^2\phi}{\partial y^2}\right|_{i,j} \approx \frac{\phi_{i, j+1} - 2\phi_{i,j} + \phi_{i, j-1}}{h^2}$$

بالتعويض في معادلة لابلاس $\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0$ والضرب في $h^2$:
$$(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}) - 4\phi_{i,j} = 0 \implies \boxed{\phi_{i,j} = \frac{1}{4}\left(\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1}\right)}$$

---
### ثانياً: البرهان الرياضي البسيط لاستحالة وجود أي مصيدة محلية (Discrete Maximum Principle)
لماذا نضمن بنسبة 100% أن المركبة لن تعلق أبداً في أي حفرة جهد وهمية (Local Minimum)؟
* **البرهان في سطر واحد:** لنفترض جدلاً أن عقدة داخلية حرة $(i,j)$ هي "قاع محلي صارم" (Strict Local Minimum)، أي أن قيمتها أصغر من جميع جيرانها الأربعة:
  $$\phi_{i,j} < \phi_{\text{North}}, \quad \phi_{i,j} < \phi_{\text{South}}, \quad \phi_{i,j} < \phi_{\text{East}}, \quad \phi_{i,j} < \phi_{\text{West}}$$
* بجمع المتباينات الأربع والقسمة على 4 نحصل على:
  $$\phi_{i,j} < \frac{1}{4}\left(\phi_{\text{North}} + \phi_{\text{South}} + \phi_{\text{East}} + \phi_{\text{West}}\right)$$
* ولكن معادلة لابلاس تفرض المساواة التامة $\phi_{i,j} = \frac{1}{4}(\phi_N + \phi_S + \phi_E + \phi_W)$! **تناقض رياضي مستحيل!**
* إذن: **لا يمكن لأي عقدة داخلية حرة أن تكون قاعاً محلياً**؛ القاع الوحيد على الخريطة بأكملها هو نقطة الهدف نفسها ($\phi = 0$)!

---
### ثالثاً: كيف نطبق شرط نيومان العازل ($\frac{\partial\phi}{\partial n} = 0$) على جدران الحفر؟
إذا كان أحد الجيران الأربعة صخرة أو عائقاً (`free == False`)، فلا يجب أن نأخذ قيمته في المتوسط! بدلاً من القسمة على 4 دائماً، نجمع **فقط الجيران الحرة المتاحة** (`pf = phi * f`) ونقسم على **عدد الجيران الحرة الفعلي** `cnt` (والذي قد يكون 3 بمحاذاة جدار مستقيم، أو 2 في زاوية):
$$\phi_{i,j} = \frac{\sum_{\text{free neighbors}} \phi_{\text{neighbor}}}{\text{cnt}_{i,j}}$$
وهذا يكافئ رياضياً جعل المشتقة العمودية على الجدار تساوي صفراً ($\frac{\partial\phi}{\partial n} = 0$).
""")

    nb.md(r"""---
## 3. 📝 تحدي الورقة والقلم 1 (الحساب اليدوي للتكرار الأول بطريقة جاكوبي — Jacobi Sweep 1)

لكي تشعر بما يفعله الكود في كل تكرار، لنحسب يدوياً **المسحة الأولى بطريقة جاكوبي المتزامنة (Jacobi Sweep 1)** على شبكة صغيرة $4 \times 4$ تحتوي على 4 خلايا داخلية $(A, B, C, D)$ مهيأة في البداية بالقيمة $\phi^{(0)} = 0.0$:

```
            الحد العلوي (ثابت: phi = 1.0)
         +--------+--------+--------+--------+
         |  1.0   |  1.0   |  1.0   |  1.0   |
         +--------+--------+--------+--------+
الحد     |  0.5   | A(0.0) | B(0.0) |  0.5   | الحد الأيمن
الأيسر   +--------+--------+--------+--------+ (ثابت Dirichlet:
(ثابت:   |  0.5   | C(0.0) | D(0.0) |  0.5   |  phi = 0.5)
phi=0.5) +--------+--------+--------+--------+
         |  0.0   |  0.0   |  0.0   |  0.0   |
         +--------+--------+--------+--------+
            الحد السفلي (ثابت: phi = 0.0)
```

> 📌 **ملاحظة مهمة:** في طريقة **جاكوبي (Jacobi)**، نحسب جميع القيم الجديدة $\phi^{(1)}$ باستخدام القيم القديمة $\phi^{(0)} = 0.0$ فقط:
> * جيران الخلية $A$ في البداية هم: أعلى $= 1.0$، أسفل ($C^{(0)}$) $= 0.0$، يسار $= 0.5$، يمين ($B^{(0)}$) $= 0.0$.
> * جيران الخلية $B$ في البداية هم: أعلى $= 1.0$، أسفل ($D^{(0)}$) $= 0.0$، يسار ($A^{(0)}$) $= 0.0$، يمين $= 0.5$.
> *(معلومة إضافية: لو كنا نستخدم طريقة Gauss-Seidel المتسلسلة، لكنا استخدمنا قيمة $A^{(1)} = 0.375$ الجديدة فوراً عند حساب $B^{(1)}$ فتعطي $0.46875$؛ لكن هنا نطلب تحديث **جاكوبي المتزامن**).*

احسب $\phi_A^{(1)}$ و $\phi_B^{(1)}$ بطريقة جاكوبي وأدخلهما أدناه:

<details>
<summary>💡 <b>تلميح (اضغط هنا إذا احتجت مساعدة)</b></summary>

اجمع الجيران الأربعة الابتدائيين للخلية $A$: $(1.0 + 0.0 + 0.5 + 0.0) / 4 = 1.5 / 4$. وبسبب التماثل الأفقي للشبكة، فإن الخلية $B$ لها نفس مجموع الجيران الابتدائيين تماماً!
</details>
""")

    if solutions:
        nb.code(r"""# خلية تقييم: حساب الشبكة اليدوي (Jacobi Sweep 1)
### START CODE HERE ###
phi_A = 0.375
phi_B = 0.375
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_1(phi_A, phi_B)
""")
    else:
        nb.code(r"""# خلية تقييم: حساب الشبكة اليدوي (Jacobi Sweep 1)
### START CODE HERE ### (≈ 2 lines of code)
# أدخل القيمتين العشريتين لـ phi_A و phi_B بعد المسحة الأولى بطريقة جاكوبي:
phi_A = None
phi_B = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_1(phi_A, phi_B)
""")

    nb.md(r"""---
## 4. 🚀 تحدي الورقة والقلم 2 (معامل الاسترخاء الأمثل $\omega_{\text{opt}}$ — الدالة `optimal_omega`)

طريقة جاكوبي بطيئة جداً على الشبكات الكبيرة لأن المعلومات تنتقل بمعدل خلية واحدة في كل تكرار.
لتسريع الحل عشرات المرات، نستخدم **الاسترخاء الفائق المتتالي (Successive Over-Relaxation - SOR)**، الذي يأخذ خطوة جريئة في اتجاه التغيير بمعامل تضخيم $\omega \in (1, 2)$:
$$\phi_{i,j}^{\text{new}} = (1 - \omega)\,\phi_{i,j}^{\text{old}} + \omega\,\text{avg}_{i,j}$$

وفقاً لنظرية يونغ (Young's Theorem) المطبقة في دالة [`optimal_omega(N)`](rover_path_finder/solvers.py) في ملف `solvers.py`، يُعطى المعامل الأمثل لشبكة حجمها $N$ بالعلاقة:
$$\omega_{\text{opt}} = \frac{2}{1 + \sin\left(\frac{\pi}{N}\right)}$$

احسب قيمة $\omega_{\text{opt}}$ عندما يكون $N = 16$:

<details>
<summary>💡 <b>تلميح (اضغط هنا إذا احتجت مساعدة)</b></summary>

عوض بـ $N = 16$ في القانون `2.0 / (1.0 + np.sin(np.pi / 16))` (أو احسبها بالآلة الحاسبة بوضع الراديان: $\sin(\pi/16) \approx 0.19509 \implies \omega_{\text{opt}} \approx 1.6735$).
</details>
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
# احسب قيمة أوميجا المثلى لـ N=16:
omega_16 = None
### END CODE HERE ###

# تشغيل اختبار التحقق التلقائي:
test_lab6.check_paper_challenge_2(omega_16)
""")

    nb.md(r"""---
## 5. 💻 التطبيق البرمجي ببايثون: بناء محرك `sor_neumann_step` الفعلي

الآن ستكتب بنفسك القلب النابض لملف [`rover_path_finder/solvers.py`](rover_path_finder/solvers.py): دالة `sor_neumann_step` التي تجمع بين:
1. **تقسيم رقعة الشطرنج (Red-Black Ordering):** تحديث الخلايا الحمراء (`(x + y) % 2 == 0`) دفعة واحدة باستخدام متجهات NumPy السريعة، ثم تحديث الخلايا السوداء (`(x + y) % 2 == 1`) بالاعتماد على القيم الحمراء المحدثة للتو!
2. **شرط نيومان العازل (`pf = phi * f` والقسمة على `cnt`):** لضمان عدم تسرب الجهد داخل العوائق.
3. **تحديث الاسترخاء الفائق (SOR):** `phi[mk] = (1 - omega) * old + omega * avg[mk]`.
""")

    if solutions:
        nb.code(r'''# دالة تقييم برمجية: sor_neumann_step
def sor_neumann_step(phi, fixed, free, omega=1.5, tol=1e-5, maxit=5000):
    # خوارزمية Red-Black SOR مع جدران نيومان العازلة للعوائق (مطابقة لـ solvers.py)
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    
    # حساب عدد الجيران الحرة (من 1 إلى 4) لكل خلية لتطبيق شرط نيومان d(phi)/dn = 0
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
    # خوارزمية Red-Black SOR مع جدران نيومان العازلة للعوائق (مطابقة لـ solvers.py)
    phi = phi.copy()
    n, m = phi.shape
    f = free.astype(float)
    
    # حساب عدد الجيران الحرة (من 1 إلى 4) لكل خلية لتطبيق شرط نيومان d(phi)/dn = 0
    cnt = sum(np.roll(f, s, a) for a in (0, 1) for s in (1, -1))
    cnt = np.maximum(cnt, 1.0)
    
    yy, xx = np.mgrid[0:n, 0:m]
    parity = (xx + yy) % 2
    masks = [(parity == c) & free & ~fixed for c in (0, 1)]
    phi[~free] = 0.0
    hist = []
    
    ### START CODE HERE ### (≈ 10-14 lines of code)
    # كرر حتى maxit:
    # 1. اجعل d = 0.0
    # 2. لكل قناع mk في masks:
    #        أ) صفر قيم العوائق: pf = phi * f
    #        ب) احسب متوسط الجيران الحرة:
    #           avg = (np.roll(pf, 1, 0) + np.roll(pf, -1, 0) + np.roll(pf, 1, 1) + np.roll(pf, -1, 1)) / cnt
    #        ج) احفظ القيم القديمة: old = phi[mk]
    #        د) طبق تحديث SOR: phi[mk] = (1 - omega) * old + omega * avg[mk]
    #        هـ) حدث أقصى فرق: d = max(d, float(np.abs(phi[mk] - old).max()))
    # 3. أضف d إلى القائمة hist: hist.append(d)
    # 4. إذا كان d < tol: اخرج من الحلقة (break)
    pass
    ### END CODE HERE ###
    
    return phi, hist

# تشغيل الاختبار الآلي:
test_lab6.test_sor_neumann_step(sor_neumann_step)
''')

    nb.md(r"""---
## 6. 🌉 لماذا تتفوق معادلة لابلاس على طريقة المجالات الاصطناعية الكلاسيكية (APF)؟

في الروبوتات التقليدية، تستخدم طريقة **مجال الجهد الاصطناعي (Artificial Potential Field - APF)** الموجودة في [`planners.apf_potential`](rover_path_finder/planners.py) جمعاً جبرياً بسيطاً لجهد جاذب نحو الهدف وجهد طارد من الصخور:
$$U(\mathbf{x}) = U_{\text{att}}(\mathbf{x}) + U_{\text{rep}}(\mathbf{x})$$

**أين تكمن الكارثة الهندسية في APF؟**
* عندما تواجه المركبة عائقاً مقعراً أو حفرة على شكل حرف **U**، تسحب قوة الجذب المركبة للأمام نحو الهدف خلف الجدار، بينما تدفعها قوة التنافر للخلف بعيداً عن الجدار.
* عند نقطة داخل الحفرة، **تتساوى القوتان في المقدار وتتعاكسان في الاتجاه** ($\nabla U = \mathbf{0}$)، فتتكون **مصيدة قاع محلي (Local Minimum Trap)** لأن $\nabla^2 U \neq 0$!
* أما في **معادلة لابلاس ($\nabla^2\phi = 0$)** مع شروط نيومان العازلة (`neumann_potential`)، فقد أثبتنا رياضياً بمبدأ القيمة العظمى استحالة وجود أي قاع محلي داخل المجال؛ لذلك يلتف تيار الجهد بسلاسة حول جدار الحفرة ويقود المركبة بأمان تام إلى الهدف!

---
## 7. 🎨 الإطلاق النهائي للمهمة: الملاحة الذاتية على تضاريس المريخ (`100x100`)

شغّل الخلية التالية لتوليد التضاريس المريخية وحل معادلة لابلاس واستخراج مسار المركبة (لاحظ كيف يتفادى المسار السماوي جميع مناطق الخطر الحمراء بفضل توافق الإحداثيات $(x, y)$ مع `descend`):
""")

    nb.code(r"""from rover_path_finder.terrain import make_terrain
from rover_path_finder.planners import neumann_potential, descend, apf_potential, trap_map

# 1. توليد تضاريس مريخية 100x100 (10,000 عقدة) مع توسيع العوائق بنصف قطر المركبة
t_data = make_terrain(N=100, seed=42, rover_radius=3)
elev, raw_hazards, hazards = t_data["h"], t_data["raw"], t_data["hazard"]
start = t_data["start"]
goal = t_data["goal"]

# 2. حل معادلة لابلاس بشروط نيومان العازلة (tol=1e-6 لتنفيذ سريع ودقيق)
phi, sweeps, elapsed = neumann_potential(hazards, start=start, goal=goal, tol=1e-6)

# 3. تتبع مسار الانحدار مع خطوط الانسياب (معادلة لاجرانج من اللاب 2)
path, reached = descend(phi, hazards, start=start, goal=goal)

# 4. رسم حقل الجهد والمسار الفعلي (p[0] هو x=col، و p[1] هو y=row)
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

print(f"✅ حالة المهمة: وصلت المركبة للهدف = {reached} | طول المسار = {len(path)} خطوة | عدد مسحات SOR = {sweeps} ({elapsed:.2f} ثانية)")
""")

    nb.md(r"""---
## 8. 🪤 الاختبار الحاسم: مقارنة مصيدة حرف U (APF مقابل معادلة لابلاس)

شغّل الخلية التالية لمشاهدة المقارنة المباشرة على خريطة المصيدة `trap_map(N=100)`:
* **على اليسار (APF):** تدخل المركبة من $(20, 50)$ باتجاه الهدف $(90, 50)$ فتعلق للأبد داخل جيب حرف U!
* **على اليمين (Laplace PDE):** يلتف المسار السماوي حول جدار المصيدة ويصل إلى الهدف $(90, 50)$ بنجاح تام!
""")

    nb.code(r"""u_trap, trap_start, trap_goal = trap_map(N=100)

# 1. الروبوت التقليدي (APF)
apf_field = apf_potential(u_trap, goal=trap_goal)
apf_path, apf_reached = descend(apf_field, u_trap, start=trap_start, goal=trap_goal, maxsteps=200)

# 2. معادلة لابلاس التوافقية مع شروط نيومان (tol=1e-6)
laplace_field, trap_sweeps, trap_time = neumann_potential(u_trap, start=trap_start, goal=trap_goal, tol=1e-6)
laplace_path, laplace_reached = descend(laplace_field, u_trap, start=trap_start, goal=trap_goal, maxsteps=400)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# رسم الروبوت الكلاسيكي (APF)
axes[0].contourf(apf_field, levels=25, cmap='magma')
axes[0].contour(u_trap, levels=[0.5], colors='white', linewidths=1.5)
axes[0].plot([p[0] for p in apf_path], [p[1] for p in apf_path], 'r-', linewidth=3, label="APF Path (Stuck)")
axes[0].plot(trap_start[0], trap_start[1], 'go', markersize=9, label="Start (20, 50)")
axes[0].plot(trap_goal[0], trap_goal[1], 'y*', markersize=13, label="Goal (90, 50)")
axes[0].set_title("Classical Robotics (APF): TRAPPED in Local Minimum", fontsize=12)
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")
axes[0].legend(loc="upper left")

# رسم معادلة لابلاس (Laplace PDE)
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

print("نتائج المقارنة الحاسمة:")
print(f"  • الروبوت التقليدي (APF) : هل وصل للهدف؟ {apf_reached} (علق داخل المصيدة المقعرة)")
print(f"  • معادلة لابلاس (Laplace) : هل وصل للهدف؟ {laplace_reached} (التف حول الجدار ووصل للهدف في {len(laplace_path)} خطوة و {trap_time:.2f} ثانية!)")
""")

    nb.md(r"""## 🏆 شهادة إتمام الكورس التطبيقي للمعادلات التفاضلية الجزئية

**تهانينا الحارة على إتمام اللابات الستة بنجاح!**

لقد بنيت بيدك الجسر الكامل بين **مذكرة المعادلات التفاضلية الجزئية** و**محرك ملاحة الفضاء `PDE-Rover-Engine`**:
1. **اللاب 1 (حذف الثوابت الاختيارية):** فهمت معنى المشتقتين الجزئيتين $(p, q)$ وربطتهما بحساب خريطة انحدار التضاريس [`terrain.slope_map`](rover_path_finder/terrain.py).
2. **اللاب 2 (طريقة لاجرانج $Pp+Qq=R$):** اشتققت المنحنيات المميزة وربطتها بمتتبع خطوط انسياب الحركة [`planners.descend`](rover_path_finder/planners.py).
3. **اللاب 3 (المعادلات غير الخطية وطريقة شاربيت):** حللت معادلة المسافة $p^2+q^2=1$ وربطتها بتوسيع العوائق بنصف قطر الأمان [`terrain.dilate`](rover_path_finder/terrain.py).
4. **اللاب 4 (المؤثرات المتجانسة من الرتب العليا):** حللت معادلة لابلاس $(D_x^2+D_y^2)z=0$ وفهمت لماذا تحقق دوالها التوافقية خاصية متوسط الجيران الأربعة [`solvers._avg`](rover_path_finder/solvers.py).
5. **اللاب 5 (المؤثرات غير المتجانسة في الرتبة):** حللت العوامل الخطية $(aD_x+bD_y+c)z=0$ وفهمت لماذا يتلاشى انحدار ديريكليه أسياً في الممرات الضيقة.
6. **اللاب 6 (الفروق المحدودة وخوارزمية SOR):** برمجت محرك `sor_neumann_step` مع شروط نيومان العازلة وأثبتَّ عملياً كيف تتغلب معادلة لابلاس على مصائد حرف U التي تعجز عنها خوارزميات الروبوتات التقليدية!
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
