import os

from tortoise import Tortoise


async def connectToDatabase():
    await Tortoise.init(
        db_url=os.getenv("DB_URL"),
        modules={'models': ['app.models']}
    )
