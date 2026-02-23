import streamlit as st
from core.chat_config import  ChatOption, CHAT_OPTIONS
from core.app_settings import ENV
from services.llm_services import get_new_thread_id

def render_title(
    title: str = "My Chat", env: ENV = ENV.LOCAL, thread_id: str | None = None
):
    if env == "local":
        title += " (Local DEV)"
    if thread_id:
        title += f" {thread_id}"

    st.set_page_config(page_title=title, layout="centered")
    st.title(title)




