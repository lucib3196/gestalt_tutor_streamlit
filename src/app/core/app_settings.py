from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional
import os
import streamlit as st

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

EnvLiteral = Literal["local", "production"]


ROOT_DIR = Path(__file__).resolve().parents[3]
print(ROOT_DIR)


class AppSettings(BaseSettings):
    name: str = Field(
        default="gestalt_tutor",
        description="Application name used for display and logging purposes.",
    )

    # ------------------------
    # AI / Agent Configuration
    # ------------------------
    agent_local_url: Optional[str] = Field(
        default="http://127.0.0.1:2024",
        description="Local LangGraph agent server URL used during development.",
        examples=["http://127.0.0.1:2024"],
    )

    agent_production_url: Optional[str] = Field(
        default=None,
        description="Production LangGraph agent URL. Required when agent_env is PRODUCTION.",
    )

    agent_env: EnvLiteral = Field(
        default="local",
        description="Environment for the agent server (local or production).",
    )

    langsmith_api_key: Optional[str] = Field(
        default=None,
        description="LangSmith API key used for tracing and observability.",
        repr=False,  # prevents accidental printing
    )

    # ------------------------
    # Backend API Configuration
    # ------------------------
    production_url: Optional[str] = Field(
        default="",
        description="Production FastAPI backend URL.",
        examples=["https://api.gestalttutor.com"],
    )

    local_url: Optional[str] = Field(
        default="http://localhost:8010",
        description="Local FastAPI backend URL used during development.",
        examples=["http://localhost:8010"],
    )

    env: EnvLiteral = Field(
        default="local",
        description="Application runtime environment (local or production).",
    )
    # ------------------------
    # FIREBASE API Configuration
    # ------------------------
    firebase_api_key: str | None = None
    # ------------------------
    # UI / Feature Flags
    # ------------------------
    show_sources: bool = Field(
        default=True,
        description="Flag to control whether source documents are displayed in the UI.",
    )

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # FIREBASE
    STORAGE_BUCKET: str | None = None

    # Derived properties
    @model_validator(mode="after")
    def validate_agent_env(
        self,
    ):
        if self.agent_env == "local" and not self.agent_local_url:
            raise ValueError("AGENT ENV  set to local but url is not set")
        if self.agent_env == "production" and not self.agent_production_url:
            raise ValueError("AGENT ENV set to production but not production url")
        return self

    @model_validator(mode="after")
    def validate_backend_env(
        self,
    ):
        if self.env == "local" and not self.local_url:
            raise ValueError("ENV  set to local but url is not set")
        if self.env == "production" and not self.production_url:
            raise ValueError("ENV set to production but not production url")
        return self

    @property
    def get_agent_url(self):
        if self.agent_env == "local":
            return self.agent_local_url
        elif self.agent_env == "production":
            return self.agent_production_url
        else:
            raise ValueError(
                f"Failed to determined agent url. Unknown mode :{self.agent_env} "
            )

    @property
    def get_backend_url(self):
        if self.env == "local":
            return self.local_url
        elif self.env == "production":
            return self.production_url
        else:
            raise ValueError(
                f"Failed to determine the backend url: Unknown mode {self.env}"
            )

    @property
    def get_firebase_url(self) -> str:
        print("Env value", self.env)
        if self.env == "local":
            # Firebase host emulator
            return "http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-key"
        elif self.env == "production":
            if not self.firebase_api_key:
                raise ValueError(
                    "Failed to define firebase url firebase api key is None. Must be set in ENV"
                )
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.firebase_api_key}"
            return url
        else:
            raise ValueError("Cannot determine firebase url")


@lru_cache
def get_settings() -> AppSettings:
    """
    Cached settings instance.
    Safe for Streamlit, FastAPI, CLI.
    """
    # Check streamlit secrets first
    try:
        print("Trying to load Streamlit secrets")

        raw_settings = {}

        # Only attempt if running inside streamlit context
        if hasattr(st, "secrets"):
            raw_settings = dict(st.secrets)

        if raw_settings:
            print("Using Streamlit secrets")

            norm_settings = {
                key.lower(): value
                for key, value in raw_settings.items()
                if value is not None
            }

            return AppSettings(**norm_settings)

    except Exception as e:
        print(f"Failed loading secrets: {e}")

    return AppSettings()


if __name__ == "__main__":
    settings = get_settings()
    print("Settings: ", settings)
    print(settings.get_firebase_url)
