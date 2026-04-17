import streamlit as st
import requests
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
from app.ui.login import render_login, render_signup, render_reset_password

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
    mode = st.radio("Choose", ["Login"], horizontal=True)
    st.title(mode)
    if mode == "Login":
        render_login()
    else:
        render_signup()



def render_ui():
    # Header Section
    app_title = (
        f"{settings.name} {settings.env if settings.env != 'production' else None}"
    )
    render_title(
        title=app_title,
        env=settings.env,
        thread_id=st.session_state.thread_id,
    )
    with st.sidebar:
        st.markdown("### 👤 Active User")
        col1, col2 = st.columns([1, 3])

        st.divider()
        st.markdown("### 🧵 Recent Threads")
        # get_user_threads()

    if settings.env == "demo":
        render_chat_page()
    else:
        if not st.session_state.id_token:
            render_auth()
        elif st.session_state.force_password_reset:
            render_reset_password()
        else:
            render_chat_page()


render_ui()
