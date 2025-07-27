from pydantic import BaseModel
from models.contato import Contato


class AtracaoShow(BaseModel):
    id_atracao: int
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    contato: Contato


class AtracaoCreate(BaseModel):
    id_atracao: int
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    id_contato: int


class AtracaoUpdate(BaseModel):
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    id_contato: int
