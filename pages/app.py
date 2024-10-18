import streamlit as st
import base64

# 设置页面配置
st.set_page_config(page_title="欢迎界面", layout="centered")





st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Analysis", "Settings"])

if page == "Home":
    st.title("Welcome to the Home Page")
    st.write("This is the home page.")
    
    with st.expander("Learn More"):
        st.write("This section can contain additional information.")
    
elif page == "Analysis":
    st.title("Data Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Input Data")
        data = st.file_uploader("Upload your data file", type=["csv", "xlsx"])
    
    with col2:
        st.header("Analysis Results")
        if data is not None:
            st.write("Show analysis results here.")
    
elif page == "Settings":
    st.title("Settings")
    
    with st.tabs(["Preferences", "Account"]):
        with st.tab("Preferences"):
            st.write("User preferences can be set here.")
        with st.tab("Account"):
            st.write("Account details can be managed here.")









# 获取本地图像的 Base64 编码
def get_image_as_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 读取本地背景图片并转换为 Base64
background_image_file = "D:\DOWNLOAD\yolov5-streamlit-main\yolov5-streamlit-main\data\images\\2.png"  # 替换为你的本地背景图文件
image_base64 = get_image_as_base64(background_image_file)

# 添加背景图的 CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpeg;base64,{image_base64}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
    }}
    .welcome-text {{
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
        font-family: 'Cursive'; /* 设置花体字体 */
    }}
    .enter-button {{
        display: flex;
        justify-content: center;
    }}
    .enter-button button {{
        font-size: 20px;
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }}
    .enter-button button:hover {{
        background-color: #0056b3;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 欢迎界面内容
st.markdown('<div class="welcome-text">This is a demo,</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-text">Please click the options in the sidebar to use different features.</div>', unsafe_allow_html=True)
