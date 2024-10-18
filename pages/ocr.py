import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
import base64

import streamlit as st

if st.session_state["logged_in"]==False:
        st.warning("You must log in to access this page.")
        st.stop()  # 停止页面继续加载



# 创建 EasyOCR 读取器
reader = easyocr.Reader(['en', 'ch_sim'])  # 语言可以根据需要更改，例如 ['ch_sim'] 用于简体中文

# 获取本地图像的 Base64 编码
def get_image_as_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 读取本地背景图像并转换为 Base64
background_image_file = "D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\bg2.png"  # 替换为你的本地背景图文件名
background_image_base64 = get_image_as_base64(background_image_file)

# 添加背景图的 CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpeg;base64,{background_image_base64}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;  
        color: white;  /* 文字颜色 */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 页面标题
st.title('EasyOCR Text Extraction')

# 文件上传
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 打开图像并转换为 NumPy 数组
    image = Image.open(uploaded_file)
    image_np = np.array(image)  # 转换为 NumPy 数组

    # 显示上传的图片
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # 识别文本
    if st.button('Extract Text'):
        # 调用 EasyOCR
        results = reader.readtext(image_np)

        # 显示结果
        st.write("Detected Text:")
        for (bbox, text, prob) in results:
            st.write(f"Text: {text} (Confidence: {prob:.2f})")

        # 可选：显示边界框
        for (bbox, text, prob) in results:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            image_np = cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)

        # 显示带有边界框的图像
        st.image(image_np, caption='Detected Text', use_column_width=True)
