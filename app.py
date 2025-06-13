import streamlit as st
import sympy as sp
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 固定値
a, b = 3, 2

# 図のサイズ設定
FIG_W, FIG_H = 8, 2

# 前処理関数（\nや^を整形）
def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

# 計算関数
def calculate(expr_str, mode):
    try:
        expr = sp.sympify(preprocess_expression(expr_str))
        if not expr.is_number:
            return None

        if mode == "add_then_mul":
            result = sp.expand((expr + b) * (2 * a))
        else:
            result = sp.expand(expr * a + (-3 * b))

        if result.is_number:
            result_val = int(result.evalf()) if result.evalf().is_integer else float(result.evalf())
            return result_val
        return None
    except Exception:
        return None

# 図の描画関数
def draw_diagram(input_value, result, mode):
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 200)
    ax.axis('off')

    y = 100
    x_input = 40
    x1 = 200
    x2 = 400
    x_out = 600
    arrow_offset = 60
    shape_w = 60
    shape_h = 80

    # 入力値
    ax.text(x_input, y, str(int(input_value)), ha='center', va='center', fontsize=16)
    ax.annotate("", xy=(x1 - arrow_offset, y), xytext=(x_input + 20, y), arrowprops=dict(arrowstyle="->", lw=2))

    if mode == "add_then_mul":
        # 四角形
        rect = patches.Rectangle((x1 - shape_w/2, y - shape_h/2), shape_w, shape_h,
                                 linewidth=2, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(x1, y, "b", ha='center', va='center', fontsize=16)

        # 矢印
        ax.annotate("", xy=(x2 - arrow_offset, y), xytext=(x1 + shape_w/2 + 10, y), arrowprops=dict(arrowstyle="->", lw=2))

        # 三角形（正三角形 + 枠付き）
        tri_height = shape_h
        tri_half_base = shape_h / (3 ** 0.5)
        triangle = patches.Polygon(
            [[x2, y - tri_height / 2],
             [x2 - tri_half_base, y + tri_height / 2],
             [x2 + tri_half_base, y + tri_height / 2]],
            closed=True, edgecolor='black', facecolor='lightgreen', linewidth=2
        )
        ax.add_patch(triangle)
        ax.text(x2, y + 5, "2a", ha='center', va='center', fontsize=16)

        # 最終矢印
        ax.annotate("", xy=(x_out - arrow_offset, y), xytext=(x2 + tri_half_base + 10, y), arrowprops=dict(arrowstyle="->", lw=2))

    else:
        # 三角形（左）
        tri_height = shape_h
        tri_half_base = shape_h / (3 ** 0.5)
        triangle = patches.Polygon(
            [[x1, y - tri_height / 2],
             [x1 - tri_half_base, y + tri_height / 2],
             [x1 + tri_half_base, y + tri_height / 2]],
            closed=True, edgecolor='black', facecolor='lightgreen', linewidth=2
        )
        ax.add_patch(triangle)
        ax.text(x1, y + 5, "a", ha='center', va='center', fontsize=16)

        # 矢印
        ax.annotate("", xy=(x2 - arrow_offset, y), xytext=(x1 + tri_half_base + 10, y), arrowprops=dict(arrowstyle="->", lw=2))

        # 四角形（右）
        rect = patches.Rectangle((x2 - shape_w/2, y - shape_h/2), shape_w, shape_h,
                                 linewidth=2, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(x2, y, "-3b", ha='center', va='center', fontsize=16)

        # 最終矢印
        ax.annotate("", xy=(x_out - arrow_offset, y), xytext=(x2 + shape_w/2 + 10, y), arrowprops=dict(arrowstyle="->", lw=2))

    # 出力値
    if result is not None:
        ax.text(x_out, y, str(int(result)), ha='center', va='center', fontsize=16)

    st.pyplot(fig)

# --- Streamlit UI ---
st.set_page_config(layout="centered")
st.title("図形と式の計算")

col1, col2 = st.columns([2, 1])
with col1:
    expr_input = st.number_input("入れる数（整数）", step=1, format="%d")
with col2:
    mode = st.radio("図形の順番", ["四角→三角", "三角→四角"], horizontal=True)

mode_key = "add_then_mul" if mode == "四角→三角" else "mul_then_add"

result = calculate(expr_input, mode_key)
draw_diagram(expr_input, result, mode_key)
