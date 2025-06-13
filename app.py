import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from sympy import sympify
import re

# 定数設定
FIG_WIDTH = 8
FIG_HEIGHT = 2
SHAPE_HEIGHT = 1.2
SHAPE_WIDTH = 1
TRIANGLE_HEIGHT = SHAPE_HEIGHT

# 定数
fixed_values = {"a": 3, "b": 2}

# 式の前処理
def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

# 計算処理
def calculate_result(value, mode):
    try:
        expr = sympify(preprocess_expression(str(value)))
        a, b = fixed_values["a"], fixed_values["b"]

        if mode == "add_then_mul":
            result = (expr + b) * (2 * a)
        else:
            result = expr * a + (-3 * b)

        result = result.evalf()
        result = int(result) if result == int(result) else result
        return int(expr), result
    except Exception:
        return None, None

# 描画処理
def draw_diagram(input_val, result_val, mode):
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis('off')

    y_center = 1
    x_positions = [0.5, 2, 4, 6, 7.5, 9]
    x_in, x1, x2, x3, x4, x_out = x_positions

    # 入力
    ax.text(x_in, y_center, str(input_val), ha='center', va='center', fontsize=14)
    ax.annotate("", xy=(x1 - 0.1, y_center), xytext=(x_in + 0.2, y_center),
                arrowprops=dict(arrowstyle="->", lw=2))

    if mode == "add_then_mul":
        # 四角形
        rect = Rectangle((x1 - SHAPE_WIDTH / 2, y_center - SHAPE_HEIGHT / 2),
                         SHAPE_WIDTH, SHAPE_HEIGHT, facecolor='lightblue', edgecolor='black', lw=2)
        ax.add_patch(rect)
        ax.text(x1, y_center, "b", ha='center', va='center', fontsize=14)

        ax.annotate("", xy=(x2 - 0.1, y_center), xytext=(x1 + SHAPE_WIDTH / 2 + 0.1, y_center),
                    arrowprops=dict(arrowstyle="->", lw=2))

        # 三角形
        triangle = Polygon([[x2, y_center + TRIANGLE_HEIGHT / 2],
                            [x2 - SHAPE_WIDTH / 2, y_center - TRIANGLE_HEIGHT / 2],
                            [x2 + SHAPE_WIDTH / 2, y_center - TRIANGLE_HEIGHT / 2]],
                           closed=True, facecolor='lightgreen', edgecolor='black', lw=2)
        ax.add_patch(triangle)
        ax.text(x2, y_center, "2a", ha='center', va='center', fontsize=14)

        ax.annotate("", xy=(x3 - 0.1, y_center), xytext=(x2 + SHAPE_WIDTH / 2 + 0.1, y_center),
                    arrowprops=dict(arrowstyle="->", lw=2))

    else:
        # 三角形
        triangle = Polygon([[x1, y_center + TRIANGLE_HEIGHT / 2],
                            [x1 - SHAPE_WIDTH / 2, y_center - TRIANGLE_HEIGHT / 2],
                            [x1 + SHAPE_WIDTH / 2, y_center - TRIANGLE_HEIGHT / 2]],
                           closed=True, facecolor='lightgreen', edgecolor='black', lw=2)
        ax.add_patch(triangle)
        ax.text(x1, y_center, "a", ha='center', va='center', fontsize=14)

        ax.annotate("", xy=(x2 - 0.1, y_center), xytext=(x1 + SHAPE_WIDTH / 2 + 0.1, y_center),
                    arrowprops=dict(arrowstyle="->", lw=2))

        # 四角形
        rect = Rectangle((x2 - SHAPE_WIDTH / 2, y_center - SHAPE_HEIGHT / 2),
                         SHAPE_WIDTH, SHAPE_HEIGHT, facecolor='lightblue', edgecolor='black', lw=2)
        ax.add_patch(rect)
        ax.text(x2, y_center, "-3b", ha='center', va='center', fontsize=14)

        ax.annotate("", xy=(x3 - 0.1, y_center), xytext=(x2 + SHAPE_WIDTH / 2 + 0.1, y_center),
                    arrowprops=dict(arrowstyle="->", lw=2))

    # 出力
    ax.annotate("", xy=(x_out - 0.1, y_center), xytext=(x3 + 0.2, y_center),
                arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(x_out, y_center, str(result_val), ha='center', va='center', fontsize=14)

    st.pyplot(fig)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("図形を通る計算アプリ")

col1, col2 = st.columns([1, 3])
with col1:
    mode = st.radio("計算の順番", ["add_then_mul", "mul_then_add"], format_func=lambda x: "四角形→三角形" if x=="add_then_mul" else "三角形→四角形")
    input_val = st.number_input("入れる数", step=1, format="%d")

with col2:
    input_expr, result = calculate_result(input_val, mode)
    if input_expr is not None:
        draw_diagram(input_expr, result, mode)
    else:
        st.error("式の計算中にエラーが発生しました。")
