from pydantic import BaseModel
from typing import Optional


class Contato(BaseModel):
    id_contato: int
    tipo_contato: str
    info_contato: str


class ContatoUpdate(BaseModel):
    tipo_contato: Optional[str] = None
    info_contato: Optional[str] = None
