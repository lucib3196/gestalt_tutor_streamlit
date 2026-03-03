import streamlit as st
import httpx
import requests
from app.models.user import UserCreate
from app.core.app_settings import get_settings


settings = get_settings()
BACKEND_URL = settings.get_backend_url


def sign_up(data: UserCreate):
    try:
        with httpx.Client() as client:
            response = client.post(f"{BACKEND_URL}/users/", json=data.model_dump())

        return response
    except Exception as e:
        raise ValueError(
            f"Failed to make request to backend {e}. Sanity Check {BACKEND_URL}"
        )


def login(email: str, password: str):
    # Use google endpoint
    ## Todo change thsi to the auth
    # url = "http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-key"
    url = settings.get_firebase_url
    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url, json=payload)
        body = dict(response.json())

        print("login response", body)

        if response.status_code != 200:
            error_msg = body.get("error", {}).get("message", "Unknown error")
            st.error(f"Login failed: {error_msg}")
            return None

        id_token = body.get("idToken")
        if not id_token:
            st.error("Login failed: No token received")
            return None

    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return None

    # Login to user account in FastAPI
    try:
        with httpx.Client() as client:
            fastapi_response = client.post(
                f"{BACKEND_URL}/users/login", json={"id_token": id_token}
            )

        if fastapi_response.status_code == 200:
            fastapi_body = fastapi_response.json()
            force_password_reset = fastapi_body.get("force_password_reset", None)
            if force_password_reset is None:
                st.error("Failed to login:")
                print("Cannot determine password reset state")
            return {
                "id_token": id_token,
                "email": email,
                "force_password_reset": force_password_reset,
            }
        else:
            error_msg = response.json().get("detail", "Unknown error")
            st.error(f"Failed to login: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Failed to login: {str(e)}")
        return None


def password_reset(new_password: str):
    id_token = st.session_state.id_token
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{BACKEND_URL}/users/password_reset/temp",
                json={"new_password": new_password},
                headers={"Authorization": f"Bearer {id_token}"},
            )


            body = response.content

        if response.status_code != 200:
            error_msg = body.get("error", {}).get("message", "Unknown error")
            raise ValueError(f"Password reset failed: {error_msg}")
    except Exception as e:
        raise ValueError(f"Failed to update password {e} ")
