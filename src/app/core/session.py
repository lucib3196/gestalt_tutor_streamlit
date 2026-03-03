from typing import Any, List

import streamlit as st
from pydantic import BaseModel

from app.services.llm_services import initialize_thread_id

from . import SourceRef, User
from .app_settings import get_settings
from .chat_config import CHAT_NAMES

settings = get_settings()
show_sources = settings.show_sources


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
    thread_id=None,
    user=User(),
    id_token=None,
)


def init_session():
    for key, value in DEFAULT_STATE.model_dump().items():
        if key not in st.session_state:
            st.session_state[key] = value
