import os

from tortoise import Tortoise
from dotenv import load_dotenv


load_dotenv()

db_url = os.getenv('DB_URL')

async def init():
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()