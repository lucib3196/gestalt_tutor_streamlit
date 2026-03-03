import streamlit as st
from app.models.user import UserCreate
from app.services.auth import sign_up, login, password_reset


def render_signup():
    st.title("Sign Up")

    # first_name = st.text_input("first_name")
    # last_name = st.text_input("last_name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    data = UserCreate(password=password, email=email)

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
        print(data)
        if data is None:
            st.error("Failed to login Unexpected Error")
        st.success("Login ok")
        st.session_state.id_token = data["id_token"]
        st.session_state.force_password_reset = data.get("force_password_reset", False)
        st.rerun()


def render_reset_password():
    st.title("Reset Password")
    st.caption("You must set a new password before continuing.")

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password", type="primary"):
        if not new_password or not confirm_password:
            st.error("Please fill in both password fields.")
            return
        if len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
            return
        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return
        if not st.session_state.id_token:
            st.error("No active session found. Please log in again.")
            return

        try:
            password_reset(new_password)
            st.session_state.force_password_reset = False
            print("Current state",st.session_state.force_password_reset)
        except Exception as e:
            st.error(f"Failed to reset password: {e}")
            return

        st.success("Password updated successfully.")
        st.rerun()
