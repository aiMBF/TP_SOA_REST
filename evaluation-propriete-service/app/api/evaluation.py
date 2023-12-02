from fastapi import APIRouter, HTTPException
from .models import Evaluation
from typing import Union


router = APIRouter()

valeurs_reference = {
    "Versailles": 300,
    "Paris": 350,
    "Nantes": 250
}


@router.get('/')
async def root():
    return "Hello World"


def verif_litiges(adresse_logement):

    adresses_avec_litiges = [
        "123 avenue Charles, Pierrefitte-sur-Seine",
        "456 Rue Louis, Versailles",
        "789 avenue Baudelaire, Mantes-la-Jolie"
    ]
    if adresse_logement in adresses_avec_litiges:
        return True
    else:
        return False


def eval_prop(taille: float, ville: str):

    if ville not in valeurs_reference.keys():
        raise HTTPException(status_code=404, detail="Ville non répertoriée")
    else:
        valeur_estimee = valeurs_reference[ville] * taille
        return valeur_estimee


@router.post("/ajouter_ville")
async def ajouter_ville(ville: str, prix_par_metre_carre: float):
    valeurs_reference[ville] = prix_par_metre_carre
    return {"message": f"Ville {ville} ajoutée avec succès"}


@router.post("/evaluer")
async def evaluation(taille: float, ville: str, adress: str):
    valeur_bien = eval_prop(taille, ville)
    litiges = verif_litiges(adress)

    return {"valeur_bien": valeur_bien, "litiges_sur_le_bien": litiges}
