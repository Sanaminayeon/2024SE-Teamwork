import streamlit as st
import requests

# FastAPI 后端 URL
REGISTER_API = "http://127.0.0.1:8000/register"
LOGIN_API = "http://127.0.0.1:8000/login"
LOGOUT_API = "http://127.0.0.1:8000/logout"  # 假设后端有这个登出端点

# 检查登录状态的函数
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False  # 初始化为未登录状态

# 登出功能
def logout():
    # 发送登出请求给后端
    payload = {"username": st.session_state["username"]}
    response = requests.post(LOGOUT_API, json=payload)

    if response.status_code == 200:
        st.session_state["logged_in"] = False  # 清除登录状态
        st.session_state["username"] = None  # 清除用户名
        st.success("You have been logged out!")
    else:
        st.error("Logout failed. Please try again.")

# Streamlit 页面
def main():
    st.title("User Registration and Login")

    # 检查登录状态
    check_login()

    # 如果用户已登录，显示登出按钮和主页面内容
    if st.session_state["logged_in"]:
        st.subheader(f"Welcome, {st.session_state['username']}! (User ID: {st.session_state['user_id']})")
        if st.button("Logout"):
            logout()  # 调用登出功能
        return  # 已登录时停止显示登录和注册表单

    # 选择功能：登录或注册
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    # 用户注册界面
    if choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if username and password:
                payload = {"username": username, "password": password}
                response = requests.post(REGISTER_API, json=payload)
                if response.status_code == 200:
                    st.success("Registration successful!")
                else:
                    st.error("Error: " + response.json()["detail"])
            else:
                st.warning("Please enter both username and password.")

    # 用户登录界面
    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                payload = {"username": username, "password": password}
                response = requests.post(LOGIN_API, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["logged_in"] = True  # 设置登录状态
                    st.session_state["username"] = username  # 保存用户名
                    st.session_state["user_id"] = data.get("user_id")  # 保存用户 ID
                    st.success("Login successful!")
                else:
                    st.error("Error: " + response.json()["detail"])
            else:
                st.warning("Please enter both username and password.")

if __name__ == "__main__":
    main()
