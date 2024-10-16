import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 页面配置
st.set_page_config(
    page_title="Streamlit 精美登录应用",
    page_icon="🔒",
    layout="wide",
)

# 登录验证函数
def login(username, password):
    # 假设用户名是 'admin'，密码是 'password123'
    if username == "admin" and password == "password123":
        return True
    else:
        return False

# 登录页面函数
def login_page():
    st.markdown("""
        <style>
        .login-container {
            background-color: #f0f2f6;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: auto;
        }
        .login-button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .login-button:hover {
            background-color: #45a049;
        }
        h2 {
            text-align: center;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h2>🔒 登录</h2>", unsafe_allow_html=True)

    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    login_button = st.button("登录")

    if login_button:
        if login(username, password):
            st.session_state['logged_in'] = True
            st.success("登录成功！欢迎回来，{}".format(username))
        else:
            st.error("用户名或密码错误，请重试。")

    st.markdown("</div>", unsafe_allow_html=True)

# 精美界面函数
def beautiful_dashboard():
    st.title("✨ 精美的 Streamlit 应用 ✨")
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #4a4a4a;
        }
        </style>
        """, unsafe_allow_html=True)

    # 侧边栏配置
    with st.sidebar:
        st.image("https://via.placeholder.com/150", width=150)
        st.title("快速导航")
        st.markdown("通过侧边栏轻松导航")
        st.radio("选择页面", ("首页", "图表展示", "联系信息"))
        if st.button("退出登录"):
            st.session_state['logged_in'] = False  # 退出登录时将状态重置

    # 分割成两列的布局
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("简介")
        st.write("这个页面是使用 Streamlit 创建的精美应用示例，集成了交互式组件和图表。")

        # 上传图片的功能
        st.subheader("上传图片")
        uploaded_image = st.file_uploader("选择一张图片", type=["jpg", "png", "jpeg"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="上传的图片", use_column_width=True)

    with col2:
        st.subheader("动态数据展示")

        # Matplotlib 图表展示
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, color="orange", linewidth=2.5)
        ax.set_title("动态生成的正弦波图")
        ax.grid(True)

        st.pyplot(fig)

    # 添加底部的版权信息
    st.markdown("""
        <hr>
        <div style='text-align: center;'>
            <p>© 2024 精美的 Streamlit 应用. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)

# 主应用逻辑
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # 初始化登录状态

if st.session_state['logged_in']:
    beautiful_dashboard()  # 用户登录后显示精美界面
else:
    login_page()  # 未登录时显示登录页面
