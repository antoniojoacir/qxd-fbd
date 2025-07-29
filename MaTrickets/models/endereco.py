from pydantic import BaseModel
from typing import Optional


class Endereco(BaseModel):
    id_endereco: int
    cep: str
    cidade: str
    rua: str
    uf: str
    numero: Optional[int] = None


class EnderecoUpdate(BaseModel):
    cep: Optional[str] = None
    cidade: Optional[str] = None
    rua: Optional[str] = None
    uf: Optional[str] = None
    numero: Optional[int] = None
