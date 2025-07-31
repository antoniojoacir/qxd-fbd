from typing import Optional
from pydantic import BaseModel
from models.contato import Contato


class Atracao(BaseModel):
    id_atracao: int
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    contato: Optional[Contato] = None


class AtracaoCreate(BaseModel):
    id_atracao: int
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    id_contato: Optional[int] = None


class AtracaoUpdate(BaseModel):
    cnpj: Optional[str] = None
    nome_atracao: Optional[str] = None
    tipo_atracao: Optional[str] = None
    id_contato: Optional[int] = None

class AtracaoNoDetails(BaseModel):
    id_atracao: int
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    id_contato: Optional[int] = None

