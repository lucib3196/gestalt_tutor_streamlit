from langgraph_sdk import get_client
from .app_settings import get_settings

settings = get_settings()

try:
    client = get_client(url=settings.get_agent_url, api_key=settings.langsmith_api_key)
except Exception as e:
    raise ValueError(f"Cannot initialize client {e}")
