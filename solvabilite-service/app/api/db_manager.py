from fastapi import HTTPException
from .models import Client, Credit
from .db import clients, database, credits


async def get_finances_client(id_client):
    query = clients.select(clients.c.id_client == id_client)
    result = await database.fetch_one(query=query)
    if result:
        infos_revenu = {"infos_finances": (result["revenu_mensuel"], result["depense_mensuel"])}
        #     {
        #     "infos_finances": {
        #         "revenu_mensuel": result["revenu_mensuel"],
        #         "depense_mensuel": result["depense_mensuel"],
        #     }
        # }
        return infos_revenu
    else:
        raise HTTPException(status_code=404, detail="Client not found")


async def get_depense_client(id_client):
    query = clients.select(clients.c.id_client == id_client)
    result = await database.fetch_one(query=query)
    if result:
        return result['depense_mensuel']
    else:
        raise HTTPException(status_code=404, detail="Client not found")


async def add_client(payload: Client):
    query = clients.insert().values(**payload.model_dump())
    return await database.execute(query=query)


async def add_credit(payload: Credit):
    query = credits.insert().values(**payload.model_dump())
    return await database.execute(query=query)


async def get_credit_informations(id_client):
    query = credits.select(credits.c.id_client == id_client)
    result = await database.fetch_one(query=query)
    if result:
        client_financial_infos = {"infos_credit": (result["dette_en_cours"], result["payement_en_retard"], True if result["antecedent_faillite"] else False)}
        #     {
        #     "infos_credit": {
        #         "dette_en_cours": result["dette_en_cours"],
        #         "payement_en_retard": result["payement_en_retard"],
        #         "antecedent_faillite": result["antecedent_faillite"]
        #     }
        # }
        return client_financial_infos
    else:
        raise HTTPException(status_code=404, detail="Client not found")

