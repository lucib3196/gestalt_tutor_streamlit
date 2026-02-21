from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str


class User(BaseModel):
    username: str | None = None
    email: str | None = None
    logged_in: bool = False
