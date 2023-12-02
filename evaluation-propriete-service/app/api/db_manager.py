from .models import Evaluation
from .db import evaluations, database


async def add_eval(payload: Evaluation):
    query = evaluations.insert().values(**payload.model_dump())

    return await database.execute(query=query)


async def get_eval(ville):
    query = evaluations.select(evaluations.c.ville == ville)

    return await database.fetch_one(query=query)

