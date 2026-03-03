import streamlit as st
from app.models.user import UserCreate
from app.services.auth import sign_up, login


def render_signup():
    st.title("Sign Up")

    # first_name = st.text_input("first_name")
    # last_name = st.text_input("last_name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    data = UserCreate(
         password=password, email=email
    )

    if st.button("Create Account"):
        response = sign_up(data)
        body = response.json()

        if not response.status_code == 200:
            st.error(f"Sign up failed {body.get("detail",None)}")
        else:
            st.success("Account Created! Please Login Now")


def render_login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        data = login(email, password)
        if not data:
            st.error("Failed to login Unexpected Error")
        st.success("Login ok")
        st.session_state.id_token = data["id_token"]
        st.rerun()