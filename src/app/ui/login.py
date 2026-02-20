import streamlit as st
from app.core.session import User
import httpx
import requests
from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

def sign_up(data: UserCreate):
    try:
        with httpx.Client() as client:
            response = client.post("http://localhost:8010/users/", json=data.model_dump())
        return response
    except Exception as e:
        raise ValueError(f"Failed to make request to backend {e}")

def login(email: str, password: str):
    # Use google endpoint
    url = "http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-key"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        response = requests.post(url, json=payload)
        body = dict(response.json())
        
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
            response = client.post("http://localhost:8010/users/login", json={"id_token": id_token})
        print("Login Response", response)
        if response.status_code == 200:
            return {"id_token": id_token, "email": email}
        else:
            error_msg = response.json().get("detail", "Unknown error")
            st.error(f"Failed to login: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Failed to login: {str(e)}")
        return None
    

def render_signup():
    st.title("Sign Up")

    first_name = st.text_input("first_name")
    last_name = st.text_input("last_name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    data = UserCreate(first_name=first_name,last_name=last_name, password=password, email=email)

    if st.button("Create Account"):
        response = sign_up(data)
        body = response.json()
        
        if not response.status_code == 200:
            st.error(f"Sign up failed {body.get("detail",None)}")
        else:
            st.success("Account Created! Please Login Now")
            


def render_login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")


    if st.button("Login"):
        data = login(email, password)
        print("Data",data)
        st.success("Login ok")
        st.session_state.id_token = data["id_token"]
        st.rerun()

    
     
    else:
        st.error("Invalid credentials")