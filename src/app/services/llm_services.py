import streamlit as st
from app.core.client import client
from .async_wrappers import run_async
from app.models.sources import SourceRef
from pathlib import Path
from typing import Any, Dict
import httpx
from app.core.app_settings import get_settings

settings = get_settings()
BACKEND_URL = settings.get_backend_url


def extract_sources(source_data: Dict[str, Any]) -> None:
    if not source_data:
        return

    source_list = source_data.get("messages")
    if not isinstance(source_list, list) or not source_list:
        return

    last_message = source_list[-1]

    # Ensure last_message is dict-like
    if not isinstance(last_message, dict):
        return

    artifact = last_message.get("artifact")
    if not artifact:
        return

    # Artifact can be dict or list depending on LangGraph config
    if isinstance(artifact, dict):
        artifact_list = list(artifact.values())
    elif isinstance(artifact, list):
        artifact_list = artifact
    else:
        return

    sources: list[SourceRef] = []
    try:

        source_list = source_data.get("messages", [])
        for doc in source_list[-1].get("artifact", []):
            metadata = doc.get("metadata", {})
            path = metadata.get("source_pdf")
            if not path:
                continue
            sources.append(
                SourceRef(
                    lecture_title=metadata.get("lecture_title", "Untitled Source"),
                    lecture_summary=metadata.get("lecture_summary", None),
                    source_pdf=Path(path),
                    page=None,
                )
            )
    except Exception as e:
        return
    st.session_state.sources = sources


async def initialize_thread_id_async() -> str | None:
    try:
        token = st.session_state.get("id_token")
        if not token:
            raise ValueError("No token found")

        async with httpx.AsyncClient() as backend_client:
            response = await backend_client.post(
                f"{BACKEND_URL}/users/thread",
                headers={"Authorization": f"Bearer {token}"},
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()
            thread_id = data.get("id")
            if not thread_id:
                raise ValueError("No thread_id returned from backend")
            await client.threads.create(thread_id=thread_id)
            return thread_id

    except Exception as e:
        print("Failed to initialize thread:", e)
        return None


def initialize_thread_id() -> str:
    st.session_state.thread_id = run_async(initialize_thread_id_async())
    return st.session_state.thread_id


async def stream_langgraph(messages, thread_id: str | None, assistant_id: str):
    async for chunk in client.runs.stream(
        thread_id,
        assistant_id=assistant_id,
        input={"messages": messages},
        stream_mode="updates",
    ):
        if chunk.event != "updates":
            continue
        model_data = chunk.data.get("model")
        source_data: Dict[str, Any] = chunk.data.get("tools", {})
        extract_sources(source_data)

        if not model_data:
            continue
        messages_list = model_data.get("messages", [])

        if not messages_list:
            continue
        last_msg = messages_list[-1]
        if last_msg:
            yield last_msg


def send_message(prompt: str):
    if not prompt:
        return
    st.chat_message("user").markdown(prompt)
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    assistant_box = st.chat_message("assistant")
    placeholder = assistant_box.empty()
    tool_placeholder = assistant_box.container()

    if "thread_id" not in st.session_state:
        print("Initalizing thread id")
        st.session_state.thread_id = initialize_thread_id()

    async def consume():
        buffer = ""
        tool_calls_rendered = set()
        thread_id = st.session_state.thread_id

        async with httpx.AsyncClient() as backend_client:
            response = await backend_client.post(
                f"{BACKEND_URL}/threads/{thread_id}/messages",
                timeout=30,
                json=user_message,
            )

        async for token in stream_langgraph(
            [user_message],
            thread_id,
            st.session_state.chat_data.chat_id,
        ):
            content = token.get("content")
            if content:
                buffer += content
                placeholder.markdown(buffer)
            tool_calls = token.get("tool_calls")
            # if tool_calls:

            #     for call in tool_calls:
            #         call_id = call.get("id")
            #         if call_id in tool_calls_rendered:
            #             continue
            #         tool_calls_rendered.add(call_id)
            #         with tool_placeholder:
            #             with st.expander(
            #                 f"Tool call: `{call['name']}`", expanded=False
            #             ):
            #                 st.json(call["args"])
            ai_message = {"role": "assistant", "content": buffer}
            async with httpx.AsyncClient() as backend_client:
                response = await backend_client.post(
                    f"{BACKEND_URL}/threads/{thread_id}/messages",
                    timeout=30,
                    json=ai_message,
                )

            st.session_state.messages.append(ai_message)

    run_async(consume())
