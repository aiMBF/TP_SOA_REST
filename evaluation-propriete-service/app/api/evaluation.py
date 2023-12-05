from fastapi import APIRouter, HTTPException
from .models import Evaluation, Litige
from typing import Union
from .db_manager import *


router = APIRouter()


async def eval_prop(taille: float, ville: str):
    valeur = await get_eval(ville)
    if valeur:
        valeur_estimee = valeur["prix_par_metre"]*taille
    return {"valeur_bien": valeur_estimee}


#Ajouter une nouvelle ville avec le prix du metre carre
@router.post("/ajouter_ville")
async def ajouter_ville(payload: Evaluation):
    ville = await add_ville(payload)
    response = {
        'ville': ville,
        **payload.model_dump()
    }
    return response


# Evaluer un bien: c'est l'endpoint central du service
@router.post("/evaluer")
async def evaluation(taille: float, ville: str, adress: str):
    valeur = await get_eval(ville)
    if valeur:
        valeur_estimee = valeur["prix_par_metre"] * taille
    litiges = await get_litiges(adress)
    return {"valeur_bien": valeur_estimee, "litiges_sur_le_bien": litiges}


# Ajouter un nouveau bien qui a des litiges
@router.post("/ajouter_litige")
async def ajouter_litiges(payload: Litige):
    adresse = await add_litiges(payload)
    response = {
        'adresse': adresse,
        **payload.model_dump()
    }
    return response
