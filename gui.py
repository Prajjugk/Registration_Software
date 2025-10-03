import streamlit as st
import requests

#  Backend API URLs 
BASE_URL = "http://127.0.0.1:5000"

REG_URL = f"{BASE_URL}/registration"
LOGIN_URL = f"{BASE_URL}/login"

st.set_page_config(page_title="User Auth System", layout="centered")
st.title(" Registration & Login System")

# Sidebar for Navigation 
choice = st.sidebar.radio("Select Action", ["Register", "Login"])

# Registration Form 
if choice == "Register":
    st.subheader(" Registration Form")
    
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if not username or not email or not password:
            st.error("Please fill in all fields")
        else:
            payload = {"username": username, "email": email, "password": password}
            try:
                response = requests.post(REG_URL, json=payload)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json["Status"] == "Success":
                        st.success(res_json["message"])
                    else:
                        st.error(res_json["message"])
                elif response.status_code in [400,401,404]:
                    res_json = response.json()
                    if res_json["Status"]=="Error":
                        st.success(res_json["message"])
                    else:
                        st.error(res_json["message"])
                else:
                    st.error("Server error, try again later")
            except Exception as e:
                st.error(f"Connection error: {e}")

# Login Form 
if choice == "Login":
    st.subheader("Login Form")
    
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        if not email or not password:
            st.error("Please fill in all fields")
        else:
            payload = {"email": email, "password": password}
            try:
                response = requests.post(LOGIN_URL, json=payload)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json["Status"] == "Success":
                        st.success(res_json["message"])
                    else:
                        st.error(res_json["message"])
                elif response.status_code in [400,401,404]:
                    res_json = response.json()
                    if res_json["Status"]=="Error":
                        st.success(res_json["message"])
                    else:
                        st.error(res_json["message"])
                else:
                    st.error("Server error, try again later")
            except Exception as e:
                st.error(f"Connection error: {e}")
