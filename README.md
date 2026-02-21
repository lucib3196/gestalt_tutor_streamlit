
---

# Gestalt Streamlit Template

A reusable Streamlit project template designed for AI-powered applications.

---

## LangGraph Local Server Integration

This template is designed to work with the LangGraph local development server, allowing you to run and iterate on LangGraph agents alongside the Streamlit UI.

For detailed guidance on developing and running the LangGraph server, refer to the official LangGraph local server documentation:
[https://docs.langchain.com/oss/python/langgraph/local-server](https://docs.langchain.com/oss/python/langgraph/local-server)

---

## Agent / Chat Configuration

For this template to function correctly, available chats (agents) must be configured in:

```
src/core/chat_config
```

This configuration defines:

* Which chatbots or agents are available
* How they appear in the Streamlit UI
* What interaction modes they support (text, file upload, or both)
* How the UI maps to LangGraph agents

The `chat_id` must match the name of the corresponding chat or agent defined in your LangGraph setup. This is how the Streamlit UI determines which backend agent to invoke.

The URL used by the chat component is configured in the application settings.

---

## Prerequisites

Before installing, ensure the following are installed:

* Python (version specified in `pyproject.toml`)
* Poetry
  Installation guide: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
* Git

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lucib3196/gestalt_streamlit_template.git
cd gestalt_streamlit_template
```

### 2. Activate the Poetry Environment

```bash
poetry shell
```

Activating the Poetry shell allows commands to be run without prefixing them with `poetry run`.

### 3. Install Dependencies

```bash
poetry install
```

This installs all required Python dependencies defined in `pyproject.toml`.

---

## Configuration

### Streamlit Secrets

This project uses Streamlit’s secrets system for configuration, including API keys and environment settings.

1. Navigate to the `src/.streamlit/` directory
2. Copy the example secrets file:

   ```bash
   cp secrets.toml.example secrets.toml
   ```
3. Edit `secrets.toml` and fill in the required values

Do not commit `secrets.toml`; it should remain local only.

Example configuration:

```bash
## Agent settings
AGENT_PRODUCTION_URL=""
AGENT_LOCAL_URL = "http://127.0.0.1:2024"
AGENT_ENV= "local"

## API Key
### APIKEY Needed for agent production
LANGSMITH_API_KEY=""

## Backend settings 
PRODUCTION_URL= ""
LOCAL_URL = "http://localhost:8010"
MODE="local"

# Other general settings
SHOW_SOURCES= true
```

---

## Running the Application

```bash
cd src
streamlit run app/main.py
```

The application will open automatically in your browser.
