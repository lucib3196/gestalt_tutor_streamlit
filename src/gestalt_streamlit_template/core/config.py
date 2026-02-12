from pydantic import BaseModel, Field
from typing import Dict, Literal
from enum import Enum


class ALLOWED_MODE(str, Enum):
    TEXT = "text"
    FILE = "file"
    BOTH = "both"


CHAT_NAMES = Literal["ME135 Transport Tutor", "ME118 Engineering Modeling and Analysis Tutor"]


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
        chat_id="agent_me135",
        description=(
            "An in-depth Transport Phenomena tutor grounded in Professor Sundar’s ME135 lecture notes. "
            "Provides concept explanations, derivations, and problem-solving guidance for momentum, heat, "
            "and mass transfer topics, with references to the original lecture material."
        ),
        mode=ALLOWED_MODE.TEXT,
    ),
    "ME118 Engineering Modeling and Analysis Tutor": ChatOption(
        label="ME118 Engineering Modeling and Analysis Tutor",
        chat_id="agent_me118",
         description=(
        "An in-depth Engineering Modeling and Analysis tutor grounded in Professor Sundar’s ME118 lecture notes. "
        "Provides structured explanations, step-by-step derivations, and analytical problem-solving guidance "
        "for system modeling, differential equations, linear algebra applications, numerical methods, and "
        "engineering interpretation of mathematical models, with references to the original lecture material."
    ),
        mode=ALLOWED_MODE.TEXT,
    )
}