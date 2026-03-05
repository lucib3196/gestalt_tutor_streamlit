import streamlit as st
from app.core.chat_config import ChatOption, CHAT_OPTIONS
from app.core.app_settings import ENV
from app.services.llm_services import initialize_thread_id, send_message


def render_chat():
    for msg in st.session_state.messages or []:
        role = msg.get("role", "ai")
        with st.chat_message(role):
            st.markdown(msg["content"])


def render_chat_input():
    prompt = st.chat_input("Type a message")
    if prompt:
        send_message(prompt)


def render_chatbot_description():
    if "chat_data" in st.session_state:
        chat_data: ChatOption = st.session_state.chat_data
        st.subheader(chat_data.label)
        st.write(chat_data.description)

        # TODO: Fix this
        if chat_data.mode == "file":
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                st.write(bytes_data)


def handle_chatbot_change():
    selected = st.session_state.chat_select
    if not selected:
        return
    chat_data = CHAT_OPTIONS[selected]
    st.session_state.chat_data = chat_data
    try:
        initialize_thread_id()
    except Exception as e:
        st.error(f"{e}")


def handle_new_chat():
    handle_chatbot_change()
    st.session_state.messages = []
    st.session_state.sources = []


def render_select_box() -> str | None:
    # Renders the labele for the option
    options = [k for k, v in CHAT_OPTIONS.items() if v.active]

    add_radio = st.selectbox(
        label="Choose Chat Mode",
        options=options,
        index=None,
        key="chat_select",
        format_func=lambda k: CHAT_OPTIONS[k].label,
        on_change=handle_chatbot_change,
    )
    st.button(label="New Chat", on_click=handle_new_chat)

    return add_radio
