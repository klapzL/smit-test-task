from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Tariff(Model):
    cargo_type = fields.CharField(max_length=255)
    rate = fields.FloatField()
    created_at = fields.DateField()

    def __str__(self):
        return f'{self.created_at}'


tariff_pydantic = pydantic_model_creator(Tariff)

tariff_pydantic_no_ids = pydantic_model_creator(Tariff, exclude_readonly=True)
