# import streamlit as st
# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
# from sparkai.core.messages import ChatMessage

# # 星火认知大模型的API和认证信息
# SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 星火API URL
# SPARKAI_APP_ID = 'fb9838aa'  # 替换为你的App ID
# SPARKAI_API_SECRET = 'Y2QwZTRjMmI1YmVkMDc0Y2JlNWE2ZTBi'  # 替换为你的API Secret
# SPARKAI_API_KEY = 'c5370fca45d7f6c12f0a4baa03431a54'  # 替换为你的API Key
# SPARKAI_DOMAIN = 'generalv3.5'  # 使用的模型版本

# # 初始化 Spark 大模型
# def init_spark_model():
#     return ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         streaming=False,
#     )

# # Streamlit 界面和处理逻辑
# def main():
#     st.title("Spark AI Chatbot with Streamlit")

#     # 初始化聊天记录
#     if 'messages' not in st.session_state:
#         st.session_state['messages'] = []

#     # 显示聊天历史记录
#     for message in st.session_state['messages']:
#         if message['role'] == 'user':
#             st.markdown(f"**You**: {message['content']}")
#         else:
#             st.markdown(f"**Bot**: {message['content']}")

#     # 用户输入
#     user_input = st.text_input("Type your message here:")

#     if st.button("Send") and user_input:
#         # 将用户输入保存到聊天记录
#         st.session_state['messages'].append({"role": "user", "content": user_input})

#         # 调用星火大模型
#         spark_model = init_spark_model()
#         messages = [ChatMessage(role="user", content=user_input)]
#         handler = ChunkPrintHandler()

#         # 获取机器人的回复
#         response = spark_model.generate([messages], callbacks=[handler])

#         # 提取回复内容
#         reply_content = response.generations[0][0].text  # 提取回复的实际文本内容

#         # 将机器人的回复保存到聊天记录
#         st.session_state['messages'].append({"role": "assistant", "content": reply_content})

#         # 使用 st.markdown 渲染机器人的回复
#         st.markdown(f"**Bot**: {reply_content}")

# if __name__ == '__main__':
#     main()



# import streamlit as st
# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
# from sparkai.core.messages import ChatMessage
# import base64

# # 星火认知大模型的API和认证信息
# SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 星火API URL
# SPARKAI_APP_ID = 'fb9838aa'  # 替换为你的App ID
# SPARKAI_API_SECRET = 'Y2QwZTRjMmI1YmVkMDc0Y2JlNWE2ZTBi'  # 替换为你的API Secret
# SPARKAI_API_KEY = 'c5370fca45d7f6c12f0a4baa03431a54'  # 替换为你的API Key
# SPARKAI_DOMAIN = 'generalv3.5'  # 使用的模型版本

# # 初始化 Spark 大模型
# def init_spark_model():
#     return ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         streaming=False,
#     )

# # 获取本地图像的 Base64 编码
# def get_image_as_base64(image_file):
#     with open(image_file, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# # 读取本地背景图像并转换为 Base64
# background_image_file = "D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\sunset.png"  # 替换为你的本地背景图文件名
# background_image_base64 = get_image_as_base64(background_image_file)

# # 添加背景图的 CSS
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url('data:image/jpeg;base64,{background_image_base64}');
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#         height: 100vh;  
#         color: white;  /* 文字颜色 */
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 清空聊天记录的功能
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# # Streamlit 界面和处理逻辑
# def main():
#     st.set_page_config(page_title="Spark AI Chatbot with Streamlit")
    

    
    
#     # 侧边栏设置
#     with st.sidebar:
#         st.title('Spark AI Chatbot')
#         st.success('API key already provided!', icon='✅')
#         st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

#     # 初始化聊天记录
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

#     # 显示聊天历史记录
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # 用户输入
#     if prompt := st.chat_input("Type your message here:"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         # 调用星火大模型生成回复
#         spark_model = init_spark_model()
#         messages = [ChatMessage(role="user", content=prompt)]
#         handler = ChunkPrintHandler()

#         # 获取机器人的回复
#         response = spark_model.generate([messages], callbacks=[handler])

#         # 提取回复内容
#         reply_content = response.generations[0][0].text  # 提取回复的实际文本内容

#         # 将机器人的回复保存到聊天记录
#         st.session_state.messages.append({"role": "assistant", "content": reply_content})

#         # 显示机器人的回复
#         with st.chat_message("assistant"):
#             st.write(reply_content)




# if __name__ == '__main__':
#     main()




# import streamlit as st
# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
# from sparkai.core.messages import ChatMessage
# import base64

# # 星火认知大模型的API和认证信息
# SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 星火API URL
# SPARKAI_APP_ID = 'fb9838aa'  # 替换为你的App ID
# SPARKAI_API_SECRET = 'Y2QwZTRjMmI1YmVkMDc0Y2JlNWE2ZTBi'  # 替换为你的API Secret
# SPARKAI_API_KEY = 'c5370fca45d7f6c12f0a4baa03431a54'  # 替换为你的API Key
# SPARKAI_DOMAIN = 'generalv3.5'  # 使用的模型版本

# # 初始化 Spark 大模型
# def init_spark_model():
#     return ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         streaming=False,
#     )

# # 清空聊天记录的功能
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# # 设置背景图的函数
# def set_background_image(image_file):
#     with open(image_file, "rb") as f:
#         data = f.read()
#     encoded_image = base64.b64encode(data).decode()
#     css = f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{encoded_image}");
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#     }}
#     </style>
#     """
#     st.markdown(css, unsafe_allow_html=True)

# # Streamlit 界面和处理逻辑
# def main():
#     st.set_page_config(page_title="Spark AI Chatbot with Streamlit")
    
#     # 设置本地背景图
#     set_background_image("D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\sunset.png")  # 替换为你的背景图片路径

#     # 侧边栏设置
#     with st.sidebar:
#         st.title('Spark AI Chatbot')
#         st.success('API key already provided!', icon='✅')
#         st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

#     # 初始化聊天记录
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

#     # 显示聊天历史记录
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # 用户输入
#     if prompt := st.chat_input("Type your message here:"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         # 调用星火大模型生成回复
#         spark_model = init_spark_model()
#         messages = [ChatMessage(role="user", content=prompt)]
#         handler = ChunkPrintHandler()

#         # 获取机器人的回复
#         response = spark_model.generate([messages], callbacks=[handler])

#         # 提取回复内容
#         reply_content = response.generations[0][0].text  # 提取回复的实际文本内容

#         # 将机器人的回复保存到聊天记录
#         st.session_state.messages.append({"role": "assistant", "content": reply_content})

#         # 显示机器人的回复
#         with st.chat_message("assistant"):
#             st.write(reply_content)

# if __name__ == '__main__':
#     main()















import streamlit as st
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import base64

    





# 星火认知大模型的API和认证信息
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 星火API URL
SPARKAI_APP_ID = 'fb9838aa'  # 替换为你的App ID
SPARKAI_API_SECRET = 'Y2QwZTRjMmI1YmVkMDc0Y2JlNWE2ZTBi'  # 替换为你的API Secret
SPARKAI_API_KEY = 'c5370fca45d7f6c12f0a4baa03431a54'  # 替换为你的API Key
SPARKAI_DOMAIN = 'generalv3.5'  # 使用的模型版本

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

# 清空聊天记录的功能
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

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
    # 将所有的对话历史构造成一个列表，发送给模型
    return [ChatMessage(role=message["role"], content=message["content"]) for message in st.session_state.messages]

# Streamlit 界面和处理逻辑
def main():
    st.set_page_config(page_title="Spark AI Chatbot with Streamlit")
    
    # 设置本地背景图
    set_background_image("D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\sunset.png")  # 替换为你的背景图片路径

    # 侧边栏设置
    with st.sidebar:
        st.title('Spark AI Chatbot')
        st.success('API key already provided!', icon='✅')
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # 显示聊天历史记录
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 用户输入
    if prompt := st.chat_input("Type your message here:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # 调用星火大模型生成回复
        spark_model = init_spark_model()
        # 获取所有的对话历史并发送给模型
        messages = get_message_history()
        handler = ChunkPrintHandler()

        # 获取机器人的回复
        response = spark_model.generate([messages], callbacks=[handler])

        # 提取回复内容
        reply_content = response.generations[0][0].text  # 提取回复的实际文本内容

        # 将机器人的回复保存到聊天记录
        st.session_state.messages.append({"role": "assistant", "content": reply_content})

        # 显示机器人的回复
        with st.chat_message("assistant"):
            st.write(reply_content)
        




if __name__ == '__main__':
    if st.session_state["logged_in"]==False:
        st.warning("You must log in to access this page.")
        st.stop()  # 停止页面继续加载
    main()
