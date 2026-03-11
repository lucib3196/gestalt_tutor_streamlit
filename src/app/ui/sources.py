from pathlib import Path
import fitz
from io import BytesIO
import streamlit as st
from models.sources import SourceRef
from typing import List
import requests
from urllib.parse import urlparse


PKG_ROOT = Path(__file__).resolve().parents[1]


def normalize_source(source: str) -> str:
    source = source.replace("\\", "/")

    # Fix malformed http:/ -> http://
    if source.startswith("http:/") and not source.startswith("http://"):
        source = source.replace("http:/", "http://", 1)

    if source.startswith("https:/") and not source.startswith("https://"):
        source = source.replace("https:/", "https://", 1)

    return source


def open_pdf(source: str | bytes) -> fitz.Document:
    if isinstance(source, (bytes, memoryview, bytearray)):
        return fitz.open(stream=source, filetype="pdf")
    parsed = urlparse(source)
    if parsed.scheme in ("http", "https"):
        source = normalize_source(source)
        response = requests.get(source)
        response.raise_for_status()
        return fitz.open(stream=response.content, filetype="pdf")
    else:
        path = Path(source)
        if path.exists():
            return fitz.open(path)

    raise ValueError(f"Invalid PDF source: {source}")


def rotate_pdf(pdf_path: Path | str, rotation: int) -> bytes:
    if isinstance(pdf_path, Path):
        pdf_path = pdf_path.as_posix()
    doc = open_pdf(pdf_path)
    for page in doc:
        page.set_rotation(rotation)
    buffer = BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()


def index_sources(sources: List[SourceRef]):
    index = {}
    for src in sources:
        key = (src.lecture_title, Path(src.source_pdf))
        index.setdefault(key, src)  # keep first occurrence
    return index


def toggle_source(key: str):
    if st.session_state.get("active_source") == key:
        st.session_state["active_source"] = None
    else:
        st.session_state["active_source"] = key


def show_sources():
    sources: List[SourceRef] = st.session_state.get("sources", [])
    indexed_sources = index_sources(sources)
    if indexed_sources:
        st.markdown("### Sources")

        for index in indexed_sources:

            is_active = st.session_state.get("active_source") == index
            label = f"▼ {index[0]}" if is_active else f"▶ {index[0]}"
            st.button(
                label,
                key=f"btn_{index[0]}",
                on_click=toggle_source,
                args=(index,),
            )


def rotation_buttons():
    if not st.session_state.get("active_source"):
        return
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⟲ Rotate"):
            st.session_state["source_rotation"] -= 90

    with col2:
        if st.button("⟳ Rotate"):
            st.session_state["source_rotation"] += 90


def render_selected_source():
    sources: List[SourceRef] = st.session_state.get("sources", [])
    source_index = index_sources(sources)
    active_key = st.session_state.get("active_source")
    active_source = source_index.get(active_key, None)
    if active_source:
        active = str(active_source.source_pdf)
        if active.startswith("http"):
            pdf_path = active
        else:
            pdf_path = (PKG_ROOT / active_source.source_pdf).resolve()
        rotated_bytes = rotate_pdf(pdf_path, st.session_state["source_rotation"])
        st.pdf(rotated_bytes)


def source_view():
    show_sources()
    render_selected_source()
    rotation_buttons()
