from .models import Tariff


async def get_tariff(cargo_type: str, date: str):
    date = date.strftime('%Y-%m-%d')
    tariff = await Tariff.filter(
        cargo_type=cargo_type,
        created_at__lte=date
    ).order_by('-created_at').first()
    return tariff.rate if tariff else None
