import streamlit as st
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import base64
import re

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

# 构建消息历史
def get_message_history():
    return [ChatMessage(role=message["role"], content=message["content"]) for message in st.session_state.homeworks]

# 检查并渲染LaTeX公式
def render_latex_content(content):
    # 使用正则表达式匹配LaTeX公式
    latex_matches = re.findall(r"\$.*?\$", content)

    if latex_matches:
        # 如果内容中有LaTeX公式，分段渲染
        parts = re.split(r"(\$.*?\$)", content)
        for part in parts:
            if part in latex_matches:
                st.latex(part.strip('$'))
            else:
                st.write(part)
    else:
        # 如果没有LaTeX公式，直接显示内容
        st.write(content)

# Streamlit 界面和处理逻辑
def main():
    st.set_page_config(page_title="作业批改与评价系统")

    # 设置本地背景图
    set_background_image("D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\sunset.png")  # 替换为你的背景图片路径

    # 侧边栏设置
    with st.sidebar:
        st.title('作业批改与评价系统')
        st.success('API key 已经配置!', icon='✅')
        st.sidebar.button('清空作业历史', on_click=clear_homework_history)

    # 初始化作业历史记录
    if "homeworks" not in st.session_state:
        st.session_state.homeworks = []

    # 显示作业历史记录
    for message in st.session_state.homeworks:
        with st.chat_message(message["role"]):
            render_latex_content(message["content"])

    # 用户输入作业内容
    homework_text = st.text_area("输入学生的作业内容（纯文本）")

    if st.button("批改与评价作业") and homework_text:
        # 将用户输入的作业保存到作业历史
        st.session_state.homeworks.append({"role": "user", "content": homework_text})
        with st.chat_message("user"):
            st.write(homework_text)

        # 调用星火大模型进行批改与评价
        spark_model = init_spark_model()

        # 构建批改与评价的请求内容
        prompt = f"请对以下作业进行批改并提供详细评价：\n\n{homework_text}"
        messages = [ChatMessage(role="user", content=prompt)]
        handler = ChunkPrintHandler()

        # 获取机器人的批改与评价
        response = spark_model.generate([messages], callbacks=[handler])

        # 提取批改与评价的内容
        correction_and_feedback = response.generations[0][0].text  # 提取实际批改内容

        # 将批改与评价结果保存到历史记录
        st.session_state.homeworks.append({"role": "assistant", "content": correction_and_feedback})

        # 显示批改与评价结果
        with st.chat_message("assistant"):
            render_latex_content(correction_and_feedback)

if __name__ == '__main__':
    # 检查登录状态
    if not st.session_state.get("logged_in", False):
        st.warning("您必须登录才能访问此页面。")
        st.stop()  # 停止页面继续加载
    main()
