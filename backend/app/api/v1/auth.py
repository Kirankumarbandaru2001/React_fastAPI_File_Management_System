from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

# Dummy in-memory user store
users_db = {"testuser": {"password": "testpassword"}}

@router.post("/login")
def login(user: User):
    if users_db.get(user.username) and users_db[user.username]["password"] == user.password:
        return {"message": "Login successful"}
    return {"message": "Invalid credentials"}, 401
