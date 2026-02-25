import streamlit as st
from app.models.user import UserCreate
from app.services.auth import sign_up, login


def render_signup():
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", placeholder="John")
    with col2:
        last_name = st.text_input("Last Name", placeholder="Doe")
    email = st.text_input("Email Address", placeholder="john.doe@example.com")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    data = UserCreate(
        first_name=first_name, last_name=last_name, password=password, email=email
    )

    if st.button("Create Account"):
        response = sign_up(data)
        body = response.json()

        if not response.status_code == 200:
            st.error(f"Sign up failed {body.get("detail",None)}")
        else:
            st.success("Account Created! Please Login Now")


def render_login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        data = login(email, password)
        if not data:
            st.error("Failed to login Unexpected Error")
        print("Data", data)
        st.success("Login ok")
        st.session_state.id_token = data["id_token"]
        st.rerun()

    else:
        st.error("Invalid credentials")
