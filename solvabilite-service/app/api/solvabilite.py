from fastapi import APIRouter
from .models import Client
from .db_manager import *


router = APIRouter()


@router.get("/client/{id_client}")
async def get_revenu_client(client: Client):

    return {"revenu_client": client.revenu_mensuel}


@router.get("/solvabilite/{id_client}")
async def get_solvabilite(id_client: str):
    pass


@router.post('/', status_code=201)
async def add_movie(payload: Client):
    movie_id = await add_movie(payload)
    response = {
        'id': movie_id,
        **payload.model_dump()
    }
    return response
