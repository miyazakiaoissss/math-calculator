import streamlit as st
from sympy import sympify, simplify
import re

# ページ設定
st.set_page_config(page_title="図形と式の計算", page_icon="📐", layout="centered")

# ----------- 入力式を補正する関数 -----------
def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)   # 2x -> 2*x
    expr = re.sub(r'(\d)\(', r'\1*(', expr)           # 3(x+1) -> 3*(x+1)
    expr = expr.replace("^", "**")                     # x^2 -> x**2
    return expr

# ----------- 表示用：* を省略 -----------
def display_expression(expr):
    return str(expr).replace("*", "")

# ----------- 計算を実行する関数 -----------
def calculate_operation(written_str, input_str, operation):
    try:
        if not written_str or not input_str:
            return "エラー", "", "空の入力があります"
        
        written = sympify(preprocess_expression(written_str))
        input_value = sympify(preprocess_expression(input_str))
        
        if operation == "add":
            result = simplify(written + input_value)
        else:  # multiply
            result = simplify(written * input_value)
        
        return (display_expression(written), 
                display_expression(input_value), 
                display_expression(result))
    except Exception as e:
        return "エラー", "", str(e)

# タイトル
st.title("📐 図形と式の計算")
st.markdown("---")

# ----------- 四角形（加算）セクション -----------
st.subheader("■ 四角形（足し算）")

col1, col2 = st.columns(2)
with col1:
    input_r = st.text_input("入力する数や式（例：2x+1）：", key="input_rect", placeholder="2x+1")
with col2:
    written_r = st.text_input("図形に書かれた数や式（例：3）：", key="written_rect", placeholder="3")

if st.button("🔄 図形に反映（四角）", key="calc_rect"):
    center_r, left_r, right_r = calculate_operation(written_r, input_r, "add")
    st.session_state.rect_result = (center_r, left_r, right_r)

# 四角形の結果表示
if hasattr(st.session_state, 'rect_result'):
    center_r, left_r, right_r = st.session_state.rect_result
    
    st.markdown("### 計算結果（四角形）")
    
    # 視覚的な表示
    col_left, col_center, col_right = st.columns([1, 1, 1])
    
    with col_left:
        if left_r:
            st.markdown(f"<div style='text-align: center; font-size: 18px;'>{left_r}</div>", unsafe_allow_html=True)
    
    with col_center:
        st.markdown(f"""
        <div style='text-align: center;'>
            <div style='display: inline-block; width: 80px; height: 60px; background-color: lightblue; 
                        border: 2px solid black; display: flex; align-items: center; justify-content: center;
                        font-size: 16px; font-weight: bold;'>
                {center_r}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        if right_r:
            st.markdown(f"<div style='text-align: center; font-size: 18px;'>{right_r}</div>", unsafe_allow_html=True)
    
    # 矢印表示
    if left_r and right_r and center_r != "エラー":
        st.markdown("<div style='text-align: center; font-size: 20px;'>→ + → =</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------- 三角形（掛け算）セクション -----------
st.subheader("▲ 三角形（掛け算）")

col3, col4 = st.columns(2)
with col3:
    input_t = st.text_input("入力する数や式（例：2x+1）：", key="input_tri", placeholder="2x+1")
with col4:
    written_t = st.text_input("図形に書かれた数や式（例：3）：", key="written_tri", placeholder="3")

if st.button("🔄 図形に反映（三角）", key="calc_tri"):
    center_t, left_t, right_t = calculate_operation(written_t, input_t, "multiply")
    st.session_state.tri_result = (center_t, left_t, right_t)

# 三角形の結果表示
if hasattr(st.session_state, 'tri_result'):
    center_t, left_t, right_t = st.session_state.tri_result
    
    st.markdown("### 計算結果（三角形）")
    
    # 視覚的な表示
    col_left2, col_center2, col_right2 = st.columns([1, 1, 1])
    
    with col_left2:
        if left_t:
            st.markdown(f"<div style='text-align: center; font-size: 18px;'>{left_t}</div>", unsafe_allow_html=True)
    
    with col_center2:
        st.markdown(f"""
        <div style='text-align: center;'>
            <div style='display: inline-block; width: 0; height: 0; 
                        border-left: 40px solid transparent; border-right: 40px solid transparent;
                        border-bottom: 60px solid lightgreen; position: relative;'>
            </div>
            <div style='position: relative; top: -35px; font-size: 16px; font-weight: bold; color: black;'>
                {center_t}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right2:
        if right_t:
            st.markdown(f"<div style='text-align: center; font-size: 18px;'>{right_t}</div>", unsafe_allow_html=True)
    
    # 矢印表示
    if left_t and right_t and center_t != "エラー":
        st.markdown("<div style='text-align: center; font-size: 20px;'>→ × → =</div>", unsafe_allow_html=True)

# 使い方の説明
st.markdown("---")
st.markdown("### 📝 使い方")
st.markdown("""
- **四角形（足し算）**: 入力した式と図形の式を足し算します
- **三角形（掛け算）**: 入力した式と図形の式を掛け算します
- **対応している記法**: 
  - `2x` → `2*x` (自動変換)
  - `x^2` → `x**2` (自動変換)  
  - `3(x+1)` → `3*(x+1)` (自動変換)
- 例: `x+1`, `2x^2+3x`, `(x+2)(x-1)` など
""")
