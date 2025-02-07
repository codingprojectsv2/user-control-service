from tortoise import Tortoise, run_async
from fastapi import FastAPI
from config import TORTOISE_ORM
from models import User

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("Database initialized and schemas generated.")

async def create_test_user():
    await User.create(
        username="testuser",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Пароль: testpassword
    )
    print("Test user created.")

def init_app():
    app = FastAPI()
    return app

async def main():
    await init_db()
    await create_test_user()

if __name__ == "__main__":
    run_async(main())