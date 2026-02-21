from typing import Any, List
from pydantic import BaseModel
import streamlit as st
from .config import CHAT_NAMES
from app.services.llm_services import initialize_thread_id
from . import SourceRef, User

show_sources = st.secrets.get("SHOW_SOURCES", False)


class DefaultState(BaseModel):
    messages: List[Any] = []
    thread_id: str | None = None
    chat_select: CHAT_NAMES | None
    sources: List[SourceRef] = []
    active_source: str = ""
    source_rotation: int = 0
    show_sources: bool = show_sources
    user: User
    id_token: str | None = None


DEFAULT_STATE = DefaultState(
    messages=[],
    chat_select=None,
    thread_id=initialize_thread_id(),
    user=User(),
    id_token=None,
)


def init_session():
    for key, value in DEFAULT_STATE.model_dump().items():
        if key not in st.session_state:
            st.session_state[key] = value
