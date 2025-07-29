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
    genero: str
    contato: Contato
    endereco: Endereco


class ClienteCreate(BaseModel):
    id_cliente: int
    cpf: str
    pnome: str
    unome: str
    data_nasc: date
    genero: str
    id_contato: int
    id_endereco: int
