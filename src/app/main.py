import streamlit as st
from app.core.app_settings import get_settings
from app.core.session import init_session
from app.ui.layout import render_title
from app.ui.chat import (
    render_chat,
    render_chat_input,
    render_select_box,
    render_chatbot_description,
)
from app.ui.sources import source_view
from app.ui.login import render_login, render_signup
# from app.services.auth import get_user_threads
settings = get_settings()
init_session()


def render_chat_page():
    render_select_box()
    render_chatbot_description()
    render_chat()
    render_chat_input()
    if st.session_state.get("show_sources"):
        source_view()


def render_auth():
    mode = st.radio("Choose", ["Login", "Sign Up"], horizontal=True)
    st.title(mode)

    if mode == "Login":
        render_login()
    else:
        render_signup()


def render_ui():
    # Header Section
    render_title(
        title=settings.name,
        env=settings.env,
        thread_id=st.session_state.thread_id,
    )
    with st.sidebar:
        st.markdown("### 👤 Active User")
        col1, col2 = st.columns([1, 3])

        st.divider()
        st.markdown("### 🧵 Recent Threads")
        # get_user_threads()
    if not st.session_state.id_token:
        render_auth()
    else:
        render_chat_page()


render_ui()
