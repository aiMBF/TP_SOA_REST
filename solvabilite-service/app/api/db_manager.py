from .models import Client
from .db import clients, database, metadata, engine


async def get_client(id_client):
    query = clients.select(clients.c.id_client==id_client)
    return await database.fetch_one(query=query)


async def add_client(payload: Client):
    query = clients.insert().values(**payload.model_dump())
    return await database.execute(query=query)