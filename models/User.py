from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)

    class Meta:
        table = "users"

    async def hash_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    async def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @classmethod
    async def authenticate(cls, username: str, password: str):
        user = await cls.get_or_none(username=username)
        if not user or not user.verify_password(password):
            return None
        return user

    async def set_password(self, new_password: str):
        self.hash_password(new_password)
        await self.save()