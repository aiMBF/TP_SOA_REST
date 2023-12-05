from pydantic import BaseModel


class Client(BaseModel):
    id_client: str
    nom: str
    adresse: str
    revenu_mensuel: int
    depense_mensuel: int


class Credit(BaseModel):
    id_credit: int
    id_client: str
    dette_en_cours: int
    payement_en_retard: int
    antecedent_faillite: bool




