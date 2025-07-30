from typing import Optional
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
    endereco: Optional[Endereco] = None


class ClienteCreate(BaseModel):
    id_cliente: int
    cpf: str
    pnome: str
    unome: str
    data_nasc: date
    genero: str
    id_contato: int
    id_endereco: Optional[int] = None


class ClienteUpdate(BaseModel):
    cpf: Optional[str] = None
    pnome: Optional[str] = None
    unome: Optional[str] = None
    data_nasc: Optional[date] = None
    genero: Optional[str] = None
    id_contato: Optional[int] = None
    id_endereco: Optional[int] = None
