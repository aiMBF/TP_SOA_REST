from .models import Evaluation, Litige
from .db import evaluations, database, litiges
from fastapi import HTTPException


async def add_ville(payload: Evaluation):
    query = evaluations.insert().values(ville=payload.ville, prix_par_metre=payload.prix_metre)
    return await database.execute(query=query)


async def get_eval(ville):
    query = evaluations.select(evaluations.c.ville == ville)
    result = await database.fetch_one(query=query)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Ville non repertoriee")


async def get_litiges(adress):
    query = litiges.select(litiges.c.adresse_bien == adress)
    result = await database.fetch_one(query=query)

    if result:
        return True
    else:
        return False


async def add_litiges(payload: Litige):
    query = litiges.insert().values(**payload.model_dump())

    return await database.execute(query=query)