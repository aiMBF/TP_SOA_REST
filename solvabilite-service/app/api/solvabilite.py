from fastapi import APIRouter, HTTPException
from .db_manager import *


router = APIRouter()


# Endpoint principal du service
@router.get("/client/{id_client}")
async def get_solvabilite_client(id_client):
    infos_credit = await get_credit_informations(id_client)
    infos_finances = await get_finances_client(id_client)
    score = 0
    client_credit_data = tuple(infos_credit["infos_credit"])
    if client_credit_data == (0, 0, False):
        score = 100
    elif client_credit_data[1] >= 2 and client_credit_data[2] == True:
        score = 0
    elif client_credit_data[1] < 2 and client_credit_data[0] < 1000:
        score = 80
    elif client_credit_data[1] < 2 and client_credit_data[0] > 1000:
        score = 60
    # # else:
    # #     solvabilite['clean'] = False
    revenu_mensuel, depense_mensuel = tuple(infos_finances["infos_finances"])
    financial_cap = revenu_mensuel - depense_mensuel
    return {'financial_cap': financial_cap, 'score': score}


# Ajouter un nouveau client avec les informations financiers
@router.post('/client', status_code=201)
async def add_new_client(payload: Client):
    id_client = await add_client(payload)
    response = {
        'id': id_client,
        **payload.model_dump()
    }
    return response


# Ajouter les informations de credit d'un client
@router.post('/credit', status_code=201)
async def add_new_credit(payload: Credit):
    id_client = await add_credit(payload)
    response = {
        'id': id_client,
        **payload.model_dump()
    }
    return response
