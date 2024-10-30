import streamlit as st
import requests

# FastAPI 后端完整接口 URL
REGISTER_API = "http://127.0.0.1:8000/register"
LOGIN_API = "http://127.0.0.1:8000/login"
CREATE_POST_API = "http://127.0.0.1:8000/create_post"
GET_POSTS_API = "http://127.0.0.1:8000/posts"

# 检查登录状态的函数
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None

# 用户注册功能
def register():
    st.subheader("用户注册")
    username = st.text_input("用户名", key="reg_username")
    password = st.text_input("密码", type="password", key="reg_password")

    if st.button("注册"):
        if username and password:
            response = requests.post(REGISTER_API, json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("注册成功！请登录。")
            else:
                st.error(f"注册失败：{response.json().get('detail', '未知错误')}")
        else:
            st.warning("请输入用户名和密码。")

# 用户登录功能
def login():
    st.subheader("用户登录")
    username = st.text_input("用户名", key="login_username")
    password = st.text_input("密码", type="password", key="login_password")

    if st.button("登录"):
        if username and password:
            response = requests.post(LOGIN_API, json={"username": username, "password": password})
            if response.status_code == 200:
                user_data = response.json()
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user_data.get("user_id")
                st.session_state["username"] = username
                st.success("登录成功！")
            else:
                st.error(f"登录失败：{response.json().get('detail', '用户名或密码错误')}")
        else:
            st.warning("请输入用户名和密码。")

# 发帖功能
def create_post():
    st.subheader("创建新帖子")
    title = st.text_input("标题", key="post_title")
    content = st.text_area("内容", key="post_content")

    if st.button("发布"):
        user_id = st.session_state.get("user_id")
        if title and content and user_id:
            post_data = {
                "title": title,
                "content": content,
                "user_id": user_id
            }
            response = requests.post(CREATE_POST_API, json=post_data)
            if response.status_code == 200:
                st.success("帖子发布成功！")
            else:
                st.error(f"发布失败：{response.json().get('detail', '未知错误')}")
        elif not user_id:
            st.error("请先登录。")
        else:
            st.warning("标题和内容不能为空！")

# 查看帖子功能
def view_posts():
    st.subheader("查看所有帖子")
    response = requests.get(GET_POSTS_API)
    if response.status_code == 200:
        posts = response.json()
        if posts:
            for post in posts:
                st.write(f"### {post['title']}")
                st.write(post['content'])
                st.write(f"发帖人 ID: {post['user_id']}")
                st.write("---")
        else:
            st.info("暂无帖子")
    else:
        st.error(f"无法获取帖子：{response.text}")

# 主页面逻辑
def main():
    st.title("用户发帖和查看帖子")

    # 检查登录状态
    check_login()

    if st.session_state["logged_in"]:
        st.subheader(f"欢迎, {st.session_state['username']}!")
        create_post()
        view_posts()

        if st.button("登出"):
            st.session_state["logged_in"] = False
            st.session_state["user_id"] = None
            st.session_state["username"] = None
            st.success("已成功登出！")
    else:
        # 展示注册和登录功能
        register()
        login()

if __name__ == "__main__":
    main()
