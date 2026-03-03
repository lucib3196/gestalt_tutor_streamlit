import streamlit as st
from app.core.chat_config import ChatOption, CHAT_OPTIONS
from app.core.app_settings import ENV


def render_title(
    title: str = "My Chat", env: ENV = ENV.LOCAL, thread_id: str | None = None
):
    if env.value == "local":
        title += " (Local DEV)"
    if thread_id:
        title += f" {thread_id}"

    st.set_page_config(page_title=title, layout="centered")
    st.title(title)
