import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR
import numpy as np
from io import BytesIO
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import base64
import re

# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 支持中文和英文

# 星火认知大模型的API和认证信息
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
SPARKAI_APP_ID = 'e8025f24'
SPARKAI_API_SECRET = 'Yjc5OTRkOThkODY2NzZjMDQ2ZDE0ODgx'
SPARKAI_API_KEY = 'd2e23d404b09b8c574b8efc074f16e43'
SPARKAI_DOMAIN = '4.0Ultra'

# 初始化 Spark 大模型
def init_spark_model():
    return ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )

# OCR功能，提取图像中的文本
def extract_text_from_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))  # 打开图像
        img_np = np.array(image)  # 转换为NumPy数组

        # 使用PaddleOCR进行文本提取
        result = ocr.ocr(img_np, cls=True)
        extracted_text = ''
        for line in result:
            for text in line:
                extracted_text += text[1][0] + '\n'
        return extracted_text
    except Exception as e:
        st.error(f"图像处理失败: {e}")
        return ""

# 清空作业历史记录
def clear_homework_history():
    st.session_state.homeworks = []

# 设置背景图的函数
def set_background_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded_image = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 检查并渲染LaTeX内容
def render_latex_content(content):
    content = re.sub(r"[^a-zA-Z0-9\s\+\-\*\/\^\(\)\.,]", "", content)
    try:
        st.latex(content)
    except Exception as e:
        st.error(f"无法渲染为LaTeX: {e}")

# Streamlit 界面和处理逻辑
def main():
    st.set_page_config(page_title="OCR与作业批改系统")

    # 设置本地背景图
    set_background_image("D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\sunset.png")  # 替换为你的背景图片路径

    # 侧边栏设置
    with st.sidebar:
        st.title('OCR与作业批改系统')
        st.success('API key 已经配置!', icon='✅')
        st.sidebar.button('清空作业历史', on_click=clear_homework_history)

    # 初始化作业历史记录
    if "homeworks" not in st.session_state:
        st.session_state.homeworks = []

    # 上传图片进行OCR处理
    uploaded_image = st.file_uploader("上传包含作业的图片", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        # 读取上传的文件为字节流
        image_bytes = uploaded_image.read()
        try:
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption='上传的图片', use_column_width=True)

            # 使用PaddleOCR提取图像中的文本
            extracted_text = extract_text_from_image(image_bytes)
            st.subheader("提取的文本")
            st.markdown(extracted_text)  # 以Markdown形式显示提取的文本

            # 选择是否将提取的文本进行批改与评价
            if st.button("批改与评价提取的作业"):
                st.session_state.homeworks.append({"role": "user", "content": extracted_text})
                with st.chat_message("user"):
                    st.markdown(extracted_text)

                # 调用星火大模型进行批改与评价
                spark_model = init_spark_model()
                prompt = f"### 请对以下作业进行批改并提供详细评价：\n\n{extracted_text}"  # 以Markdown格式传递
                messages = [ChatMessage(role="user", content=prompt)]
                handler = ChunkPrintHandler()

                # 获取机器人的批改与评价
                response = spark_model.generate([messages], callbacks=[handler])
                correction_and_feedback = response.generations[0][0].text  # 提取实际批改内容

                # 将批改与评价结果保存到历史记录
                st.session_state.homeworks.append({"role": "assistant", "content": correction_and_feedback})

                # 显示批改与评价结果
                with st.chat_message("assistant"):
                    st.markdown(correction_and_feedback)  # 以Markdown形式显示

        except Exception as e:
            st.error(f"无法处理上传的图片: {e}")

if __name__ == '__main__':
    # 检查登录状态
    if not st.session_state.get("logged_in", False):
        st.warning("您必须登录才能访问此页面。")
        st.stop()  # 停止页面继续加载
    main()
