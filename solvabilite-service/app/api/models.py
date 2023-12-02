from pydantic import BaseModel


class Client(BaseModel):
    id_client: str
    nom: str
    adresse: str
    revenu_mensuel: int
    depense_mensuel: int



