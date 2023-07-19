import os

from datetime import datetime
from dotenv import load_dotenv

from tortoise import Tortoise
from fastapi import FastAPI, HTTPException

from app.models import Tariff, tariff_pydantic
from app.utils import get_tariff


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


@app.get('/tariffs')
async def get_tariffs():
    tariffs = await Tariff.all()
    tariffs_date = {}
    for tariff in tariffs:
        date = tariff.created_at.strftime('%Y-%m-%d')
        if date not in tariffs_date:
            tariffs_date[date] = []
        tariffs_date[date].append({
            'cargo_type': tariff.cargo_type,
            'rate': tariff.rate,
        })
    return tariffs_date


@app.post('/tariffs/create')
async def create_tariff(cargo_type: str, rate: float):
    tariff = await Tariff.create(
        cargo_type=cargo_type,
        rate=rate,
        created_at=datetime.now().strftime('%Y-%m-%d')
    )
    return await tariff_pydantic.from_tortoise_orm(tariff)


@app.get('/calculate_insurance/')
async def calculate_insurance_cost(
                    cargo_type: str,
                    cost: float,
                    date: str = datetime.now().strftime('%Y-%m-%d')
                ):
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Неверный формат даты. Пример: 2023-07-19.'
        )

    rate = await get_tariff(cargo_type, date)
    if not rate:
        raise HTTPException(
            status_code=404,
            detail='Тарифа с такими данными не найдено.'
        )
    return {'insurance': cost * rate}
