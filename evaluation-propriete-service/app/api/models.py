from pydantic import BaseModel


class Evaluation(BaseModel):
    ville: str
    prix_metre: int
