from pydantic import BaseModel
from datetime import date
from models.endereco import Endereco
from models.contato import Contato

class Cliente(BaseModel):
    id_cliente: int
    cpf: str
    pnome: str
    unome: str
    data_nasc: date
    id_endereco: Endereco
    id_contato: Contato