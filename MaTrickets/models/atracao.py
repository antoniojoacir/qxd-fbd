from pydantic import BaseModel
from models.contato import Contato


class Atracao(BaseModel):
    id_atracao: int
    cnpj: str
    nome_atracao: str
    tipo_atracao: str
    contato: Contato
