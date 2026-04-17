from pydantic import BaseModel, Field
from typing import Dict, Literal
from enum import Enum


class ALLOWED_MODE(str, Enum):
    TEXT = "text"
    FILE = "file"
    BOTH = "both"

CHAT_NAMES = Literal[
    "ME135 Transport Tutor",
    "ME118 Engineering Modeling and Analysis Tutor",
    "Sundar Tutor",
    "Differential Equations Tutor",
    "stem_textbook_retrieval"
]


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
        active=True,
    ),
    "ME118 Engineering Modeling and Analysis Tutor": ChatOption(
        label="ME118 Engineering Modeling and Analysis Tutor",
        chat_id="agent_me118",
        description=(
            "An in-depth Engineering Modeling and Analysis tutor grounded in Professor Sundar’s ME118 lecture notes with additional access to relevant resources from the LibreTexts differential equations textbook. "
            "Provides structured explanations, step-by-step derivations, and analytical problem-solving guidance "
            "for system modeling, differential equations, linear algebra applications, numerical methods, and "
            "engineering interpretation of mathematical models, with references to the original lecture material."
        ),
        mode=ALLOWED_MODE.TEXT,
    ),
    "Sundar Tutor": ChatOption(
        label="Sundar Tutor",
        chat_id="sundar_agent",
        active=False,
        description=(
            "A unified upper-division Mechanical Engineering tutor covering both ME118 (Engineering Modeling and Analysis) "
            "and ME135 (Transport Phenomena), grounded exclusively in Professor Sundar’s lecture notes. "
            "Automatically retrieves from the appropriate course materials and provides concept explanations, "
            "step-by-step derivations, modeling guidance, and structured problem-solving support with explicit "
            "lecture references."
        ),
        mode=ALLOWED_MODE.TEXT,
    ),
    "Differential Equations Tutor": ChatOption(
        label="Differential Equations Tutor",
        chat_id="differential_eq_tutor",
        active=True,
        description=(
            "A Differential Equations tutor focused on clear, step-by-step learning using LibreTexts sources. "
            "Covers first-order and higher-order ODEs, Laplace transforms, systems of differential equations, "
            "series solutions, and applications, with guidance aligned to textbook-style explanations and methods."
        ),
        mode=ALLOWED_MODE.TEXT,
    ),
    "stem_textbook_retrieval": ChatOption(
        label="STEM Textbook Retrieval",
        chat_id="stem_textbook_retrieval",
        description=(
            "A STEM textbook retrieval chat with a collection of open-source textbooks in calculus, "
            "differential equations, fluid mechanics, and physics. The agent attempts to answer "
            "questions based on these parsed textbooks."
        ),
        active=True,
        mode=ALLOWED_MODE.TEXT,
    ),
}
