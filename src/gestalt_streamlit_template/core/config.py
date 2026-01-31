from pydantic import BaseModel, Field
from typing import Dict, Literal
from enum import Enum


class ALLOWED_MODE(str, Enum):
    TEXT = "text"
    FILE = "file"
    BOTH = "both"


CHAT_NAMES = Literal["ME135 Transport Tutor"]


class ChatOption(BaseModel):
    label: str = Field(description="Label for UI")
    chat_id: str = Field(description="ID for chatbot")
    description: str | None = Field(description="chatbot description")
    mode: ALLOWED_MODE = Field(
        default=ALLOWED_MODE.TEXT,
        description="Whether it accepts files or not",
    )
    active: bool = Field(default=True, description="Wether chatbot is available")


CHAT_OPTIONS: Dict[CHAT_NAMES, ChatOption] = {
    "ME135 Transport Tutor": ChatOption(
        label="ME135 Transport Phenomena Tutor",
        chat_id="agent",
        description=(
            "An in-depth Transport Phenomena tutor grounded in Professor Sundar’s ME135 lecture notes. "
            "Provides concept explanations, derivations, and problem-solving guidance for momentum, heat, "
            "and mass transfer topics, with references to the original lecture material."
        ),
        mode=ALLOWED_MODE.TEXT,
    )
}