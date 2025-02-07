from fastapi import FastAPI, Depends, HTTPException, status
from models import User
from schemas import UserCreate, UserInDB, Token
from auth import get_current_user
from config import JWT_EXPIRE_MINUTES
from datetime import timedelta

app = FastAPI()

@app.post("/register", response_model=UserInDB)
async def register(user: UserCreate):
    db_user = await User.create(username=user.username)
    await db_user.hash_password(user.password)
    return db_user
