from core import init_session
from ui import (
    render_title,
    render_select_box,
    render_chatbot_description,
    render_chat,
    render_chat_input,
    source_view,
)
from ui.login import render_signup, render_login
import streamlit as st


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
        title=st.secrets["NAME"],
        env=st.secrets["ENV"],
        thread_id=st.session_state.thread_id,
    )
    if not st.session_state.id_token:
        render_auth()
    else:
        render_chat_page()



render_ui()
