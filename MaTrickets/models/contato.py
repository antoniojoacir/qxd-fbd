from pydantic import BaseModel
from typing import Optional


class Contato(BaseModel):
    id_contato: int
    tipo_contato: str
    info_contato: str
