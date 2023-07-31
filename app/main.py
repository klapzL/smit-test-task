import os

from dotenv import load_dotenv

from fastapi import FastAPI
from tortoise import Tortoise

from app.router.tariffs import router


app = FastAPI()

load_dotenv()

db_url = os.getenv('DB_URL')

@app.on_event('startup')
async def init():
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()


app.include_router(router)
