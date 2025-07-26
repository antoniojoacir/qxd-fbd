from pydantic import BaseModel
from typing import Optional

class Endereco(BaseModel):
    id_endereco: int
    cep: str
    cidade: str
    rua: str
    uf: str
    numero: Optional[int] = None
